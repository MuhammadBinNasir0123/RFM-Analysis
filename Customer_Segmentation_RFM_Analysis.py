# =============================================================================
# RFM Customer Segmentation Analysis
#
# This analysis segments customers based on their purchasing behavior:
# - Recency (R): How recently did the customer purchase?
# - Frequency (F): How often do they purchase?
# - Monetary (M): How much do they spend?
#
# We'll use these metrics to group customers and suggest targeted marketing strategies.
# =============================================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set a clean style for our visualizations
sns.set_style("whitegrid")
print("✅ All libraries imported successfully!")

# =============================================================================
# STEP 1: LOAD AND EXPLORE THE DATA
# =============================================================================
print("\n📊 STEP 1: Loading and exploring the dataset...")

# Load the retail dataset
file_path = 'Online_Retail.csv'  # Make sure this file is in your working directory

try:
    df = pd.read_csv(file_path, encoding='iso-8859-1')
    print("✅ Dataset loaded successfully!")
    print(f"   - The dataset contains {df.shape[0]} rows and {df.shape[1]} columns")
except FileNotFoundError:
    print("❌ File not found! Please check the file path.")
    print("   Current file path:", file_path)
    exit()

# Let's take a quick look at the data structure
print("\nFirst glimpse of the data:")
print(df.head())

# =============================================================================
# STEP 2: CLEAN AND PREPARE THE DATA
# =============================================================================
print("\n\n🧹 STEP 2: Cleaning and preparing the data...")
print("   - Removing records without Customer ID")
print("   - Filtering out returns and cancellations")
print("   - Calculating total sales value")

# Create a working copy of the data
df_clean = df.copy()

# Remove rows where Customer ID is missing (we can't analyze anonymous customers)
initial_count = df_clean.shape[0]
df_clean = df_clean.dropna(subset=['Customer ID'])
print(f"   - Removed {initial_count - df_clean.shape[0]} records without Customer ID")

# Remove returns (negative quantities) and zero/negative prices
df_clean = df_clean[df_clean['Quantity'] > 0]
df_clean = df_clean[df_clean['Price'] > 0]
print(f"   - Removed returns and invalid transactions, {df_clean.shape[0]} records remain")

# Calculate the total sales for each transaction line
df_clean['TotalSales'] = df_clean['Quantity'] * df_clean['Price']

# Convert invoice date to proper datetime format
print("   - Converting invoice dates to datetime format...")
df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'], format='%d/%m/%Y %H:%M', errors='coerce')

# Check if any dates couldn't be converted
failed_dates = df_clean['InvoiceDate'].isnull().sum()
if failed_dates > 0:
    print(f"   ⚠️  {failed_dates} dates could not be converted and were removed")
    df_clean = df_clean.dropna(subset=['InvoiceDate'])

print("✅ Data cleaning completed!")
print(f"   - Final dataset size: {df_clean.shape[0]} records")
print(f"   - Date range: {df_clean['InvoiceDate'].min().date()} to {df_clean['InvoiceDate'].max().date()}")

# =============================================================================
# STEP 3: CALCULATE RFM METRICS
# =============================================================================
print("\n\n📈 STEP 3: Calculating RFM metrics for each customer...")
print("   - Recency: Days since last purchase")
print("   - Frequency: Number of purchases")
print("   - Monetary: Total amount spent")

# Set analysis date (day after last purchase)
snapshot_date = df_clean['InvoiceDate'].max() + pd.Timedelta(days=1)
print(f"   - Analysis snapshot date: {snapshot_date.date()}")

# Calculate RFM metrics for each customer
rfm = df_clean.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice': 'nunique',  # Frequency
    'TotalSales': 'sum'  # Monetary
})

# Rename columns for clarity
rfm.columns = ['Recency', 'Frequency', 'Monetary']
print(f"✅ RFM metrics calculated for {rfm.shape[0]} customers!")

# Show basic statistics
print("\nRFM Statistics Overview:")
print(rfm.describe())

# =============================================================================
# STEP 4: ASSIGN RFM SCORES
# =============================================================================
print("\n\n🎯 STEP 4: Assigning RFM scores (1-4 scale)...")
print("   - 4 = Best, 1 = Worst")
print("   - Lower Recency is better (recent customers score higher)")
print("   - Higher Frequency and Monetary values score higher")

# Score Recency (lower values are better)
rfm['R_Score'] = pd.qcut(rfm['Recency'], q=4, labels=[4, 3, 2, 1])

