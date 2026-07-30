"""
BrickView - Database Loader
Reads all JSON/CSV files and loads them into SQLite (brickview.db)
Run: python load_db.py
"""

import sqlite3
import json
import csv
import os

DB_PATH = "brickview.db"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def create_schema(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS buyers;
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS property_attributes;
        DROP TABLE IF EXISTS listings;
        DROP TABLE IF EXISTS agents;

        CREATE TABLE agents (
            Agent_ID         TEXT PRIMARY KEY,
            Name             TEXT NOT NULL,
            City             TEXT,
            Contact          TEXT,
            Commission_Rate  REAL,
            Deals_Closed     INTEGER,
            Rating           REAL,
            Experience_Years INTEGER,
            Avg_Closing_Days INTEGER
        );

        CREATE TABLE listings (
            Listing_ID    TEXT PRIMARY KEY,
            City          TEXT,
            Property_Type TEXT,
            Price         REAL,
            Area_sqft     REAL,
            Agent_ID      TEXT REFERENCES agents(Agent_ID),
            Listed_Date   TEXT,
            Latitude      REAL,
            Longitude     REAL,
            Neighborhood  TEXT
        );

        CREATE TABLE property_attributes (
            Attribute_ID       TEXT PRIMARY KEY,
            Listing_ID         TEXT REFERENCES listings(Listing_ID),
            Bedrooms           INTEGER,
            Bathrooms          INTEGER,
            Floor_Number       INTEGER,
            Total_Floors       INTEGER,
            Year_Built         INTEGER,
            Is_Rented          INTEGER,
            Tenant_Count       INTEGER,
            Furnishing_Status  TEXT,
            Metro_Distance_Km  REAL,
            Parking_Available  INTEGER,
            Power_Backup       INTEGER
        );

        CREATE TABLE sales (
            Sale_ID        TEXT PRIMARY KEY,
            Listing_ID     TEXT REFERENCES listings(Listing_ID),
            Sale_Date      TEXT,
            Sale_Price     REAL,
            Days_On_Market INTEGER
        );

        CREATE TABLE buyers (
            Buyer_ID      TEXT PRIMARY KEY,
            Sale_ID       TEXT REFERENCES sales(Sale_ID),
            Buyer_Type    TEXT,
            Payment_Mode  TEXT,
            Loan_Taken    INTEGER,
            Loan_Provider TEXT,
            Loan_Amount   REAL
        );

        CREATE INDEX idx_listings_city   ON listings(City);
        CREATE INDEX idx_listings_agent  ON listings(Agent_ID);
        CREATE INDEX idx_sales_listing   ON sales(Listing_ID);
        CREATE INDEX idx_buyers_sale     ON buyers(Sale_ID);
        CREATE INDEX idx_attr_listing    ON property_attributes(Listing_ID);
    """)
    print("✅ Schema created")

def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def load_csv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))

def bool_int(v):
    if isinstance(v, bool): return int(v)
    if isinstance(v, str):  return 1 if v.lower() in ("true","1","yes") else 0
    return int(v) if v is not None else 0

def insert_agents(conn, data):
    rows = [(r["Agent_ID"], r["Name"], r.get("City"), r.get("Contact"),
             r.get("Commission_Rate"), r.get("Deals_Closed"), r.get("Rating"),
             r.get("Experience_Years"), r.get("Avg_Closing_Days")) for r in data]
    conn.executemany(
        "INSERT OR REPLACE INTO agents VALUES (?,?,?,?,?,?,?,?,?)", rows)
    print(f"✅ Agents loaded: {len(rows)}")

def insert_listings(conn, data):
    rows = [(r["Listing_ID"], r["City"], r["Property_Type"], r["Price"],
             r["Area_sqft"], r["Agent_ID"], r["Listed_Date"],
             r.get("Latitude"), r.get("Longitude"), r.get("Neighborhood")) for r in data]
    conn.executemany(
        "INSERT OR REPLACE INTO listings VALUES (?,?,?,?,?,?,?,?,?,?)", rows)
    print(f"✅ Listings loaded: {len(rows)}")

def insert_attributes(conn, data):
    rows = [(r["Attribute_ID"], r["Listing_ID"], r.get("Bedrooms"), r.get("Bathrooms"),
             r.get("Floor_Number"), r.get("Total_Floors"), r.get("Year_Built"),
             bool_int(r.get("Is_Rented", 0)), r.get("Tenant_Count"),
             r.get("Furnishing_Status"), r.get("Metro_Distance_Km"),
             bool_int(r.get("Parking_Available", 0)),
             bool_int(r.get("Power_Backup", 0))) for r in data]
    conn.executemany(
        "INSERT OR REPLACE INTO property_attributes VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    print(f"✅ Property attributes loaded: {len(rows)}")

def insert_sales(conn, data):
    rows = [(r["Sale_ID"], r["Listing_ID"], r["Sale_Date"],
             float(r["Sale_Price"]), int(r["Days_On_Market"])) for r in data]
    conn.executemany(
        "INSERT OR REPLACE INTO sales VALUES (?,?,?,?,?)", rows)
    print(f"✅ Sales loaded: {len(rows)}")

def insert_buyers(conn, data):
    rows = [(r["Buyer_ID"], r["Sale_ID"], r.get("Buyer_Type"), r.get("Payment_Mode"),
             bool_int(r.get("Loan_Taken", 0)), r.get("Loan_Provider"),
             float(r.get("Loan_Amount") or 0)) for r in data]
    conn.executemany(
        "INSERT OR REPLACE INTO buyers VALUES (?,?,?,?,?,?,?)", rows)
    print(f"✅ Buyers loaded: {len(rows)}")

if __name__ == "__main__":
    # Check if data files exist; if not, generate them first
    if not os.path.exists("listings_final_expanded.json"):
        print("⚠️  Data files not found. Generating sample data first...")
        import generate_data  # noqa

    conn = get_conn()
    create_schema(conn)

    insert_agents(conn,     load_json("agents_cleaned.json"))
    insert_listings(conn,   load_json("listings_final_expanded.json"))
    insert_attributes(conn, load_json("property_attributes_final_expanded.json"))
    insert_sales(conn,      load_csv("sales_cleaned.csv"))
    insert_buyers(conn,     load_json("buyers_cleaned.json"))

    conn.commit()
    conn.close()
    print(f"\n🎉 Database ready: {DB_PATH}")
    print("Now run: streamlit run app.py")
