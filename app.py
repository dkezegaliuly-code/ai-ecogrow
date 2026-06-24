import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
from datetime import datetime

# Беттің баптаулары (Бұл біздің Landing + Dashboard)
st.set_page_config(page_title="AI-EcoGrow | Smart IoT Incubator", layout="wide", page_icon="🌱")

# Мәліметтерді симуляциялау (Робототехника бөлімі - Датчиктер)
def generate_mock_data():
    now = datetime.now()
    times = [datetime.fromtimestamp(now.timestamp() - i*60) for i in range(20, 0, -1)]
    # Датчик көрсеткіштері
    temperature = np.random.uniform(22.0, 29.0, 20)
    humidity = np.random.uniform(45.0, 65.0, 20)
    soil_moisture = np.random.uniform(30.0, 55.0, 20)
    
    return pd.DataFrame({
        "Уақыт": times,
        "Температура (°C)": temperature,
        "Ылғалдылық (%)": humidity,
        "Топырақ ылғалдылығы (%)": soil_moisture
    })

df = generate_mock_data()
latest_temp = round(df["Температура (°C)"].iloc[-1], 1)
latest_hum = round(df["Ылғалдылық (%)"].iloc[-1], 1)
latest_soil = round(df["Топырақ ылғалдылығы (%)"].iloc[-1], 1)

# --- 1. LANDING PAGE БӨЛІМІ (Таныстыру) ---
st.title("🌱 AI-EcoGrow — Ақылды IoT Жылыжай Тұғырнамасы")
st.markdown("### Өндірістік практиканың MVP жобасы | Команда: AI-Incubator Wizards")
st.write("**Мәселе:** Шағын және орта жылыжайларда микроклиматты бақылаудың автоматтандырылмауы өнімділікті 30%-ға төмендетеді.")
st.write("**Шешім:** Датчиктер арқылы деректерді жинайтын, автоматты суаратын және AI (жасанды интеллект) арқылы өсімдік жағдайын талдайтын IoT жүйесі.")

st.markdown("---")

# --- 2. DASHBOARD БӨЛІМІ (Нақты уақыттағы IoT көрсеткіштері) ---
st.header("📊 Нақты уақыттағы IoT Телеметриясы (Симуляция)")

col1, col2, col3 = st.columns(3)
col1.metric(label="🌡️ Температура", value=f"{latest_temp} °C", delta="Қалыпты" if latest_temp < 28 else "Жоғары!")
col2.metric(label="💧 Ауа ылғалдылығы", value=f"{latest_hum} %")
col3.metric(label="🪴 Топырақ ылғалдылығы", value=f"{latest_soil} %", delta="-2%" if latest_soil < 40 else "Жеткілікті")

# Графиктер
st.subheader("📈 Датчиктердің динамикасы")
fig_temp = px.line(df, x="Уақыт", y="Температура (°C)", title="Температура өзгерісі")
st.plotly_chart(fig_temp, use_container_width=True)

fig_hum = px.line(df, x="Уақыт", y=["Ылғалдылық (%)", "Топырақ ылғалдылығы (%)"], title="Ылғалдылық көрсеткіштері", barmode='group')
st.plotly_chart(fig_hum, use_container_width=True)

st.markdown("---")

# --- 3. AUTOMATION & AI БӨЛІМІ (Міндетті талап) ---
st.header("🤖 AI Автоматтандыру және Аналитика Модулі")

col_act1, col_act2 = st.columns(2)

with col_act1:
    st.subheader("⚙️ Автоматты жүйелердің күйі")
    if latest_temp > 27.5:
        st.error("🚨 Ескерту: Температура жоғары! Автоматты желдеткіш іске қосылды.")
        fan_status = "🟢 Қосулы (Желдету)"
    else:
        st.success("✅ Жүйе тұрақты.")
        fan_status = "🔴 Өшірулі"
        
    if latest_soil < 35:
        st.warning("⚠️ Топырақ құрғақ! Автоматты суару помпасы іске қосылды.")
        pump_status = "🟢 Қосулы (Суару)"
    else:
        pump_status = "🔴 Өшірулі"
        
    st.write(f"**Ауа салқындатқыш (Фан):** {fan_status}")
    st.write(f"**Суару помпасы:** {pump_status}")

with col_act2:
    st.subheader("🧠 AI-Агроном Кеңесі (DeepSeek / Gemini API模擬)")
    if st.button("AI-дан есеп алу"):
        with st.spinner('Жасанды интеллект деректерді талдауда...'):
            time.sleep(1.5) # Эффект құру
            # AI жауабы (Егер интернет немесе API кілт болмаса, дайын модельдік талдау шығады)
            st.info(f"""
            **AI Генерацияланған Есеп (Дата: {datetime.now().strftime('%d.%m.%Y')}):**
            1. **Қорытынды:** Соңғы сағатта температура {latest_temp}°C-қа дейін көтерілген. Бұл өсімдік үшін сәл ыстық. Автоматты жүйенің желдеткішті қосқаны дұрыс болды.
            2. **Ұсыныс:** Ылғалдылық деңгейі жақсы ({latest_hum}%), бірақ топырақ құрғап кетпеуі үшін келесі суару режимін 10 минутқа ұзартуды ұсынамын.
            3. **Болжам:** Күй осылай сақталса, өнімділік 12%-ға артады.
            """)

st.markdown("---")
st.caption("© 2026 AI-EcoGrow Incubator Sprint. Барлық құқықтар қорғалған.")
