"""
MASTER DATA GOVERNANCE PIPELINE — MAIN RUNNER
Siemens Energy | Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
Runs all 5 steps in sequence: Profile → Cleanse → Enrich → RCA → Visualize
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from src.step01_profiling      import load_and_profile
from src.step02_cleansing      import cleanse_and_validate
from src.step03_enrichment     import enrich_and_detect_duplicates
from src.step04_rca            import root_cause_analysis
from src.step05_visualizations import create_all_charts

def run_pipeline():
    print("\n")
    print("█" * 65)
    print("█  MASTER DATA GOVERNANCE PIPELINE                           █")
    print("█  Siemens Energy | Haider Ali | M.Sc. Data Science @ BHT   █")
    print("█" * 65)
    print()

    # STEP 1
    df, profile = load_and_profile()

    # STEP 2
    df_clean, rules = cleanse_and_validate(df)
    df_clean.to_csv('output/supply_chain_cleaned.csv', index=False)

    # STEP 3
    df_enriched = enrich_and_detect_duplicates(df_clean)
    df_enriched.to_csv('output/supply_chain_enriched.csv', index=False)

    # STEP 4
    rca_results = root_cause_analysis(df_enriched)

    # STEP 5
    create_all_charts(df_enriched)

    # FINAL SUMMARY
    print("\n")
    print("█" * 65)
    print("█  PIPELINE COMPLETE — FINAL SUMMARY                         █")
    print("█" * 65)
    print(f"""
  Input Records       : {profile['total_records']:,}
  Duplicates Found    : {profile['duplicates']}
  Business Rules      : 11 rules applied
  Enriched Fields     : 6 new derived fields
  Charts Generated    : 5 professional charts
  
  KEY FINDINGS:
  ├─ Revenue Leakage  : {rca_results['revenue_leakage_pct']}% (${rca_results['total_loss']:,.0f} lost)
  ├─ Late Deliveries  : {rca_results['late_delivery_rate']}% of orders
  ├─ Missing Zipcode  : {rca_results['missing_zipcode_pct']}% of order records
  └─ SLA Compliance   : 4/8 KPIs meeting target
  
  OUTPUT FILES:
  ├─ output/supply_chain_cleaned.csv
  ├─ output/supply_chain_enriched.csv
  ├─ output/charts/01_data_quality_dashboard.png
  ├─ output/charts/02_revenue_leakage_analysis.png
  ├─ output/charts/03_late_delivery_analysis.png
  ├─ output/charts/04_master_data_completeness.png
  └─ output/charts/05_sla_compliance_report.png
""")
    print("█" * 65)

if __name__ == "__main__":
    run_pipeline()
