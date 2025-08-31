# 🎯 RFM Customer Segmentation Analysis

## 📊 Project Overview
A comprehensive customer segmentation analysis using **RFM (Recency, Frequency, Monetary)** modeling on retail transactional data. This project identifies distinct customer groups based on purchasing behavior and provides **targeted marketing strategies** for each segment.

---

## 🚀 Key Insights
- Analyzed **5,860 unique customers** from **800,000+ transactions**
- Identified **7 strategic segments** using RFM scoring
- **Top 5 customers** generated over **$1.9M in revenue**
- **615 high-value customers** identified as **"Can't Lose Them"** segment

---

## 📈 Customer Segments Discovered
| Segment             | Customers | Priority   | Description |
|---------------------|-----------|------------|-------------|
| At Risk Customers   | 1,470     | 🔴 High    | Recent but infrequent buyers needing re-engagement |
| Potential Loyalists | 1,430     | 🟡 Medium  | Moderate recency and frequency with growth potential |
| Lost Customers      | 842       | ⚫ Low     | Inactive customers requiring win-back campaigns |
| Champions           | 720       | 🟢 High    | Best customers: recent, frequent, high spenders |
| Can't Lose Them     | 615       | 🔴 Critical| High-value customers at risk of churn |
| Loyal Customers     | 506       | 🟡 Medium  | Frequent buyers but not necessarily recent |
| New Customers       | 123       | 🟡 Medium  | Recently acquired customers |

---
# 📊 Visualizations, Marketing Strategies & Business Impact

## 📊 Visualizations Created
- **Customer Segment Distribution** → Horizontal bar chart of segment sizes  
- **Average RFM Scores** → Bar chart comparing R, F, M metrics  
- **RFM Heatmap** → Spending patterns across Recency/Frequency scores  
- **Distribution Charts** → Histograms for R, F, M values  
- **Top Customers** → Visualization of highest spending customers  

---

## 💡 Marketing Strategies
- **Champions** → VIP treatment, exclusive offers, premium loyalty rewards  
- **At Risk Customers** → Win-back campaigns with 15–20% discounts  
- **Can't Lose Them** → Personal outreach & high-value retention offers  
- **New Customers** → Welcome series and onboarding emails  

---

## 📋 Dependencies
- Python 3.7+  
- pandas  
- numpy  
- matplotlib  
- seaborn  

---

## 🎯 Business Impact
This analysis enables **data-driven marketing decisions** by:
- Identifying high-value customers for retention programs  
- Pinpointing at-risk customers for win-back campaigns  
- Optimizing marketing spend through targeted segmentation  
- Providing actionable insights for **customer lifecycle management**  

## 🛠️ Technical Implementation
```python
# Core RFM Calculation
rfm = df_clean.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice': 'nunique',                                    # Frequency  
    'TotalSales': 'sum'                                      # Monetary


