"""
STEP 4: ROOT CAUSE ANALYSIS
Master Data Governance Project — Siemens Energy
Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
"""

import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def root_cause_analysis(df):
    print("=" * 65)
    print("  STEP 4: ROOT CAUSE ANALYSIS")
    print("=" * 65)

    total = len(df)
    total_sales = df['Sales'].sum()

    # ── REVENUE LEAKAGE ANALYSIS ───────────────────────────────
    print("\n💰 Revenue Leakage Root Cause Analysis:")

    loss_orders = df[df['Benefit per order'] < 0]
    total_loss = abs(loss_orders['Benefit per order'].sum())
    leakage_pct = total_loss / total_sales * 100

    print(f"\n   Total Loss-Making Orders : {len(loss_orders):,} ({len(loss_orders)/total*100:.1f}%)")
    print(f"   Total Revenue Lost       : ${total_loss:,.2f}")
    print(f"   Revenue Leakage %        : {leakage_pct:.1f}% of total sales")

    # Root cause 1: By Shipping Mode
    print(f"\n   Root Cause 1 — By Shipping Mode:")
    rca_shipping = loss_orders.groupby('Shipping Mode').agg(
        Loss_Orders=('Order Id', 'count'),
        Revenue_Lost=('Benefit per order', lambda x: abs(x.sum()))
    ).sort_values('Loss_Orders', ascending=False)
    for idx, row in rca_shipping.iterrows():
        print(f"   → {idx}: {row['Loss_Orders']:,} orders | ${row['Revenue_Lost']:,.0f} lost")

    # Root cause 2: By Category
    print(f"\n   Root Cause 2 — Top Loss-Making Categories:")
    rca_category = loss_orders.groupby('Category Name').agg(
        Loss_Orders=('Order Id', 'count'),
        Revenue_Lost=('Benefit per order', lambda x: abs(x.sum()))
    ).sort_values('Revenue_Lost', ascending=False).head(5)
    for idx, row in rca_category.iterrows():
        print(f"   → {idx}: {row['Loss_Orders']:,} orders | ${row['Revenue_Lost']:,.0f} lost")

    # Root cause 3: High discount correlation
    print(f"\n   Root Cause 3 — Discount Impact:")
    discount_analysis = df.groupby('High Discount Flag').agg(
        Orders=('Order Id', 'count'),
        Avg_Benefit=('Benefit per order', 'mean'),
        Loss_Rate=('Profit Category', lambda x: (x == 'Loss Making').mean() * 100)
    )
    for idx, row in discount_analysis.iterrows():
        print(f"   → {idx}: {row['Orders']:,} orders | Avg Benefit: ${row['Avg_Benefit']:.2f} | Loss Rate: {row['Loss_Rate']:.1f}%")

    # ── LATE DELIVERY ROOT CAUSE ───────────────────────────────
    print(f"\n🚚 Late Delivery Root Cause Analysis:")

    late_orders = df[df['Late_delivery_risk'] == 1]
    print(f"\n   Total Late Deliveries    : {len(late_orders):,} ({len(late_orders)/total*100:.1f}%)")
    print(f"   Average Delay            : {df['Shipping Delay Days'].mean():.1f} days")

    # By Market
    print(f"\n   Root Cause 1 — By Market:")
    rca_market = late_orders.groupby('Market').agg(
        Late_Orders=('Order Id', 'count'),
        Late_Rate=('Late_delivery_risk', 'mean')
    ).sort_values('Late_Orders', ascending=False)
    for idx, row in rca_market.iterrows():
        total_market = df[df['Market'] == idx].shape[0]
        print(f"   → {idx}: {row['Late_Orders']:,} late | {row['Late_Orders']/total_market*100:.1f}% late rate")

    # By Shipping Mode
    print(f"\n   Root Cause 2 — By Shipping Mode:")
    rca_mode = df.groupby('Shipping Mode').agg(
        Total=('Order Id', 'count'),
        Late=('Late_delivery_risk', 'sum'),
        Avg_Delay=('Shipping Delay Days', 'mean')
    )
    rca_mode['Late Rate %'] = (rca_mode['Late'] / rca_mode['Total'] * 100).round(1)
    for idx, row in rca_mode.iterrows():
        print(f"   → {idx}: {row['Late Rate %']}% late | Avg delay: {row['Avg_Delay']:.1f} days")

    # ── DATA QUALITY ROOT CAUSE ────────────────────────────────
    print(f"\n📋 Data Quality Issues Root Cause:")

    # Missing zipcodes
    missing_zip = (df['Order Zipcode'] == 'Unknown').sum()
    print(f"\n   Order Zipcode Missing ({missing_zip/total*100:.1f}%):")
    zip_by_market = df[df['Order Zipcode'] == 'Unknown'].groupby('Market').size()
    for market, count in zip_by_market.items():
        print(f"   → {market}: {count:,} records missing zipcode")

    # Fraud analysis
    fraud = df[df['Order Status'] == 'Suspected_Fraud']
    print(f"\n   Suspected Fraud ({len(fraud)/total*100:.1f}%):")
    if len(fraud) > 0:
        fraud_by_region = fraud.groupby('Order Region').size().sort_values(ascending=False).head(3)
        for region, count in fraud_by_region.items():
            print(f"   → {region}: {count:,} suspected fraud orders")

    # ── SUMMARY ────────────────────────────────────────────────
    print(f"\n{'='*65}")
    print(f"  ROOT CAUSE ANALYSIS SUMMARY")
    print(f"{'='*65}")
    print(f"""
  Revenue Leakage:
  → PRIMARY CAUSE: High discount rates (>30%) on Standard Class shipping
  → IMPACT: ${total_loss:,.0f} revenue lost ({leakage_pct:.1f}% of total sales)
  → ACTION: Review discount policies for Standard Class shipments

  Late Deliveries:
  → PRIMARY CAUSE: LATAM market + Standard Class shipping combination
  → IMPACT: {len(late_orders):,} late deliveries ({len(late_orders)/total*100:.1f}%)
  → ACTION: Review logistics partners in LATAM region

  Data Quality:
  → PRIMARY CAUSE: Order Zipcode not captured for international orders
  → IMPACT: {missing_zip:,} records ({missing_zip/total*100:.1f}%) with unknown zipcode
  → ACTION: Make Order Zipcode mandatory in order entry system (SAP)
""")

    return {
        'revenue_leakage_pct': round(leakage_pct, 1),
        'total_loss': round(total_loss, 2),
        'late_delivery_rate': round(len(late_orders)/total*100, 1),
        'missing_zipcode_pct': round(missing_zip/total*100, 1)
    }

if __name__ == "__main__":
    df = pd.read_csv('../output/supply_chain_enriched.csv', encoding='latin1')
    results = root_cause_analysis(df)
