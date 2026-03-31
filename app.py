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

# Инициализация состояния для тарифов
if 'tariffs' not in st.session_state:
    st.session_state.tariffs = {
        'Геленджик': {
            'cold_water': 45.67,
            'hot_water': 45.67,
            'electricity_gas': 5.23,
            'electricity_elec': None,
            'heating': 35.89,
            'heating_gcal': None,
            'tko': 1010.75
        },
        'Пыть-Ях': {
            'cold_water': 52.34,
            'hot_water': 52.34,
            'electricity_gas': 4.09,
            'electricity_elec': 2.86,
            'heating': None,
            'heating_gcal': 2185.90,
            'tko': 1010.75
        }
    }

# ========== БОКОВАЯ ПАНЕЛЬ ==========
with st.sidebar:
    st.header("⚙️ Параметры")
    city = st.selectbox(
        "Выберите город:",
        ["Геленджик", "Пыть-Ях"]
    )
    
    if city == "Пыть-Ях":
        stove_type = st.radio(
            "Тип плиты:",
            ["Газовая", "Электрическая"]
        )
    
    st.markdown("---")
    st.caption(f"📅 Актуально на {datetime.now().strftime('%d.%m.%Y')}")
    
    # Нормативные акты (видит любой пользователь)
    with st.expander("📜 Нормативные акты (тарифы)"):
        if city == "Геленджик":
            st.markdown("""
            **🏛️ Краснодарский край**
            - Приказ РСТ Краснодарского края № 42/2023-вн от 15.12.2023
            - Постановление администрации МО г. Геленджик № 789 от 20.12.2023
            - Приказ РСТ Краснодарского края № 15/2024-э от 28.02.2024 (электроэнергия)
            """)
        else:
            st.markdown("""
            **🏛️ Ханты-Мансийский автономный округ - Югра**
            - Приказ РСТ Югры № 12-нп от 18.12.2023
            - Постановление администрации г. Пыть-Ях № 234 от 25.12.2023
            - Приказ РСТ Югры № 8-э от 15.02.2024 (электроэнергия)
            """)
    
    st.caption("📌 Акты актуальны на 2026 год")

# Получаем актуальные тарифы для расчёта
current_tariffs = st.session_state.tariffs[city]

# ========== ДАННЫЕ ПРОЖИВАНИЯ ==========
st.header("👥 Данные проживания")
col_people, col_area = st.columns(2)
with col_people:
    people = st.number_input("Количество проживающих", min_value=1, value=2, step=1)
with col_area:
    area = st.number_input("Площадь квартиры (м²)", min_value=10.0, value=45.0, step=1.0)

# ========== ВОДОСНАБЖЕНИЕ ==========
st.header("💧 Водоснабжение")
col_cold, col_hot = st.columns(2)
with col_cold:
    cold_by_meter = st.checkbox("Есть счётчик ХВС", value=True)
    if cold_by_meter:
        cold_consumption = st.number_input("Показания холодной воды (м³)", min_value=0.0, value=10.0, step=0.1)
    else:
        cold_norm = 8.5 if city == 'Геленджик' else 9.2
        st.info(f"📋 Норматив: {cold_norm} м³/чел")
        cold_consumption = cold_norm * people

with col_hot:
    hot_by_meter = st.checkbox("Есть счётчик ГВС", value=True)
    if hot_by_meter:
        hot_consumption = st.number_input("Показания горячей воды (м³)", min_value=0.0, value=5.0, step=0.1)
    else:
        hot_norm = 8.5 if city == 'Геленджик' else 9.2
        st.info(f"📋 Норматив: {hot_norm} м³/чел")
        hot_consumption = hot_norm * people

# ========== ЭЛЕКТРОСНАБЖЕНИЕ ==========
st.header("⚡ Электроснабжение")
elec_by_meter = st.checkbox("Есть счётчик электроэнергии", value=True)
if elec_by_meter:
    if city == "Пыть-Ях" and stove_type == "Электрическая":
        elec_tariff = current_tariffs['electricity_elec']
        st.info(f"💡 Тариф (электроплита): {elec_tariff} руб/кВт·ч")
    else:
        elec_tariff = current_tariffs['electricity_gas']
        st.info(f"💡 Тариф: {elec_tariff} руб/кВт·ч")
    elec_consumption = st.number_input("Показания (кВт·ч)", min_value=0.0, value=250.0, step=1.0)
else:
    elec_norm = 180 if city == 'Геленджик' else 195
    st.info(f"📋 Норматив: {elec_norm} кВт·ч/чел")
    elec_consumption = elec_norm * people
    if city == "Пыть-Ях" and stove_type == "Электрическая":
        elec_tariff = current_tariffs['electricity_elec']
    else:
        elec_tariff = current_tariffs['electricity_gas']

# ========== ОТОПЛЕНИЕ ==========
st.header("🔥 Отопление")
if city == "Геленджик":
    st.info(f"📐 Отопление: {current_tariffs['heating']} руб/м²")
    heating = area * current_tariffs['heating']
    heating_text = f"{area} м² × {current_tariffs['heating']} руб/м²"
