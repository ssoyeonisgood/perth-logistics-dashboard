"""Compute summary metrics from cleansed shipment data."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cleanse import run_cleanse  


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


if __name__ == "__main__":
    metrics = run_analysis()
    print(f"  Total shipments: {metrics['total_shipments']}")
    print(f"  On-time %: {metrics['on_time_pct']}")
    print(f"  Peak lift: {metrics['peak_lift_pct']}%")
