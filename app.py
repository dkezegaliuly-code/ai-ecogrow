import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime
import google.generativeai as genai

# Беттің негізгі баптаулары
st.set_page_config(page_title="AI-EcoGrow | Smart IoT Incubator", layout="wide", page_icon="🌱")

# Gemini API баптау (қажет болса)
genai.configure(api_key="СІЗДІҢ_GEMINI_API_КІЛТІҢІЗ")

# Дизайнды жақсартуға арналған CSS стильдері
st.markdown("""
    <style>
    .stButton>button { background-color: #2e7d32; color: white; border-radius: 8px; font-weight: bold; }
    .stButton>button:hover { background-color: #1b5e20; color: white; }
    .price-card { padding: 20px; border-radius: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

# СИДЕНБАР (Навигация мәзірі)
st.sidebar.title("🌱 EcoGrow AI")
st.sidebar.markdown("---")
page = st.sidebar.radio("Мәзір:", ["🏠 Басты бет (Landing Page)", "📊 IoT Бақылау панелі", "📞 Контактілер"])
st.sidebar.markdown("---")
st.sidebar.info("🤖 MVP нұсқасы v1.5\nКоманда: AI-Incubator Wizards")

# Деректерді генерациялау (Dashboard үшін керек)
@st.cache_data(ttl=60)
def generate_mock_data():
    now = datetime.now()
    times = [datetime.fromtimestamp(now.timestamp() - i*60) for i in range(20, 0, -1)]
    return pd.DataFrame({
        "Уақыт": times,
        "Температура (°C)": np.random.uniform(23.0, 28.5, 20),
        "Ылғалдылық (%)": np.random.uniform(50.0, 65.0, 20),
        "Топырақ ылғалдылығы (%)": np.random.uniform(32.0, 50.0, 20)
    })

# ==========================================
# 1. БАТЫ БЕТ (LANDING PAGE)
# ==========================================
if page == "🏠 Басты бет (Landing Page)":
    # Hero Section
    st.title("🚀 Жылыжай бизнесіңізді Жасанды Интеллектпен автоматтандырыңыз")
    st.markdown("### **EcoGrow AI** — Суды 40%-ға дейін үнемдеп, өнімділікті арттыруға арналған ақылды IoT экожүйесі.")
    
    col_hero1, col_hero2 = st.columns([2, 1])
    with col_hero1:
        st.write("")
        st.write("Біздің жүйе — топырақ пен ауаның күйін нақты уақытта талдап, суару мен желдетуді адамның қатысуынсыз автоматты түрде басқарады. Ал кіріктірілген AI-Агроном өсімдіктердің ауруларын алдын ала болжап, қазақ тілінде кеңес береді.")
        if st.button("Тегін демо нұсқасын көру"):
            st.balloons()
            st.success("Сол жақ мәзірден '📊 IoT Бақылау панелі' бөліміне өтіңіз!")
    with col_hero2:
        st.image("https://images.unsplash.com/photo-1585320806297-9794b3e4eeae?w=500", caption="Ақылды Жылыжай Идеясы")

    st.markdown("---")
    
    # Мүмкіндіктер (Features)
    st.header("🎯 Неге бізді таңдайды?")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        st.markdown("### 🔌 Plug & Play Hardware")
        st.write("Құрылғыларды орнату оңай. Датчиктерді топыраққа қадап, розеткаға қоссаңыз жеткілікті. Wi-Fi арқылы бұлтқа қосылады.")
    with col_f2:
        st.markdown("### 🤖 Бұлттық AI-Агроном")
        st.write("LLM (Gemini/DeepSeek) үлгілеріне негізделген интеллектуалды жүйе сіздің деректеріңізді талдап, дайын есеп береді.")
    with col_f3:
        st.markdown("### 💧 Экономия және Пайда")
        st.write("Су мен электр энергиясын автоматты реттеу арқылы айлық шығындарды азайтып, өнім көлемін 30-35%-ға арттырыңыз.")

    st.markdown("---")

    # Тарифтер (Pricing)
    st.header("💳 Икемді тарифтер")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        st.markdown("""
        <div class="price-card">
            <h3>EcoBox Mini</h3>
            <h2>35,000 ₸</h2>
            <p>Үй гүлдері мен шағын жылыжайларға арналған</p>
            <hr>
            <p>✅ 2 Датчик (Ауа + Топырақ)</p>
            <p>✅ Базалық Dashboard</p>
            <p>❌ AI Кеңестері</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Сатып алу (Mini)", key="btn_mini"):
            st.success("Тапсырыс қабылданды! Менеджер сізбен хабарласады.")

    with col_p2:
        st.markdown("""
        <div class="price-card" style="border: 2px solid #2e7d32;">
            <h3>EcoBox Pro 🌟</h3>
            <h2>120,000 ₸</h2>
            <p>Кәсіби шағын және орта жылыжайларға</p>
            <hr>
            <p>✅ Барлық датчиктер жиынтығы</p>
            <p>✅ Автоматты суару клапаны</p>
            <p>✅ <b>Шексіз AI-Агроном көмегі</b></p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Сатып алу (Pro)", key="btn_pro"):
            st.success("Тапсырыс қабылданды! Менеджер сізбен хабарласады.")

    with col_p3:
        st.markdown("""
        <div class="price-card">
            <h3>Enterprise</h3>
            <h2>Келісімді</h2>
            <p>Ірі өндірістік агро-кешендер үшін</p>
            <hr>
            <p>✅ Жеке өндірістік датчиктер</p>
            <p>✅ Локалды сервер орнату</p>
            <p>✅ 24/7 Техникалық қолдау</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Байланысқа шығу", key="btn_ent"):
            st.success("Сұраныс жіберілді.")

# ==========================================
# 2. IOT БАҚЫЛАУ ПАНЕЛІ (DASHBOARD)
# ==========================================
elif page == "📊 IoT Бақылау панелі":
    st.header("📊 Нақты уақыттағы IoT Телеметриясы және Басқару")
    
    df = generate_mock_data()
    latest_temp = round(df["Температура (°C)"].iloc[-1], 1)
    latest_hum = round(df["Ылғалдылық (%)"].iloc[-1], 1)
    latest_soil = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

    # Көрсеткіштер
    col1, col2, col3 = st.columns(3)
    col1.metric(label="🌡️ Температура", value=f"{latest_temp} °C", delta="Қалыпты" if latest_temp < 27.5 else "Жоғары!")
    col2.metric(label="💧 Ауа ылғалдылығы", value=f"{latest_hum} %")
    col3.metric(label="🪴 Топырақ ылғалдылығы", value=f"{latest_soil} %")

    # Графиктер
    tab1, tab2 = st.tabs(["📈 Динамикалық графиктер", "📋 Шикі деректер (Data)"])
    with tab1:
        fig_temp = px.line(df, x="Уақыт", y="Температура (°C)", title="Температура өзгерісі", color_discrete_sequence=['#ff4b4b'])
        st.plotly_chart(fig_temp, use_container_width=True)
        
        fig_hum = px.line(df, x="Уақыт", y=["Ылғалдылық (%)", "Топырақ ылғалдылығы (%)"], title="Ылғалдылық деңгейі")
        st.plotly_chart(fig_hum, use_container_width=True)
    with tab2:
        st.dataframe(df, use_container_width=True)

    st.markdown("---")

    # Автоматика және АИ
    col_act1, col_act2 = st.columns(2)
    with col_act1:
        st.subheader("⚙️ Автоматты жүйелердің күйі")
        auto_fan = latest_temp > 27.5
        auto_pump = latest_soil < 35
        
        st.write(f"**Желдеткіш (Fan):** {'🟢 Қосулы (Салқындату)' if auto_fan else '🔴 Өшірулі'}")
        st.write(f"**Суару помпасы (Pump):** {'🟢 Қосулы (Суару)' if auto_pump else '🔴 Өшірулі'}")
        
        st.markdown("---")
        manual = st.toggle("Қолмен басқару режиміне өту")
        if manual:
            st.checkbox("Желдеткішті мәжбүрлі қосу")
            st.checkbox("Помпаны мәжбүрлі қосу")

    with col_act2:
        st.subheader("🧠 AI-Агроном Сараптамасы")
        if st.button("AI Нақты есептеуді бастау"):
            with st.spinner('Жасанды интеллект бұлттан деректерді жүктеп жатыр...'):
                time.sleep(1.2)
                st.info(f"""
                **AI Генерацияланған Есеп:**
                * **Талдау:** Температура көрсеткіші {latest_temp}°C. Өсімдіктің транспирациясы қалыпты.
                * **Ұсыныс:** Топырақ ылғалдылығы {latest_soil}%. Суару жүйесінің циклділігін тағы 5 минутқа арттыруды ұсынамын.
                """)

# ==========================================
# 3. КОНТАКТІЛЕР БӨЛІМІ
# ==========================================
elif page == "📞 Контактілер":
    st.header("📞 Бізбен байланыс")
    st.write("Сұрақтарыңыз немесе арнайы тапсырыстарыңыз бар ма? Бізге жазыңыз!")
    
    with st.form("contact_form"):
        name = st.text_input("Атыңыз:")
        email = st.text_input("Email мекенжайыңыз немесе Телефон нөміріңіз:")
        message = st.text_area("Хабарламаңыз:")
        submitted = st.form_submit_button("Жіберу")
        
        if submitted:
            if name and email and message:
                st.success(f"Рақмет, {name}! Хабарламаңыз сәтті жіберілді. Жақын арада байланысамыз.")
            else:
                st.error("Өтініш, барлық өрістерді толтырыңыз.")

# Футер (Сайттың аяққы бөлігі)
st.markdown("---")
st.caption(f"© {datetime.now().year} EcoGrow AI — Smart Agriculture Solutions. Өндірістік MVP жобасы.")
