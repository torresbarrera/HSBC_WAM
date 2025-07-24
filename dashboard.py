
import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import os
import json
import google.generativeai as genai
import numpy as np

# --- Page Setup ---
st.set_page_config(page_title="Workplace Analytics Dashboard", layout="wide")
st.title("Workplace Analytics Dashboard")
st.markdown("Analyzing workspace utilization patterns for the ASP Region.")

# --- API Key Input ---
st.sidebar.header("API Configuration")
api_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# --- Configuration & Initialization ---
DB_FILE = 'workspace_analytics.db'
llm_model = None

if api_key:
    try:
        genai.configure(api_key=api_key)
        llm_model = genai.GenerativeModel('gemini-pro') # Or your preferred model
        st.sidebar.success("API Key configured successfully!")
    except Exception as e:
        st.sidebar.error(f"Error configuring the AI model: {e}")
else:
    st.sidebar.warning("Please enter your Gemini API Key to enable AI features.")


# --- AI Insight Generation ---
def convert_to_json_serializable(obj):
    """Recursively convert non-serializable data types to serializable ones."""
    if isinstance(obj, dict):
        return {k: convert_to_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_to_json_serializable(i) for i in obj]
    elif isinstance(obj, (np.integer, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.floating, np.float64)):
        return float(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif pd.isna(obj):
        return None
    return obj

def generate_insights(data_summary):
    """Generates insights using the configured generative AI model."""
    if not llm_model:
        return "AI Model not available. Please enter your API key in the sidebar."

    serializable_summary = convert_to_json_serializable(data_summary)
    prompt = f"""
    You are a senior Workspace Analytics consultant for HSBC. Your task is to provide data-driven insights based on a JSON summary from the Workplace Analytics Dashboard.

    **Dashboard Data Summary:**
    {json.dumps(serializable_summary, indent=2)}

    **Your Task:**
    Identify the 2-3 most critical and actionable insights from this data. For each insight, provide a specific data point that backs it up and a concrete recommendation.

    **Output Format (Use Markdown):**
    **Insight 1:** [A clear, one-sentence insight about a key trend or anomaly.]
    *   **Data Point:** [The specific metric from the data that supports your insight.]
    *   **Recommendation:** [A concrete, actionable suggestion.]
    """
    try:
        response = llm_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred while generating insights: {e}"

# --- Database Connection & Caching ---
@st.cache_data(ttl=600)
def run_query(query):
    """Run a SQL query and return the result as a DataFrame."""
    if not os.path.exists(DB_FILE):
        st.error(f"Database file not found at '{DB_FILE}'. Please run `load_to_sqlite.py` first.")
        st.stop()
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# --- Sidebar Filters ---
st.sidebar.header("Dashboard Filters")

max_date_df = run_query("SELECT MAX(Date) as MaxDate FROM bookings")
max_date = pd.to_datetime(max_date_df['MaxDate'].iloc[0])
default_start_date = max_date - pd.Timedelta(days=30)

date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(default_start_date, max_date),
    min_value=pd.to_datetime(run_query("SELECT MIN(Date) as MinDate FROM bookings")['MinDate'].iloc[0]),
    max_value=max_date,
)

if len(date_range) != 2:
    st.sidebar.warning("Please select a start and end date.")
    st.stop()

start_date, end_date = date_range
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

countries = run_query("SELECT DISTINCT Country FROM spaces ORDER BY Country")
selected_country = st.sidebar.selectbox("Country", countries['Country'].unique(), index=None, placeholder="All Countries")

if selected_country:
    cities = run_query(f"SELECT DISTINCT City FROM spaces WHERE Country = '{selected_country}' ORDER BY City")
    selected_city = st.sidebar.selectbox("City", cities['City'].unique(), index=None, placeholder="All Cities")
else:
    selected_city = None