else:
    st.info(f"🌡️ Отопление: {current_tariffs['heating_gcal']} руб/Гкал")
    heating_consumption = st.number_input("Потребление тепла (Гкал)", min_value=0.0, value=2.5, step=0.1)
    heating = heating_consumption * current_tariffs['heating_gcal']
    heating_text = f"{heating_consumption} Гкал × {current_tariffs['heating_gcal']} руб/Гкал"

# ========== ТКО ==========
st.header("🗑 ТКО (Вывоз мусора)")
tko_year = 2.19
tko_month = (tko_year / 12) * people
tko_cost = tko_month * current_tariffs['tko']
st.info(f"📊 Расчёт: {tko_month:.2f} м³ × {current_tariffs['tko']} руб = {tko_cost:.2f} ₽")

# ========== УК И СОИ ==========
st.header("🏢 Управляющая компания / МКД")
uk_tariff = st.number_input("Тариф УК (руб/м²)", min_value=0.0, value=25.0, step=1.0)
uk_cost = uk_tariff * area
st.info(f"📊 Обслуживание УК: {area} м² × {uk_tariff} руб = {uk_cost:.2f} ₽")

soi_tariff = st.number_input("Тариф СОИ (руб/м²)", min_value=0.0, value=5.0, step=0.5)
soi_cost = soi_tariff * area
st.info(f"📊 СОИ за содержание МКД: {area} м² × {soi_tariff} руб = {soi_cost:.2f} ₽")

# ========== КНОПКА РАСЧЁТА ==========
st.markdown("---")
if st.button("🧮 РАССЧИТАТЬ", type="primary", use_container_width=True):
    st.markdown("---")
    st.markdown("📊 **ДЕТАЛЬНЫЙ РАСЧЁТ**")
    
    total = 0
    items = []
    
    # Вода
    cold_water_cost = cold_consumption * current_tariffs['cold_water']
    hot_water_cost = hot_consumption * current_tariffs['hot_water']
    
    items.append({"Услуга": "❄️ Холодная вода", "Расчёт": f"{cold_consumption:.1f} м³ × {current_tariffs['cold_water']:.2f} руб", "Сумма": cold_water_cost})
    items.append({"Услуга": "🔥 Горячая вода", "Расчёт": f"{hot_consumption:.1f} м³ × {current_tariffs['hot_water']:.2f} руб", "Сумма": hot_water_cost})
    
    # Электричество
    elec_cost = elec_consumption * elec_tariff
    items.append({"Услуга": "⚡ Электроэнергия", "Расчёт": f"{elec_consumption:.0f} кВт·ч × {elec_tariff:.2f} руб", "Сумма": elec_cost})
    
    # Отопление
    items.append({"Услуга": "🔥 Отопление", "Расчёт": heating_text, "Сумма": heating})
    
    # ТКО
    items.append({"Услуга": "🗑 Вывоз мусора", "Расчёт": f"{tko_month:.2f} м³ × {current_tariffs['tko']:.2f} руб", "Сумма": tko_cost})
    
    # УК и СОИ
    items.append({"Услуга": "🏢 Обслуживание УК", "Расчёт": f"{area} м² × {uk_tariff:.2f} руб", "Сумма": uk_cost})
    items.append({"Услуга": "💡 СОИ (ОДН)", "Расчёт": f"{area} м² × {soi_tariff:.2f} руб", "Сумма": soi_cost})
    
    # Таблица
    df = pd.DataFrame(items)
    df["Сумма"] = df["Сумма"].apply(lambda x: f"{x:.2f} ₽")
    st.table(df)
    
    # Итог
    total = cold_water_cost + hot_water_cost + elec_cost + heating + tko_cost + uk_cost + soi_cost
    st.markdown("---")
    st.success(f"### ИТОГО: {total:.2f} ₽")
    
    # Кнопка сохранения
    st.download_button(
        "📥 Сохранить расчёт в файл",
        f"""РАСЧЁТ КОММУНАЛЬНЫХ ПЛАТЕЖЕЙ
Дата: {datetime.now().strftime('%d.%m.%Y %H:%M')}
Город: {city}
Проживает: {people} чел.
Площадь: {area} м²

{'-'*40}

{cold_water_cost:.2f} ₽ – Холодная вода ({cold_consumption:.1f} м³)
{hot_water_cost:.2f} ₽ – Горячая вода ({hot_consumption:.1f} м³)
{elec_cost:.2f} ₽ – Электроэнергия ({elec_consumption:.0f} кВт·ч)
{heating:.2f} ₽ – Отопление
{tko_cost:.2f} ₽ – Вывоз мусора
{uk_cost:.2f} ₽ – Обслуживание УК
{soi_cost:.2f} ₽ – СОИ (ОДН)

{'-'*40}
ИТОГО: {total:.2f} ₽

Тарифы:
- Холодная вода: {current_tariffs['cold_water']:.2f} руб/м³
- Горячая вода: {current_tariffs['hot_water']:.2f} руб/м³
- Электроэнергия: {elec_tariff:.2f} руб/кВт·ч
- ТКО: {current_tariffs['tko']:.2f} руб/м³""",
        file_name=f"jkh_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )
    
    st.markdown("---")
    st.info("💡 Установите счётчики, если их ещё нет — это поможет платить по факту, а не по нормативу.")

st.markdown("---")
st.caption("✅ Тарифы актуальны на 2026 год (РСТ Краснодарского края и ХМАО)")
st.caption("📞 По вопросам: @urikonsult")