# Score Frequency and Monetary (higher values are better)
freq_bins = [rfm['Frequency'].min() - 1, 1, 2, 3, rfm['Frequency'].max()]
monetary_bins = [rfm['Monetary'].min() - 1,
                 rfm['Monetary'].quantile(0.25),
                 rfm['Monetary'].quantile(0.5),
                 rfm['Monetary'].quantile(0.75),
                 rfm['Monetary'].max()]

rfm['F_Score'] = pd.cut(rfm['Frequency'], bins=freq_bins, labels=[1, 2, 3, 4], include_lowest=True)
rfm['M_Score'] = pd.cut(rfm['Monetary'], bins=monetary_bins, labels=[1, 2, 3, 4], include_lowest=True)

# Handle any missing scores
for column in ['R_Score', 'F_Score', 'M_Score']:
    if rfm[column].isnull().any():
        null_count = rfm[column].isnull().sum()
        median_val = rfm[column].median()
        rfm[column].fillna(median_val, inplace=True)

# Create combined RFM segment string
rfm['RFM_Segment'] = rfm['R_Score'].astype(int).astype(str) + rfm['F_Score'].astype(int).astype(str) + rfm[
    'M_Score'].astype(int).astype(str)

print("✅ RFM scores assigned successfully!")
print("\nScore Distributions:")
print("Recency Scores:", rfm['R_Score'].value_counts().sort_index().to_dict())
print("Frequency Scores:", rfm['F_Score'].value_counts().sort_index().to_dict())
print("Monetary Scores:", rfm['M_Score'].value_counts().sort_index().to_dict())

# =============================================================================
# STEP 5: CREATE CUSTOMER SEGMENTS
# =============================================================================
print("\n\n👥 STEP 5: Grouping customers into strategic segments...")


def get_segment(rfm_row):
    """
    Maps RFM scores to meaningful customer segments
    """
    r_score = rfm_row['R_Score']
    f_score = rfm_row['F_Score']
    m_score = rfm_row['M_Score']

    # Strategic segmentation logic
    if r_score == 4 and f_score == 4 and m_score == 4:
        return 'Champions'  # Best customers - recent, frequent, high spenders
    elif r_score == 4 and f_score >= 3:
        return 'Loyal Customers'  # Recent and frequent buyers
    elif r_score == 4 and f_score == 1:
        return 'New Customers'  # Recent but infrequent buyers
    elif r_score == 3:
        return 'Potential Loyalists'  # Moderately recent customers
    elif r_score == 2:
        return 'At Risk Customers'  # Becoming less recent
    elif r_score == 1 and f_score >= 2:
        return 'Cant Lose Them'  # Inactive but previously valuable
    elif r_score == 1:
        return 'Lost Customers'  # Completely inactive
    else:
        return 'Others'  # Everything else


# Apply segmentation
rfm['Customer_Group'] = rfm.apply(get_segment, axis=1)
segment_counts = rfm['Customer_Group'].value_counts()

print("✅ Customer segments created!")
print("\nCustomer Distribution by Segment:")
for segment, count in segment_counts.items():
    print(f"   - {segment}: {count} customers ({(count / len(rfm) * 100):.1f}%)")

# =============================================================================
# STEP 6: MARKETING RECOMMENDATIONS
# =============================================================================
print("\n\n💡 STEP 6: Marketing suggestions for each customer group...")

suggestions = {
    'Champions': "VIP treatment: Exclusive offers, early access to new products, premium loyalty rewards",
    'Loyal Customers': "Loyalty programs: Tiered rewards, special discounts, personalized recommendations",
    'New Customers': "Welcome series: Onboarding emails, first-purchase follow-up, small discount on next order",
    'Potential Loyalists': "Engagement campaigns: Product recommendations, educational content, moderate discounts",
    'At Risk Customers': "Win-back offers: 'We miss you' campaigns, 15-20% discounts, highlight new products",
    'Cant Lose Them': "Aggressive retention: High-value offers, personal outreach, understand their needs",
    'Lost Customers': "Re-engagement surveys: Understand why they left, strong comeback incentives",
    'Others': "General marketing: Newsletter campaigns, broad promotions, brand awareness content"
}

print("=" * 60)
for segment, count in segment_counts.items():
    print(f"\n📌 {segment} ({count} customers):")
    print(f"   {suggestions.get(segment, 'General marketing approach')}")
print("=" * 60)

# =============================================================================
# STEP 7: CREATE VISUALIZATIONS - PAGE 1
# =============================================================================
print("\n\n📊 STEP 7: Creating visualization dashboards...")
print("   - Page 1: Customer overview and key metrics")

