"""
BrickView – Real Estate Analytics Platform
Run: streamlit run app.py
"""

import sqlite3
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import queries as Q

# ─── Page config ────────────────────────────────────────────
st.set_page_config(
    page_title="BrickView",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

DB_PATH = "brickview.db"

# ─── DB helpers ─────────────────────────────────────────────
@st.cache_resource
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def qdf(sql, params=()):
    return pd.read_sql_query(sql, get_conn(), params=params)

# ─── Sidebar navigation ─────────────────────────────────────
PAGES = ["🏠 Dashboard", "📊 SQL Queries", "🗃️ CRUD Operations", "🔍 Filters & Map"]
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/buildings.png", width=60)
    st.title("BrickView")
    st.caption("Real Estate Analytics Platform")
    st.divider()
    page = st.radio("Navigate", PAGES, label_visibility="collapsed")
    st.divider()
    st.caption("GUVI × HCL Capstone Project")

# ════════════════════════════════════════════════════════════
#  PAGE 1 – DASHBOARD
# ════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.title("🏢 BrickView – Real Estate Analytics")
    st.caption("Live insights across listings, sales, agents, and buyers")

    # KPI row
    total_listings = qdf("SELECT COUNT(*) AS c FROM listings").iloc[0]["c"]
    total_sales    = qdf("SELECT COUNT(*) AS c FROM sales").iloc[0]["c"]
    total_agents   = qdf("SELECT COUNT(*) AS c FROM agents").iloc[0]["c"]
    avg_price      = qdf("SELECT ROUND(AVG(Price),0) AS c FROM listings").iloc[0]["c"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Listings",  f"{total_listings:,}")
    c2.metric("Properties Sold", f"{total_sales:,}")
    c3.metric("Active Agents",   f"{total_agents:,}")
    c4.metric("Avg List Price",  f"₹{avg_price:,.0f}")

    st.divider()

    col1, col2 = st.columns(2)

    # Bar – Avg price by city
    with col1:
        st.subheader("Average Price by City")
        _, df = Q.q1_avg_price_by_city()
        fig = px.bar(df, x="City", y="Avg_Price", color="City",
                     labels={"Avg_Price": "Avg Price (₹)"},
                     color_discrete_sequence=px.colors.qualitative.Bold)
        fig.update_layout(showlegend=False, height=340)
        st.plotly_chart(fig, use_container_width=True)

    # Pie – property type distribution
    with col2:
        st.subheader("Property Type Distribution")
        df_pt = qdf("SELECT Property_Type, COUNT(*) AS Count FROM listings GROUP BY Property_Type")
        fig2 = px.pie(df_pt, names="Property_Type", values="Count",
                      color_discrete_sequence=px.colors.qualitative.Pastel)
        fig2.update_layout(height=340)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)

    # Line – monthly sales trend
    with col3:
        st.subheader("Monthly Sales Trend")
        _, df_trend = Q.q17_monthly_sales_trend()
        fig3 = px.line(df_trend, x="Month", y="Total_Sales", markers=True,
                       labels={"Total_Sales": "Sales"},
                       color_discrete_sequence=["#2563EB"])
        fig3.update_layout(height=300)
        st.plotly_chart(fig3, use_container_width=True)

    # Bar – top 5 agents
    with col4:
        st.subheader("Top 5 Agents by Sales")
        _, df_ag = Q.q19_top_agents_by_sales()
        fig4 = px.bar(df_ag.head(5), x="Name", y="Sales_Closed",
                      color="Sales_Closed",
                      color_continuous_scale="Blues",
                      labels={"Sales_Closed": "Deals Closed"})
        fig4.update_layout(height=300, showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    # Furnishing status vs price
    st.subheader("Furnishing Status vs Avg Price")
    _, df_f = Q.q3_furnishing_vs_price()
    fig5 = px.bar(df_f, x="Furnishing_Status", y="Avg_Price",
                  color="Furnishing_Status",
                  color_discrete_sequence=["#10B981","#F59E0B","#EF4444"],
                  labels={"Avg_Price": "Avg Price (₹)"})
    fig5.update_layout(showlegend=False, height=300)
    st.plotly_chart(fig5, use_container_width=True)


# ════════════════════════════════════════════════════════════
#  PAGE 2 – SQL QUERIES
# ════════════════════════════════════════════════════════════
elif page == "📊 SQL Queries":
    st.title("📊 SQL Queries & Results")
    st.caption("All 30 analytical queries with their SQL and output tables")

    selected = st.selectbox(
        "Select a Query",
        [label for label, _ in Q.ALL_QUERIES],
        index=0
    )

    fn = dict(Q.ALL_QUERIES)[selected]
    sql_str, df = fn()

    with st.expander("🔍 View SQL Query", expanded=True):
        st.code(sql_str, language="sql")

    st.subheader("Query Result")
    st.dataframe(df, use_container_width=True, height=400)
    st.caption(f"{len(df)} rows returned")

    # Auto-chart where possible
    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    text_cols    = df.select_dtypes(exclude="number").columns.tolist()

    if len(numeric_cols) >= 1 and len(text_cols) >= 1:
        st.subheader("Quick Visualisation")
        x_col = st.selectbox("X-axis (category)", text_cols,  key="qx")
        y_col = st.selectbox("Y-axis (numeric)",   numeric_cols, key="qy")
        chart_type = st.radio("Chart Type", ["Bar", "Line", "Pie"], horizontal=True)

        if chart_type == "Bar":
            fig = px.bar(df, x=x_col, y=y_col,
                         color_discrete_sequence=["#2563EB"])
        elif chart_type == "Line":
            fig = px.line(df, x=x_col, y=y_col, markers=True,
                          color_discrete_sequence=["#10B981"])
        else:
            fig = px.pie(df, names=x_col, values=y_col)
        st.plotly_chart(fig, use_container_width=True)


# ════════════════════════════════════════════════════════════
#  PAGE 3 – CRUD OPERATIONS
# ════════════════════════════════════════════════════════════
elif page == "🗃️ CRUD Operations":
    st.title("🗃️ CRUD Operations")
    st.caption("Create, Read, Update, and Delete records across all tables")

    TABLE_COLS = {
        "agents":               ["Agent_ID","Name","City","Contact","Commission_Rate","Deals_Closed","Rating","Experience_Years","Avg_Closing_Days"],
        "listings":             ["Listing_ID","City","Property_Type","Price","Area_sqft","Agent_ID","Listed_Date","Latitude","Longitude","Neighborhood"],
        "property_attributes":  ["Attribute_ID","Listing_ID","Bedrooms","Bathrooms","Floor_Number","Total_Floors","Year_Built","Is_Rented","Tenant_Count","Furnishing_Status","Metro_Distance_Km","Parking_Available","Power_Backup"],
        "sales":                ["Sale_ID","Listing_ID","Sale_Date","Sale_Price","Days_On_Market"],
        "buyers":               ["Buyer_ID","Sale_ID","Buyer_Type","Payment_Mode","Loan_Taken","Loan_Provider","Loan_Amount"],
    }
    PK = {"agents":"Agent_ID","listings":"Listing_ID","property_attributes":"Attribute_ID",
          "sales":"Sale_ID","buyers":"Buyer_ID"}

    table = st.selectbox("Select Table", list(TABLE_COLS.keys()))
    cols  = TABLE_COLS[table]
    pk    = PK[table]

    tab_r, tab_c, tab_u, tab_d = st.tabs(["📖 View", "➕ Add", "✏️ Update", "🗑️ Delete"])

    conn = get_conn()

    # ── READ ────────────────────────────────────────────────
    with tab_r:
        st.subheader(f"All records in '{table}'")
        search = st.text_input("🔎 Filter by keyword")
        df_all = pd.read_sql_query(f"SELECT * FROM {table}", conn)
        if search:
            mask = df_all.apply(lambda col: col.astype(str).str.contains(search, case=False)).any(axis=1)
            df_all = df_all[mask]
        st.dataframe(df_all, use_container_width=True, height=500)
        st.caption(f"{len(df_all)} records shown")

    # ── CREATE ──────────────────────────────────────────────
    with tab_c:
        st.subheader(f"Add a new record to '{table}'")
        new_vals = {}
        for col in cols:
            new_vals[col] = st.text_input(col, key=f"c_{col}")

        if st.button("➕ Insert Record", type="primary"):
            placeholders = ",".join(["?"] * len(cols))
            col_str      = ",".join(cols)
            try:
                conn.execute(
                    f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})",
                    [new_vals[c] for c in cols]
                )
                conn.commit()
                st.success("✅ Record inserted!")
                st.cache_resource.clear()
            except Exception as e:
                st.error(f"❌ {e}")

    # ── UPDATE ──────────────────────────────────────────────
    with tab_u:
        st.subheader(f"Update a record in '{table}'")
        upd_pk = st.text_input(f"Enter {pk} to update", key="upd_pk")
        if upd_pk:
            row = pd.read_sql_query(
                f"SELECT * FROM {table} WHERE {pk}=?", conn, params=(upd_pk,))
            if row.empty:
                st.warning("Record not found.")
            else:
                upd_vals = {}
                for col in cols:
                    default = str(row.iloc[0][col]) if col in row.columns else ""
                    upd_vals[col] = st.text_input(col, value=default, key=f"u_{col}")

                if st.button("💾 Save Changes", type="primary"):
                    set_clause = ", ".join([f"{c}=?" for c in cols if c != pk])
                    values     = [upd_vals[c] for c in cols if c != pk] + [upd_pk]
                    try:
                        conn.execute(
                            f"UPDATE {table} SET {set_clause} WHERE {pk}=?", values)
                        conn.commit()
                        st.success("✅ Record updated!")
                    except Exception as e:
                        st.error(f"❌ {e}")

    # ── DELETE ──────────────────────────────────────────────
    with tab_d:
        st.subheader(f"Delete a record from '{table}'")
        del_pk = st.text_input(f"Enter {pk} to delete", key="del_pk")
        if del_pk:
            row = pd.read_sql_query(
                f"SELECT * FROM {table} WHERE {pk}=?", conn, params=(del_pk,))
            if row.empty:
                st.warning("Record not found.")
            else:
                st.dataframe(row, use_container_width=True)
                if st.button("🗑️ Delete Record", type="primary"):
                    try:
                        conn.execute(
                            f"DELETE FROM {table} WHERE {pk}=?", (del_pk,))
                        conn.commit()
                        st.success("✅ Record deleted!")
                    except Exception as e:
                        st.error(f"❌ {e}")


