# 🎯 RFM Customer Segmentation Analysis

## 📊 Project Overview
A comprehensive customer segmentation analysis using RFM (Recency, Frequency, Monetary) modeling on transactional retail data. This project identifies distinct customer groups based on purchasing behavior and provides targeted marketing strategies for each segment.

## 🚀 Key Insights
- **5,860 unique customers** analyzed from over **800,000 transactions**
- **7 strategic segments** identified using RFM scoring
- **Top 5 customers** generated over **$1.9M in revenue**
- **615 high-value customers** identified as "Can't Lose Them" segment

## 📈 Customer Segments Discovered
| Segment | Customers | Priority | Description |
|---------|-----------|----------|-------------|
| At Risk Customers | 1,470 | 🔴 High | Recent but infrequent buyers needing re-engagement |
| Potential Loyalists | 1,430 | 🟡 Medium | Moderate recency and frequency with growth potential |
| Lost Customers | 842 | ⚫ Low | Inactive customers requiring win-back campaigns |
| Champions | 720 | 🟢 High | Best customers: recent, frequent, high spenders |
| Can't Lose Them | 615 | 🔴 Critical | High-value customers at risk of churn |
| Loyal Customers | 506 | 🟡 Medium | Frequent buyers but not necessarily recent |
| New Customers | 123 | 🟡 Medium | Recently acquired customers |

## 🛠️ Technical Implementation
```python
# Core RFM Calculation
rfm = df_clean.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice': 'nunique',                                    # Frequency  
    'TotalSales': 'sum'                                      # Monetary
})
- **Language:** Python 🐍  
- **Libraries:** Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn  

---


