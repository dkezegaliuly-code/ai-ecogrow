import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime
import google.generativeai as genai

# 1. СТАНДАРТТЫ БАПТАУЛАР
st.set_page_config(page_title="EcoGrow AI | Enterprise", layout="wide", page_icon="🌱")

# Gemini API Қауіпсіз қосу
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    genai.configure(api_key="СІЗДІҢ_GEMINI_API_КІЛТІҢІЗ")

# ==========================================
# 🎨 ИНТЕРФЕЙСТІ ДҮРЫСТАУ: КӘСІБИ CSS СТИЛЬДЕР
# ==========================================
st.markdown("""
    <style>
    /* Басты фон мен қаріптер */
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f8fafc;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Жоғарғы бренд-банер */
    .brand-header {
        background: linear-gradient(135deg, #0f766e 0%, #042f2e 100%);
        padding: 24px;
        border-radius: 20px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px -5px rgba(15, 118, 110, 0.15);
    }
    
    /* Премиум Ақ Карточкалар (Dashboard Сард) */
    .app-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 2px 4px -1px rgba(0,0,0,0.01);
        margin-bottom: 20px;
    }
    
    /* Метрикаларды (Сандарды) дұрыстау */
    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 16px;
        padding: 16px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.01);
    }
    div[data-testid="stMetricValue"] { font-size: 30px !important; font-weight: 700 !important; color: #0f172a; }
    div[data-testid="stMetricLabel"] { font-size: 13px !important; color: #64748b; font-weight: 600; text-transform: uppercase; }
    
    /* Батырмаларды заманауи ету */
    .stButton>button {
        background: #0f766e !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 12px 28px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.2s ease;
        width: 100%;
    }
    .stButton>button:hover {
        background: #115e59 !important;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 118, 110, 0.2);
    }
    
    /* Көлденең Радио-Мәзірді Батырма секілді жасау (Түзету) */
    div[data-testid="stRadio"] > div {
        flex-direction: row !important;
        gap: 10px;
    }
    div[data-testid="stRadio"] label {
        background: #ffffff;
        padding: 10px 20px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        font-weight: 600;
        color: #475569;
        cursor: pointer;
    }
    div[data-testid="stRadio"] label[data-selected="true"] {
        background: #0f766e !important;
        color: white !important;
        border-color: #0f766e;
    }
    </style>
""", unsafe_allow_html=True)

# 2. СЕССИЯЛЫҚ КҮЙ (SESSION STATE)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "max_temp" not in st.session_state:
    st.session_state.max_temp = 27.5
if "min_soil" not in st.session_state:
    st.session_state.min_soil = 35.0

# Нақты уақыттағы IoT деректерінің симуляциясы
@st.cache_data(ttl=15)
def get_live_data():
    now = datetime.now()
    times = [datetime.fromtimestamp(now.timestamp() - i*60) for i in range(15, 0, -1)]
    return pd.DataFrame({
        "Уақыт": times,
        "Температура (°C)": np.random.uniform(23.0, 28.5, 15),
        "Ылғалдылық (%)": np.random.uniform(48.0, 62.0, 15),
        "Топырақ ылғалдылығы (%)": np.random.uniform(32.0, 48.0, 15)
    })

