import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime
import google.generativeai as genai

# 1. ПЛАТФОРМА БАПТАУЛАРЫ
st.set_page_config(page_title="EcoGrow AI", layout="wide", page_icon="🌱")

# Gemini API қауіпсіз баптау
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    genai.configure(api_key="СІЗДІҢ_GEMINI_API_КІЛТІҢІЗ")

# Сәнді және тұрақты дизайнға арналған CSS (Текст түстері түзетілді)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #f4f6f8;
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    /* Басты жасыл баннер */
    .hero-banner {
        background: linear-gradient(135deg, #064e3b 0%, #115e59 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(6, 78, 59, 0.15);
    }
    
    /* Ақ ақылды карточкалар */
    .custom-card {
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    
    /* Батырмалар стилі */
    .stButton>button {
        background-color: #0f766e !important;
        color: white !important;
        border-radius: 10px !important;
        border: none !important;
        font-weight: 600 !important;
        padding: 10px 20px !important;
        width: 100%;
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

# Датчик деректері
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
# 🗺️ БАСТЫ ЖАСЫЛ БАННЕР
# ==========================================
st.markdown("""
    <div class='hero-banner'>
        <div style='display: flex; align-items: center; gap: 20px;'>
            <span style='font-size: 40px;'>🌱</span>
            <div>
                <h1 style='margin:0; font-size: 28px; font-weight:800; color: white;'>EcoGrow AI Platform</h1>
                <p style='margin:5px 0 0 0; font-size:14px; color:#a7f3d0;'>Бұлттық IoT және Интеллектуалды Жылыжай Басқару Жүйесі</p>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 🗂️ НАВИГАЦИЯ: СЕНІМДІ ТАБТАР ЖҮЙЕСІ (ТҮЗЕТІЛДІ)
# ==========================================
# Мәзірді бұзылмайтын ресми st.tabs жүйесіне ауыстырдық
if st.session_state.logged_in:
    tabs = st.tabs(["🏠 Басты бет", "📊 IoT Бақылау панелі", "⚙️ Жүйелік баптаулар", "📞 Сату бөлімі"])
else:
    tabs = st.tabs(["🏠 Басты бет", "🔐 Платформаға кіру", "📞 Сату бөлімі"])

# 🌐 Сол жақ сидбарды таза ұстау
st.sidebar.markdown("### 🖥️ Жүйе күйі")
st.sidebar.info("• Сервер: AWS Cloud\n• База: Firebase Realtime\n• Нұсқа: MVP 3.0 Stable")
if st.session_state.logged_in:
    st.sidebar.success(f"👤 Пайдаланушы: {st.session_state.username}")
    if st.sidebar.button("🚪 Жүйеден шығу"):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# 🏠 1-ТАБ: БАСТЫ БЕТ
# ==========================================
with tabs[0]:
    col1, col2 = st.columns([1.4, 1])
    with col1:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.header("Жылыжай бизнесін автоматтандыру")
        st.write("EcoGrow AI — топырақ пен ауаның күйін нақты уақытта талдап, суару, желдету жүйелерін адамның қатысуынсыз автоматты басқаратын өндірістік IoT экожүйесі.")
        st.markdown("""
        * **🎯 Нақты телеметрия:** Датчик көрсеткіштерін қашықтан бақылау.
        * **💧 Ресурстарды үнемдеу:** Су мен электр энергиясын 40%-ға дейін үнемдеу.
        * **🤖 AI-Агроном:** Gemini үлгісіне негізделген қазақша кәсіби кеңесші.
        """)
        st.markdown("</div>", unsafe_allow_html=True)
    with col2:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=500", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🔐 2-ТАБ: КІРУ НЕМЕСЕ БАҚЫЛАУ ПАНЕЛІ
# ==========================================
if not st.session_state.logged_in:
    with tabs[1]: # Тіркелу беті
        col_c, _ = st.columns([1, 1])
        with col_c:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.subheader("🔐 Жүйеге кіру")
            u_name = st.text_input("Логин немесе Email:", key="user_inp")
            u_pass = st.text_input("Құпия сөз:", type="password", key="pass_inp")
            if st.button("Платформаға кіру"):
                if u_name and u_pass:
                    st.session_state.logged_in = True
                    st.session_state.username = u_name
                    st.success("Сәтті кірдіңіз! Енді көрші '📊 IoT Бақылау панелі' табы ашылды.")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("Өрістерді толтырыңыз.")
            st.markdown("</div>", unsafe_allow_html=True)
else:
    # Егер кіріп тұрса, Дашборд ашылады
    with tabs[1]:
        st.markdown("### 📊 Нақты уақыттағы IoT Дашборды")
        df = get_live_data()
        t_now = round(df["Температура (°C)"].iloc[-1], 1)
        h_now = round(df["Ылғалдылық (%)"].iloc[-1], 1)
        s_now = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

        # 3 Көрнекі Метрика
        m1, m2, m3 = st.columns(3)
        t_status = "⚠️ Жоғары" if t_now > st.session_state.max_temp else "Қалыпты"
        m1.metric(label="🌡️ Температура", value=f"{t_now} °C", delta=t_status, delta_color="inverse" if "⚠️" in t_status else "normal")
        m2.metric(label="💧 Ауа ылғалдылығы", value=f"{h_now} %")
        s_status = "🚨 Құрғақ" if s_now < st.session_state.min_soil else "Жеткілікті"
        m3.metric(label="🪴 Топырақ ылғалдылығы", value=f"{s_now} %", delta=s_status, delta_color="inverse" if "🚨" in s_status else "normal")

        st.markdown("<br>", unsafe_allow_html=True)

        col_g, col_ctrl = st.columns([2, 1])
        with col_g:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            fig = px.line(df, x="Уақыт", y="Температура (°C)", title="Микроклимат өзгерісі", markers=True, color_discrete_sequence=['#0f766e'])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_ctrl:
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.subheader("⚙️ Реле статусы")
            st.write(f"💨 **Желдеткіш:** {'🟢 ҚОСУЛЫ' if t_now > st.session_state.max_temp else '🔴 ӨШІРУЛІ'}")
            st.write(f"🚰 **Помпа:** {'🟢 ҚОСУЛЫ' if s_now < st.session_state.min_soil else '🔴 ӨШІРУЛІ'}")
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.subheader("🧠 AI Кеңес")
            if st.button("AI Есеп алу"):
                st.info("AI: Жылыжайдағы көрсеткіштер тұрақты. Автоматты суару оңтайландырылды.")
            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ⚙️ 3-ТАБ: БАПТАУЛАР (ЕГЕР КІРГЕН БОЛСА)
# ==========================================
if st.session_state.logged_in:
    with tabs[2]:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.header("⚙️ Контроллер шектерін баптау")
        st.session_state.max_temp = st.slider("Макс. температура (°C):", 20.0, 35.0, st.session_state.max_temp, 0.5)
        st.session_state.min_soil = st.slider("Мин. топырақ ылғалдылығы (%):", 15.0, 60.0, st.session_state.min_soil, 1.0)
        st.success("Баптаулар IoT модуліне жіберілді.")
        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[3]: # Контактілер
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.header("📞 Сату бөлімімен байланыс")
        with st.form("contact"):
            st.text_input("Атыңыз:")
            st.text_input("Телефон:")
            if st.form_submit_button("Жіберу"):
                st.success("Тапсырыс қабылданды!")
        st.markdown("</div>", unsafe_allow_html=True)
else:
    with tabs[2]: # Қонақтар үшін контактілер соңғы табта
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.header("📞 Сату бөлімімен байланыс")
        with st.form("contact_guest"):
            st.text_input("Атыңыз:")
            st.text_input("Телефон:")
            if st.form_submit_button("Жіберу"):
                st.success("Тапсырыс қабылданды!")
        st.markdown("</div>", unsafe_allow_html=True)

# Төменгі жазу
st.markdown("<hr><center style='color: #64748b; font-size: 12px;'>© 2026 EcoGrow AI. Тұрақты әрі таза UI нұсқасы v3.0</center>", unsafe_allow_html=True)
