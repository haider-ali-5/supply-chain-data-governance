"""
SUPPLY CHAIN MASTER DATA GOVERNANCE PIPELINE — MAIN RUNNER
Supply Chain Master Data Governance | Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
Runs all 5 steps in sequence: Profile → Cleanse → Enrich → RCA → Visualize
"""

import os
import importlib.util
import warnings
warnings.filterwarnings('ignore')

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, 'src')
OUTPUT_DIR = os.path.join(ROOT, 'output')


def _load_step(filename, func_name):
    """Load a function from a numbered step file (e.g. 01_data_profiling.py).

    Names starting with a digit are not valid for a normal `import`,
    so the file is loaded by path with importlib.
    """
    path = os.path.join(SRC_DIR, filename)
    spec = importlib.util.spec_from_file_location(filename[:-3].replace('.', '_'), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, func_name)


load_and_profile              = _load_step('01_data_profiling.py',           'load_and_profile')
cleanse_and_validate          = _load_step('02_cleansing_validation.py',     'cleanse_and_validate')
enrich_and_detect_duplicates  = _load_step('03_enrichment_deduplication.py', 'enrich_and_detect_duplicates')
root_cause_analysis           = _load_step('04_root_cause_analysis.py',      'root_cause_analysis')
create_all_charts             = _load_step('05_visualizations.py',           'create_all_charts')


def run_pipeline():
    print("\n")
    print("█" * 65)
    print("█  MASTER DATA GOVERNANCE PIPELINE                           █")
    print("█  Supply Chain Master Data Governance | Haider Ali         █")
    print("█" * 65)
    print()

    # The step modules use paths relative to src/ (e.g. ../data/supply_chain.csv),
    # so run the pipeline from there regardless of where main.py was launched.
    os.chdir(SRC_DIR)
    os.makedirs(os.path.join(OUTPUT_DIR, 'charts'), exist_ok=True)

    # STEP 1
    df, profile = load_and_profile()

    # STEP 2
    df_clean, rules = cleanse_and_validate(df)
    df_clean.to_csv(os.path.join(OUTPUT_DIR, 'supply_chain_cleaned.csv'), index=False)

    # STEP 3
    df_enriched = enrich_and_detect_duplicates(df_clean)
    df_enriched.to_csv(os.path.join(OUTPUT_DIR, 'supply_chain_enriched.csv'), index=False)

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
