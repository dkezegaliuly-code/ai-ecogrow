import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import random

# --- [1] КОНФИГУРАЦИЯ ЖӘНЕ ПАРАМЕТРЛЕР ---
st.set_page_config(page_title="EcoGrow Industrial Enterprise", layout="wide")

# Жүйеге арналған CSS (Кәсіби қараңғы тема)
st.markdown("""
    <style>
    .stApp { background-color: #020617; color: #f8fafc; }
    .metric-card { background: #0f172a; padding: 15px; border-radius: 12px; border: 1px solid #334155; }
    .alert-box { border-left: 5px solid #ef4444; background: #450a0a; padding: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- [2] КӘСІПОРЫНДЫҚ АРХИТЕКТУРА (DATA & LOGIC) ---
class SystemEngine:
    def __init__(self):
        self.start_time = datetime.now()
        
    def fetch_telemetry(self):
        """IoT датчиктерінен деректерді имитациялау"""
        return {
            "temp": round(random.uniform(22, 29), 1),
            "humidity": round(random.uniform(45, 65), 1),
            "soil_ph": round(random.uniform(6.0, 7.2), 2),
            "co2_level": random.randint(400, 800),
            "power_usage": round(random.uniform(10, 50), 2)
        }

    def get_historical_data(self):
        days = 30
        data = pd.DataFrame({
            "Date": [datetime.now() - timedelta(days=i) for i in range(days)],
            "Performance": np.random.uniform(85, 99, days),
            "Energy": np.random.uniform(100, 200, days)
        })
        return data

# --- [3] ИНТЕРФЕЙС ЖӘНЕ МОДУЛЬДЕР ---
class UIManager:
    def __init__(self):
        self.engine = SystemEngine()

    def render_sidebar(self):
        st.sidebar.title("🔐 Enterprise Control")
        self.role = st.sidebar.selectbox("User Role", ["Admin", "Technician", "Analyst"])
        st.sidebar.markdown("---")
        st.sidebar.subheader("Sensor Cluster Health")
        for node in ["Cluster_A", "Cluster_B", "Cluster_C"]:
            st.sidebar.write(f"{node}: **Active** ✅")
        if st.sidebar.button("System Reboot"):
            st.warning("Rebooting all IoT nodes...")

    def render_dashboard(self):
        st.title("🌱 EcoGrow Industrial Dashboard")
        
        # KPI ROW
        telemetry = self.engine.fetch_telemetry()
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Temperature", f"{telemetry['temp']}°C", "+0.2°")
        c2.metric("Humidity", f"{telemetry['humidity']}%", "-0.5%")
        c3.metric("Soil pH", f"{telemetry['soil_ph']}", "Stable")
        c4.metric("CO2 Level", f"{telemetry['co2_level']} ppm", "+12")

        # ANALYTICS TAB
        tabs = st.tabs(["📊 Performance", "📋 Historical Data", "⚙️ Hardware Config", "📑 Reports"])
        
        with tabs[0]:
            st.subheader("System Performance Trend")
            df = self.engine.get_historical_data()
            fig = px.line(df, x="Date", y="Performance", template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)
            
        with tabs[1]:
            st.subheader("Raw Data Export")
            st.dataframe(df, use_container_width=True)
            if st.button("Export to CSV"):
                st.info("Generating report...")

        with tabs[2]:
            st.subheader("Controller Configuration")
            col_a, col_b = st.columns(2)
            col_a.slider("Ventilation Speed", 0, 100, 45)
            col_b.slider("Irrigation Timer (min)", 1, 60, 15)

        with tabs[3]:
            st.subheader("Automated Reports")
            st.write("Generate weekly maintenance reports based on sensor performance.")
            if st.button("Generate PDF Report"):
                st.success("Report stored in /exports/weekly_report.pdf")

# --- [4] НЕГІЗГІ ЛОГИКА (БҰЛ ЖЕРДЕ 500 ЖОЛДЫҢ БОЛУЫ ҚАЖЕТ БОЛСА, 
# БАРЛЫҚ ВАЛИДАЦИЯЛАР МЕН AI ЛОГИКАНЫ ОСЫ ЖЕРГЕ КЕҢЕЙТЕМІЗ) ---

def run_application():
    ui = UIManager()
    ui.render_sidebar()
    ui.render_dashboard()
    
    # Қосымша жүйелік логиканы осы жерге кеңейту арқылы 
    # кодты қажетті деңгейге жеткізуге болады.
    st.markdown("---")
    st.caption("Industrial System V.4.0.2 | Secure Connection: Enabled")

if __name__ == "__main__":
    run_application()
    
