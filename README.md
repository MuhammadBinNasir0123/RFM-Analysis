# 🎯 RFM Customer Segmentation Analysis  

## 📊 Project Overview  
This project applies **RFM (Recency, Frequency, Monetary)** modeling on retail transactional data to segment customers based on their purchasing behavior. The goal is to uncover distinct customer groups and recommend **targeted marketing strategies** for retention and growth.  

---

## 🚀 Key Insights  
- Analyzed **5,860 customers** from **800,000+ transactions**  
- Discovered **7 customer segments** using RFM scoring  
- **Top 5 customers** contributed **$1.9M+ revenue**  
- Identified **615 high-value customers** at risk of churn  

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

## 📊 Visualizations Created  
- **Segment Distribution** → Horizontal bar chart of customer groups  
- **Average RFM Scores** → Compare Recency, Frequency, and Monetary metrics  
- **RFM Heatmap** → Spending patterns across Recency/Frequency matrix  
- **Distribution Charts** → Histograms for R, F, M values  
- **Top Customers** → Highest revenue contributors  

---

## 💡 Marketing Strategies  
- **Champions** → VIP treatment, exclusive offers, premium loyalty rewards  
- **At Risk Customers** → Win-back campaigns with 15–20% discounts  
- **Can't Lose Them** → Personal outreach + retention packages  
- **New Customers** → Welcome series and onboarding journey  

---

## 🛠️ Tools & Dependencies  
- Python 3.7+  
- pandas | numpy  
- matplotlib | seaborn  

---

## 🎯 Business Impact  
This segmentation provides actionable insights for:  
- Retaining **high-value customers**  
- Targeting **at-risk customers** before churn  
- Optimizing **marketing spend** with precision  
- Enhancing **customer lifecycle management**  

---

## 🛠️ Technical Implementation  

```python
# RFM Calculation
rfm = df_clean.groupby('Customer ID').agg({
    'InvoiceDate': lambda x: (snapshot_date - x.max()).days,  # Recency
    'Invoice': 'nunique',                                    # Frequency
    'TotalSales': 'sum'                                      # Monetary
}).reset_index()

rfm.columns = ['CustomerID', 'Recency', 'Frequency', 'Monetary']

