"""
BrickView - All 30 SQL Queries
Each function returns (sql_string, dataframe)
"""

import sqlite3
import pandas as pd

DB_PATH = "brickview.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def run(sql, params=()):
    conn = get_conn()
    df = pd.read_sql_query(sql, conn, params=params)
    conn.close()
    return df

# ════════════════════════════════════════════════════════════
#  PROPERTY & PRICING ANALYSIS  (Q1–Q10)
# ════════════════════════════════════════════════════════════

Q1_SQL = """
SELECT City,
       ROUND(AVG(Price), 0)       AS Avg_Price,
       COUNT(*)                   AS Total_Listings
FROM   listings
GROUP  BY City
ORDER  BY Avg_Price DESC;
"""
def q1_avg_price_by_city():
    return Q1_SQL, run(Q1_SQL)

Q2_SQL = """
SELECT l.Property_Type,
       ROUND(AVG(l.Price / l.Area_sqft), 2) AS Avg_Price_Per_Sqft
FROM   listings l
WHERE  l.Area_sqft > 0
GROUP  BY l.Property_Type
ORDER  BY Avg_Price_Per_Sqft DESC;
"""
def q2_price_per_sqft():
    return Q2_SQL, run(Q2_SQL)

Q3_SQL = """
SELECT pa.Furnishing_Status,
       ROUND(AVG(l.Price), 0) AS Avg_Price,
       COUNT(*)               AS Count
FROM   listings l
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP  BY pa.Furnishing_Status
ORDER  BY Avg_Price DESC;
"""
def q3_furnishing_vs_price():
    return Q3_SQL, run(Q3_SQL)

Q4_SQL = """
SELECT CASE
         WHEN pa.Metro_Distance_Km < 2  THEN '< 2 km'
         WHEN pa.Metro_Distance_Km < 5  THEN '2–5 km'
         WHEN pa.Metro_Distance_Km < 10 THEN '5–10 km'
         ELSE '10+ km'
       END                        AS Metro_Zone,
       ROUND(AVG(l.Price), 0)    AS Avg_Price,
       COUNT(*)                  AS Count
FROM   listings l
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP  BY Metro_Zone
ORDER  BY Avg_Price DESC;
"""
def q4_metro_distance_price():
    return Q4_SQL, run(Q4_SQL)

Q5_SQL = """
SELECT CASE pa.Is_Rented WHEN 1 THEN 'Rented' ELSE 'Not Rented' END AS Status,
       ROUND(AVG(l.Price), 0) AS Avg_Price,
       COUNT(*)               AS Count
FROM   listings l
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP  BY pa.Is_Rented;
"""
def q5_rented_vs_price():
    return Q5_SQL, run(Q5_SQL)

Q6_SQL = """
SELECT pa.Bedrooms, pa.Bathrooms,
       ROUND(AVG(l.Price), 0) AS Avg_Price,
       COUNT(*)               AS Count
FROM   listings l
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP  BY pa.Bedrooms, pa.Bathrooms
ORDER  BY pa.Bedrooms, pa.Bathrooms;
"""
def q6_bedrooms_bathrooms_price():
    return Q6_SQL, run(Q6_SQL)

Q7_SQL = """
SELECT CASE
         WHEN pa.Parking_Available = 1 AND pa.Power_Backup = 1 THEN 'Both'
         WHEN pa.Parking_Available = 1                          THEN 'Parking Only'
         WHEN pa.Power_Backup = 1                               THEN 'Power Only'
         ELSE 'Neither'
       END                        AS Amenity_Group,
       ROUND(AVG(l.Price), 0)    AS Avg_Price,
       COUNT(*)                  AS Count
FROM   listings l
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP  BY Amenity_Group
ORDER  BY Avg_Price DESC;
"""
def q7_parking_power_price():
    return Q7_SQL, run(Q7_SQL)

Q8_SQL = """
SELECT pa.Year_Built,
       ROUND(AVG(l.Price), 0) AS Avg_Price,
       COUNT(*)               AS Count
FROM   listings l
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
WHERE  pa.Year_Built IS NOT NULL
GROUP  BY pa.Year_Built
ORDER  BY pa.Year_Built;
"""
def q8_year_built_price():
    return Q8_SQL, run(Q8_SQL)

Q9_SQL = """
SELECT City,
       ROUND(AVG(Price), 0) AS Avg_Price
FROM   listings
GROUP  BY City
ORDER  BY Avg_Price DESC
LIMIT  5;
"""
def q9_top_cities_by_price():
    return Q9_SQL, run(Q9_SQL)