# Convert scores to numeric for plotting
rfm['R_Score_Num'] = rfm['R_Score'].astype(int)
rfm['F_Score_Num'] = rfm['F_Score'].astype(int)
rfm['M_Score_Num'] = rfm['M_Score'].astype(int)

# Create overview dashboard
fig1, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Customer Segment Distribution
ax1 = axes[0, 0]
segment_counts_sorted = segment_counts.sort_values(ascending=True)
colors = plt.cm.Set3(np.linspace(0, 1, len(segment_counts_sorted)))
bars = ax1.barh(range(len(segment_counts_sorted)), segment_counts_sorted.values, color=colors, alpha=0.85)
ax1.set_title('CUSTOMER SEGMENT DISTRIBUTION', fontweight='bold', pad=10)
ax1.set_yticks(range(len(segment_counts_sorted)))
ax1.set_yticklabels(segment_counts_sorted.index, fontsize=9)
ax1.set_xlabel('Number of Customers', fontsize=10)
ax1.grid(True, alpha=0.3, axis='x')

# Add value labels to bars
for i, (bar, count) in enumerate(zip(bars, segment_counts_sorted.values)):
    ax1.text(bar.get_width() + max(segment_counts_sorted.values) * 0.01,
             bar.get_y() + bar.get_height() / 2, f'{count}',
             ha='left', va='center', fontweight='bold', fontsize=9)

# 2. Average RFM Scores
ax2 = axes[0, 1]
score_means = [rfm['R_Score_Num'].mean(), rfm['F_Score_Num'].mean(), rfm['M_Score_Num'].mean()]
score_labels = ['Recency', 'Frequency', 'Monetary']
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
bars = ax2.bar(score_labels, score_means, color=colors, alpha=0.8)
ax2.set_title('AVERAGE RFM SCORES (1-4 Scale)', fontweight='bold', pad=10)
ax2.set_ylabel('Average Score', fontsize=10)
ax2.set_ylim(0, 4.5)
ax2.grid(True, alpha=0.3, axis='y')

for bar, value in zip(bars, score_means):
    ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
             f'{value:.2f}', ha='center', va='bottom', fontweight='bold', fontsize=10)

# 3. Key Metrics Summary
ax3 = axes[1, 0]
ax3.axis('off')
summary_text = (
    f"KEY METRICS SUMMARY\n\n"
    f"Total Customers: {len(rfm):,}\n"
    f"Most Common Segment: {segment_counts.idxmax()}\n"
    f"Largest Segment Size: {segment_counts.max():,}\n"
    f"Top Spending Segment: {rfm.groupby('Customer_Group')['Monetary'].mean().idxmax()}\n"
    f"Avg Recency: {rfm['Recency'].mean():.0f} days\n"
    f"Avg Frequency: {rfm['Frequency'].mean():.1f} purchases\n"
    f"Avg Spending: ${rfm['Monetary'].mean():.0f}\n"
    f"Total Revenue: ${rfm['Monetary'].sum():,.0f}"
)
ax3.text(0.5, 0.5, summary_text, transform=ax3.transAxes, fontsize=11,
         ha='center', va='center', fontweight='bold',
         bbox=dict(boxstyle="round,pad=1", facecolor="lightblue", alpha=0.8))

# 4. Top Customers by Spending
ax4 = axes[1, 1]
top_customers = rfm.nlargest(5, 'Monetary')
bars = ax4.barh(range(len(top_customers)), top_customers['Monetary'], color='orange', alpha=0.7)
ax4.set_title('TOP 5 CUSTOMERS BY SPENDING', fontweight='bold', pad=10)
ax4.set_xlabel('Total Spending ($)', fontsize=10)
ax4.set_yticks(range(len(top_customers)))
ax4.set_yticklabels([f'Customer {int(idx)}' for idx in top_customers.index], fontsize=9)
ax4.grid(True, alpha=0.3, axis='x')

