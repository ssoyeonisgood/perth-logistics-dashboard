"""Load cleansed data into PostgreSQL mart tables."""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import DATABASE_URL, SQL_DIR  # noqa: E402
from cleanse import run_cleanse  # noqa: E402
from validate import validate_and_save  # noqa: E402


def _run_setup_sql(engine) -> None:
    setup = (SQL_DIR / "00_setup.sql").read_text(encoding="utf-8")
    statements = [s.strip() for s in setup.split(";") if s.strip()]
    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))


def _build_dim_date(ship: pd.DataFrame, inv: pd.DataFrame) -> pd.DataFrame:
    ship_dates = pd.to_datetime(ship["scheduled_dt"]).dt.normalize()
    inv_dates = pd.to_datetime(inv["date"]).dt.normalize()
    all_dates = pd.concat([ship_dates, inv_dates]).dropna().unique()
    dim = pd.DataFrame({"date_key": pd.to_datetime(all_dates)})
    dim["year"] = dim["date_key"].dt.year
    dim["month"] = dim["date_key"].dt.month
    dim["month_name"] = dim["date_key"].dt.strftime("%B")
    dim["quarter"] = dim["date_key"].dt.quarter
    dim["is_peak_period"] = dim["month"].isin([11, 12])
    return dim.drop_duplicates("date_key")


def load_mart(cleanse_result: dict | None = None, qa_report: dict | None = None) -> None:
    data = cleanse_result or run_cleanse()
    report = qa_report or validate_and_save(data)

    if not report["summary"]["all_critical_passed"]:
        raise RuntimeError("QA validation failed — fix data before loading to PostgreSQL.")

    ship = data["shipments"].copy()
    inv = data["inventory"].copy()

    dim_date = _build_dim_date(ship, inv)
    dim_wh = data["warehouses"]
    dim_cust = data["customers"]

    fact_ship = ship.drop(columns=["scheduled_date", "actual_delivery"]).copy()
    fact_ship["date_key"] = pd.to_datetime(fact_ship["scheduled_dt"]).dt.normalize()
    fact_ship = fact_ship.rename(
        columns={"scheduled_dt": "scheduled_date", "actual_dt": "actual_delivery"}
    )
    fact_ship = fact_ship[
        [
            "shipment_id",
            "date_key",
            "warehouse_id",
            "customer_id",
            "is_delayed",
            "delay_hours",
            "on_time",
            "scheduled_date",
            "actual_delivery",
        ]
    ]

    fact_inv = inv.copy()
    fact_inv["date_key"] = pd.to_datetime(fact_inv["date"]).dt.normalize()
    fact_inv = fact_inv[["date_key", "warehouse_id", "sku", "quantity_on_hand"]]

    qa_df = pd.DataFrame(report["rules"]).rename(
        columns={
            "rule_id": "rule_id",
            "name": "rule_name",
            "before": "before_count",
            "after": "after_count",
            "passed": "passed",
            "detail": "detail",
        }
    )[["rule_id", "rule_name", "before_count", "after_count", "passed", "detail"]]

    engine = create_engine(DATABASE_URL)
    _run_setup_sql(engine)

    dim_date.to_sql("dim_date", engine, schema="mart", if_exists="append", index=False)
    dim_wh.to_sql("dim_warehouse", engine, schema="mart", if_exists="append", index=False)
    dim_cust.to_sql("dim_customer", engine, schema="mart", if_exists="append", index=False)
    fact_ship.to_sql("fact_shipments", engine, schema="mart", if_exists="append", index=False)
    fact_inv.to_sql("fact_inventory", engine, schema="mart", if_exists="append", index=False)
    qa_df.to_sql("qa_summary", engine, schema="mart", if_exists="append", index=False)

    print("Loaded mart tables successfully.")
    print(f"  dim_date: {len(dim_date)} rows")
    print(f"  fact_shipments: {len(fact_ship)} rows")
    print(f"  fact_inventory: {len(fact_inv)} rows")
    print(f"  qa_summary: {len(qa_df)} rows")


if __name__ == "__main__":
    load_mart()
