import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime
import google.generativeai as genai

# 1. БЕТТІҢ БАПТАУЛАРЫ
st.set_page_config(page_title="AI-EcoGrow | Enterprise IoT", layout="wide", page_icon="🌱")

# Gemini API баптау
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    genai.configure(api_key="СІЗДІҢ_GEMINI_API_КІЛТІҢІЗ")

# Жақсартылған CSS стильдері (Жоғарғы мәзір мен батырмалар дизайны)
st.markdown("""
    <style>
    .stButton>button { background-color: #1b5e20; color: white; border-radius: 6px; font-weight: bold; }
    .stButton>button:hover { background-color: #2e7d32; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #1b5e20; }
    /* Жоғарғы басты блокты безендіру */
    .nav-container { background-color: #f1f8e9; padding: 10px; border-radius: 8px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# 2. СЕССИЯЛЫҚ КҮЙДІ БАПТАУ
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "max_temp" not in st.session_state:
    st.session_state.max_temp = 27.5
if "min_soil" not in st.session_state:
    st.session_state.min_soil = 35.0

# Деректерді бұлттан тарту симуляциясы
@st.cache_data(ttl=30)
def fetch_iot_data():
    now = datetime.now()
    times = [datetime.fromtimestamp(now.timestamp() - i*60) for i in range(20, 0, -1)]
    return pd.DataFrame({
        "Уақыт": times,
        "Температура (°C)": np.random.uniform(22.0, 29.0, 20),
        "Ылғалдылық (%)": np.random.uniform(45.0, 65.0, 20),
        "Топырақ ылғалдылығы (%)": np.random.uniform(30.0, 55.0, 20)
    })

# ==========================================
# 🗺️ ЖОҒАРҒЫ НАВИГАЦИЯ ПАНЕЛІ (КӨЗГЕ ЫҢҒАЙЛЫ)
# ==========================================
st.markdown("<div class='nav-container'>", unsafe_allow_html=True)
col_logo, col_nav, col_auth = st.columns([1, 3, 1])

with col_logo:
    st.subheader("🌱 EcoGrow")

# Пайдаланушының күйіне байланысты мәзір нұсқалары
if st.session_state.logged_in:
    nav_options = ["🏠 Басты бет", "📊 IoT Дашборд", "⚙️ Баптаулар", "📞 Контактілер"]
else:
    nav_options = ["🏠 Басты бет", "🔐 Кіру / Тіркелу", "📞 Контактілер"]

with col_nav:
    # Жоғарыдағы көлденең заманауи селектор
    page = st.segmented_control("Мәзір таңдаңыз:", nav_options, default="🏠 Басты бет")

with col_auth:
    if st.session_state.logged_in:
        st.write(f"👤 **{st.session_state.username}**")
        if st.button("🚪 Шығу", key="logout_btn"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        st.write("🔒 Қонақ режимі")
st.markdown("</div>", unsafe_allow_html=True)

# Сидбар енді тек көмекші ақпарат үшін ғана жасырын тұрады
st.sidebar.markdown("### 🤖 Жүйе статусы")
st.sidebar.success("Сервер: Онлайн (Бұлтты)")
st.sidebar.info("MVP v2.5 | AI-Incubator Wizards")

# ==========================================
# 🏠 БАСТЫ БЕТ
# ==========================================
if page == "🏠 Басты бет":
    st.title("🚀 Ауыл шаруашылығын AI-мен автоматтандыру")
    st.markdown("### Өндірістік IoT шешімдері мен интеллектуалды агро-аналитика")
    
    col_h1, col_h2 = st.columns([2, 1])
    with col_h1:
        st.write("EcoGrow AI — бұл заманауи фермерлерге арналған кешенді экожүйе. Біз жылыжайларды толық автоматты режимге көшіріп, адам факторынан болатын шығындарды нөлге теңестіреміз.")
        st.markdown("""
        * **Нақты уақыттағы бақылау:** Әлемнің кез келген нүктесінен жылыжай күйін көру.
        * **Ақылды суару:** Топырақ датчиктерінің көрсеткішіне негізделген дәл суару (суды 40%-ға дейін үнемдеу).
        * **LLM Агроном:** Gemini негізіндегі AI сізге күн сайын есеп дайындап береді.
        """)
        if not st.session_state.logged_in:
            st.info("💡 Жоғарғы мәзірден '🔐 Кіру / Тіркелу' батырмасын басып, дашбордты іске қосыңыз.")
    with col_h2:
        st.image("https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=500", caption="EcoGrow IoT контроллерлері")

# ==========================================
# 🔐 ЖҮЙЕГЕ КІРУ / ТІРКЕЛУ
# ==========================================
elif page == "🔐 Кіру / Тіркелу":
    st.header("🔐 Платформаға кіру")
    tab_login, tab_register = st.tabs(["🔑 Кіру", "📝 Жаңа аккаунт ашу"])
    
    with tab_login:
        login_user = st.text_input("Логин (немесе Email):", key="log_user")
        login_pass = st.text_input("Құпия сөз:", type="password", key="log_pass")
        if st.button("Кіру"):
            if login_user and login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("Жүйеге сәтті кірдіңіз!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Өрістерді толтырыңыз!")
                
    with tab_register:
        reg_user = st.text_input("Жаңа логин ойлап табыңыз:", key="reg_user")
        reg_email = st.text_input("Email:")
        reg_pass = st.text_input("Құпия сөз жазыңыз:", type="password", key="reg_pass")
        if st.button("Тіркелу"):
            if reg_user and reg_email and reg_pass:
                st.success("Аккаунт сәтті жасалды! Енді 'Кіру' бөлімі арқылы өтіңіз.")
            else:
                st.error("Барлық мәліметті толтырыңыз.")

# ==========================================
# 📊 IOT БАҚЫЛАУ ПАНЕЛІ (DASHBOARD)
# ==========================================
elif page == "📊 IoT Дашборд":
    st.header("📊 Нақты уақыттағы IoT Дашборды")
    
    df = fetch_iot_data()
    latest_temp = round(df["Температура (°C)"].iloc[-1], 1)
    latest_hum = round(df["Ылғалдылық (%)"].iloc[-1], 1)
    latest_soil = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

    col1, col2, col3 = st.columns(3)
    temp_status = "Жоғары!" if latest_temp > st.session_state.max_temp else "Қалыпты"
    col1.metric(label="🌡️ Температура", value=f"{latest_temp} °C", delta=temp_status, delta_color="inverse" if temp_status == "Жоғары!" else "normal")
    col2.metric(label="💧 Ауа ылғалдылығы", value=f"{latest_hum} %")
    soil_status = "⚠️ Құрғақ!" if latest_soil < st.session_state.min_soil else "Жеткілікті"
    col3.metric(label="🪴 Топырақ ылғалдылығы", value=f"{latest_soil} %", delta=soil_status, delta_color="inverse" if soil_status == "⚠️ Құрғақ!" else "normal")

    tab_graphs, tab_table = st.tabs(["📈 Динамикалық Графиктер", "📋 Кестелік деректер"])
    with tab_graphs:
        f_temp = px.line(df, x="Уақыт", y="Температура (°C)", title="Жылыжай температурасы", color_discrete_sequence=['#e65100'])
        st.plotly_chart(f_temp, use_container_width=True)
        f_hum = px.line(df, x="Уақыт", y=["Ылғалдылық (%)", "Топырақ ылғалдылығы (%)"], title="Ылғалдылық деңгейлері")
        st.plotly_chart(f_hum, use_container_width=True)
    with tab_table:
        st.dataframe(df, use_container_width=True)

    st.markdown("---")

    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.subheader("⚙️ Автоматты релелердің күйі")
        fan_on = latest_temp > st.session_state.max_temp
        pump_on = latest_soil < st.session_state.min_soil
        st.write(f"**Желдеткіш жүйесі:** {'🟢 Іске қосылды' if fan_on else '🔴 Күту режимінде'}")
        st.write(f"**Суару клапаны:** {'🟢 Қосулы (Су құйылуда)' if pump_on else '🔴 Жабық'}")
        
    with col_a2:
        st.subheader("🧠 Кәсіби AI-Агроном есебі")
        if st.button("Есепті генерациялау"):
            with st.spinner('AI деректерді талдауда...'):
                prompt = f"Сен EcoGrow стартапының бас агрономысың. Мына соңғы IoT деректеріне қарап фермерге қысқа 3 тармақпен қазақша кеңес жаз: Температура: {latest_temp}°C, Ылғалдылық: {latest_soil}%."
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.info(response.text)
                except:
                    st.warning("⚠️ Офлайн режим: Көрсеткіштер тұрақты. Суару алгоритмі жұмыс істеп тұр.")

# ==========================================
# ⚙️ ҚҰРЫЛҒЫЛАРДЫ БАПТАУ
# ==========================================
elif page == "⚙️ Баптаулар":
    st.header("⚙️ IoT Датчиктері мен Шегін Баптау (Thresholds)")
    st.write("Осы жерде орнатылған мәндер негізінде автоматты суару помпасы мен желдеткіштер іске қосылады.")
    
    st.session_state.max_temp = st.slider(
        "Максималды рұқсат етілген температура (°C):", 
        min_value=20.0, max_value=35.0, value=st.session_state.max_temp, step=0.5
    )
    st.session_state.min_soil = st.slider(
        "Минималды топырақ ылғалдылығы (%):", 
        min_value=15.0, max_value=60.0, value=st.session_state.min_soil, step=1.0
    )
    st.success(f"Баптаулар жаңартылды! Критикалық температура: {st.session_state.max_temp}°C, Критикалық ылғалдылық: {st.session_state.min_soil}%.")

# ==========================================
# 📞 КОНТАКТІЛЕР
# ==========================================
elif page == "📞 Контактілер":
    st.header("📞 Техникалық қолдау және Сауда бөлімі")
    with st.form("feedback"):
        u_name = st.text_input("Атыңыз:")
        u_phone = st.text_input("Телефон нөміріңіз:")
        u_txt = st.text_area("Қандай көмек немесе өнім қажет?")
        if st.form_submit_button("Сұраныс қалдыру"):
            st.success("Рақмет! Менеджерлер сізбен жақын арада байланысады.")

# Төменгі жазу (Footer)
st.markdown("---")
st.caption(f"© {datetime.now().year} EcoGrow AI Enterprise. Барлық құқықтар қорғалған. Навигация жаңартылды.")
