"""Generate analysis brief from cleansed shipment data."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DOCS_DIR  # noqa: E402
from cleanse import run_cleanse  # noqa: E402

BRIEF_PATH = DOCS_DIR / "analysis_brief.md"


def run_analysis(cleanse_result: dict | None = None) -> dict:
    data = cleanse_result or run_cleanse()
    ship = data["shipments"].copy()
    ship["month"] = ship["scheduled_dt"].dt.month
    ship["year"] = ship["scheduled_dt"].dt.year

    monthly = ship.groupby(["year", "month"]).size().reset_index(name="shipments")
    peak = ship[ship["month"].isin([11, 12])]
    non_peak = ship[~ship["month"].isin([11, 12])]
    peak_avg = len(peak) / max(peak["year"].nunique(), 1) / 2
    non_peak_avg = len(non_peak) / max(non_peak["year"].nunique(), 1) / 10

    wh_stats = (
        ship.groupby("warehouse_id")
        .agg(shipments=("shipment_id", "count"), on_time_pct=("on_time", "mean"))
        .reset_index()
    )
    wh_stats["on_time_pct"] = (wh_stats["on_time_pct"] * 100).round(1)
    top_wh = wh_stats.sort_values("shipments", ascending=False).iloc[0]

    delay_by_wh = (
        ship.groupby("warehouse_id")["is_delayed"].mean().mul(100).round(1).sort_values(ascending=False)
    )

    return {
        "total_shipments": len(ship),
        "on_time_pct": round(ship["on_time"].mean() * 100, 1),
        "peak_monthly_avg": round(peak_avg, 0),
        "non_peak_monthly_avg": round(non_peak_avg, 0),
        "peak_lift_pct": round((peak_avg / non_peak_avg - 1) * 100, 1) if non_peak_avg else 0,
        "top_warehouse": top_wh["warehouse_id"],
        "top_warehouse_share_pct": round(top_wh["shipments"] / len(ship) * 100, 1),
        "top_warehouse_on_time_pct": top_wh["on_time_pct"],
        "highest_delay_warehouse": delay_by_wh.index[0],
        "highest_delay_pct": delay_by_wh.iloc[0],
        "monthly": monthly,
        "warehouse_stats": wh_stats,
    }


def write_brief(metrics: dict, path: Path | None = None) -> Path:
    path = path or BRIEF_PATH
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    content = f"""# Analysis Brief — Perth Logistics Co.

> Auto-generated statistics from `scripts/analyze.py`. Narrative and recommendations should be reviewed before use in applications.

## Context

Perth Logistics Co. operates three warehouses (Perth, Fremantle, Kewdale). Shipment data from multiple source systems showed inconsistent warehouse codes, duplicate records, and conflicting KPI definitions. This analysis uses the **cleansed** dataset ({metrics["total_shipments"]:,} shipments) after Python QA validation.

## Key Findings

### 1. Peak-season demand spike

- Average monthly shipments in **Nov–Dec**: ~{metrics["peak_monthly_avg"]:.0f}
- Average monthly shipments in other months: ~{metrics["non_peak_monthly_avg"]:.0f}
- **Peak lift: ~{metrics["peak_lift_pct"]}%** above non-peak months

Peak-period volume creates capacity pressure across the network, especially at the highest-volume site.

### 2. Warehouse concentration and on-time performance

- **{metrics["top_warehouse"]}** handles **{metrics["top_warehouse_share_pct"]}%** of all shipments
- On-time delivery at {metrics["top_warehouse"]}: **{metrics["top_warehouse_on_time_pct"]}%**
- Highest delay rate: **{metrics["highest_delay_warehouse"]}** ({metrics["highest_delay_pct"]}% delayed)

Concentration at Perth WH suggests bottleneck risk during peak season.

### 3. Network on-time performance

- Overall on-time delivery (cleansed data): **{metrics["on_time_pct"]}%**
- Delay patterns vary materially by warehouse — targeted intervention is warranted rather than network-wide blanket changes.

## Evidence-Based Recommendations

1. **Workforce planning:** Increase Perth WH staffing by ~15% for weeks 45–52 based on peak lift of {metrics["peak_lift_pct"]}%.
2. **Inventory readiness:** Review safety stock for top SKUs at {metrics["highest_delay_warehouse"]} where delay rates are highest.
3. **Customer communication:** Tighten order cutoff times for high-volume segments before peak season to reduce last-mile pressure.

## Limitations

- Synthetic data generated for portfolio demonstration (`random_seed=42`).
- Forecasting uses simple historical averages; production planning would require time-series models.
- External factors (weather, port delays) not modelled.

## Data Quality Note

All metrics above are computed on data that passed **12 automated QA rules**. See `data/reports/qa_report.json` for before/after validation results.
"""
    path.write_text(content, encoding="utf-8")
    return path


if __name__ == "__main__":
    metrics = run_analysis()
    out = write_brief(metrics)
    print(f"Wrote {out}")
    print(f"  On-time %: {metrics['on_time_pct']}")
    print(f"  Peak lift: {metrics['peak_lift_pct']}%")
