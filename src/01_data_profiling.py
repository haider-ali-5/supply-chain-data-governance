"""
STEP 1: DATA PROFILING & QUALITY ASSESSMENT
Master Data Governance Project — Siemens Energy
Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def load_and_profile():
    print("=" * 65)
    print("  STEP 1: DATA PROFILING & QUALITY ASSESSMENT")
    print("  Master Data Governance | Haider Ali | BHT Berlin")
    print("=" * 65)

    # Load dataset
    df = pd.read_csv('../data/supply_chain.csv', encoding='latin1')
    
    print(f"\n📦 Dataset Overview:")
    print(f"   Records       : {len(df):,}")
    print(f"   Columns       : {len(df.columns)}")
    print(f"   Memory Usage  : {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    print(f"   Duplicates    : {df.duplicated().sum():,}")

    # Master Data Domains
    print(f"\n📋 Master Data Domains Identified:")
    domains = {
        'Customer Master Data': ['Customer Id', 'Customer Fname', 'Customer Lname', 
                                  'Customer Email', 'Customer Segment', 
                                  'Customer City', 'Customer State', 
                                  'Customer Zipcode', 'Customer Country'],
        'Product Master Data':  ['Product Card Id', 'Product Name', 
                                  'Product Description', 'Product Price', 
                                  'Product Image', 'Category Name', 'Category Id'],
        'Order Master Data':    ['Order Id', 'Order Status', 'Order Date (DateOrders)',
                                  'Order City', 'Order State', 'Order Zipcode', 
                                  'Order Region', 'Order Country'],
        'Vendor/Shipping Data': ['Shipping Mode', 'Days for shipping (real)',
                                  'Days for shipment (scheduled)', 
                                  'Late_delivery_risk', 'Delivery Status'],
    }

    for domain, cols in domains.items():
        existing = [c for c in cols if c in df.columns]
        print(f"   {domain}: {len(existing)} fields")

    # Missing Values
    print(f"\n🔍 Missing Values Analysis:")
    null_report = df.isnull().sum()
    null_pct = (null_report / len(df) * 100).round(2)
    missing = pd.DataFrame({
        'Column': null_report.index,
        'Missing Count': null_report.values,
        'Missing %': null_pct.values
    }).query('`Missing Count` > 0').sort_values('Missing %', ascending=False)
    
    for _, row in missing.iterrows():
        status = "❌ CRITICAL" if row['Missing %'] > 50 else "⚠️  WARNING" if row['Missing %'] > 5 else "ℹ️  MINOR"
        print(f"   {status} | {row['Column']}: {row['Missing Count']:,} ({row['Missing %']}%)")

    # Data Types
    print(f"\n📊 Data Type Summary:")
    dtype_counts = df.dtypes.value_counts()
    for dtype, count in dtype_counts.items():
        print(f"   {dtype}: {count} columns")

    # Save profiling report
    profile_report = {
        'total_records': len(df),
        'total_columns': len(df.columns),
        'duplicates': int(df.duplicated().sum()),
        'missing_columns': len(missing),
        'total_missing_values': int(null_report.sum())
    }
    
    print(f"\n✅ Profiling complete! Report saved.")
    return df, profile_report

if __name__ == "__main__":
    df, report = load_and_profile()