Q10_SQL = """
SELECT CASE
         WHEN Price < 3000000  THEN '< 30L'
         WHEN Price < 6000000  THEN '30L–60L'
         WHEN Price < 10000000 THEN '60L–1Cr'
         WHEN Price < 20000000 THEN '1Cr–2Cr'
         ELSE '2Cr+'
       END          AS Price_Bucket,
       COUNT(*)     AS Count
FROM   listings
GROUP  BY Price_Bucket
ORDER  BY MIN(Price);
"""
def q10_price_buckets():
    return Q10_SQL, run(Q10_SQL)

# ════════════════════════════════════════════════════════════
#  SALES & MARKET PERFORMANCE  (Q11–Q18)
# ════════════════════════════════════════════════════════════

Q11_SQL = """
SELECT l.City,
       ROUND(AVG(s.Days_On_Market), 1) AS Avg_Days_On_Market,
       COUNT(s.Sale_ID)                AS Total_Sales
FROM   sales s
JOIN   listings l ON s.Listing_ID = l.Listing_ID
GROUP  BY l.City
ORDER  BY Avg_Days_On_Market;
"""
def q11_avg_days_by_city():
    return Q11_SQL, run(Q11_SQL)

Q12_SQL = """
SELECT l.Property_Type,
       ROUND(AVG(s.Days_On_Market), 1) AS Avg_Days,
       COUNT(*)                        AS Sales
FROM   sales s
JOIN   listings l ON s.Listing_ID = l.Listing_ID
GROUP  BY l.Property_Type
ORDER  BY Avg_Days;
"""
def q12_fastest_selling_types():
    return Q12_SQL, run(Q12_SQL)

Q13_SQL = """
SELECT ROUND(
         100.0 * SUM(CASE WHEN s.Sale_Price > l.Price THEN 1 ELSE 0 END) / COUNT(*),
         2) AS Pct_Above_List_Price,
       COUNT(*) AS Total_Sales
FROM   sales s
JOIN   listings l ON s.Listing_ID = l.Listing_ID;
"""
def q13_pct_above_list():
    return Q13_SQL, run(Q13_SQL)

Q14_SQL = """
SELECT l.City,
       ROUND(AVG(s.Sale_Price * 1.0 / l.Price), 4) AS Sale_To_List_Ratio
FROM   sales s
JOIN   listings l ON s.Listing_ID = l.Listing_ID
GROUP  BY l.City
ORDER  BY Sale_To_List_Ratio DESC;
"""
def q14_sale_to_list_ratio():
    return Q14_SQL, run(Q14_SQL)

Q15_SQL = """
SELECT l.Listing_ID, l.City, l.Property_Type, l.Price,
       s.Days_On_Market
FROM   sales s
JOIN   listings l ON s.Listing_ID = l.Listing_ID
WHERE  s.Days_On_Market > 90
ORDER  BY s.Days_On_Market DESC;
"""
def q15_slow_listings():
    return Q15_SQL, run(Q15_SQL)

Q16_SQL = """
SELECT CASE
         WHEN pa.Metro_Distance_Km < 2  THEN '< 2 km'
         WHEN pa.Metro_Distance_Km < 5  THEN '2–5 km'
         WHEN pa.Metro_Distance_Km < 10 THEN '5–10 km'
         ELSE '10+ km'
       END                                    AS Metro_Zone,
       ROUND(AVG(s.Days_On_Market), 1)        AS Avg_Days
FROM   sales s
JOIN   listings l            ON s.Listing_ID = l.Listing_ID
JOIN   property_attributes pa ON l.Listing_ID = pa.Listing_ID
GROUP  BY Metro_Zone
ORDER  BY Avg_Days;
"""
def q16_metro_vs_days():
    return Q16_SQL, run(Q16_SQL)

Q17_SQL = """
SELECT STRFTIME('%Y-%m', s.Sale_Date) AS Month,
       COUNT(*)                       AS Total_Sales,
       ROUND(SUM(s.Sale_Price), 0)    AS Total_Revenue
FROM   sales s
GROUP  BY Month
ORDER  BY Month;
"""
def q17_monthly_sales_trend():
    return Q17_SQL, run(Q17_SQL)

Q18_SQL = """
SELECT l.Listing_ID, l.City, l.Property_Type, l.Price,
       l.Listed_Date, a.Name AS Agent_Name
FROM   listings l
LEFT   JOIN sales s   ON l.Listing_ID = s.Listing_ID
LEFT   JOIN agents a  ON l.Agent_ID   = a.Agent_ID
WHERE  s.Sale_ID IS NULL
ORDER  BY l.Listed_Date;
"""
def q18_unsold_properties():
    return Q18_SQL, run(Q18_SQL)

# ════════════════════════════════════════════════════════════
#  AGENT PERFORMANCE  (Q19–Q25)
# ════════════════════════════════════════════════════════════

