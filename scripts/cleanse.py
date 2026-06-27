"""Pandas-based cleansing for raw logistics data."""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import (
    CUSTOMERS_RAW,
    INVENTORY_RAW,
    SHIPMENTS_RAW,
    WAREHOUSE_MASTER,
)

WAREHOUSE_LOOKUP = {
    "wh01": "WH01",
    "perth wh": "WH01",
    "wh02": "WH02",
    "fremantle wh": "WH02",
    "wh03": "WH03",
    "kewdale wh": "WH03",
}


def load_raw() -> dict[str, pd.DataFrame]:
    return {
        "shipments": pd.read_csv(SHIPMENTS_RAW),
        "inventory": pd.read_csv(INVENTORY_RAW),
        "customers": pd.read_csv(CUSTOMERS_RAW),
        "warehouses": pd.read_csv(WAREHOUSE_MASTER),
    }


def standardize_warehouse_id(series: pd.Series) -> pd.Series:
    def _map(val):
        if pd.isna(val):
            return np.nan
        key = str(val).strip().lower()
        if key in WAREHOUSE_LOOKUP:
            return WAREHOUSE_LOOKUP[key]
        upper = str(val).strip().upper()
        if upper in {"WH01", "WH02", "WH03"}:
            return upper
        return str(val).strip()

    return series.map(_map)


def parse_delay_flag(series: pd.Series) -> pd.Series:
    truthy = {"y", "yes", "1", "true"}
    return series.astype(str).str.strip().str.lower().map(lambda x: 1 if x in truthy else 0)


def cleanse_shipments(
    df: pd.DataFrame,
    warehouses: pd.DataFrame,
    customers: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return cleansed shipments and quarantine rows."""
    raw = df.copy()
    quarantine_parts: list[pd.DataFrame] = []

    valid_wh = set(warehouses["warehouse_id"])
    valid_customers = set(customers["customer_id"])

    raw["scheduled_dt"] = pd.to_datetime(raw["scheduled_date"], errors="coerce")
    raw["actual_dt"] = pd.to_datetime(raw["actual_delivery"], errors="coerce")

    bad_dates = raw["scheduled_dt"].isna() | raw["actual_dt"].isna()
    if bad_dates.any():
        q = raw.loc[bad_dates].copy()
        q["reject_reason"] = "invalid_date"
        quarantine_parts.append(q)
    work = raw.loc[~bad_dates].copy()

    work["warehouse_id"] = standardize_warehouse_id(work["warehouse_id"])

    null_wh = work["warehouse_id"].isna()
    if null_wh.any():
        q = work.loc[null_wh].copy()
        q["reject_reason"] = "null_warehouse_id"
        quarantine_parts.append(q)
        work = work.loc[~null_wh]

    invalid_wh = ~work["warehouse_id"].isin(valid_wh)
    if invalid_wh.any():
        q = work.loc[invalid_wh].copy()
        q["reject_reason"] = "invalid_warehouse_id"
        quarantine_parts.append(q)
        work = work.loc[~invalid_wh]

    orphan_cust = ~work["customer_id"].isin(valid_customers)
    if orphan_cust.any():
        q = work.loc[orphan_cust].copy()
        q["reject_reason"] = "orphan_customer_id"
        quarantine_parts.append(q)
        work = work.loc[~orphan_cust]

    work = work.sort_values("actual_dt")
    dup_mask = work.duplicated(subset="shipment_id", keep="last")
    if dup_mask.any():
        q = work.loc[dup_mask].copy()
        q["reject_reason"] = "duplicate_shipment_id"
        quarantine_parts.append(q)
        work = work.loc[~dup_mask]

    work["is_delayed"] = parse_delay_flag(work["delay_flag"])
    work.loc[work["delay_hours"] < 0, "delay_hours"] = 0

    today = pd.Timestamp.now().normalize() + pd.Timedelta(days=1)
    future = work["actual_dt"] > today
    if future.any():
        q = work.loc[future].copy()
        q["reject_reason"] = "future_delivery_date"
        quarantine_parts.append(q)
        work = work.loc[~future]

    cleansed = work[
        [
            "shipment_id",
            "warehouse_id",
            "customer_id",
            "scheduled_date",
            "actual_delivery",
            "is_delayed",
            "delay_hours",
            "scheduled_dt",
            "actual_dt",
        ]
    ].copy()

    cleansed["on_time"] = (
        cleansed["actual_dt"] <= cleansed["scheduled_dt"] + pd.Timedelta(hours=24)
    ).astype(int)

    quarantine = (
        pd.concat(quarantine_parts, ignore_index=True) if quarantine_parts else pd.DataFrame()
    )

    return cleansed, quarantine


def cleanse_inventory(df: pd.DataFrame, warehouses: pd.DataFrame) -> pd.DataFrame:
    work = df.copy()
    work["warehouse_id"] = standardize_warehouse_id(work["warehouse_id"])
    work["date"] = pd.to_datetime(work["date"], errors="coerce")
    work = work.dropna(subset=["date", "warehouse_id"])
    work = work[work["warehouse_id"].isin(warehouses["warehouse_id"])]
    work["quantity_on_hand"] = work["quantity_on_hand"].clip(lower=0)
    return work


def cleanse_customers(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates(subset="customer_id").copy()


def compute_before_after_stats(
    raw_shipments: pd.DataFrame,
    cleansed_shipments: pd.DataFrame,
    quarantine: pd.DataFrame,
) -> dict:
    return {
        "raw_row_count": len(raw_shipments),
        "cleansed_row_count": len(cleansed_shipments),
        "quarantine_row_count": len(quarantine),
        "duplicate_shipment_id_before": int(raw_shipments["shipment_id"].duplicated().sum()),
        "duplicate_shipment_id_after": int(cleansed_shipments["shipment_id"].duplicated().sum()),
        "null_warehouse_before": int(raw_shipments["warehouse_id"].isna().sum()),
        "null_warehouse_after": int(cleansed_shipments["warehouse_id"].isna().sum()),
        "invalid_date_before": int(
            pd.to_datetime(raw_shipments["scheduled_date"], errors="coerce").isna().sum()
        ),
        "invalid_date_after": 0,
    }


def run_cleanse() -> dict[str, pd.DataFrame | dict]:
    raw = load_raw()
    raw_shipments = raw["shipments"]

    customers = cleanse_customers(raw["customers"])
    cleansed_inv = cleanse_inventory(raw["inventory"], raw["warehouses"])
    cleansed_ship, quarantine = cleanse_shipments(
        raw_shipments, raw["warehouses"], customers
    )

    stats = compute_before_after_stats(raw_shipments, cleansed_ship, quarantine)

    return {
        "shipments": cleansed_ship,
        "inventory": cleansed_inv,
        "customers": customers,
        "warehouses": raw["warehouses"],
        "quarantine": quarantine,
        "before_after_stats": stats,
        "raw_shipments": raw_shipments,
    }


if __name__ == "__main__":
    result = run_cleanse()
    stats = result["before_after_stats"]
    print("Cleansing complete.")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(f"  quarantine rows: {len(result['quarantine'])}")
