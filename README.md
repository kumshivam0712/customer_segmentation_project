<div align="center">
  
# 🛍️ Customer Segmentation Project
  
[![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)](https://www.python.org)
[![Pandas](https://img.shields.io/badge/Pandas-2.0-green?style=for-the-badge&logo=pandas)](https://pandas.pydata.org/)
[![Matplotlib](https://img.shields.io/badge/Matplotlib-3.7-orange?style=for-the-badge&logo=python)](https://matplotlib.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](https://opensource.org/licenses/MIT)

### 🎯 Turning Raw Data into Business Intelligence
*RFM Analysis on 100,000+ E-Commerce Orders*

<img src="https://user-images.githubusercontent.com/73097560/115834477-dbab4500-a447-11eb-908a-139a6edaec5c.gif">

</div>

---

## 📋 Table of Contents

- [🚀 Overview](#-overview)
- [📊 Key Findings](#-key-findings)
- [🎯 Customer Segments](#-customer-segments)
- [📈 Visualizations](#-visualizations)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [💡 Business Recommendations](#-business-recommendations)
- [⚙️ How to Run](#️-how-to-run)
- [📊 Key Metrics](#-key-metrics-to-track)
- [📝 License](#-license)

---

## 🚀 Overview

This project performs **Customer Segmentation** on **100,000+ e-commerce orders** using **RFM (Recency, Frequency, Monetary)** analysis.

Instead of treating all customers the same, it automatically groups them into meaningful segments so businesses can:

| 🎯 Target Marketing | 💰 Increase Revenue | ⚠️ Prevent Churn | 💝 Personalize Experience |
|:---:|:---:|:---:|:---:|
| Send right offers | Focus on high-value | Catch at-risk early | Treat customers uniquely |

---

## 📊 Key Findings

| Segment | Customers | % of Total | Revenue | % of Revenue |
|----------|----------:|-----------:|--------:|-------------:|
| 🏆 Champions | 6,429 | 6.9% | R$1.85M | 13.4% |
| 💝 Loyal | 9,176 | 9.8% | R$2.62M | 19.0% |
| 🌟 Potential | 16,380 | 17.5% | R$3.18M | 23.0% |
| 🆕 New | 6,067 | 6.5% | R$0.25M | 1.8% |
| ⚠️ At Risk | 20,959 | 22.5% | R$2.78M | 20.1% |
| 🔴 High Value At Risk | 2,817 | 3.0% | R$0.83M | 6.0% |
| 💤 Hibernating | 7,458 | 8.0% | R$0.19M | 1.4% |
| 📦 Others | 24,072 | 25.8% | R$2.10M | 15.2% |

### 💡 Power Insight

**Top 3 segments (Champions + Loyal + Potential) = 34.2% customers → 55.4% revenue**

**At-risk customers = 33.5% customers → 27.5% revenue at stake**

---

## 🎯 Customer Segments

| Segment | Description | Action |
|----------|-------------|--------|
| 🏆 Champions | Buy recently, buy often, spend most | VIP perks |
| 💝 Loyal | Regular buyers, good spending | Loyalty program |
| 🌟 Potential | Recent buyers with promise | Nurture |
| 🆕 New | First-time buyers | Welcome series |
| ⚠️ At Risk | Stopped purchasing | Reactivation |
| 🔴 High Value At Risk | Big spenders who stopped | Urgent win-back |
| 💤 Hibernating | Long inactive | Final campaign |
| 📦 Others | Mixed behavior | Monitor |

---

## 📈 Visualizations

| | |
|:---:|:---:|
| 📊 Segment Distribution | 💰 Revenue by Segment |
| ![](figures/segment_distribution_pie.png) | ![](figures/revenue_by_segment.png) |
| 💵 Average Spend | 🔥 RFM Heatmap |
| ![](figures/avg_spend_by_segment.png) | ![](figures/rfm_heatmap.png) |
| 🗺️ Top States | ⏰ Recency Distribution |
| ![](figures/top_states.png) | ![](figures/recency_distribution.png) |

---

## 🛠️ Tech Stack

- **Python 3.11**
- **Pandas**
- **NumPy**
- **Matplotlib**
- **Seaborn**
- **RFM Analysis Methodology**

---

## 📁 Project Structure

```bash
📦 customer_segmentation_project
├── 📂 python/
│   ├── 01_data_exploration.py
│   ├── 02_data_preparation.py
│   ├── 03_customer_metrics.py
│   ├── 04_rfm_segmentation.py
│   ├── 05_visualizations.py
│   └── 06_final_report.py
│
├── 📂 figures/
│   ├── segment_distribution_pie.png
│   ├── revenue_by_segment.png
│   ├── avg_spend_by_segment.png
│   ├── rfm_heatmap.png
│   ├── top_states.png
│   ├── recency_distribution.png
│   ├── state_composition.png
│   └── value_distribution.png
│
└── 📂 reports/
    ├── customer_segmentation_report.html
    ├── segment_summary.csv
    └── executive_summary.txt
💡 Business Recommendations
🏆 Champions
VIP loyalty program

Early access to products

Personalized thank-you notes

Referral bonuses

📈 Expected: +20% spending

⚠️ At-Risk Customers
"We miss you" campaign

25–30% reactivation discount

Feedback survey

Personalized product showcase

📈 Expected: Recover 25% revenue

🆕 New Customers
3-email welcome series

15% off second purchase

Product education

Easy reorder

📈 Expected: 30% higher repeat rate

💝 Loyal Customers
Points-based rewards

Cross-selling

Birthday discounts

Early sale access

📈 Expected: 15% more frequent orders

⚙️ How to Run
1️⃣ Clone Repository
git clone https://github.com/kumshivam0712/customer_segmentation_project.git
cd customer_segmentation_project
2️⃣ Install Dependencies
pip install pandas numpy matplotlib seaborn
3️⃣ Download Dataset
Download dataset from Kaggle and place CSV files inside data/ folder.

4️⃣ Run Scripts
cd python
python 01_data_exploration.py
python 02_data_preparation.py
python 03_customer_metrics.py
python 04_rfm_segmentation.py
python 05_visualizations.py
python 06_final_report.py
5️⃣ View Results
📊 Charts → figures/

📑 Report → reports/customer_segmentation_report.html

📋 Summary → reports/executive_summary.txt

📊 Key Metrics to Track
Metric	Current	Target
🔄 Repeat Customer Rate	30.4%	40%
🏆 Champions Revenue Share	13.4%	20%
📈 At-Risk Recovery Rate	0%	25%
💰 Customer Lifetime Value	R$160	R$200
📝 License
This project is licensed under the MIT License.

<div align="center">
⭐ If you found this project useful, please star it!
Happy Analyzing! 🚀

</div> ```
