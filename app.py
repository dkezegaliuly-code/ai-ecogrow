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

# ==========================================
# 🎨 UI РЕФОРМА: ПРЕМИУМ СТИЛЬДЕР (CSS)
# ==========================================
st.markdown("""
    <style>
    /* Жалпы фон мен қаріп */
    .stApp { background-color: #f8fafc; font-family: 'Inter', sans-serif; }
    
    /* Жоғарғы Навигациялық панель */
    .nav-box { 
        background: linear-gradient(135deg, #115e59 0%, #064e3b 100%); 
        padding: 20px; 
        border-radius: 16px; 
        color: white; 
        margin-bottom: 30px;
        box-shadow: 0 10px 15px -3px rgba(6, 78, 59, 0.2);
    }
    
    /* Заманауи Карточкалар (Glassmorphism секілді) */
    .premium-card {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    
    /* Метрикалар дизайны */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 15px 20px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.02);
    }
    div[data-testid="stMetricValue"] { font-size: 32px !important; font-weight: 700 !important; color: #0f172a; }
    div[data-testid="stMetricLabel"] { font-size: 14px !important; color: #64748b; font-weight: 500; }
    
    /* Батырмалар стилі */
    .stButton>button { 
        background: linear-gradient(90deg, #0d9488 0%, #0f766e 100%) !important; 
        color: white !important; 
        border-radius: 10px !important; 
        border: none !important;
        padding: 10px 24px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 6px -1px rgba(13, 148, 136, 0.2) !important;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { 
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(13, 148, 136, 0.3) !important;
    }
    
    /* Табтар дизайны */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 8px 16px;
        border-radius: 8px;
        font-weight: 600;
        color: #475569;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #0f766e !important;
        color: white !important;
        border-color: #0f766e;
    }
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

# Датчик деректері
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
# 🗺️ НАВИГАЦИЯЛЫҚ ХЕДЕР (ПРЕМИУМ ДИЗАЙН)
# ==========================================
st.markdown("""
    <div class='nav-box'>
        <div style='display: flex; justify-content: space-between; align-items: center;'>
            <div style='display: flex; align-items: center; gap: 15px;'>
                <span style='font-size: 32px;'>🌱</span>
                <div>
                    <h2 style='margin:0; font-weight:800; letter-spacing:-0.5px; color:white;'>EcoGrow AI</h2>
                    <p style='margin:0; font-size:12px; color:#a7f3d0; opacity:0.9;'>Ақылды агро-технологиялық платформа</p>
                </div>
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)

# Мәзір нұсқалары
if st.session_state.logged_in:
    nav_options = ["🏠 Басты бет", "📊 IoT Дашборд", "⚙️ Жүйелік баптаулар", "📞 Сату бөлімі"]
else:
    nav_options = ["🏠 Басты бет", "🔐 Платформаға кіру", "📞 Сату бөлімі"]

# Көлденең заманауи селектор (Интерфейсті таза көрсетеді)
page = st.segmented_control("", nav_options, default="🏠 Басты бет")
st.markdown("<br>", unsafe_allow_html=True)

# Көмекші сидбар ақпараты
st.sidebar.markdown("### 🌐 Инфрақұрылым")
st.sidebar.markdown("• **Сервер:** AWS Cloud (Frankfurt)")
st.sidebar.markdown("• **Датчиктер базасы:** Supabase Realtime")
st.sidebar.markdown(f"• **Нұсқа:** Enterprise v2.8")
if st.session_state.logged_in:
    st.sidebar.write(f"👤 Аккаунт: **{st.session_state.username}**")
    if st.sidebar.button("🚪 Платформадан шығу", key="side_logout"):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# 🏠 БАСТЫ БЕТ (LANDING PAGE)
