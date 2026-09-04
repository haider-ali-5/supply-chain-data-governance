"""
STEP 3: DATA ENRICHMENT & DUPLICATE DETECTION
Master Data Governance Project — Siemens Energy
Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def enrich_and_detect_duplicates(df):
    print("=" * 65)
    print("  STEP 3: DATA ENRICHMENT & DUPLICATE DETECTION")
    print("=" * 65)

    # ── DATA ENRICHMENT ────────────────────────────────────────
    print("\n🔧 Data Enrichment — Adding Derived Master Data Fields:")

    # 1. Customer Value Tier (RFM-style)
    df['Customer Value Tier'] = pd.cut(
        df['Sales per customer'],
        bins=[0, 100, 300, 600, float('inf')],
        labels=['Bronze', 'Silver', 'Gold', 'Platinum']
    )
    print(f"   ✅ Customer Value Tier added (Bronze/Silver/Gold/Platinum)")
    print(f"      Distribution: {df['Customer Value Tier'].value_counts().to_dict()}")

    # 2. Delivery Performance Category
    df['Delivery Performance'] = df.apply(
        lambda x: 'On Time' if x['Late_delivery_risk'] == 0 else 'Late Delivery', axis=1
    )
    print(f"\n   ✅ Delivery Performance added")

    # 3. Profit Category
    df['Profit Category'] = df['Benefit per order'].apply(
        lambda x: 'Profitable' if x > 0 else ('Break Even' if x == 0 else 'Loss Making')
    )
    print(f"   ✅ Profit Category added")
    print(f"      Distribution: {df['Profit Category'].value_counts().to_dict()}")

    # 4. Shipping Delay Days
    df['Shipping Delay Days'] = (
        df['Days for shipping (real)'] - df['Days for shipment (scheduled)']
    )
    print(f"\n   ✅ Shipping Delay Days calculated")
    print(f"      Avg Delay: {df['Shipping Delay Days'].mean():.1f} days")
    print(f"      Max Delay: {df['Shipping Delay Days'].max():.0f} days")

    # 5. Order Size Category
    df['Order Size'] = pd.cut(
        df['Order Item Quantity'],
        bins=[0, 1, 3, 5, float('inf')],
        labels=['Single', 'Small', 'Medium', 'Large']
    )
    print(f"\n   ✅ Order Size Category added")

    # 6. Discount Impact Flag
    df['High Discount Flag'] = df['Order Item Discount Rate'].apply(
        lambda x: 'High Discount (>30%)' if x > 0.30 else 'Normal Discount'
    )
    discount_high = (df['High Discount Flag'] == 'High Discount (>30%)').sum()
    print(f"   ✅ High Discount Flag added: {discount_high:,} high-discount orders")

    # 7. Data Completeness Score per record
    key_fields = ['Customer Id', 'Customer Email', 'Customer Segment',
                  'Product Name', 'Order Id', 'Shipping Mode']
    df['Record Completeness Score'] = df[key_fields].notna().sum(axis=1) / len(key_fields) * 100
    print(f"\n   ✅ Record Completeness Score added")
    print(f"      Avg Score: {df['Record Completeness Score'].mean():.1f}%")

    # ── DUPLICATE DETECTION ────────────────────────────────────
    print(f"\n🔍 Duplicate Detection:")

    # Check exact duplicates
    exact_dupes = df.duplicated().sum()
    print(f"   Exact Duplicate Records    : {exact_dupes:,} {'✅ None' if exact_dupes == 0 else '❌ Found'}")

    # Check Customer Email duplicates
    email_dupes = df.groupby('Customer Email')['Customer Id'].nunique()
    email_issues = email_dupes[email_dupes > 1]
    print(f"   Email → Multiple CustomerID: {len(email_issues):,} cases")

    # Check product name duplicates
    product_dupes = df.groupby('Product Name')['Product Card Id'].nunique()
    product_issues = product_dupes[product_dupes > 1]
    print(f"   Product Name → Multiple IDs: {len(product_issues):,} cases")

    # Suspicious orders (same customer, same product, same date)
    suspicious = df.groupby(
        ['Customer Id', 'Product Card Id', 'Order Date (DateOrders)']
    ).size().reset_index(name='count')
    suspicious = suspicious[suspicious['count'] > 1]
    print(f"   Suspicious Order Duplicates : {len(suspicious):,} cases")

    # Summary
    print(f"\n   Duplicate Detection Summary:")
    print(f"   → Data integrity is {'✅ GOOD' if exact_dupes == 0 else '❌ NEEDS ATTENTION'}")
    print(f"   → {len(email_issues)} customer email conflicts need resolution")

    print(f"\n✅ Enrichment & duplicate detection complete!")
    return df

if __name__ == "__main__":
    df = pd.read_csv('../output/supply_chain_cleaned.csv', encoding='latin1')
    df_enriched = enrich_and_detect_duplicates(df)
    df_enriched.to_csv('../output/supply_chain_enriched.csv', index=False)
    print("   Enriched data saved to output/")
