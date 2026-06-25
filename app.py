import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# 1. ПЛАТФОРМА БАПТАУЛАРЫ
st.set_page_config(page_title="EcoGrow AI | Dark Mode", layout="wide", page_icon="🌱")

# Көзді ауыртпайтын "Soft Dark" интерфейс стилі
st.markdown("""
    <style>
    /* Фонды жұмсақ күңгірт түске ауыстыру */
    .stApp { background-color: #0f172a; color: #e2e8f0; }
    
    /* Баннер дизайны */
    .hero-banner {
        background: linear-gradient(135deg, #020617 0%, #0f172a 100%);
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #1e293b;
        color: #f8fafc;
        margin-bottom: 25px;
    }
    
    /* Карточкалар дизайны (Күңгірт түс) */
    .custom-card {
        background: #1e293b;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #334155;
        color: #f1f5f9;
        margin-bottom: 20px;
    }
    
    /* Мәтіндер мен тақырыптар */
    h1, h2, h3, p { color: #f8fafc !important; }
    
    /* Метрикалар */
    div[data-testid="stMetric"] {
        background: #1e293b !important;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #334155;
    }
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; }
    
    /* Батырмалар */
    .stButton>button {
        background-color: #0284c7 !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. ДЕРЕКТЕР
@st.cache_data(ttl=15)
def get_data():
    return pd.DataFrame({
        "Уақыт": [f"{i}:00" for i in range(1, 13)],
        "Температура (°C)": np.random.uniform(22, 26, 12),
        "Ылғалдылық (%)": np.random.uniform(40, 60, 12)
    })

# ==========================================
# 🗺️ ЖОҒАРҒЫ БАННЕР
# ==========================================
st.markdown("""
    <div class='hero-banner'>
        <h1 style='margin:0;'>🌱 EcoGrow AI Platform</h1>
        <p style='color:#94a3b8;'>Интеллектуалды агро-басқару жүйесі (Dark Mode)</p>
    </div>
""", unsafe_allow_html=True)

# 🗂️ НАВИГАЦИЯ
tabs = st.tabs(["🏠 Басты бет", "📊 IoT Дашборд", "⚙️ Баптаулар"])

# 1-ТАБ
with tabs[0]:
    st.markdown("<div class='custom-card'><h3>Жүйеге қош келдіңіз</h3><p>Бұл платформа сіздің жылыжайыңызды 24/7 бақылауда ұстайды.</p></div>", unsafe_allow_html=True)

# 2-ТАБ
with tabs[1]:
    df = get_data()
    m1, m2 = st.columns(2)
    m1.metric("Температура", "24.5 °C")
    m2.metric("Ылғалдылық", "52 %")
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    fig = px.line(df, x="Уақыт", y="Температура (°C)", template="plotly_dark")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 3-ТАБ
with tabs[2]:
    st.markdown("<div class='custom-card'><h3>Жүйелік баптаулар</h3>", unsafe_allow_html=True)
    st.slider("Температура лимиті:", 20, 35, 27)
    st.button("Сақтау")
    st.markdown("</div>", unsafe_allow_html=True)
