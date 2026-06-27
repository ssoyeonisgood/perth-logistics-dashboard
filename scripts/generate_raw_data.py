#!/usr/bin/env python3
"""Generate synthetic raw logistics data with intentional quality issues."""
from __future__ import annotations

import sys
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import ( 
    CUSTOMERS_RAW,
    INVENTORY_RAW,
    RANDOM_SEED,
    RAW_DIR,
    SHIPMENTS_RAW,
    WAREHOUSE_MASTER,
)

np.random.seed(RANDOM_SEED)

WAREHOUSES = [
    {"warehouse_id": "WH01", "name": "Perth WH", "capacity": 50000},
    {"warehouse_id": "WH02", "name": "Fremantle WH", "capacity": 35000},
    {"warehouse_id": "WH03", "name": "Kewdale WH", "capacity": 40000},
]

WAREHOUSE_ALIASES = {
    "WH01": ["WH01", "Perth WH", "perth wh", "WH01"],
    "WH02": ["WH02", "Fremantle WH", "fremantle wh"],
    "WH03": ["WH03", "Kewdale WH", "kewdale wh"],
}

DELAY_FLAG_VARIANTS = {
    0: ["N", "No", "0", "false", "FALSE"],
    1: ["Y", "Yes", "1", "true", "TRUE"],
}

SEGMENTS = ["Retail", "Wholesale", "E-commerce"]
REGIONS = [
    "Perth CBD",
    "North Perth",
    "South Perth",
    "Fremantle",
    "Joondalup",
    "Canning Vale",
    "Kewdale",
    "Mandurah",
    "Rockingham",
    "Armadale",
    "Midland",
    "Bunbury",
]
SKUS = [f"SKU-{i:04d}" for i in range(1, 101)]


def _warehouse_alias(canonical: str) -> str:
    return np.random.choice(WAREHOUSE_ALIASES[canonical])


def _delay_flag(is_delayed: int) -> str:
    return np.random.choice(DELAY_FLAG_VARIANTS[is_delayed])


def generate_warehouse_master() -> pd.DataFrame:
    return pd.DataFrame(WAREHOUSES)


def generate_customers(n: int = 200) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "customer_id": [f"CUST-{i:05d}" for i in range(1, n + 1)],
            "segment": np.random.choice(SEGMENTS, n),
            "region": np.random.choice(REGIONS, n),
        }
    )


def generate_shipments(
    customers: pd.DataFrame,
    n: int = 5000,
    start: datetime | None = None,
) -> pd.DataFrame:
    start = start or datetime(2023, 1, 1)
    end = datetime(2024, 12, 31)
    days = (end - start).days

    customer_ids = customers["customer_id"].tolist()
    canonical_wh = [w["warehouse_id"] for w in WAREHOUSES]

    rows = []
    for i in range(1, n + 1):
        scheduled = start + timedelta(days=int(np.random.randint(0, days)))
        month_weight = 3 if scheduled.month in (11, 12) else 1
        if np.random.random() > month_weight / 3:
            scheduled = start + timedelta(days=int(np.random.randint(0, days)))

        is_delayed = int(np.random.random() < 0.18)
        delay_hours = round(np.random.uniform(1, 48), 1) if is_delayed else 0.0
        actual = scheduled + timedelta(
            hours=int(delay_hours) if is_delayed else np.random.randint(0, 20)
        )

        wh = np.random.choice(canonical_wh)
        rows.append(
            {
                "shipment_id": f"SHP-{i:06d}",
                "warehouse_id": _warehouse_alias(wh),
                "customer_id": np.random.choice(customer_ids),
                "scheduled_date": scheduled.strftime("%Y-%m-%d"),
                "actual_delivery": actual.strftime("%Y-%m-%d %H:%M"),
                "delay_flag": _delay_flag(is_delayed),
                "delay_hours": delay_hours,
            }
        )

    df = pd.DataFrame(rows)

    dup_sample = df.sample(50, random_state=RANDOM_SEED)
    df = pd.concat([df, dup_sample], ignore_index=True)

    null_idx = df.sample(frac=0.05, random_state=RANDOM_SEED).index
    df.loc[null_idx, "warehouse_id"] = None

    bad_idx = df.sample(frac=0.02, random_state=RANDOM_SEED + 1).index
    df.loc[bad_idx, "scheduled_date"] = np.random.choice(
        ["2024-13-45", "invalid", "2023-02-30"], len(bad_idx)
    )

    orphan_idx = df.sample(frac=0.01, random_state=RANDOM_SEED + 2).index
    df.loc[orphan_idx, "customer_id"] = [f"ORPHAN-{i}" for i in range(len(orphan_idx))]

    peak_mask = pd.to_datetime(df["scheduled_date"], errors="coerce").dt.month.isin([11, 12])
    peak_extra = df[peak_mask].sample(800, replace=True, random_state=RANDOM_SEED)
    peak_extra["shipment_id"] = [f"SHP-PEAK-{i:05d}" for i in range(len(peak_extra))]
    df = pd.concat([df, peak_extra], ignore_index=True)

    return df.sample(frac=1, random_state=RANDOM_SEED).reset_index(drop=True)


def generate_inventory(n_days: int = 365) -> pd.DataFrame:
    start = datetime(2024, 1, 1)
    rows = []
    canonical_wh = [w["warehouse_id"] for w in WAREHOUSES]

    for day in range(n_days):
        date_str = (start + timedelta(days=day)).strftime("%Y-%m-%d")
        for _ in range(8):
            wh = np.random.choice(canonical_wh)
            rows.append(
                {
                    "date": date_str,
                    "warehouse_id": _warehouse_alias(wh),
                    "sku": np.random.choice(SKUS),
                    "quantity_on_hand": int(np.random.randint(50, 5000)),
                }
            )

    return pd.DataFrame(rows)


def main() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    warehouses = generate_warehouse_master()
    customers = generate_customers()
    shipments = generate_shipments(customers)
    inventory = generate_inventory()

    warehouses.to_csv(WAREHOUSE_MASTER, index=False)
    customers.to_csv(CUSTOMERS_RAW, index=False)
    shipments.to_csv(SHIPMENTS_RAW, index=False)
    inventory.to_csv(INVENTORY_RAW, index=False)

    print(f"Wrote {WAREHOUSE_MASTER} ({len(warehouses)} rows)")
    print(f"Wrote {CUSTOMERS_RAW} ({len(customers)} rows)")
    print(f"Wrote {SHIPMENTS_RAW} ({len(shipments)} rows)")
    print(f"Wrote {INVENTORY_RAW} ({len(inventory)} rows)")
    print("\nIntentional issues in shipments_raw:")
    print(f"  - Duplicate shipment_id: {shipments['shipment_id'].duplicated().sum()}")
    print(f"  - Null warehouse_id: {shipments['warehouse_id'].isna().sum()}")
    print(
        "  - Invalid scheduled_date: "
        f"{pd.to_datetime(shipments['scheduled_date'], errors='coerce').isna().sum()}"
    )


if __name__ == "__main__":
    main()
