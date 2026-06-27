# Analysis Brief — Perth Logistics Co.

> Auto-generated statistics from `scripts/analyze.py`. Narrative and recommendations should be reviewed before use in applications.

## Context

Perth Logistics Co. operates three warehouses (Perth, Fremantle, Kewdale). Shipment data from multiple source systems showed inconsistent warehouse codes, duplicate records, and conflicting KPI definitions. This analysis uses the **cleansed** dataset (5,373 shipments) after Python QA validation.

## Key Findings

### 1. Peak-season demand spike

- Average monthly shipments in **Nov–Dec**: ~473
- Average monthly shipments in other months: ~174
- **Peak lift: ~171.8%** above non-peak months

Peak-period volume creates capacity pressure across the network, especially at the highest-volume site.

### 2. Warehouse concentration and on-time performance

- **WH03** handles **33.9%** of all shipments
- On-time delivery at WH03: **91.3%**
- Highest delay rate: **WH03** (19.1% delayed)

Concentration at Perth WH suggests bottleneck risk during peak season.

### 3. Network on-time performance

- Overall on-time delivery (cleansed data): **91.3%**
- Delay patterns vary materially by warehouse — targeted intervention is warranted rather than network-wide blanket changes.

## Evidence-Based Recommendations

1. **Workforce planning:** Increase Perth WH staffing by ~15% for weeks 45–52 based on peak lift of 171.8%.
2. **Inventory readiness:** Review safety stock for top SKUs at WH03 where delay rates are highest.
3. **Customer communication:** Tighten order cutoff times for high-volume segments before peak season to reduce last-mile pressure.

## Limitations

- Synthetic data generated for portfolio demonstration (`random_seed=42`).
- Forecasting uses simple historical averages; production planning would require time-series models.
- External factors (weather, port delays) not modelled.

## Data Quality Note

All metrics above are computed on data that passed **12 automated QA rules**. See `data/reports/qa_report.json` for before/after validation results.