if selected_city:
    buildings = run_query(f"SELECT DISTINCT Building FROM spaces WHERE City = '{selected_city}' ORDER BY Building")
    selected_building = st.sidebar.selectbox("Building", buildings['Building'].unique(), index=None, placeholder="All Buildings")
else:
    selected_building = None

# --- Build WHERE clauses ---
base_where_conditions = [
    "b.Booking_Status = 'Confirmed'",
    f"b.Date BETWEEN '{start_date_str}' AND '{end_date_str}'"
]
space_where_conditions = []
no_show_where_conditions = [f"b.Date BETWEEN '{start_date_str}' AND '{end_date_str}'"]

if selected_building:
    location_filter = f"s.Building = '{selected_building}'"
    space_location_filter = f"Building = '{selected_building}'"
    base_where_conditions.append(location_filter)
    space_where_conditions.append(space_location_filter)
    no_show_where_conditions.append(location_filter)
elif selected_city:
    location_filter = f"s.City = '{selected_city}'"
    space_location_filter = f"City = '{selected_city}'"
    base_where_conditions.append(location_filter)
    space_where_conditions.append(space_location_filter)
    no_show_where_conditions.append(location_filter)
elif selected_country:
    location_filter = f"s.Country = '{selected_country}'"
    space_location_filter = f"Country = '{selected_country}'"
    base_where_conditions.append(location_filter)
    space_where_conditions.append(space_location_filter)
    no_show_where_conditions.append(location_filter)

where_clause = "WHERE " + " AND ".join(base_where_conditions)
space_where_clause = "WHERE " + " AND ".join(space_where_conditions) if space_where_conditions else ""
no_show_where_clause = "WHERE " + " AND ".join(no_show_where_conditions) if no_show_where_conditions else ""

base_query = f"FROM bookings b JOIN spaces s ON b.Space_ID = s.Space_ID JOIN employees e ON b.Employee_ID = e.Employee_ID {where_clause}"

# --- Pre-calculate all dataframes ---
peak_occupancy_df = run_query(f"SELECT COUNT(DISTINCT b.Employee_ID) as Occupancy {base_query}")
total_spaces_df = run_query(f"SELECT COUNT(DISTINCT Space_ID) as TotalSpaces FROM spaces {space_where_clause}")
avg_daily_users_df = run_query(f"SELECT AVG(DailyUsers) as AvgUsers FROM (SELECT COUNT(DISTINCT b.Employee_ID) as DailyUsers {base_query} GROUP BY Date) as DailyCounts")
no_show_df = run_query(f"SELECT CAST(SUM(CASE WHEN Booking_Status = 'No-Show' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100 as NoShowRate FROM bookings b JOIN spaces s ON b.Space_ID = s.Space_ID {no_show_where_clause}")
adhoc_df = run_query(f"SELECT CAST(SUM(CASE WHEN Activity_Type = 'Check-in' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100 as AdhocRate {base_query}")
day_of_week_df = run_query(f"SELECT CASE strftime('%w', daily.Date) WHEN '0' THEN 'Sunday' WHEN '1' THEN 'Monday' WHEN '2' THEN 'Tuesday' WHEN '3' THEN 'Wednesday' WHEN '4' THEN 'Thursday' WHEN '5' THEN 'Friday' ELSE 'Saturday' END as DayOfWeek, AVG(daily.Occupancy) as AvgOccupancy FROM (SELECT Date, COUNT(DISTINCT b.Employee_ID) as Occupancy {base_query} GROUP BY Date) as daily GROUP BY DayOfWeek ORDER BY strftime('%w', daily.Date)")
space_type_df = run_query(f"SELECT s.Space_Type, COUNT(*) as BookingCount {base_query} GROUP BY s.Space_Type ORDER BY BookingCount DESC")

