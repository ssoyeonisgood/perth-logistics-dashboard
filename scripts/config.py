"""Project paths and shared settings."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
CLEANSED_DIR = DATA_DIR / "cleansed"
REPORTS_DIR = DATA_DIR / "reports"
DOCS_DIR = PROJECT_ROOT / "docs"
SQL_DIR = PROJECT_ROOT / "sql"

RANDOM_SEED = 42

SHIPMENTS_RAW = RAW_DIR / "shipments_raw.csv"
INVENTORY_RAW = RAW_DIR / "inventory_raw.csv"
CUSTOMERS_RAW = RAW_DIR / "customers_raw.csv"
WAREHOUSE_MASTER = RAW_DIR / "warehouse_master.csv"

QA_REPORT_PATH = REPORTS_DIR / "qa_report.json"