"""
BrickView - Data Generator
Run this FIRST to create all datasets if you don't have the original JSON/CSV files.
It generates realistic fake data matching the exact schema required.
"""

import json
import csv
import random
from datetime import datetime, timedelta

random.seed(42)

CITIES = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"]
PROPERTY_TYPES = ["Apartment", "Villa", "Condo", "Townhouse", "Studio", "Penthouse"]
FURNISHING = ["Furnished", "Semi-Furnished", "Unfurnished"]
PAYMENT_MODES = ["Cash", "UPI", "Bank Transfer", "Cheque"]
BUYER_TYPES = ["Investor", "End User"]
LOAN_PROVIDERS = ["HDFC", "SBI", "ICICI", "Axis Bank", "Kotak", "LIC Housing"]

# ── Agents ──────────────────────────────────────────────────────────────────
agents = []
agent_names = [
    "Arjun Sharma", "Priya Patel", "Rahul Gupta", "Sneha Rao", "Vikram Singh",
    "Anjali Mehta", "Rohan Verma", "Kavita Nair", "Sanjay Iyer", "Deepa Reddy",
    "Amit Joshi", "Pooja Shah", "Nikhil Desai", "Swati Kulkarni", "Manoj Tiwari"
]
for i, name in enumerate(agent_names, 1):
    agents.append({
        "Agent_ID": f"AGT{i:03d}",
        "Name": name,
        "City": random.choice(CITIES),
        "Contact": f"+91-9{random.randint(100000000, 999999999)}",
        "Commission_Rate": round(random.uniform(1.5, 4.0), 2),
        "Deals_Closed": random.randint(5, 80),
        "Rating": round(random.uniform(3.0, 5.0), 1),
        "Experience_Years": random.randint(1, 20),
        "Avg_Closing_Days": random.randint(20, 90)
    })

with open("agents_cleaned.json", "w") as f:
    json.dump(agents, f, indent=2)
print(f"✅ agents_cleaned.json — {len(agents)} records")

# ── Listings ─────────────────────────────────────────────────────────────────
listings = []
city_coords = {
    "Mumbai":    (19.076, 72.877), "Delhi":     (28.613, 77.209),
    "Bangalore": (12.971, 77.594), "Chennai":   (13.083, 80.270),
    "Hyderabad": (17.385, 78.486), "Pune":      (18.520, 73.856),
    "Kolkata":   (22.572, 88.363), "Ahmedabad": (23.023, 72.572),
}
city_price_base = {
    "Mumbai": 12000000, "Delhi": 9000000, "Bangalore": 8000000,
    "Chennai": 6000000, "Hyderabad": 6500000, "Pune": 7000000,
    "Kolkata": 5000000, "Ahmedabad": 5500000,
}

for i in range(1, 501):
    city = random.choice(CITIES)
    lat_base, lng_base = city_coords[city]
    price_base = city_price_base[city]
    prop_type = random.choice(PROPERTY_TYPES)
    area = random.randint(400, 4000)
    price = int(price_base * random.uniform(0.5, 2.5) * (area / 1000))
    listed_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 900))

    listings.append({
        "Listing_ID": f"LST{i:04d}",
        "City": city,
        "Property_Type": prop_type,
        "Price": price,
        "Area_sqft": area,
        "Agent_ID": random.choice(agents)["Agent_ID"],
        "Listed_Date": listed_date.strftime("%Y-%m-%d"),
        "Latitude": round(lat_base + random.uniform(-0.1, 0.1), 6),
        "Longitude": round(lng_base + random.uniform(-0.1, 0.1), 6),
        "Neighborhood": random.choice(["North", "South", "East", "West", "Central"]) + " " + city
    })

with open("listings_final_expanded.json", "w") as f:
    json.dump(listings, f, indent=2)
print(f"✅ listings_final_expanded.json — {len(listings)} records")

# ── Property Attributes ───────────────────────────────────────────────────────
attrs = []
for i, l in enumerate(listings, 1):
    attrs.append({
        "Attribute_ID": f"ATTR{i:04d}",
        "Listing_ID": l["Listing_ID"],
        "Bedrooms": random.randint(1, 6),
        "Bathrooms": random.randint(1, 4),
        "Floor_Number": random.randint(0, 30),
        "Total_Floors": random.randint(1, 40),
        "Year_Built": random.randint(1990, 2023),
        "Is_Rented": random.choice([True, False]),
        "Tenant_Count": random.randint(0, 4),
        "Furnishing_Status": random.choice(FURNISHING),
        "Metro_Distance_Km": round(random.uniform(0.2, 15.0), 2),
        "Parking_Available": random.choice([True, False]),
        "Power_Backup": random.choice([True, False])
    })

with open("property_attributes_final_expanded.json", "w") as f:
    json.dump(attrs, f, indent=2)
print(f"✅ property_attributes_final_expanded.json — {len(attrs)} records")

# ── Sales ─────────────────────────────────────────────────────────────────────
sold_listings = random.sample(listings, 380)
sales = []
for i, l in enumerate(sold_listings, 1):
    listed = datetime.strptime(l["Listed_Date"], "%Y-%m-%d")
    days_on_market = random.randint(5, 180)
    sale_date = listed + timedelta(days=days_on_market)
    sale_price = int(l["Price"] * random.uniform(0.88, 1.12))
    sales.append({
        "Sale_ID": f"SAL{i:04d}",
        "Listing_ID": l["Listing_ID"],
        "Sale_Date": sale_date.strftime("%Y-%m-%d"),
        "Sale_Price": sale_price,
        "Days_On_Market": days_on_market
    })

with open("sales_cleaned.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["Sale_ID","Listing_ID","Sale_Date","Sale_Price","Days_On_Market"])
    writer.writeheader()
    writer.writerows(sales)
print(f"✅ sales_cleaned.csv — {len(sales)} records")

# ── Buyers ────────────────────────────────────────────────────────────────────
buyers = []
for i, s in enumerate(sales, 1):
    loan_taken = random.choice([True, False])
    buyers.append({
        "Buyer_ID": f"BYR{i:04d}",
        "Sale_ID": s["Sale_ID"],
        "Buyer_Type": random.choice(BUYER_TYPES),
        "Payment_Mode": random.choice(PAYMENT_MODES),
        "Loan_Taken": loan_taken,
        "Loan_Provider": random.choice(LOAN_PROVIDERS) if loan_taken else None,
        "Loan_Amount": int(s["Sale_Price"] * random.uniform(0.6, 0.85)) if loan_taken else 0
    })

with open("buyers_cleaned.json", "w") as f:
    json.dump(buyers, f, indent=2)
print(f"✅ buyers_cleaned.json — {len(buyers)} records")

print("\n🎉 All datasets generated! Now run: python load_db.py")