Q19_SQL = """
SELECT a.Agent_ID, a.Name, a.City,
       COUNT(s.Sale_ID)                AS Sales_Closed,
       ROUND(AVG(s.Days_On_Market), 1) AS Avg_Days
FROM   agents a
JOIN   listings l ON a.Agent_ID  = l.Agent_ID
JOIN   sales s    ON l.Listing_ID = s.Listing_ID
GROUP  BY a.Agent_ID
ORDER  BY Sales_Closed DESC
LIMIT  10;
"""
def q19_top_agents_by_sales():
    return Q19_SQL, run(Q19_SQL)

Q20_SQL = """
SELECT a.Name,
       COUNT(s.Sale_ID)              AS Sales,
       ROUND(SUM(s.Sale_Price), 0)   AS Total_Revenue,
       ROUND(SUM(s.Sale_Price * a.Commission_Rate / 100), 0) AS Commission_Earned
FROM   agents a
JOIN   listings l ON a.Agent_ID   = l.Agent_ID
JOIN   sales s    ON l.Listing_ID = s.Listing_ID
GROUP  BY a.Agent_ID
ORDER  BY Total_Revenue DESC
LIMIT  10;
"""
def q20_top_agents_by_revenue():
    return Q20_SQL, run(Q20_SQL)

Q21_SQL = """
SELECT a.Name,
       ROUND(AVG(s.Days_On_Market), 1) AS Avg_Close_Days,
       COUNT(s.Sale_ID)                AS Sales
FROM   agents a
JOIN   listings l ON a.Agent_ID   = l.Agent_ID
JOIN   sales s    ON l.Listing_ID = s.Listing_ID
GROUP  BY a.Agent_ID
HAVING Sales >= 3
ORDER  BY Avg_Close_Days
LIMIT  10;
"""
def q21_fastest_closing_agents():
    return Q21_SQL, run(Q21_SQL)

Q22_SQL = """
SELECT a.Experience_Years,
       COUNT(s.Sale_ID)               AS Deals_Closed,
       ROUND(AVG(s.Days_On_Market),1) AS Avg_Days
FROM   agents a
JOIN   listings l ON a.Agent_ID   = l.Agent_ID
JOIN   sales s    ON l.Listing_ID = s.Listing_ID
GROUP  BY a.Experience_Years
ORDER  BY a.Experience_Years;
"""
def q22_experience_vs_deals():
    return Q22_SQL, run(Q22_SQL)

Q23_SQL = """
SELECT CASE
         WHEN a.Rating >= 4.5 THEN '4.5–5.0'
         WHEN a.Rating >= 4.0 THEN '4.0–4.4'
         WHEN a.Rating >= 3.5 THEN '3.5–3.9'
         ELSE 'Below 3.5'
       END                                    AS Rating_Band,
       ROUND(AVG(s.Days_On_Market), 1)        AS Avg_Close_Days,
       COUNT(s.Sale_ID)                       AS Sales
FROM   agents a
JOIN   listings l ON a.Agent_ID   = l.Agent_ID
JOIN   sales s    ON l.Listing_ID = s.Listing_ID
GROUP  BY Rating_Band
ORDER  BY Avg_Close_Days;
"""
def q23_rating_vs_close_speed():
    return Q23_SQL, run(Q23_SQL)

Q24_SQL = """
SELECT a.Name, a.Commission_Rate,
       ROUND(SUM(s.Sale_Price * a.Commission_Rate / 100), 0) AS Total_Commission
FROM   agents a
JOIN   listings l ON a.Agent_ID   = l.Agent_ID
JOIN   sales s    ON l.Listing_ID = s.Listing_ID
GROUP  BY a.Agent_ID
ORDER  BY Total_Commission DESC;
"""
def q24_avg_commission():
    return Q24_SQL, run(Q24_SQL)

Q25_SQL = """
SELECT a.Name,
       COUNT(l.Listing_ID)                         AS Active_Listings,
       ROUND(AVG(l.Price), 0)                      AS Avg_Price
FROM   agents a
JOIN   listings l ON a.Agent_ID = l.Agent_ID
LEFT   JOIN sales s ON l.Listing_ID = s.Listing_ID
WHERE  s.Sale_ID IS NULL
GROUP  BY a.Agent_ID
ORDER  BY Active_Listings DESC
LIMIT  10;
"""
def q25_agents_most_active():
    return Q25_SQL, run(Q25_SQL)

# ════════════════════════════════════════════════════════════
#  BUYER & FINANCING BEHAVIOR  (Q26–Q30)
# ════════════════════════════════════════════════════════════

Q26_SQL = """
SELECT Buyer_Type,
       COUNT(*)                            AS Count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM buyers), 2) AS Percentage
FROM   buyers
GROUP  BY Buyer_Type;
"""
def q26_investor_vs_enduser():
    return Q26_SQL, run(Q26_SQL)

