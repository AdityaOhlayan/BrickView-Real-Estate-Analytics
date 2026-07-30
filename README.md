# 🏢 BrickView – Real Estate Analytics Platform

**GUVI × HCL Capstone | Python · SQL · Streamlit**

---

## ⚡ Quick Start (5 minutes)

### Step 1 – Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 – Load the database
```bash
# If you have the original JSON/CSV dataset files, place them in this folder first.
# If NOT (starting from scratch), the loader auto-generates realistic sample data.
python load_db.py
```

### Step 3 – Run the app
```bash
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## 📁 Project Structure

```
brickview/
├── app.py              ← Main Streamlit application (4 pages)
├── queries.py          ← All 30 SQL queries as Python functions
├── load_db.py          ← Loads JSON/CSV data into SQLite
├── generate_data.py    ← Generates sample data if you have none
├── requirements.txt    ← pip dependencies
├── brickview.db        ← SQLite database (created after load_db.py)
│
├── listings_final_expanded.json          ← Dataset 1
├── property_attributes_final_expanded.json ← Dataset 2
├── agents_cleaned.json                   ← Dataset 3
├── sales_cleaned.csv                     ← Dataset 4
└── buyers_cleaned.json                   ← Dataset 5
```

---

## 🗄️ Database Schema

```
agents ──────────────── listings ──── property_attributes
                            │
                          sales
                            │
                          buyers
```

---

## 📊 App Pages

| Page | Description |
|---|---|
| 🏠 Dashboard | KPI cards, charts, monthly trends |
| 📊 SQL Queries | All 30 queries in dropdown – shows SQL + table + chart |
| 🗃️ CRUD Operations | View / Add / Update / Delete records in any table |
| 🔍 Filters & Map | Interactive map + filters by city, type, price, agent, date |

---

## 📝 30 SQL Queries Covered

**Property & Pricing (Q1–Q10)**
- Avg price by city, price per sqft, furnishing vs price, metro distance, rented vs not, bedrooms/bathrooms, parking/power, year built, top cities, price buckets

**Sales & Market (Q11–Q18)**
- Avg days on market, fastest types, % above list, sale-to-list ratio, slow listings (90+ days), metro vs time, monthly trend, unsold properties

**Agent Performance (Q19–Q25)**
- Top by sales count, top by revenue, fastest closers, experience vs deals, rating vs speed, commission earned, active listings

**Buyer & Financing (Q26–Q30)**
- Investor vs end user, loan uptake by city, avg loan by buyer type, payment mode, loan vs close time

---

## 🛠️ Tech Stack
- **Python 3.10+**
- **SQLite** – lightweight embedded database
- **Streamlit** – web dashboard framework
- **Plotly** – interactive charts & maps
- **Pandas** – data manipulation