for i, (bar, value) in enumerate(zip(bars, top_customers['Monetary'])):
    ax4.text(bar.get_width() + max(top_customers['Monetary']) * 0.01,
             bar.get_y() + bar.get_height() / 2, f'${value:,.0f}',
             ha='left', va='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.subplots_adjust(top=0.95, hspace=0.4, wspace=0.3)
plt.savefig('rfm_page1_overview.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Page 1 saved as 'rfm_page1_overview.png'")
plt.show()

# Clean up temporary columns
rfm = rfm.drop(['R_Score_Num', 'F_Score_Num', 'M_Score_Num'], axis=1)

# =============================================================================
# STEP 8: CREATE VISUALIZATIONS - PAGE 2
# =============================================================================
print("\n\n📊 STEP 8: Creating second page of visualizations...")
print("   - Page 2: RFM distributions and heatmap")

# Convert scores to numeric again for the second page
rfm['R_Score_Num'] = rfm['R_Score'].astype(int)
rfm['F_Score_Num'] = rfm['F_Score'].astype(int)
rfm['M_Score_Num'] = rfm['M_Score'].astype(int)

# Create distributions dashboard
fig2, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. RFM Heatmap (Top Left)
ax1 = axes[0, 0]
heatmap_data = rfm.groupby(['R_Score_Num', 'F_Score_Num'])['Monetary'].mean().unstack().fillna(0)
im = ax1.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
ax1.set_title('RFM HEATMAP: AVERAGE SPENDING', fontweight='bold', pad=10)
ax1.set_xlabel('Frequency Score', fontsize=10)
ax1.set_ylabel('Recency Score', fontsize=10)
ax1.set_xticks(range(4))
ax1.set_yticks(range(4))
ax1.set_xticklabels([1, 2, 3, 4], fontsize=9)
ax1.set_yticklabels([4, 3, 2, 1], fontsize=9)

# Add value annotations to heatmap
for i in range(4):
    for j in range(4):
        if j < heatmap_data.shape[1] and i < heatmap_data.shape[0]:
            value = heatmap_data.iloc[i, j]
            ax1.text(j, i, f'${value:.0f}', ha='center', va='center',
                     color='black', fontweight='bold', fontsize=8)

plt.colorbar(im, ax=ax1, shrink=0.8, label='Average Spending ($)')

# 2. Recency Distribution (Top Right)
ax2 = axes[0, 1]
recency_data = rfm[rfm['Recency'] <= 365]  # Focus on last year for better visualization
sns.histplot(data=recency_data, x='Recency', bins=25, ax=ax2, color='skyblue', alpha=0.7)
ax2.set_title('RECENCY DISTRIBUTION', fontweight='bold', pad=10)
ax2.set_xlabel('Days Since Last Purchase', fontsize=10)
ax2.set_ylabel('Number of Customers', fontsize=10)
ax2.grid(True, alpha=0.3)

# 3. Frequency Distribution (Bottom Left)
ax3 = axes[1, 0]
frequency_data = rfm[rfm['Frequency'] <= 25]  # Focus on typical range
sns.histplot(data=frequency_data, x='Frequency', bins=15, ax=ax3, color='lightgreen', alpha=0.7)
ax3.set_title('FREQUENCY DISTRIBUTION', fontweight='bold', pad=10)
ax3.set_xlabel('Number of Purchases', fontsize=10)
ax3.set_ylabel('Number of Customers', fontsize=10)
ax3.grid(True, alpha=0.3)

# 4. Monetary Distribution (Bottom Right)
ax4 = axes[1, 1]
monetary_data = rfm[rfm['Monetary'] <= 5000]  # Focus on typical range
sns.histplot(data=monetary_data, x='Monetary', bins=20, ax=ax4, color='salmon', alpha=0.7)
ax4.set_title('SPENDING DISTRIBUTION', fontweight='bold', pad=10)
ax4.set_xlabel('Spending per Customer ($)', fontsize=10)
ax4.set_ylabel('Number of Customers', fontsize=10)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.subplots_adjust(top=0.95, hspace=0.4, wspace=0.3)
plt.savefig('rfm_page2_distributions.png', dpi=300, bbox_inches='tight', facecolor='white')
print("✅ Page 2 saved as 'rfm_page2_distributions.png'")
plt.show()

# Clean up temporary columns
rfm = rfm.drop(['R_Score_Num', 'F_Score_Num', 'M_Score_Num'], axis=1)

# =============================================================================
# STEP 9: SAVE RESULTS
# =============================================================================
print("\n\n💾 STEP 9: Saving analysis results...")

# Save the RFM results to a CSV file
rfm.to_csv('rfm_analysis_results.csv')
print("✅ RFM results saved to 'rfm_analysis_results.csv'")

print("\n🎉 ANALYSIS COMPLETE!")
print("📁 Outputs created:")
print("   - rfm_page1_overview.png (Customer overview dashboard)")
print("   - rfm_page2_distributions.png (RFM distributions and heatmap)")
print("   - rfm_analysis_results.csv (Complete RFM scores and segments)")
print("\nNext step: Use these insights to create targeted marketing campaigns!")