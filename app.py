import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import hashlib
import random  # <--- Осы жол міндетті түрде болуы керек!

# --- [1] АРХИТЕКТУРА ЖӘНЕ CONFIG ---
st.set_page_config(page_title="EcoGrow Industrial OS", layout="wide")

# Қауіпсіздік және Аутентификация
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state.password_correct = False
    if not st.session_state.password_correct:
        st.subheader("🔐 Кіру жүйесі")
        pwd = st.text_input("Құпия сөзді енгізіңіз:", type="password")
        if st.button("Кіру"):
            if pwd == "admin123":
                st.session_state.password_correct = True
                st.rerun()
            else:
                st.error("Қате құпия сөз!")
        return False
    return True

# --- [2] ДЕРЕКТЕРДІ БАСҚАРУ ---
class DatabaseEngine:
    def get_logs(self):
        return pd.DataFrame({
            "Timestamp": [datetime.now() - timedelta(minutes=i) for i in range(20)],
            "Event": ["Pump_ON", "Vent_Speed_Up", "Sensor_Read", "Alert_Critical"] * 5,
            "Severity": ["Info", "Warning", "Info", "Critical"] * 5
        })

    def get_sensor_data(self):
        return {
            "temp": round(random.uniform(22, 28), 1),
            "hum": round(random.uniform(40, 60), 1),
            "soil": round(random.uniform(30, 50), 1),
            "co2": random.randint(400, 900)
        }

# --- [3] UI КОМПОНЕНТТЕРІ ---
def render_dashboard(db):
    st.title("🌱 EcoGrow Enterprise | Industrial Control OS")
    data = db.get_sensor_data()
    
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Температура", f"{data['temp']}°C", "0.2°")
    c2.metric("Ылғалдылық", f"{data['hum']}%", "-1.1%")
    c3.metric("Топырақ", f"{data['soil']}%", "Stable")
    c4.metric("CO2 Деңгейі", f"{data['co2']} ppm", "+5")
    
    st.markdown("---")
    
    t1, t2, t3, t4 = st.tabs(["📊 Live Data", "📈 Analytics", "⚠️ System Logs", "🤖 AI Auditor"])
    
    with t1:
        st.subheader("Нақты уақыттағы телеметрия")
        df = pd.DataFrame(np.random.randn(20, 3), columns=["Temp", "Hum", "Soil"])
        st.line_chart(df)
        
    with t2:
        st.subheader("Өнімділік тарихы")
        df_hist = pd.DataFrame({'Date': pd.date_range(start='1/1/2026', periods=10), 'Efficiency': np.random.uniform(80, 100, 10)})
        fig = px.bar(df_hist, x='Date', y='Efficiency', template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
        
    with t3:
        st.subheader("Жүйелік журналдар (Logs)")
        st.dataframe(db.get_logs(), use_container_width=True)
        
    with t4:
        st.subheader("AI Deep Learning Module")
        st.info("AI Анализ: Тұқым себу кезеңінде топырақ ылғалдылығын 5%-ға көтеру ұсынылады.")
        if st.button("AI есебін PDF ретінде экспорттау"):
            st.success("Report_2026.pdf дайындалды.")

# --- [4] НЕГІЗГІ ЛОГИКА ---
def main():
    if not check_password():
        return
    
    db = DatabaseEngine()
    
    st.sidebar.title("🛠️ Settings")
    st.sidebar.subheader("Active Modules")
    st.sidebar.checkbox("AI Predictor", value=True)
    st.sidebar.checkbox("Auto-Irrigation", value=True)
    
    render_dashboard(db)

if __name__ == "__main__":
    main()
