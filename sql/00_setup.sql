-- Perth Ops Dashboard — mart schema DDL
-- Run: psql -d perth_ops -f sql/00_setup.sql

CREATE SCHEMA IF NOT EXISTS mart;

DROP TABLE IF EXISTS mart.qa_summary CASCADE;
DROP TABLE IF EXISTS mart.fact_inventory CASCADE;
DROP TABLE IF EXISTS mart.fact_shipments CASCADE;
DROP TABLE IF EXISTS mart.dim_customer CASCADE;
DROP TABLE IF EXISTS mart.dim_warehouse CASCADE;
DROP TABLE IF EXISTS mart.dim_date CASCADE;

CREATE TABLE mart.dim_date (
    date_key        DATE PRIMARY KEY,
    year            INT NOT NULL,
    month           INT NOT NULL,
    month_name      VARCHAR(20),
    quarter         INT,
    is_peak_period  BOOLEAN
);

CREATE TABLE mart.dim_warehouse (
    warehouse_id    VARCHAR(10) PRIMARY KEY,
    name            VARCHAR(100),
    capacity        INT
);

CREATE TABLE mart.dim_customer (
    customer_id     VARCHAR(20) PRIMARY KEY,
    segment         VARCHAR(50),
    region          VARCHAR(50)
);

CREATE TABLE mart.fact_shipments (
    shipment_id     VARCHAR(20) PRIMARY KEY,
    date_key        DATE,
    warehouse_id    VARCHAR(10) REFERENCES mart.dim_warehouse(warehouse_id),
    customer_id     VARCHAR(20) REFERENCES mart.dim_customer(customer_id),
    is_delayed      SMALLINT,
    delay_hours     NUMERIC(8,2),
    on_time         SMALLINT,
    scheduled_date  TIMESTAMP,
    actual_delivery TIMESTAMP
);

CREATE TABLE mart.fact_inventory (
    id              SERIAL PRIMARY KEY,
    date_key        DATE,
    warehouse_id    VARCHAR(10) REFERENCES mart.dim_warehouse(warehouse_id),
    sku             VARCHAR(20),
    quantity_on_hand INT
);

CREATE TABLE mart.qa_summary (
    rule_id         VARCHAR(5) PRIMARY KEY,
    rule_name       VARCHAR(100),
    before_count    NUMERIC,
    after_count     NUMERIC,
    passed          BOOLEAN,
    detail          TEXT,
    loaded_at       TIMESTAMP DEFAULT NOW()
);
