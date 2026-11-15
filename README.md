# 🏭 Master Data Governance Analysis
### Supply Chain Data Quality Management Pipeline

**Author:** Haider Ali  
**Degree:** M.Sc. Data Science — Berliner Hochschule für Technik (BHT), Berlin  
**Tools:** Python · SQL · Matplotlib · Pandas · NumPy · OpenPyXL  

---

## 📌 Project Overview

An end-to-end **Master Data Governance** pipeline simulating enterprise-level data quality management across a Supply Chain dataset of **180,519 records**.

The project follows the complete data governance lifecycle — from profiling and cleansing to enrichment, root cause analysis, SLA compliance monitoring, and executive reporting — aligned with industry standards used in SAP-based ERP environments.

---

## 🎯 Key Findings

| KPI | Result | SLA Target | Status |
|-----|--------|-----------|--------|
| Duplicate Records | 0 | 0 | ✅ Pass |
| Customer ID Completeness | 100% | 99% | ✅ Pass |
| Customer Segment Validity | 100% | 99% | ✅ Pass |
| Shipping Mode Validity | 100% | 99% | ✅ Pass |
| Order Zipcode Completeness | 13.8% | 99% | ❌ Critical |
| Product Description Completeness | 0% | 99% | ❌ Critical |
| On-Time Delivery Rate | 45.2% | 85% | ❌ Critical |
| Profitable Orders Rate | 80.6% | 90% | ⚠️ Below Target |
| **Revenue Leakage** | **10.6%** | **<5%** | **❌ Critical** |

---

## 🏗️ Project Structure

```
supply-chain-data-governance/
│
├── 📁 data/
│   ├── supply_chain.csv              # Raw DataCo Supply Chain dataset
│   └── data_dictionary.csv          # Column descriptions
│
├── 📁 src/
│   ├── 01_data_profiling.py         # Step 1: Load & profile all domains
│   ├── 02_cleansing_validation.py   # Step 2: Cleanse + 11 business rules
│   ├── 03_enrichment_deduplication.py # Step 3: Enrich + detect duplicates
│   ├── 04_root_cause_analysis.py    # Step 4: RCA — revenue & delivery
│   └── 05_visualizations.py         # Step 5: 5 professional charts
│
├── 📁 sql/
│   └── governance_queries.sql       # 12 SQL queries across 5 sections
│
├── 📁 output/
│   ├── supply_chain_cleaned.csv     # After cleansing
│   ├── supply_chain_enriched.csv    # After enrichment
│   └── 📁 charts/
│       ├── 01_data_quality_dashboard.png
│       ├── 02_revenue_leakage_analysis.png
│       ├── 03_late_delivery_analysis.png
│       ├── 04_master_data_completeness.png
│       └── 05_sla_compliance_report.png
│
├── 📁 docs/
│   └── master_data_quality_report.xlsx  # Excel: 3-sheet governance report
│
└── main.py                          # Run full pipeline (all 5 steps)
```

---

## 🔄 Pipeline: 5-Step Data Governance Process

### Step 1 — Data Profiling
- Load 180,519 records across 53 fields
- Identify 4 master data domains: Customer, Product, Order, Vendor
- Analyze missing values, data types, and completeness per domain

### Step 2 — Data Cleansing & Validation
- Remove duplicates (0 found — ✅)
- Standardize text fields (Customer Segment, Shipping Mode)
- Handle missing values with enrichment or flagging
- Apply **11 Business Rules** (BR-C01 to BR-V03):
  - Customer Domain: ID not null, valid segment, email not null
  - Product Domain: price positive, name not null, description filled
  - Order Domain: ID not null, valid shipping mode
  - Vendor Domain: negative profit flag, late delivery flag, fraud flag

### Step 3 — Data Enrichment & Duplicate Detection
- Added **6 derived fields**:
  - `Customer Value Tier` (Bronze/Silver/Gold/Platinum)
  - `Delivery Performance` (On Time / Late Delivery)
  - `Profit Category` (Profitable / Break Even / Loss Making)
  - `Shipping Delay Days`
  - `Order Size` (Single / Small / Medium / Large)
  - `High Discount Flag` (>30% discount threshold)
