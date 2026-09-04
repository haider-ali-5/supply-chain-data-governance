"""
STEP 5: DATA GOVERNANCE VISUALIZATIONS
Master Data Governance Project — Siemens Energy
Author: Haider Ali | M.Sc. Data Science @ BHT Berlin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import warnings
warnings.filterwarnings('ignore')

# Color Palette — Professional
BLUE     = '#2563EB'
DARK     = '#1A1A2E'
GREEN    = '#16A34A'
RED      = '#DC2626'
YELLOW   = '#F59E0B'
GRAY     = '#6B7280'
LIGHT    = '#EFF6FF'
WHITE    = '#FFFFFF'

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.facecolor': WHITE,
    'figure.facecolor': WHITE,
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.color': '#E5E7EB'
})

def create_all_charts(df):
    print("=" * 65)
    print("  STEP 5: GENERATING VISUALIZATIONS")
    print("=" * 65)

    # ── CHART 1: DATA QUALITY OVERVIEW DASHBOARD ─────────────
    print("\n📊 Chart 1: Data Quality Overview Dashboard...")

    fig = plt.figure(figsize=(18, 10))
    fig.patch.set_facecolor(WHITE)
    gs = gridspec.GridSpec(2, 4, figure=fig, hspace=0.45, wspace=0.4)

    # Title
    fig.suptitle('Master Data Quality & Governance Dashboard\nDataCo Supply Chain — Haider Ali | BHT Berlin',
                 fontsize=16, fontweight='bold', color=DARK, y=1.01)

    # KPI 1: Data Quality Score
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    quality_score = 72.3
    color = GREEN if quality_score >= 90 else YELLOW if quality_score >= 70 else RED
    ax_kpi1.text(0.5, 0.6, f'{quality_score}%', ha='center', va='center',
                fontsize=32, fontweight='bold', color=color, transform=ax_kpi1.transAxes)
    ax_kpi1.text(0.5, 0.25, 'Data Quality Score', ha='center', va='center',
                fontsize=10, color=GRAY, transform=ax_kpi1.transAxes)
    ax_kpi1.text(0.5, 0.1, '⚠️ Needs Improvement', ha='center', va='center',
                fontsize=8, color=YELLOW, transform=ax_kpi1.transAxes)
    ax_kpi1.set_xlim(0, 1); ax_kpi1.set_ylim(0, 1)
    ax_kpi1.axis('off')
    ax_kpi1.set_facecolor(LIGHT)
    for spine in ax_kpi1.spines.values(): spine.set_visible(False)

    # KPI 2: Revenue Leakage
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    ax_kpi2.text(0.5, 0.6, '19.4%', ha='center', va='center',
                fontsize=32, fontweight='bold', color=RED, transform=ax_kpi2.transAxes)
    ax_kpi2.text(0.5, 0.25, 'Revenue Leakage', ha='center', va='center',
                fontsize=10, color=GRAY, transform=ax_kpi2.transAxes)
    ax_kpi2.text(0.5, 0.1, '❌ Critical — $3.9M Lost', ha='center', va='center',
                fontsize=8, color=RED, transform=ax_kpi2.transAxes)
    ax_kpi2.set_xlim(0, 1); ax_kpi2.set_ylim(0, 1)
    ax_kpi2.axis('off')
    ax_kpi2.set_facecolor('#FEF2F2')

    # KPI 3: Late Delivery
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    ax_kpi3.text(0.5, 0.6, '54.8%', ha='center', va='center',
                fontsize=32, fontweight='bold', color=RED, transform=ax_kpi3.transAxes)
    ax_kpi3.text(0.5, 0.25, 'Late Delivery Rate', ha='center', va='center',
                fontsize=10, color=GRAY, transform=ax_kpi3.transAxes)
    ax_kpi3.text(0.5, 0.1, '❌ Critical — 98,977 Orders', ha='center', va='center',
                fontsize=8, color=RED, transform=ax_kpi3.transAxes)
    ax_kpi3.set_xlim(0, 1); ax_kpi3.set_ylim(0, 1)
    ax_kpi3.axis('off')
    ax_kpi3.set_facecolor('#FEF2F2')

    # KPI 4: Records Analyzed
    ax_kpi4 = fig.add_subplot(gs[0, 3])
    ax_kpi4.text(0.5, 0.6, '180K+', ha='center', va='center',
                fontsize=32, fontweight='bold', color=BLUE, transform=ax_kpi4.transAxes)
    ax_kpi4.text(0.5, 0.25, 'Records Analyzed', ha='center', va='center',
                fontsize=10, color=GRAY, transform=ax_kpi4.transAxes)
    ax_kpi4.text(0.5, 0.1, '✅ 53 Fields | 0 Duplicates', ha='center', va='center',
                fontsize=8, color=GREEN, transform=ax_kpi4.transAxes)
    ax_kpi4.set_xlim(0, 1); ax_kpi4.set_ylim(0, 1)
    ax_kpi4.axis('off')
    ax_kpi4.set_facecolor(LIGHT)

    # Chart: Missing Values by Domain
    ax_missing = fig.add_subplot(gs[1, :2])
    domains = ['Customer\nZipcode', 'Order\nZipcode', 'Product\nDescription', 
               'Customer\nLname']
    missing_pcts = [0.0, 86.2, 100.0, 0.004]
    colors_bar = [GREEN if p < 5 else YELLOW if p < 50 else RED for p in missing_pcts]
    bars = ax_missing.barh(domains, missing_pcts, color=colors_bar, height=0.5)
    ax_missing.set_xlabel('Missing %', color=GRAY, fontsize=10)
    ax_missing.set_title('Missing Values by Master Data Field', 
                         fontweight='bold', color=DARK, fontsize=11)
    ax_missing.set_xlim(0, 110)
    for bar, pct in zip(bars, missing_pcts):
        ax_missing.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2,
                       f'{pct}%', va='center', fontsize=9, 
                       color=RED if pct > 50 else GRAY)
    ax_missing.axvline(x=99, color=GREEN, linestyle='--', alpha=0.5, label='SLA Target (99%)')
    ax_missing.legend(fontsize=8)

    # Chart: Business Rules Status
    ax_rules = fig.add_subplot(gs[1, 2:])
    rule_names = ['Customer ID\nNot Null', 'Product Price\nPositive', 
                  'Valid Customer\nSegment', 'Valid Shipping\nMode',
                  'No Negative\nProfit', 'On-Time\nDelivery']
    scores = [100, 100, 100, 100, 80.6, 45.2]
    colors_rules = [GREEN if s >= 99 else YELLOW if s >= 80 else RED for s in scores]
    bars2 = ax_rules.bar(rule_names, scores, color=colors_rules, width=0.5)
    ax_rules.set_ylabel('Compliance %', color=GRAY, fontsize=10)
    ax_rules.set_title('Business Rules Compliance', fontweight='bold', color=DARK, fontsize=11)
    ax_rules.set_ylim(0, 115)
    ax_rules.axhline(y=99, color=GREEN, linestyle='--', alpha=0.5, label='SLA Target (99%)')
    ax_rules.legend(fontsize=8)
    for bar, score in zip(bars2, scores):
        ax_rules.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                     f'{score}%', ha='center', fontsize=8, fontweight='bold',
                     color=RED if score < 80 else GRAY)
    ax_rules.tick_params(axis='x', labelsize=8)

    plt.savefig('../output/charts/01_data_quality_dashboard.png', 
                bbox_inches='tight', dpi=150, facecolor=WHITE)
    plt.close()
    print("   ✅ Chart 1 saved: 01_data_quality_dashboard.png")

    # ── CHART 2: REVENUE LEAKAGE ANALYSIS ────────────────────
    print("\n📊 Chart 2: Revenue Leakage Analysis...")

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Revenue Leakage Root Cause Analysis\nMaster Data Governance | Haider Ali',
                fontsize=14, fontweight='bold', color=DARK, y=1.02)

    # Profit Category donut
    profit_counts = df['Profit Category'].value_counts()
    colors_profit = [GREEN if x == 'Profitable' else RED if x == 'Loss Making' else YELLOW 
                    for x in profit_counts.index]
    wedges, texts, autotexts = axes[0].pie(
        profit_counts.values,
        labels=profit_counts.index,
        autopct='%1.1f%%',
        colors=colors_profit,
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5)
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    axes[0].set_title('Order Profitability Distribution', fontweight='bold', color=DARK)

    # Revenue leakage by shipping mode
    loss_df = df[df['Profit Category'] == 'Loss Making']
    shipping_loss = loss_df.groupby('Shipping Mode').agg(
        Revenue_Lost=('Benefit per order', lambda x: abs(x.sum()))
    ).sort_values('Revenue_Lost', ascending=True)
    colors_ship = [RED if i == len(shipping_loss)-1 else YELLOW 
                  for i in range(len(shipping_loss))]
    bars = axes[1].barh(shipping_loss.index, shipping_loss['Revenue_Lost']/1000, 
                        color=colors_ship, height=0.5)
    axes[1].set_xlabel('Revenue Lost ($K)', color=GRAY)
    axes[1].set_title('Revenue Leakage by\nShipping Mode', fontweight='bold', color=DARK)
    for bar in bars:
        axes[1].text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
                    f'${bar.get_width():.0f}K', va='center', fontsize=8)

    # Discount impact
    discount_rca = df.groupby('High Discount Flag').agg(
        Loss_Rate=('Profit Category', lambda x: (x == 'Loss Making').mean() * 100),
        Avg_Benefit=('Benefit per order', 'mean')
    ).reset_index()
    colors_disc = [RED if 'High' in x else GREEN for x in discount_rca['High Discount Flag']]
    bars3 = axes[2].bar(
        ['Normal\nDiscount', 'High Discount\n(>30%)'],
        discount_rca['Loss_Rate'].values,
        color=colors_disc, width=0.4
    )
    axes[2].set_ylabel('Loss Rate %', color=GRAY)
    axes[2].set_title('Loss Rate by\nDiscount Level', fontweight='bold', color=DARK)
    axes[2].set_ylim(0, 50)
    for bar, val in zip(bars3, discount_rca['Loss_Rate'].values):
        axes[2].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}%', ha='center', fontsize=10, fontweight='bold')

    plt.tight_layout()
    plt.savefig('../output/charts/02_revenue_leakage_analysis.png',
                bbox_inches='tight', dpi=150, facecolor=WHITE)
    plt.close()
    print("   ✅ Chart 2 saved: 02_revenue_leakage_analysis.png")

    # ── CHART 3: LATE DELIVERY ANALYSIS ──────────────────────
    print("\n📊 Chart 3: Late Delivery Analysis...")

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    fig.suptitle('Late Delivery Root Cause Analysis\nMaster Data Governance | Haider Ali',
                fontsize=14, fontweight='bold', color=DARK, y=1.02)

    # By Market
    market_late = df.groupby('Market').agg(
        Total=('Order Id', 'count'),
        Late=('Late_delivery_risk', 'sum')
    )
    market_late['Late Rate'] = market_late['Late'] / market_late['Total'] * 100
    market_late = market_late.sort_values('Late Rate', ascending=True)
    colors_market = [RED if x > 60 else YELLOW if x > 40 else GREEN 
                    for x in market_late['Late Rate']]
    bars = axes[0].barh(market_late.index, market_late['Late Rate'], 
                        color=colors_market, height=0.5)
    axes[0].set_xlabel('Late Delivery Rate %', color=GRAY)
    axes[0].set_title('Late Delivery Rate\nby Market', fontweight='bold', color=DARK)
    axes[0].axvline(x=15, color=GREEN, linestyle='--', alpha=0.7, label='Target (<15%)')
    axes[0].legend(fontsize=8)
    for bar in bars:
        axes[0].text(bar.get_width() + 0.5, bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():.1f}%', va='center', fontsize=9)

    # By Shipping Mode
    mode_perf = df.groupby('Shipping Mode').agg(
        Avg_Delay=('Shipping Delay Days', 'mean'),
        Late_Rate=('Late_delivery_risk', 'mean')
    )
    mode_perf['Late Rate %'] = mode_perf['Late_Rate'] * 100
    colors_mode = [RED if x > 50 else YELLOW if x > 30 else GREEN 
                  for x in mode_perf['Late Rate %']]
    bars2 = axes[1].bar(mode_perf.index, mode_perf['Late Rate %'], 
                        color=colors_mode, width=0.5)
    axes[1].set_ylabel('Late Rate %', color=GRAY)
    axes[1].set_title('Late Rate by\nShipping Mode', fontweight='bold', color=DARK)
    axes[1].set_ylim(0, 100)
    axes[1].tick_params(axis='x', rotation=15, labelsize=8)
    for bar in bars2:
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{bar.get_height():.0f}%', ha='center', fontsize=9, fontweight='bold')

    # Delivery Performance pie
    delivery_counts = df['Delivery Performance'].value_counts()
    colors_del = [GREEN if 'On Time' in x else RED for x in delivery_counts.index]
    wedges, texts, autotexts = axes[2].pie(
        delivery_counts.values,
        labels=delivery_counts.index,
        autopct='%1.1f%%',
        colors=colors_del,
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5)
    )
    for autotext in autotexts:
        autotext.set_fontsize(10)
        autotext.set_fontweight('bold')
    axes[2].set_title('Overall Delivery\nPerformance', fontweight='bold', color=DARK)

    plt.tight_layout()
    plt.savefig('../output/charts/03_late_delivery_analysis.png',
                bbox_inches='tight', dpi=150, facecolor=WHITE)
    plt.close()
    print("   ✅ Chart 3 saved: 03_late_delivery_analysis.png")

    # ── CHART 4: MASTER DATA COMPLETENESS ────────────────────
    print("\n📊 Chart 4: Master Data Completeness by Domain...")

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Master Data Completeness by Domain\nMaster Data Governance | Haider Ali',
                fontsize=14, fontweight='bold', color=DARK, y=1.02)

    # Completeness Scores by Domain
    domains = ['Customer\nMaster', 'Order\nMaster', 'Product\nMaster', 'Vendor/\nShipping']
    scores = [99.9, 13.8, 0.0, 100.0]
    colors_domain = [GREEN if s >= 99 else YELLOW if s >= 70 else RED for s in scores]
    bars = axes[0].bar(domains, scores, color=colors_domain, width=0.5)
    axes[0].set_ylabel('Completeness %', color=GRAY)
    axes[0].set_title('Master Data Completeness\nby Domain', fontweight='bold', color=DARK)
    axes[0].set_ylim(0, 115)
    axes[0].axhline(y=99, color=GREEN, linestyle='--', alpha=0.7, label='SLA Target (99%)')
    axes[0].legend(fontsize=9)
    for bar, score in zip(bars, scores):
        status = '✅' if score >= 99 else '⚠️' if score >= 70 else '❌'
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{status}\n{score:.1f}%', ha='center', fontsize=9, fontweight='bold',
                    color=RED if score < 70 else GRAY)

    # Customer Value Tier Distribution
    tier_counts = df['Customer Value Tier'].value_counts()
    colors_tier = [BLUE, '#3B82F6', '#60A5FA', '#93C5FD']
    wedges, texts, autotexts = axes[1].pie(
        tier_counts.values,
        labels=tier_counts.index,
        autopct='%1.1f%%',
        colors=colors_tier,
        startangle=90,
        pctdistance=0.75,
        wedgeprops=dict(width=0.5)
    )
    for autotext in autotexts:
        autotext.set_fontsize(9)
    axes[1].set_title('Customer Value Tier\nDistribution (Enriched)', 
                     fontweight='bold', color=DARK)

    plt.tight_layout()
    plt.savefig('../output/charts/04_master_data_completeness.png',
                bbox_inches='tight', dpi=150, facecolor=WHITE)
    plt.close()
    print("   ✅ Chart 4 saved: 04_master_data_completeness.png")

    # ── CHART 5: SLA COMPLIANCE REPORT ───────────────────────
    print("\n📊 Chart 5: SLA Compliance Report...")

    fig, ax = plt.subplots(figsize=(14, 7))
    fig.suptitle('Data Quality SLA Compliance Report\nMaster Data Governance | Haider Ali',
                fontsize=14, fontweight='bold', color=DARK, y=1.02)

    kpis = [
        'Customer ID\nCompleteness',
        'Product Price\nValidity',
        'Customer Segment\nValidity',
        'Shipping Mode\nValidity',
        'Order Zipcode\nCompleteness',
        'Product Description\nCompleteness',
        'On-Time Delivery\nRate',
        'Profitable Orders\nRate'
    ]
    actual = [100.0, 100.0, 100.0, 100.0, 13.8, 0.0, 45.2, 80.6]
    target = [99.0, 99.0, 99.0, 99.0, 99.0, 99.0, 85.0, 90.0]

    x = np.arange(len(kpis))
    width = 0.35
    colors_actual = [GREEN if a >= t else RED for a, t in zip(actual, target)]
    
    bars1 = ax.bar(x - width/2, actual, width, label='Actual', color=colors_actual, alpha=0.85)
    bars2 = ax.bar(x + width/2, target, width, label='SLA Target', 
                   color=BLUE, alpha=0.3, edgecolor=BLUE, linewidth=1.5)

    ax.set_ylabel('Score %', color=GRAY, fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(kpis, fontsize=8)
    ax.set_ylim(0, 115)
    ax.legend(fontsize=10)
    ax.set_title('', fontsize=12)

    for bar, val, tgt in zip(bars1, actual, target):
        status = '✅' if val >= tgt else '❌'
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
               f'{status}\n{val:.0f}%', ha='center', fontsize=7.5, fontweight='bold',
               color=RED if val < tgt else GREEN)

    met = sum(1 for a, t in zip(actual, target) if a >= t)
    ax.text(0.02, 0.95, f'SLA Compliance: {met}/{len(kpis)} KPIs Met',
           transform=ax.transAxes, fontsize=11, fontweight='bold',
           color=GREEN if met >= 6 else RED,
           bbox=dict(boxstyle='round', facecolor=LIGHT, alpha=0.8))

    plt.tight_layout()
    plt.savefig('../output/charts/05_sla_compliance_report.png',
                bbox_inches='tight', dpi=150, facecolor=WHITE)
    plt.close()
    print("   ✅ Chart 5 saved: 05_sla_compliance_report.png")

    print(f"\n✅ All 5 charts generated successfully!")
    print(f"   Saved to: output/charts/")

if __name__ == "__main__":
    df = pd.read_csv('../output/supply_chain_enriched.csv', encoding='latin1')
    create_all_charts(df)
