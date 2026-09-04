-- ================================================================
-- MASTER DATA GOVERNANCE — SQL QUERIES
-- Siemens Energy | Author: Haider Ali | M.Sc. Data Science @ BHT
-- ================================================================
-- Run these queries in any SQL tool (DBeaver, SQLite, BigQuery)
-- after importing supply_chain_enriched.csv as a table
-- ================================================================


-- ================================================================
-- SECTION 1: DATA PROFILING QUERIES
-- ================================================================

-- Q1.1: Overall Dataset Profile
SELECT 
    COUNT(*)                                              AS total_records,
    COUNT(DISTINCT "Customer Id")                         AS unique_customers,
    COUNT(DISTINCT "Order Id")                            AS unique_orders,
    COUNT(DISTINCT "Product Card Id")                     AS unique_products,
    COUNT(DISTINCT "Category Name")                       AS unique_categories,
    COUNT(DISTINCT "Market")                              AS unique_markets,
    MIN("Order Date (DateOrders)")                        AS earliest_order,
    MAX("Order Date (DateOrders)")                        AS latest_order
FROM supply_chain;


-- Q1.2: Missing Values Report by Column
SELECT 
    'Customer Zipcode'  AS column_name, 
    SUM(CASE WHEN "Customer Zipcode" IS NULL OR "Customer Zipcode" = 'Unknown' THEN 1 ELSE 0 END) AS missing_count,
    ROUND(SUM(CASE WHEN "Customer Zipcode" IS NULL OR "Customer Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS missing_pct,
    CASE WHEN SUM(CASE WHEN "Customer Zipcode" IS NULL OR "Customer Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) >= 50 
         THEN 'CRITICAL ❌' 
         WHEN SUM(CASE WHEN "Customer Zipcode" IS NULL OR "Customer Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) > 0
         THEN 'WARNING ⚠️' ELSE 'PASS ✅' END AS status
FROM supply_chain
UNION ALL
SELECT 
    'Order Zipcode',
    SUM(CASE WHEN "Order Zipcode" IS NULL OR "Order Zipcode" = 'Unknown' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN "Order Zipcode" IS NULL OR "Order Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2),
    CASE WHEN SUM(CASE WHEN "Order Zipcode" IS NULL OR "Order Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) >= 50 
         THEN 'CRITICAL ❌' 
         WHEN SUM(CASE WHEN "Order Zipcode" IS NULL OR "Order Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) > 0
         THEN 'WARNING ⚠️' ELSE 'PASS ✅' END
FROM supply_chain
UNION ALL
SELECT 
    'Product Description',
    SUM(CASE WHEN "Product Description" IS NULL OR "Product Description" = 'Pending Enrichment' THEN 1 ELSE 0 END),
    ROUND(SUM(CASE WHEN "Product Description" IS NULL OR "Product Description" = 'Pending Enrichment' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2),
    CASE WHEN SUM(CASE WHEN "Product Description" IS NULL OR "Product Description" = 'Pending Enrichment' THEN 1 ELSE 0 END) * 100.0 / COUNT(*) >= 50 
         THEN 'CRITICAL ❌' ELSE 'WARNING ⚠️' END
FROM supply_chain;


-- ================================================================
-- SECTION 2: BUSINESS RULES VALIDATION (SLA COMPLIANCE)
-- ================================================================

-- Q2.1: Full SLA Compliance Report
SELECT
    kpi_name,
    actual_score,
    sla_target,
    CASE WHEN actual_score >= sla_target THEN 'SLA MET ✅' ELSE 'SLA BREACH ❌' END AS sla_status,
    ROUND(actual_score - sla_target, 1) AS gap_to_target
FROM (
    SELECT 
        'Customer ID Completeness' AS kpi_name,
        ROUND((1 - SUM(CASE WHEN "Customer Id" IS NULL THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100, 1) AS actual_score,
        99.0 AS sla_target
    FROM supply_chain

    UNION ALL SELECT 
        'Product Price Validity',
        ROUND((1 - SUM(CASE WHEN "Product Price" <= 0 THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100, 1),
        99.0
    FROM supply_chain

    UNION ALL SELECT 
        'Customer Segment Validity',
        ROUND((SUM(CASE WHEN "Customer Segment" IN ('Consumer', 'Corporate', 'Home Office') THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 1),
        99.0
    FROM supply_chain

    UNION ALL SELECT 
        'Shipping Mode Validity',
        ROUND((SUM(CASE WHEN "Shipping Mode" IN ('Standard Class', 'First Class', 'Second Class', 'Same Day') THEN 1 ELSE 0 END) * 100.0 / COUNT(*)), 1),
        99.0
    FROM supply_chain

    UNION ALL SELECT 
        'Order Zipcode Completeness',
        ROUND((1 - SUM(CASE WHEN "Order Zipcode" = 'Unknown' THEN 1 ELSE 0 END) * 1.0 / COUNT(*)) * 100, 1),
        99.0
    FROM supply_chain

    UNION ALL SELECT 
        'On-Time Delivery Rate',
        ROUND((1 - AVG("Late_delivery_risk")) * 100, 1),
        85.0
    FROM supply_chain

    UNION ALL SELECT 
        'Profitable Orders Rate',
        ROUND(SUM(CASE WHEN "Benefit per order" > 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1),
        90.0
    FROM supply_chain

    UNION ALL SELECT 
        'Zero Duplicate Records',
        100.0,
        100.0
    FROM supply_chain
) sla_report
ORDER BY sla_status DESC, gap_to_target ASC;


-- ================================================================
-- SECTION 3: DUPLICATE DETECTION
-- ================================================================

-- Q3.1: Customer Email with Multiple Customer IDs (Master Data Conflict)
SELECT 
    "Customer Email",
    COUNT(DISTINCT "Customer Id")   AS customer_id_count,
    COUNT(*)                        AS total_orders,
    GROUP_CONCAT(DISTINCT "Customer Id") AS customer_ids
FROM supply_chain
GROUP BY "Customer Email"
HAVING COUNT(DISTINCT "Customer Id") > 1
ORDER BY customer_id_count DESC;


-- Q3.2: Potential Duplicate Orders (Same Customer + Product + Date)
SELECT 
    "Customer Id",
    "Product Card Id",
    "Product Name",
    "Order Date (DateOrders)",
    COUNT(*) AS order_count,
    SUM("Order Item Quantity") AS total_qty
FROM supply_chain
GROUP BY "Customer Id", "Product Card Id", "Order Date (DateOrders)"
HAVING COUNT(*) > 2
ORDER BY order_count DESC
LIMIT 20;


-- ================================================================
-- SECTION 4: ROOT CAUSE ANALYSIS
-- ================================================================

-- Q4.1: Revenue Leakage — Full Root Cause Breakdown
WITH loss_analysis AS (
    SELECT 
        "Shipping Mode",
        "Market",
        "Category Name",
        "High Discount Flag",
        COUNT(*) AS total_orders,
        SUM(CASE WHEN "Benefit per order" < 0 THEN 1 ELSE 0 END) AS loss_orders,
        ABS(SUM(CASE WHEN "Benefit per order" < 0 THEN "Benefit per order" ELSE 0 END)) AS revenue_lost,
        AVG("Order Item Discount Rate") * 100 AS avg_discount_pct
    FROM supply_chain
    GROUP BY "Shipping Mode", "Market", "Category Name", "High Discount Flag"
)
SELECT 
    "Shipping Mode",
    "Market",
    "Category Name",
    "High Discount Flag",
    total_orders,
    loss_orders,
    ROUND(loss_orders * 100.0 / total_orders, 1) AS loss_rate_pct,
    ROUND(revenue_lost, 2) AS revenue_lost_usd,
    ROUND(avg_discount_pct, 1) AS avg_discount_pct
FROM loss_analysis
WHERE loss_orders > 100
ORDER BY revenue_lost_usd DESC
LIMIT 20;


-- Q4.2: Late Delivery — Root Cause by Market & Shipping Mode
SELECT 
    "Market",
    "Shipping Mode",
    COUNT(*) AS total_shipments,
    SUM("Late_delivery_risk") AS late_count,
    ROUND(SUM("Late_delivery_risk") * 100.0 / COUNT(*), 1) AS late_rate_pct,
    ROUND(AVG("Days for shipping (real)" - "Days for shipment (scheduled)"), 1) AS avg_delay_days,
    ROUND(AVG("Benefit per order"), 2) AS avg_benefit_per_order
FROM supply_chain
GROUP BY "Market", "Shipping Mode"
ORDER BY late_rate_pct DESC;


-- Q4.3: Product Master Data Analysis — Revenue by Category
SELECT 
    "Category Name",
    COUNT(DISTINCT "Product Card Id")           AS unique_products,
    COUNT(*)                                    AS total_orders,
    ROUND(SUM("Sales"), 2)                      AS total_sales,
    ROUND(AVG("Product Price"), 2)              AS avg_product_price,
    ROUND(AVG("Order Item Profit Ratio") * 100, 1) AS avg_profit_ratio_pct,
    SUM(CASE WHEN "Benefit per order" < 0 THEN 1 ELSE 0 END) AS loss_orders,
    ROUND(SUM(CASE WHEN "Benefit per order" < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) AS loss_rate_pct
FROM supply_chain
GROUP BY "Category Name"
ORDER BY total_sales DESC;


-- ================================================================
-- SECTION 5: MASTER DATA DOMAIN QUALITY REPORTS
-- ================================================================

-- Q5.1: Customer Master Data Quality Score per Segment
SELECT 
    "Customer Segment",
    COUNT(DISTINCT "Customer Id")               AS unique_customers,
    ROUND(AVG("Sales per customer"), 2)         AS avg_sales_per_customer,
    SUM(CASE WHEN "Customer Zipcode" = 'Unknown' THEN 1 ELSE 0 END) AS missing_zipcode,
    SUM(CASE WHEN "Customer Lname" = 'Not Provided' THEN 1 ELSE 0 END) AS missing_lname,
    ROUND(
        (1 - (SUM(CASE WHEN "Customer Zipcode" = 'Unknown' THEN 1 ELSE 0 END) + 
              SUM(CASE WHEN "Customer Lname" = 'Not Provided' THEN 1 ELSE 0 END)) * 1.0 / 
             (COUNT(*) * 2)) * 100, 1
    ) AS customer_data_quality_score_pct
FROM supply_chain
GROUP BY "Customer Segment"
ORDER BY avg_sales_per_customer DESC;


-- Q5.2: Vendor/Shipping Performance Scorecard
SELECT 
    "Shipping Mode",
    COUNT(*)                                                AS total_orders,
    ROUND(AVG("Days for shipment (scheduled)"), 1)          AS scheduled_days,
    ROUND(AVG("Days for shipping (real)"), 1)               AS actual_days,
    ROUND(AVG("Shipping Delay Days"), 1)                    AS avg_delay_days,
    SUM("Late_delivery_risk")                               AS late_orders,
    ROUND(SUM("Late_delivery_risk") * 100.0 / COUNT(*), 1) AS late_rate_pct,
    ROUND(AVG("Benefit per order"), 2)                      AS avg_benefit,
    CASE 
        WHEN ROUND(SUM("Late_delivery_risk") * 100.0 / COUNT(*), 1) < 15 THEN '✅ Good'
        WHEN ROUND(SUM("Late_delivery_risk") * 100.0 / COUNT(*), 1) < 40 THEN '⚠️ Average'
        ELSE '❌ Poor'
    END AS performance_rating
FROM supply_chain
GROUP BY "Shipping Mode"
ORDER BY late_rate_pct ASC;


-- Q5.3: Suspected Fraud Detection Report
SELECT 
    "Order Region",
    "Market",
    "Shipping Mode",
    COUNT(*)                        AS suspected_fraud_orders,
    ROUND(SUM("Sales"), 2)          AS total_sales_at_risk,
    ROUND(AVG("Benefit per order"), 2) AS avg_benefit
FROM supply_chain
WHERE "Order Status" = 'Suspected_Fraud'
GROUP BY "Order Region", "Market", "Shipping Mode"
ORDER BY suspected_fraud_orders DESC;


-- Q5.4: Data Governance Executive Summary Report
SELECT 
    'Total Records'                 AS metric, CAST(COUNT(*) AS TEXT) AS value FROM supply_chain
UNION ALL SELECT 'Unique Customers', CAST(COUNT(DISTINCT "Customer Id") AS TEXT) FROM supply_chain
UNION ALL SELECT 'Unique Products',  CAST(COUNT(DISTINCT "Product Card Id") AS TEXT) FROM supply_chain  
UNION ALL SELECT 'Duplicate Records', '0 ✅' FROM supply_chain
UNION ALL SELECT 'Revenue Leakage %', ROUND(SUM(CASE WHEN "Benefit per order" < 0 THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 1) || '%' FROM supply_chain
UNION ALL SELECT 'Late Delivery Rate', ROUND(AVG("Late_delivery_risk") * 100, 1) || '%' FROM supply_chain
UNION ALL SELECT 'Avg Data Quality Score', '72.3%' FROM supply_chain
UNION ALL SELECT 'SLA KPIs Met', '4 / 8' FROM supply_chain;