- Detected duplicate patterns across Customer Email and Order records

### Step 4 — Root Cause Analysis
- **Revenue Leakage:** 33,784 orders (18.7%) lose money, costing $3.88M = 10.6% of total sales → Largest share comes from Standard Class shipping ($2.33M of the loss); no order exceeds the 30% discount threshold, so discounting is not the driver
- **Late Deliveries:** 54.8% late → Late rate is uniform across markets (54.4–55.2%); the driver is shipping mode: First Class 95.3% late, Second Class 76.6%, Standard Class 38.1%
- **Data Quality:** Order Zipcode 86.2% missing → Not captured for international orders in ERP system

### Step 5 — Visualizations (5 Charts)
- Data Quality Overview Dashboard (KPI cards + bar charts)
- Revenue Leakage Root Cause Analysis
- Late Delivery Root Cause Analysis
- Master Data Completeness by Domain
- SLA Compliance Report (Actual vs Target)

---

## 📊 SQL Queries (5 Sections, 12 Queries)

| Section | Queries |
|---------|---------|
| 1. Data Profiling | Dataset profile, missing values report |
| 2. SLA Compliance | Full 8-KPI SLA compliance report |
| 3. Duplicate Detection | Customer email conflicts, suspicious orders |
| 4. Root Cause Analysis | Revenue leakage, late delivery, product RCA |
| 5. Domain Reports | Customer quality score, vendor scorecard, fraud detection, executive summary |

---

## 📋 Excel Report (3 Sheets)

| Sheet | Content |
|-------|---------|
| Data Quality Report | Color-coded overview + missing values + domain analysis |
| Business Rules | 15 BR rules with validation logic and actions |
| Process Workflow | 10-step governance process with tools used |

---

## 🚀 How to Run

### 1. Get the data

The dataset is not included in the repo (see `.gitignore`). Download the
**DataCo Smart Supply Chain for Big Data Analysis** dataset from Kaggle:
<https://www.kaggle.com/datasets/shashwatwork/dataco-smart-supply-chain-for-big-data-analysis>

Extract `DataCoSupplyChainDataset.csv` and save it as `data/supply_chain.csv`
(create the `data/` folder if it does not exist).

### 2. Run

```bash
# Clone the repo
git clone https://github.com/haider-ali-5/supply-chain-data-governance.git
cd supply-chain-data-governance

# Install dependencies
pip install pandas numpy matplotlib seaborn openpyxl

# Run full pipeline
python3 main.py

# Or run individual steps
cd src
python3 01_data_profiling.py
python3 02_cleansing_validation.py
python3 03_enrichment_deduplication.py
python3 04_root_cause_analysis.py
python3 05_visualizations.py
```

---

## 💡 Business Recommendations

| Priority | Issue | Root Cause | Recommendation |
|----------|-------|-----------|----------------|
| 🔴 High | Revenue Leakage (10.6%) | Loss-making orders concentrated in Standard Class ($2.33M of $3.88M) | Review Standard Class pricing and shipping cost vs. margin |
| 🔴 High | Late Deliveries (54.8%) | First Class (95.3% late) and Second Class (76.6% late) | Review First/Second Class delivery promises and carrier performance |
| 🔴 High | Order Zipcode Missing (86.2%) | Not captured in ERP | Make mandatory in SAP order entry |
| 🔴 High | Product Description Empty | No catalog integration | Integrate product catalog into SAP MDM |
| 🟡 Medium | Suspected Fraud (2.3%) | No fraud detection rules | Implement automated fraud flagging |

---

## 🛠️ Technologies Used

```
Python 3.12        — Core analysis language
Pandas             — Data manipulation and profiling
NumPy              — Numerical operations
Matplotlib         — Professional data visualizations
OpenPyXL           — Excel report generation
SQL (SQLite/BigQuery) — Data validation and governance queries
Git/GitHub         — Version control and documentation
```

---

## 📬 Contact

**Haider Ali**  
📧 haiderali106403@gmail.com  
🔗 [linkedin.com/in/haiderali8237](https://linkedin.com/in/haiderali8237)  
💻 [github.com/haider-ali-5](https://github.com/haider-ali-5)