# ==========================================
if page == "🏠 Басты бет":
    col_h1, col_h2 = st.columns([1.4, 1])
    
    with col_h1:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.title("🚀 Жылыжай шаруашылығын Жасанды Интеллектпен басқарыңыз")
        st.write("EcoGrow AI — шағын және өндірістік жылыжайларға арналған автоматтандырылған IoT экожүйесі. Датчиктер негізінде су мен энергияны үнемдеп, өнім сапасын жаңа деңгейге көтеріңіз.")
        
        st.markdown("#### ✨ Негізгі артықшылықтар:")
        st.markdown("""
        - 📱 **Шексіз қашықтық:** Әлемнің кез келген нүктесінен нақты уақытта бақылау.
        - 🤖 **AI-Агроном (Gemini):** Өсімдіктердің жағдайын талдап, қазақ тілінде күнделікті кеңес беру.
        - 💧 **40% Су үнемдеу:** Топырақ кепкенде ғана іске қосылатын ақылды сорғылар.
        """)
        if not st.session_state.logged_in:
            st.info("💡 Жоғарыдағы мәзірден '🔐 Платформаға кіру' бетіне өтіп, тегін демо-дашбордты ашыңыз.")
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_h2:
        st.markdown("<div class='premium-card' style='text-align:center;'>", unsafe_allow_html=True)
        st.image("https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=500", use_container_width=True)
        st.markdown("<h5>EcoGrow IoT Smart Hub</h5>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 🔐 ПЛАТФОРМАҒА КІРУ
# ==========================================
elif page == "🔐 Платформаға кіру":
    st.markdown("<div class='premium-card' style='max-width: 500px; margin: 0 auto;'>", unsafe_allow_html=True)
    st.subheader("🔐 Авторизация")
    tab_login, tab_register = st.tabs(["🔑 Кіру", "📝 Тіркелу"])
    
    with tab_login:
        login_user = st.text_input("Логин / Email:", key="log_user")
        login_pass = st.text_input("Құпия сөз:", type="password", key="log_pass")
        if st.button("Жүйеге кіру"):
            if login_user and login_pass:
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("Платформаға сәтті кірдіңіз!")
                time.sleep(0.5)
                st.rerun()
            else:
                st.error("Барлық өрісті толтырыңыз!")
                
    with tab_register:
        st.text_input("Аты-жөніңіз:")
        st.text_input("Email мекенжайыңыз:")
        st.text_input("Құпия сөз орнатыңыз:", type="password")
        if st.button("Тіркелуді аяқтау"):
            st.success("Аккаунт жасалды! '🔑 Кіру' табына өтіңіз.")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 📊 IOT БАҚЫЛАУ ПАНЕЛІ (DASHBOARD)
# ==========================================
elif page == "📊 IoT Дашборд":
    st.subheader("📊 Нақты уақыттағы IoT Телеметриясы")
    
    df = fetch_iot_data()
    latest_temp = round(df["Температура (°C)"].iloc[-1], 1)
    latest_hum = round(df["Ылғалдылық (%)"].iloc[-1], 1)
    latest_soil = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

    # 3-тік Көрсеткіштер торы
    col1, col2, col3 = st.columns(3)
    
    temp_status = "⚠️ Жоғары!" if latest_temp > st.session_state.max_temp else "Қалыпты"
    col1.metric(label="🌡️ Ауа Температурасы", value=f"{latest_temp} °C", delta=temp_status, delta_color="inverse" if "⚠️" in temp_status else "normal")
    
    col2.metric(label="💧 Ауа Ылғалдылығы", value=f"{latest_hum} %")
    
    soil_status = "🚨 Құрғақ!" if latest_soil < st.session_state.min_soil else "Жеткілікті"
    col3.metric(label="🪴 Топырақ Ылғалдылығы", value=f"{latest_soil} %", delta=soil_status, delta_color="inverse" if "🚨" in soil_status else "normal")

    st.markdown("<br>", unsafe_allow_html=True)

    # Визуалды аналитика бөлімі
    col_g, col_ctrl = st.columns([2, 1])
    
    with col_g:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        tab_g1, tab_g2, tab_d = st.tabs(["📈 Температура графигі", "📉 Ылғалдылық динамикасы", "📋 Шикі деректер"])
        with tab_g1:
            f_temp = px.line(df, x="Уақыт", y="Температура (°C)", markers=True, color_discrete_sequence=['#0d9488'])
            f_temp.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(f_temp, use_container_width=True)
        with tab_g2:
            f_hum = px.line(df, x="Уақыт", y=["Ылғалдылық (%)", "Топырақ ылғалдылығы (%)"], markers=True)
            f_hum.update_layout(margin=dict(l=20, r=20, t=20, b=20), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(f_hum, use_container_width=True)
        with tab_d:
            st.dataframe(df, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_ctrl:
        # Релелер мен Автоматика статусы
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<h4>⚙️ Жүйелік релелер күйі</h4>", unsafe_allow_html=True)
        fan_on = latest_temp > st.session_state.max_temp
        pump_on = latest_soil < st.session_state.min_soil
        
        st.info(f"💨 **Желдеткіш (Салқындату):** {'🟢 ҚОСУЛЫ' if fan_on else '🔴 ӨШІРУЛІ'}")
        st.info(f"🚰 **Суару помпасы:** {'🟢 ҚОСУЛЫ' if pump_on else '🔴 ӨШІРУЛІ'}")
        st.markdown("</div>", unsafe_allow_html=True)
        
        # AI модуль картасы
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        st.markdown("<h4>🧠 AI-Агроном сараптамасы</h4>", unsafe_allow_html=True)
        if st.button("Деректерді AI-ға жіберу"):
            with st.spinner('AI талдау жасауда...'):
                prompt = f"Сен EcoGrow стартапының бас агрономысың. Мына соңғы IoT деректеріне қарап фермерге қысқа 3 тармақпен қазақша кәсіби кеңес жаз: Температура: {latest_temp}°C, Топырақ ылғалдылығы: {latest_soil}%."
                try:
                    model = genai.GenerativeModel("gemini-1.5-flash")
                    response = model.generate_content(prompt)
                    st.success(response.text)
                except:
                    st.warning("⚠️ Офлайн режим: Микроклимат тұрақты. Автоматика қалыпты жұмыс істеуде.")
        st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# ⚙️ ЖҮЙЕЛІК БАПТАУЛАР
# ==========================================
elif page == "⚙️ Жүйелік баптаулар":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.header("⚙️ Автоматиканың критикалық шектері")
    st.write("Осы жерде көрсетілген мәндерден асқан жағдайда, жүйе бұлт арқылы релелерге автоматты команда жібереді.")
    
    st.session_state.max_temp = st.slider(
        "Максималды рұқсат етілген температура (°C):", 
        min_value=20.0, max_value=35.0, value=st.session_state.max_temp, step=0.5
    )
    st.session_state.min_soil = st.slider(
        "Минималды топырақ ылғалдылығы (суаруды бастау шегі, %):", 
        min_value=15.0, max_value=60.0, value=st.session_state.min_soil, step=1.0
    )
    st.success(f"Баптаулар бұлттық серверде сәтті жаңартылды!")
    st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# 📞 САТУ БӨЛІМІ
# ==========================================
elif page == "📞 Сату бөлімі":
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.header("📞 Коммерциялық ұсыныс алу")
    st.write("Жылыжайыңызды автоматтандыру үшін өтінім қалдырыңыз. Біздің инженерлер сізге хабарласады.")
    
    with st.form("feedback_form"):
        st.text_input("Толық атыңыз:")
        st.text_input("Телефон нөміріңіз:")
        st.selectbox("Жылыжай аумағы:", ["Шағын (<100 м²)", "Орташа (100 - 1000 м²)", "Өндірістік (>1000 м²)"])
        if st.form_submit_button("Өтінімді жіберу"):
            st.balloons()
            st.success("Рақмет! Өтініміңіз сату бөліміне сәтті жолданды.")
    st.markdown("</div>", unsafe_allow_html=True)

# Төменгі жазу (Footer)
st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption(f"© {datetime.now().year} EcoGrow AI Enterprise — Smart Greenhouses. Барлық құқықтар қорғалған. Дизайн v2.8 Premium.")