# ════════════════════════════════════════════════════════════
#  PAGE 4 – FILTERS & MAP
# ════════════════════════════════════════════════════════════
elif page == "🔍 Filters & Map":
    st.title("🔍 Filters & Interactive Map")
    st.caption("Explore listings by city, property type, price range, agent, and date")

    # Load filter options
    cities    = qdf("SELECT DISTINCT City FROM listings ORDER BY City")["City"].tolist()
    types     = qdf("SELECT DISTINCT Property_Type FROM listings ORDER BY Property_Type")["Property_Type"].tolist()
    agents_df = qdf("SELECT Agent_ID, Name FROM agents ORDER BY Name")
    agent_map = dict(zip(agents_df["Name"], agents_df["Agent_ID"]))
    prices    = qdf("SELECT MIN(Price) AS mn, MAX(Price) AS mx FROM listings").iloc[0]

    # Sidebar filters
    with st.sidebar:
        st.subheader("🎛️ Filters")
        sel_cities = st.multiselect("City", cities, default=cities[:3])
        sel_types  = st.multiselect("Property Type", types, default=types)
        sel_agents = st.multiselect("Agent", list(agent_map.keys()))
        price_min, price_max = st.slider(
            "Price Range (₹)",
            min_value=int(prices["mn"]),
            max_value=int(prices["mx"]),
            value=(int(prices["mn"]), int(prices["mx"])),
            step=100000,
            format="₹%d"
        )
        date_from = st.date_input("Listed From", value=pd.to_datetime("2022-01-01"))
        date_to   = st.date_input("Listed To",   value=pd.to_datetime("2024-12-31"))

    # Build dynamic query
    where_parts = ["l.Price BETWEEN ? AND ?"]
    params      = [price_min, price_max]

    if sel_cities:
        placeholders = ",".join(["?"] * len(sel_cities))
        where_parts.append(f"l.City IN ({placeholders})")
        params.extend(sel_cities)

    if sel_types:
        placeholders = ",".join(["?"] * len(sel_types))
        where_parts.append(f"l.Property_Type IN ({placeholders})")
        params.extend(sel_types)

    if sel_agents:
        agent_ids    = [agent_map[n] for n in sel_agents]
        placeholders = ",".join(["?"] * len(agent_ids))
        where_parts.append(f"l.Agent_ID IN ({placeholders})")
        params.extend(agent_ids)

    where_parts.append("l.Listed_Date BETWEEN ? AND ?")
    params.extend([str(date_from), str(date_to)])

    where_clause = " AND ".join(where_parts)
    sql_filter = f"""
        SELECT l.Listing_ID, l.City, l.Property_Type, l.Price, l.Area_sqft,
               l.Listed_Date, l.Latitude, l.Longitude,
               a.Name AS Agent_Name,
               pa.Bedrooms, pa.Bathrooms, pa.Furnishing_Status
        FROM   listings l
        LEFT   JOIN agents a             ON l.Agent_ID   = a.Agent_ID
        LEFT   JOIN property_attributes pa ON l.Listing_ID = pa.Listing_ID
        WHERE  {where_clause}
        ORDER  BY l.Price DESC
        LIMIT  500;
    """
    df_filtered = qdf(sql_filter, params)

    # KPIs
    k1, k2, k3 = st.columns(3)
    k1.metric("Listings Found",  len(df_filtered))
    k2.metric("Avg Price",       f"₹{df_filtered['Price'].mean():,.0f}" if len(df_filtered) else "—")
    k3.metric("Avg Area (sqft)", f"{df_filtered['Area_sqft'].mean():,.0f}" if len(df_filtered) else "—")

    st.divider()

    # Map
    if not df_filtered.empty and df_filtered["Latitude"].notna().any():
        st.subheader("📍 Property Map")
        map_df = df_filtered.dropna(subset=["Latitude","Longitude"])
        fig_map = px.scatter_mapbox(
            map_df,
            lat="Latitude", lon="Longitude",
            color="Property_Type",
            size="Price",
            size_max=18,
            hover_name="Listing_ID",
            hover_data={"City":True,"Price":True,"Area_sqft":True,
                        "Bedrooms":True,"Agent_Name":True,
                        "Latitude":False,"Longitude":False},
            mapbox_style="carto-positron",
            zoom=4,
            height=500,
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        st.plotly_chart(fig_map, use_container_width=True)

    # Charts
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Listings by City")
        city_count = df_filtered["City"].value_counts().reset_index()
        city_count.columns = ["City","Count"]
        fig_c = px.bar(city_count, x="City", y="Count",
                       color="City", color_discrete_sequence=px.colors.qualitative.Bold)
        fig_c.update_layout(showlegend=False, height=300)
        st.plotly_chart(fig_c, use_container_width=True)

    with col2:
        st.subheader("Property Type Mix")
        pt_count = df_filtered["Property_Type"].value_counts().reset_index()
        pt_count.columns = ["Property_Type","Count"]
        fig_p = px.pie(pt_count, names="Property_Type", values="Count",
                       color_discrete_sequence=px.colors.qualitative.Pastel)
        fig_p.update_layout(height=300)
        st.plotly_chart(fig_p, use_container_width=True)

    # Table
    st.subheader("📋 Filtered Listings Table")
    st.dataframe(
        df_filtered[["Listing_ID","City","Property_Type","Price","Area_sqft",
                     "Bedrooms","Bathrooms","Furnishing_Status","Agent_Name","Listed_Date"]],
        use_container_width=True,
        height=400
    )
