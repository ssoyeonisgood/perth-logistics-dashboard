"""Export cleansed DataFrames to CSV samples for portfolio proof."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from config import CLEANSED_DIR  # noqa: E402
from cleanse import run_cleanse  # noqa: E402

SAMPLE_ROWS = 1000


def export_cleansed(cleanse_result: dict | None = None, sample_rows: int = SAMPLE_ROWS) -> dict[str, Path]:
    data = cleanse_result or run_cleanse()
    CLEANSED_DIR.mkdir(parents=True, exist_ok=True)

    paths: dict[str, Path] = {}
    exports = {
        "shipments_cleansed.csv": data["shipments"],
        "inventory_cleansed.csv": data["inventory"],
        "customers_cleansed.csv": data["customers"],
        "quarantine.csv": data["quarantine"],
    }

    for filename, df in exports.items():
        out = CLEANSED_DIR / filename
        sample = df.head(sample_rows) if len(df) > sample_rows else df
        sample.to_csv(out, index=False)
        paths[filename] = out
        print(f"Wrote {out} ({len(sample)} rows)")

    return paths


if __name__ == "__main__":
    export_cleansed()
