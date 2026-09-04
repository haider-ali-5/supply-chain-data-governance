"""
STEP 2: DATA CLEANSING & VALIDATION
Master Data Governance Project — Siemens Energy
Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def cleanse_and_validate(df):
    print("=" * 65)
    print("  STEP 2: DATA CLEANSING & VALIDATION")
    print("=" * 65)

    original_count = len(df)

    # ── CLEANSING ──────────────────────────────────────────────
    print("\n🧹 Data Cleansing:")

    # Remove duplicates
    df = df.drop_duplicates()
    removed = original_count - len(df)
    print(f"   Duplicates removed     : {removed:,}")

    # Standardize text fields
    text_cols = ['Customer Segment', 'Shipping Mode', 'Order Status', 
                 'Customer City', 'Order Status']
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].str.strip().str.title()

    # Fill missing values
    df['Customer Lname']        = df['Customer Lname'].fillna('Not Provided')
    df['Customer Zipcode']      = df['Customer Zipcode'].fillna('Unknown')
    df['Order Zipcode']         = df['Order Zipcode'].fillna('Unknown')
    df['Product Description']   = df['Product Description'].fillna('Pending Enrichment')
    print(f"   Missing values handled : ✅")

    # Fix data types
    if 'Order Date (DateOrders)' in df.columns:
        df['Order Date (DateOrders)'] = pd.to_datetime(
            df['Order Date (DateOrders)'], errors='coerce')
    if 'Shipping Date (DateOrders)' in df.columns:
        df['Shipping Date (DateOrders)'] = pd.to_datetime(
            df['Shipping Date (DateOrders)'], errors='coerce')
    print(f"   Data types corrected   : ✅")

    # ── VALIDATION (Business Rules) ───────────────────────────
    print(f"\n✔️  Business Rules Validation:")

    rules = {}

    # Customer Domain Rules
    rules['BR-C01: Customer ID Not Null'] = (
        'PASS ✅' if df['Customer Id'].isnull().sum() == 0 
        else f'FAIL ❌ ({df["Customer Id"].isnull().sum()} records)')

    rules['BR-C02: Valid Customer Segment'] = (
        'PASS ✅' if df[~df['Customer Segment'].isin(
            ['Consumer', 'Corporate', 'Home Office'])].shape[0] == 0
        else f'FAIL ❌')

    rules['BR-C03: Customer Email Not Null'] = (
        'PASS ✅' if df['Customer Email'].isnull().sum() == 0
        else f'FAIL ❌ ({df["Customer Email"].isnull().sum()} records)')

    # Product Domain Rules
    rules['BR-P01: Product Price Positive'] = (
        'PASS ✅' if df[df['Product Price'] <= 0].shape[0] == 0
        else f'FAIL ❌ ({df[df["Product Price"] <= 0].shape[0]} records)')

    rules['BR-P02: Product Name Not Null'] = (
        'PASS ✅' if df['Product Name'].isnull().sum() == 0
        else f'FAIL ❌ ({df["Product Name"].isnull().sum()} records)')

    rules['BR-P03: Product Description Filled'] = (
        'PASS ✅' if (df['Product Description'] == 'Pending Enrichment').sum() == 0
        else f'REVIEW ⚠️ ({(df["Product Description"] == "Pending Enrichment").sum():,} need enrichment)')

    # Order Domain Rules
    rules['BR-O01: Order ID Not Null'] = (
        'PASS ✅' if df['Order Id'].isnull().sum() == 0
        else f'FAIL ❌')

    rules['BR-O02: Valid Shipping Mode'] = (
        'PASS ✅' if df[~df['Shipping Mode'].isin(
            ['Standard Class', 'First Class', 'Second Class', 'Same Day'])].shape[0] == 0
        else f'FAIL ❌')

    # Vendor Domain Rules
    neg_profit = df[df['Benefit per order'] < 0].shape[0]
    rules['BR-V01: Negative Profit Orders'] = (
        f'REVIEW ⚠️ ({neg_profit:,} orders = {neg_profit/len(df)*100:.1f}%)')

    late = df['Late_delivery_risk'].sum()
    rules['BR-V02: Late Delivery Rate'] = (
        f'REVIEW ⚠️ ({late:,} orders = {late/len(df)*100:.1f}%)')

    fraud = df[df['Order Status'] == 'Suspected_Fraud'].shape[0]
    rules['BR-V03: Suspected Fraud Orders'] = (
        f'REVIEW ⚠️ ({fraud:,} orders = {fraud/len(df)*100:.1f}%)'
        if fraud > 0 else 'PASS ✅')

    # Print results
    pass_count = sum(1 for v in rules.values() if 'PASS' in v)
    fail_count = sum(1 for v in rules.values() if 'FAIL' in v)
    review_count = sum(1 for v in rules.values() if 'REVIEW' in v)

    for rule, result in rules.items():
        print(f"   {rule}: {result}")

    print(f"\n   Summary: {pass_count} PASS | {fail_count} FAIL | {review_count} REVIEW")

    print(f"\n✅ Cleansing & validation complete!")
    return df, rules

if __name__ == "__main__":
    df = pd.read_csv('../data/supply_chain.csv', encoding='latin1')
    df_clean, rules = cleanse_and_validate(df)
    df_clean.to_csv('../output/supply_chain_cleaned.csv', index=False)
    print("   Cleaned data saved to output/")
