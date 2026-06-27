"""Run 12 data quality rules and write qa_report.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import QA_REPORT_PATH, REPORTS_DIR  # noqa: E402
from cleanse import run_cleanse  # noqa: E402


def _rule(
    rule_id: str,
    name: str,
    before: int | float,
    after: int | float,
    passed: bool,
    detail: str = "",
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "name": name,
        "before": before,
        "after": after,
        "passed": bool(passed),
        "detail": detail,
    }


def run_validation(cleanse_result: dict | None = None) -> dict[str, Any]:
    data = cleanse_result or run_cleanse()
    ship = data["shipments"]
    inv = data["inventory"]
    customers = data["customers"]
    warehouses = data["warehouses"]
    quarantine = data["quarantine"]
    stats = data["before_after_stats"]

    valid_wh = set(warehouses["warehouse_id"])
    valid_cust = set(customers["customer_id"])

    rules: list[dict] = []

    dup_after = int(ship["shipment_id"].duplicated().sum())
    rules.append(
        _rule("01", "duplicate_shipment_id", stats["duplicate_shipment_id_before"], dup_after, dup_after == 0)
    )

    null_after = int(ship["warehouse_id"].isna().sum())
    rules.append(
        _rule("02", "null_warehouse_id", stats["null_warehouse_before"], null_after, null_after == 0)
    )

    invalid_wh = int((~ship["warehouse_id"].isin(valid_wh)).sum())
    rules.append(_rule("03", "invalid_warehouse_id", 0, invalid_wh, invalid_wh == 0))

    rules.append(
        _rule("04", "invalid_date", stats["invalid_date_before"], 0, stats["invalid_date_after"] == 0)
    )

    orphan = int((~ship["customer_id"].isin(valid_cust)).sum())
    rules.append(_rule("05", "orphan_customer_id", 0, orphan, orphan == 0))

    bad_delay = int((~ship["is_delayed"].isin([0, 1])).sum())
    rules.append(_rule("06", "is_delayed_consistency", 0, bad_delay, bad_delay == 0))

    neg_delay = int((ship["delay_hours"] < 0).sum())
    rules.append(_rule("07", "negative_delay_hours", 0, neg_delay, neg_delay == 0))

    today = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
    future = int((ship["actual_dt"] > today).sum())
    rules.append(_rule("08", "future_delivery_dates", 0, future, future == 0))

    reconciled = stats["raw_row_count"] == stats["cleansed_row_count"] + stats["quarantine_row_count"]
    rules.append(
        _rule(
            "09",
            "row_count_reconciliation",
            stats["raw_row_count"],
            stats["cleansed_row_count"] + stats["quarantine_row_count"],
            reconciled,
            detail=f"cleansed={stats['cleansed_row_count']}, quarantine={stats['quarantine_row_count']}",
        )
    )

    fk_fail = int(
        (~ship["warehouse_id"].isin(valid_wh)).sum()
        + (~ship["customer_id"].isin(valid_cust)).sum()
        + (~inv["warehouse_id"].isin(valid_wh)).sum()
    )
    rules.append(_rule("10", "referential_integrity", 0, fk_fail, fk_fail == 0))

    on_time_pct = ship["on_time"].mean() * 100 if len(ship) else 0
    kpi_ok = 0 <= on_time_pct <= 100
    rules.append(
        _rule("11", "kpi_sanity_on_time_pct", 0, round(on_time_pct, 2), kpi_ok, detail=f"{on_time_pct:.1f}%")
    )

    q_count = len(quarantine)
    rules.append(
        _rule(
            "12",
            "quarantine_review",
            0,
            q_count,
            True,
            detail="quarantine rows documented for review",
        )
    )

    all_passed = all(r["passed"] for r in rules if r["rule_id"] != "12")

    return {
        "summary": {
            "all_critical_passed": all_passed,
            "rules_passed": sum(1 for r in rules if r["passed"]),
            "rules_total": len(rules),
            "before_after_stats": stats,
        },
        "rules": rules,
    }


def save_report(report: dict, path: Path | None = None) -> Path:
    path = path or QA_REPORT_PATH
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return path


def validate_and_save(cleanse_result: dict | None = None) -> dict:
    report = run_validation(cleanse_result)
    save_report(report)
    return report


if __name__ == "__main__":
    result = validate_and_save()
    print(json.dumps(result["summary"], indent=2))
    if not result["summary"]["all_critical_passed"]:
        sys.exit(1)
