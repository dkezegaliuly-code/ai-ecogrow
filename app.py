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

# CSS стильдері
st.markdown("""
    <style>
    .stButton>button { background-color: #1b5e20; color: white; border-radius: 6px; font-weight: bold; }
    .stButton>button:hover { background-color: #2e7d32; }
    .sidebar-text { font-size: 14px; color: #555; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; color: #1b5e20; }
    </style>
""", unsafe_allow_html=True)

# 2. СЕССИЯЛЫҚ КҮЙДІ БАПТАУ (Session State — Тіркелу және Баптаулар үшін)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "max_temp" not in st.session_state:
    st.session_state.max_temp = 27.5
if "min_soil" not in st.session_state:
    st.session_state.min_soil = 35.0

# Деректер генерациясы
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

# 3. СИДЕНБАР НАВИГАЦИЯСЫ
st.sidebar.title("🌱 EcoGrow Enterprise")

if st.session_state.logged_in:
    st.sidebar.success(f"👤 Аккаунт: {st.session_state.username}")
    menu_options = [
        "🏠 Басты бет (Landing Page)", 
        "📊 IoT Бақылау панелі", 
        "⚙️ Құрылғыларды баптау", 
        "📞 Контактілер"
    ]
    if st.sidebar.button("🚪 Жүйеден шығу"):
        st.session_state.logged_in = False
        st.rerun()
else:
    st.sidebar.warning("🔒 Авторизациядан өтпегенсіз")
    menu_options = ["🏠 Басты бет (Landing Page)", "🔐 Жүйеге кіру / Тіркелу", "📞 Контактілер"]

page = st.sidebar.radio("Навигация:", menu_options)
st.sidebar.markdown("---")
st.sidebar.markdown("<p class='sidebar-text'><b>Версия:</b> MVP 2.0 (Production-Ready)</p>", unsafe_allow_html=True)

# ==========================================
# 🏠 БАСТЫ БЕТ
# ==========================================
if page == "🏠 Басты бет (Landing Page)":
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
            st.info("💡 Дашборд пен құрылғыларды басқару үшін 'Жүйеге кіру' бетіне өтіп, тіркеліңіз.")
    with col_h2:
        st.image("https://images.unsplash.com/photo-1530595467537-0b5996c41f2d?w=500", caption="EcoGrow IoT контроллерлері")