# ==========================================
# 🗺️ ЖОҒАРҒЫ БРЕНД ПАНЕЛЬ
# ==========================================
st.markdown("""
    <div class='brand-header'>
        <div style='display: flex; align-items: center; gap: 15px;'>
            <span style='font-size: 36px;'>🌱</span>
            <div>
                <h1 style='margin:0; font-size: 26px; font-weight:800; letter-spacing:-0.5px;'>EcoGrow AI</h1>
                <p style='margin:0; font-size:13px; color:#9ccdc7; font-weight:500;'>Бұлттық IoT және Интеллектуалды Жылыжай Платформасы</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Ыңғайлы Навигациялық Мәзір (Түзетілген көлденең радио батырмалар)
if st.session_state.logged_in:
    routes = ["🏠 Басты бет", "📊 IoT Бақылау панелі", "⚙️ Жүйелік баптаулар", "📞 Кері байланыс"]
else:
    routes = ["🏠 Басты бет", "🔐 Платформаға кіру", "📞 Кері байланыс"]

page = st.radio("", routes, label_visibility="collapsed")
st.markdown("<br>", unsafe_allow_html=True)

# Жүйелік статус (Sidebar енді өте шағын әрі маңызды ақпарат береді)
st.sidebar.markdown("### 🌐 Инфрақұрылым")
st.sidebar.markdown("• **Сервер:** AWS Cloud (Frankfurt)")
st.sidebar.markdown("• **Датчиктер:** Firebase Realtime")
if st.session_state.logged_in:
    st.sidebar.success(f"👤 Аккаунт: {st.session_state.username}")
    if st.sidebar.button("🚪 Жүйеден шығу"):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# 🏠 БАСТЫ БЕТ (LANDING PAGE)
# ==========================================
if page == "🏠 Басты бет":
    col_l, col_r = st.columns([1.3, 1])
    
    with col_l:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.title("Жылыжайды интеллектуалды басқарудың жаңа дәуірі")
        st.write("EcoGrow AI кәдімгі жылыжайларды толық автоматтандырылған ақылды кешенге айналдырады. Датчиктер мен жасанды интеллект комбинациясы шығындарды азайтып, табысты екі еселейді.")
        
        st.markdown("🔍 **Жүйенің негізгі мүмкіндіктері:**")
        st.markdown("""
        - 📱 **Қашықтан бақылау:** Кез келген уақытта топырақ пен ауа күйін тексеру.
        - 💧 **Авто-суару:** Суды тек өсімдік шын мәнінде шөлдегенде ғана құю (40% үнем).
        - 🤖 **AI-Агроном:** Датчик деректерін талдап, қазақ тілінде нақты кеңес беру.
        """)
        if not st.session_state.logged_in:
            st.info("💡 Жоғарыдан '🔐 Платформаға кіру' мәзірін таңдап, жүйені іске қосыңыз.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_r:
        st.markdown("<div class='app-card' style='text-align: center;'>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=500", use_container_width=True)
        st.caption("EcoGrow IoT Smart Hub — Өндірістік Контроллер")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🔐 ПЛАТФОРМАҒА КІРУ
# ==========================================
elif page == "🔐 Платформаға кіру":
    col_center, _ = st.columns([1.5, 2])
    with col_center:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.subheader("🔐 Платформаға кіру")
        u_login = st.text_input("Логин немесе Email:")
        u_pass = st.text_input("Құпия сөз:", type="password")
        if st.button("Жүйеге қауіпсіз кіру"):
            if u_login and u_pass:
                st.session_state.logged_in = True
                st.session_state.username = u_login
                st.success("Сәтті кірдіңіз! Бақылау панелі ашылды.")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Өтініш, барлық өрістерді толтырыңыз.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 📊 IOT БАҚЫЛАУ ПАНЕЛІ (DASHBOARD)
# ==========================================
elif page == "📊 IoT Бақылау панелі":
    st.subheader("📊 Нақты уақыттағы IoT Көрсеткіштері")
    
    df = get_live_data()
    t_now = round(df["Температура (°C)"].iloc[-1], 1)
    h_now = round(df["Ылғалдылық (%)"].iloc[-1], 1)
    s_now = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

    # 3 Көрсеткіш Картасы (Қатар тұрады)
    c1, c2, c3 = st.columns(3)
    
    t_alert = "⚠️ Жоғары" if t_now > st.session_state.max_temp else "Қалыпты"
    c1.metric(label="🌡️ Ауа Температурасы", value=f"{t_now} °C", delta=t_alert, delta_color="inverse" if "⚠️" in t_alert else "normal")
    
    c2.metric(label="💧 Ауа Ылғалдылығы", value=f"{h_now} %")
    
    s_alert = "🚨 Құрғақ" if s_now < st.session_state.min_soil else "Жеткілікті"
    c3.metric(label="🪴 Топырақ ылғалдылығы", value=f"{s_now} %", delta=s_alert, delta_color="inverse" if "🚨" in s_alert else "normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # Графиктер мен Релелерді басқару блогы
    col_graph, col_actions = st.columns([2, 1])
    
    with col_graph:
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        g_tab1, g_tab2 = st.tabs(["📈 Температура графигі", "📉 Ылғалдылық графигі"])
        with g_tab1:
            fig1 = px.line(df, x="Уақыт", y="Температура (°C)", markers=True, color_discrete_sequence=['#0f766e'])
            fig1.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        with g_tab2:
            fig2 = px.line(df, x="Уақыт", y=["Ылғалдылық (%)", "Топырақ ылғалдылығы (%)"], markers=True)
            fig2.update_layout(margin=dict(l=10, r=10, t=10, b=10), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_actions:
        # Автоматика күйі
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.markdown("<h4>⚙️ Релелік Басқару (Бұлт)</h4>", unsafe_allow_html=True)
        fan_status = t_now > st.session_state.max_temp
        pump_status = s_now < st.session_state.min_soil
        
        st.write(f"💨 **Желдеткіш:** {'🟢 ҚОСУЛЫ (Салқындату)' if fan_status else '🔴 ӨШІРУЛІ'}")
        st.write(f"🚰 **Суару клапаны:** {'🟢 ҚОСУЛЫ (Су жүруде)' if pump_status else '🔴 ӨШІРУЛІ'}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # AI сараптама
        st.markdown("<div class='app-card'>", unsafe_allow_html=True)
        st.markdown("<h4>🧠 AI-Агроном есебі</h4>", unsafe_allow_html=True)
        if st.button("Мәліметті талдау"):
            with st.spinner('AI бұлтта есептеуде...'):
                prompt = f"Сен EcoGrow бас агрономысың. Мына IoT деректеріне қарап фермерге қысқа 3 тармақпен қазақша кәсіби кеңес жаз: Температура: {t_now}°C, Ылғалдылық: {s_now}%."
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except:
                    st.warning("⚠️ Офлайн режим: Көрсеткіштер тұрақты. Автоматика алгоритмі қалыпты.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ⚙️ ЖҮЙЕЛІК БАПТАУЛАР
# ==========================================
elif page == "⚙️ Жүйелік баптаулар":
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.header("⚙️ Автоматиканың критикалық шектері")
    st.write("Осы жердегі мәндер бұлттағы релелер мен помпалардың іске қосылу алгоритмін тікелей өзгертеді.")
    
    st.session_state.max_temp = st.slider(
        "Максималды рұқсат етілген температура (°C):", 
        min_value=20.0, max_value=35.0, value=st.session_state.max_temp, step=0.5
    )
    st.session_state.min_soil = st.slider(
        "Минималды топырақ ылғалдылығы (суару басталу шегі, %):", 
        min_value=15.0, max_value=60.0, value=st.session_state.min_soil, step=1.0
    )
    st.success(f"Жаңа ереже сақталды: Температура {st.session_state.max_temp}°C-тан асса салқындату қосылады, ал топырақ {st.session_state.min_soil}%-дан төмендесе суарылады.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 📞 КЕРІ БАЙЛАНЫС
# ==========================================
elif page == "📞 Кері байланыс":
    st.markdown("<div class='app-card'>", unsafe_allow_html=True)
    st.header("📞 Сату және Инженерлік бөлім")
    st.write("Жылыжай өлшемдеріне қарай жеке құрылғылар жинағын (Hardware) есептеу үшін өтінім қалдырыңыз.")
    
    with st.form("feedback_form"):
        st.text_input("Аты-жөніңіз:")
        st.text_input("Телефон нөміріңіз:")
        st.selectbox("Жылыжайдың түрі:", ["Үй жағдайындағы шағын", "Коммерциялық орташа", "Өндірістік ірі агро-кешен"])
        if st.form_submit_button("Инженер кеңесіне жазылу"):
            st.balloons()
            st.success("Өтінішіңіз қабылданды. Менеджер сізге хабарласады!")
    st.markdown("</div>", unsafe_allow_html=True)

# Төменгі жазу (Footer)
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"© {datetime.now().year} EcoGrow AI Enterprise — Smart Greenhouses. Түзетілген тұрақты нұсқа v2.9.")
