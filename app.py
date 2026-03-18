import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Калькулятор ЖКХ",
    page_icon="🏠",
    layout="centered"
)

st.title("🏠 Калькулятор ЖКХ")
st.markdown("---")

with st.sidebar:
    st.header("Настройки")
    city = st.selectbox(
        "Выберите город:",
        ["Геленджик", "Пыть-Ях"]
    )
    st.markdown("---")
    st.caption(f"Актуально на {datetime.now().strftime('%d.%m.%Y')}")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💧 Водоснабжение")
    cold_water = st.number_input("Холодная вода (м³)", min_value=0.0, value=5.0, step=0.1)
    hot_water = st.number_input("Горячая вода (м³)", min_value=0.0, value=3.0, step=0.1)

with col2:
    st.subheader("⚡ Электроснабжение")
    electricity_day = st.number_input("День (кВт·ч)", min_value=0.0, value=100.0, step=1.0)
    electricity_night = st.number_input("Ночь (кВт·ч)", min_value=0.0, value=50.0, step=1.0)

if city == "Геленджик":
    tariffs = {
        "cold_water": 65.32,
        "hot_water": 185.47,
        "electricity_day": 6.83,
        "electricity_night": 3.52
    }
else:  # Пыть-Ях
    tariffs = {
        "cold_water": 58.90,
        "hot_water": 168.30,
        "electricity_day": 5.94,
        "electricity_night": 3.11
    }

if st.button("🧮 Рассчитать", type="primary", use_container_width=True):
    total = 0
    
    st.markdown("---")
    st.subheader("📊 Результаты расчёта")
    
    col_a, col_b, col_c = st.columns(3)
    
    with col_a:
        cold_cost = cold_water * tariffs['cold_water']
        st.metric("Холодная вода", f"{cold_water:.1f} м³", f"{cold_cost:.2f} ₽")
        total += cold_cost
    
    with col_b:
        hot_cost = hot_water * tariffs['hot_water']
        st.metric("Горячая вода", f"{hot_water:.1f} м³", f"{hot_cost:.2f} ₽")
        total += hot_cost
    
    with col_c:
        day_cost = electricity_day * tariffs['electricity_day']
        st.metric("Электричество день", f"{electricity_day:.0f} кВт·ч", f"{day_cost:.2f} ₽")
        total += day_cost
    
    night_cost = electricity_night * tariffs['electricity_night']
    st.metric("Электричество ночь", f"{electricity_night:.0f} кВт·ч", f"{night_cost:.2f} ₽")
    total += night_cost
    
    st.markdown("---")
    st.success(f"### ИТОГО: {total:.2f} ₽")
    
    st.download_button(
        "📥 Сохранить расчёт",
        f"""Результаты расчёта ЖКХ
Город: {city}
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}

Показания:
- Холодная вода: {cold_water} м³
- Горячая вода: {hot_water} м³
- Электричество (день): {electricity_day} кВт·ч
- Электричество (ночь): {electricity_night} кВт·ч

Итоговая сумма: {total:.2f} ₽""",
        file_name=f"jkh_calc_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

st.markdown("---")
st.caption(
    "✅ Тарифы актуальны на 2026 год\n\n"
    "📞 По вопросам: @urikonsult"
)