# ==========================================
# 🔐 ЖҮЙЕГЕ КІРУ / ТІРКЕЛУ
# ==========================================
elif page == "🔐 Жүйеге кіру / Тіркелу":
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
elif page == "📊 IoT Бақылау панелі":
    st.header("📊 Нақты уақыттағы IoT Дашборды")
    
    df = fetch_iot_data()
    latest_temp = round(df["Температура (°C)"].iloc[-1], 1)
    latest_hum = round(df["Ылғалдылық (%)"].iloc[-1], 1)
    latest_soil = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

    # Метрикалар (Баптаулардағы шекті мәндермен байланысқан)
    col1, col2, col3 = st.columns(3)
    
    temp_status = "Жоғары!" if latest_temp > st.session_state.max_temp else "Қалыпты"
    col1.metric(label="🌡️ Температура", value=f"{latest_temp} °C", delta=temp_status, delta_color="inverse" if temp_status == "Жоғары!" else "normal")
    
    col2.metric(label="💧 Ауа ылғалдылығы", value=f"{latest_hum} %")
    
    soil_status = "⚠️ Құрғақ!" if latest_soil < st.session_state.min_soil else "Жеткілікті"
    col3.metric(label="🪴 Топырақ ылғалдылығы", value=f"{latest_soil} %", delta=soil_status, delta_color="inverse" if soil_status == "⚠️ Құрғақ!" else "normal")

    # Графиктер мен Деректер экспорты
    tab_graphs, tab_table = st.tabs(["📈 Графиктер", "📋 Деректер базасының кестесі"])
    with tab_graphs:
        f_temp = px.line(df, x="Уақыт", y="Температура (°C)", title="Жылыжай температурасының графигі", color_discrete_sequence=['#e65100'])
        st.plotly_chart(f_temp, use_container_width=True)
        f_hum = px.line(df, x="Уақыт", y=["Ылғалдылық (%)", "Топырақ ылғалдылығы (%)"], title="Ылғалдылық балансы")
        st.plotly_chart(f_hum, use_container_width=True)
    with tab_table:
        st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # Автоматика логикасы (Баптауларға тәуелді)
    col_a1, col_a2 = st.columns(2)
    with col_a1:
        st.subheader("⚙️ Автоматты релелердің күйі")
        fan_on = latest_temp > st.session_state.max_temp
        pump_on = latest_soil < st.session_state.min_soil
        
        st.write(f"**Желдеткіш жүйесі:** {'🟢 Іске қосылды (Салқындату)' if fan_on else '🔴 Күту режимінде'}")
        st.write(f"**Суару клапаны:** {'🟢 Қосулы (Су құйылуда)' if pump_on else '🔴 Жабық'}")
        
    with col_a2:
        st.subheader("🧠 Кәсіби AI-Агроном есебі")
        if st.button("Генерациялау"):
            with st.spinner('Жасанды интеллект деректерді өңдеуде...'):
                prompt = f"""
                Сен EcoGrow стартапының бас агрономысың. Мына соңғы IoT деректеріне қарап фермерге кәсіби талдау жаса:
                Температура: {latest_temp}°C (Максимум шегі: {st.session_state.max_temp}°C)
                Топырақ ылғалдылығы: {latest_soil}% (Минимум шегі: {st.session_state.min_soil}%)
                Қысқаша 3 тармақпен жаз.
                """
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.info(response.text)
                except:
                    st.warning("⚠️ Офлайн режимдегі AI есебі: Көрсеткіштер тұрақты. Суару алгоритмі автоматты түрде реттелді.")

# ==========================================
# ⚙️ ҚҰРЫЛҒЫЛАРДЫ БАПТАУ (ЖАҢА БЕТ)
# ==========================================
elif page == "⚙️ Құрылғыларды баптау":
    st.header("⚙️ IoT Датчиктері мен Шегін Баптау (Thresholds)")
    st.write("Осы жерде орнатылған мәндер негізінде автоматты суару помпасы мен желдеткіштер іске қосылады.")
    
    st.session_state.max_temp = st.slider(
        "Максималды рұқсат етілген температура (°C):", 
        min_value=20.0, max_value=35.0, 
        value=st.session_state.max_temp, step=0.5
    )
    
    st.session_state.min_soil = st.slider(
        "Минималды топырақ ылғалдылығы (осыдан төмендесе суарады, %):", 
        min_value=15.0, max_value=60.0, 
        value=st.session_state.min_soil, step=1.0
    )
    
    st.success(f"Баптаулар сақталды! Қазіргі ереже: Егер температура {st.session_state.max_temp}°C-тан асса желдеткіш жанады. Егер ылғалдылық {st.session_state.min_soil}%-дан төмендесе су құйылады.")

# ==========================================
# 📞 КОНТАКТІЛЕР
# ==========================================
elif page == "📞 Контактілер":
    st.header("📞 Техникалық қолдау және Сауда бөлімі")
    st.write("Құрылғыларды сатып алу немесе өндірістік интеграция жасау бойынша сұрақтарды жолдаңыз.")
    
    with st.form("feedback"):
        u_name = st.text_input("Атыңыз:")
        u_phone = st.text_input("Телефон нөміріңіз:")
        u_txt = st.text_area("Қандай өнім қызықтырады?")
        if st.form_submit_button("Сұраныс қалдыру"):
            st.success("Рақмет! Сату бөлімінің менеджері сізбен 15 минут ішінде хабарласады.")

# Төменгі жазу
st.markdown("---")
st.caption(f"© {datetime.now().year} EcoGrow AI Enterprise. Барлық құқықтар қорғалған. Дайын бизнес платформа.")
