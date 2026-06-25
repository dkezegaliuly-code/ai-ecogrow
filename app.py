import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import time

# --- 1. CONFIGURATION & STYLE (Enterprise Grade) ---
st.set_page_config(page_title="EcoGrow Industrial AI", layout="wide", page_icon="🌱")

# Көзді ауыртпайтын, заманауи "Dark Mode" стилі
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f1f5f9; }
    .card { background: #0f172a; padding: 20px; border-radius: 12px; border: 1px solid #1e293b; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .alert-crit { border-left: 5px solid #ef4444; background: #450a0a; padding: 10px; }
    .metric-val { font-size: 28px; font-weight: bold; color: #38bdf8; }
    </style>
""", unsafe_allow_html=True)

# --- 2. ADVANCED DATA ENGINE (Backend logic) ---
class TelemetryManager:
    """Датчиктерді басқару және имитациялау модулі"""
    @staticmethod
    def get_realtime_data():
        return {
            "temp": round(random.uniform(22, 28), 1),
            "hum": round(random.uniform(40, 60), 1),
            "soil": round(random.uniform(30, 50), 1),
            "co2": random.randint(400, 900),
            "energy": round(random.uniform(5, 20), 2)
        }

    @staticmethod
    def get_historical_df():
        days = 30
        return pd.DataFrame({
            "Date": [datetime.now() - timedelta(days=i) for i in range(days)],
            "Yield_Efficiency": np.random.uniform(85, 99, days),
            "Power_Usage": np.random.uniform(100, 300, days)
        })

# --- 3. DASHBOARD COMPONENTS ---
def sidebar_menu():
    st.sidebar.title("🔐 Control Panel")
    role = st.sidebar.selectbox("Access Role", ["Admin", "Operator", "Analyst"])
    st.sidebar.markdown("---")
    st.sidebar.subheader("Hardware Diagnostics")
    for sensor in ["Node_A", "Node_B", "Node_C"]:
        status = random.choice(["OK", "WARN", "CRIT"])
        st.sidebar.write(f"{sensor}: {'✅' if status=='OK' else '⚠️'}")
    return role

def main_dashboard():
    tm = TelemetryManager()
    data = tm.get_realtime_data()
    
    st.title("🌱 EcoGrow Enterprise | Industrial IoT System")
    
    # KPI Row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Temperature", f"{data['temp']}°C", "Stable")
    c2.metric("Humidity", f"{data['hum']}%", "-1.2%")
    c3.metric("Soil Moisture", f"{data['soil']}%", "+2.1%")
    c4.metric("CO2 Level", f"{data['co2']} ppm", "+15")

    # Tabs for Organization
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Live Analytics", "📉 Performance Trends", "⚙️ Hardware Config", "🤖 AI Auditor"])

    with tab1:
        st.subheader("Real-time Telemetry Stream")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["Temp", "Hum", "Soil"])
        st.line_chart(chart_data)

    with tab2:
        st.subheader("30-Day Efficiency Report")
        df = tm.get_historical_df()
        fig = px.area(df, x="Date", y="Yield_Efficiency", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("Hardware Actuator Settings")
        col_x, col_y = st.columns(2)
        vent_speed = col_x.slider("Ventilation Speed (%)", 0, 100, 45)
        pump_timer = col_y.slider("Irrigation Cycle (min)", 5, 60, 15)
        if st.button("Apply Configuration"):
            st.success("New parameters synced with IoT Controllers.")

    with tab4:
        st.subheader("AI System Diagnostics")
        st.info("AI Analysis: Sector 4 requires 15% more irrigation due to soil compaction.")
        if st.button("Run Deep System Scan"):
            with st.spinner("Analyzing all sensor arrays..."):
                time.sleep(2)
                st.success("Scan complete. No hardware failures detected.")

# --- 4. EXECUTION ---
role = sidebar_menu()
main_dashboard()

st.markdown("---")
st.caption("Industrial System V4.0.0 | Enterprise Edition | Secure Connection Active")