Q27_SQL = """
SELECT l.City,
       ROUND(100.0 * SUM(b.Loan_Taken) / COUNT(*), 2) AS Loan_Uptake_Pct
FROM   buyers b
JOIN   sales s    ON b.Sale_ID    = s.Sale_ID
JOIN   listings l ON s.Listing_ID = l.Listing_ID
GROUP  BY l.City
ORDER  BY Loan_Uptake_Pct DESC;
"""
def q27_loan_uptake_by_city():
    return Q27_SQL, run(Q27_SQL)

Q28_SQL = """
SELECT Buyer_Type,
       ROUND(AVG(Loan_Amount), 0) AS Avg_Loan_Amount
FROM   buyers
WHERE  Loan_Taken = 1
GROUP  BY Buyer_Type;
"""
def q28_avg_loan_by_buyer_type():
    return Q28_SQL, run(Q28_SQL)

Q29_SQL = """
SELECT Payment_Mode,
       COUNT(*) AS Count,
       ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM buyers), 2) AS Percentage
FROM   buyers
GROUP  BY Payment_Mode
ORDER  BY Count DESC;
"""
def q29_payment_mode():
    return Q29_SQL, run(Q29_SQL)

Q30_SQL = """
SELECT CASE b.Loan_Taken WHEN 1 THEN 'Loan' ELSE 'No Loan' END AS Financing,
       ROUND(AVG(s.Days_On_Market), 1) AS Avg_Days_To_Close,
       COUNT(*)                        AS Count
FROM   buyers b
JOIN   sales s ON b.Sale_ID = s.Sale_ID
GROUP  BY b.Loan_Taken;
"""
def q30_loan_vs_close_time():
    return Q30_SQL, run(Q30_SQL)

# ────────────────────────────────────────────────────────────
# Registry used by the SQL Queries page in the Streamlit app
# ────────────────────────────────────────────────────────────
ALL_QUERIES = [
    ("Q1  – Average Listing Price by City",              q1_avg_price_by_city),
    ("Q2  – Average Price per Sqft by Property Type",    q2_price_per_sqft),
    ("Q3  – Furnishing Status vs Price",                 q3_furnishing_vs_price),
    ("Q4  – Metro Distance vs Price",                    q4_metro_distance_price),
    ("Q5  – Rented vs Non-Rented Price",                 q5_rented_vs_price),
    ("Q6  – Bedrooms & Bathrooms vs Price",              q6_bedrooms_bathrooms_price),
    ("Q7  – Parking & Power Backup vs Price",            q7_parking_power_price),
    ("Q8  – Year Built vs Price",                        q8_year_built_price),
    ("Q9  – Top Cities by Avg Price",                    q9_top_cities_by_price),
    ("Q10 – Price Bucket Distribution",                  q10_price_buckets),
    ("Q11 – Avg Days on Market by City",                 q11_avg_days_by_city),
    ("Q12 – Fastest Selling Property Types",             q12_fastest_selling_types),
    ("Q13 – % Properties Sold Above List Price",         q13_pct_above_list),
    ("Q14 – Sale-to-List Price Ratio by City",           q14_sale_to_list_ratio),
    ("Q15 – Listings Taking 90+ Days to Sell",           q15_slow_listings),
    ("Q16 – Metro Distance vs Time on Market",           q16_metro_vs_days),
    ("Q17 – Monthly Sales Trend",                        q17_monthly_sales_trend),
    ("Q18 – Currently Unsold Properties",                q18_unsold_properties),
    ("Q19 – Top Agents by Sales Count",                  q19_top_agents_by_sales),
    ("Q20 – Top Agents by Revenue",                      q20_top_agents_by_revenue),
    ("Q21 – Fastest Deal-Closing Agents",                q21_fastest_closing_agents),
    ("Q22 – Experience vs Deals Closed",                 q22_experience_vs_deals),
    ("Q23 – Agent Rating vs Close Speed",                q23_rating_vs_close_speed),
    ("Q24 – Commission Earned per Agent",                q24_avg_commission),
    ("Q25 – Agents with Most Active Listings",           q25_agents_most_active),
    ("Q26 – Investor vs End User Buyers",                q26_investor_vs_enduser),
    ("Q27 – Loan Uptake Rate by City",                   q27_loan_uptake_by_city),
    ("Q28 – Avg Loan Amount by Buyer Type",              q28_avg_loan_by_buyer_type),
    ("Q29 – Most Common Payment Mode",                   q29_payment_mode),
    ("Q30 – Loan-backed vs Cash Purchase Close Time",    q30_loan_vs_close_time),
]