# --- Display KPIs and Charts ---
st.header("Key Performance Indicators")
kpi_cols = st.columns(4)
peak_occupancy = peak_occupancy_df['Occupancy'].iloc[0] if not peak_occupancy_df.empty else 0
total_spaces = total_spaces_df['TotalSpaces'].iloc[0]
avg_daily_users = avg_daily_users_df['AvgUsers'].iloc[0] if not avg_daily_users_df.empty and avg_daily_users_df['AvgUsers'].iloc[0] is not None else 0
avg_utilization = (avg_daily_users / total_spaces) * 100 if total_spaces > 0 else 0
no_show_rate = no_show_df['NoShowRate'].iloc[0] if not no_show_df.empty and no_show_df['NoShowRate'].iloc[0] is not None else 0
adhoc_rate = adhoc_df['AdhocRate'].iloc[0] if not adhoc_df.empty and adhoc_df['AdhocRate'].iloc[0] is not None else 0

kpi_cols[0].metric("Peak Daily Occupancy", f"{peak_occupancy:,}")
kpi_cols[1].metric("Average Daily Utilization", f"{avg_utilization:.1f}%")
kpi_cols[2].metric("Booking No-Show Rate", f"{no_show_rate:.1f}%")
kpi_cols[3].metric("Ad-Hoc Booking Rate", f"{adhoc_rate:.1f}%")

st.divider()

st.header("Occupancy & Utilization Trends")
agg_level = st.radio("Aggregate data by:", ('Daily', 'Weekly', 'Monthly'), horizontal=True, key='agg_level')
date_format = '%Y-%m-%d' if agg_level == 'Daily' else ('%Y-%W' if agg_level == 'Weekly' else '%Y-%m')
title = f'{agg_level} Occupancy Over Time'
occupancy_trend_query = f"SELECT strftime('{date_format}', Date) as AggDate, COUNT(DISTINCT b.Employee_ID) as Occupancy {base_query} GROUP BY AggDate ORDER BY AggDate"
occupancy_trend_df = run_query(occupancy_trend_query)

if not occupancy_trend_df.empty:
    fig1 = px.line(occupancy_trend_df, x='AggDate', y='Occupancy', title=title, labels={'Occupancy': 'Number of Employees', 'AggDate': 'Date'})
    st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("No occupancy data available for the selected filters.")

st.divider()

st.header("Space & Department Analysis")
analysis_cols = st.columns(2)
if not day_of_week_df.empty:
    fig2 = px.bar(day_of_week_df, x='DayOfWeek', y='AvgOccupancy', title='Average Occupancy by Day of Week', labels={'AvgOccupancy': 'Avg. Number of Employees'})
    analysis_cols[0].plotly_chart(fig2, use_container_width=True)
else:
    analysis_cols[0].warning("No data for day-of-week analysis.")
if not space_type_df.empty:
    fig3 = px.bar(space_type_df, x='Space_Type', y='BookingCount', title='Bookings by Space Type', labels={'BookingCount': 'Number of Bookings'})
    analysis_cols[1].plotly_chart(fig3, use_container_width=True)

st.divider()

# --- AI-Powered Analysis Section ---
st.header("AI-Powered Analysis")
if not llm_model:
    st.warning("Please enter your Gemini API Key in the sidebar to use this feature.")
else:
    if st.button("✨ Generate Insights & Recommendations"):
        with st.spinner("Analyzing data and generating insights... (This may take a moment)"):
            data_summary = {
                "kpis": {
                    "peak_daily_occupancy": peak_occupancy,
                    "avg_daily_utilization_percent": round(avg_utilization, 2),
                    "no_show_rate_percent": round(no_show_rate, 2),
                    "adhoc_booking_rate_percent": round(adhoc_rate, 2)
                },
                "avg_occupancy_by_day": day_of_week_df.to_dict(orient='records'),
                "bookings_by_space_type": space_type_df.to_dict(orient='records'),
            }
            report = generate_insights(data_summary)
            st.markdown(report)
    else:
        st.info("Click the button to get an AI-powered analysis of the current data view.")
