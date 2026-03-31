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
    st.caption("📊 Тарифы утверждены РСТ")

st.header("👥 Данные проживания")
col_people, col_area = st.columns(2)
with col_people:
    people = st.number_input("Количество проживающих", min_value=1, value=2, step=1)
with col_area:
    area = st.number_input("Площадь квартиры (м²)", min_value=10.0, value=45.0, step=1.0)

# Водоснабжение
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

# Электроснабжение
st.header("⚡ Электроснабжение")
elec_by_meter = st.checkbox("Есть счётчик электроэнергии", value=True)
if elec_by_meter:
    if city == "Пыть-Ях" and stove_type == "Электрическая":
        st.info("💡 Для электроплит действует пониженный тариф")
    elec_consumption = st.number_input("Показания (кВт·ч)", min_value=0.0, value=250.0, step=1.0)
else:
    elec_norm = 180 if city == 'Геленджик' else 195
    st.info(f"📋 Норматив: {elec_norm} кВт·ч/чел")
    elec_consumption = elec_norm * people

# Отопление
st.header("🔥 Отопление")
if city == "Геленджик":
    st.info("📐 Отопление считается по площади квартиры")
    heating = area * 35.89
    heating_text = f"{area} м² × 35.89 руб/м²"
else:  # Пыть-Ях
    st.info("🌡️ Отопление считается по фактическому потреблению тепла")
    heating_consumption = st.number_input("Потребление тепла (Гкал)", min_value=0.0, value=2.5, step=0.1)
    heating = heating_consumption * 2185.90
    heating_text = f"{heating_consumption} Гкал × 2185.90 руб/Гкал"

# ТКО (мусор)
st.header("🗑 ТКО (Вывоз мусора)")
tko_year = 2.19
tko_month = (tko_year / 12) * people
tko_cost = tko_month * 1010.75
st.info(f"📊 Расчёт: {tko_month:.2f} м³ × 1010.75 руб = {tko_cost:.2f} ₽")

# ========== НОВЫЕ ПОЛЯ ==========
st.header("🏢 Управляющая компания / МКД")

# Стоимость обслуживания УК
uk_tariff = st.number_input(
    "Тариф УК (руб/м²)", 
    min_value=0.0, 
    value=25.0, 
    step=1.0,
    help="Указывается в квитанции как 'Содержание жилья'"
)
uk_cost = uk_tariff * area
st.info(f"📊 Обслуживание УК: {area} м² × {uk_tariff} руб = {uk_cost:.2f} ₽")

# СОИ (общедомовые нужды)
soi_tariff = st.number_input(
    "Тариф СОИ (руб/м²)", 
    min_value=0.0, 
    value=5.0, 
    step=0.5,
    help="Коммунальные ресурсы на ОДН (вода, свет на места общего пользования)"
)
soi_cost = soi_tariff * area
st.info(f"📊 СОИ за содержание МКД: {area} м² × {soi_tariff} руб = {soi_cost:.2f} ₽")

# Кнопка расчёта
st.markdown("---")
if st.button("🧮 РАССЧИТАТЬ", type="primary", use_container_width=True):
    st.markdown("---")
    st.markdown('<p class="section-header">📊 ДЕТАЛЬНЫЙ РАСЧЁТ</p>', unsafe_allow_html=True)
    
    total = 0
    items = []
    
    # Вода
    cold_water_cost = cold_consumption * (45.67 if city == 'Геленджик' else 52.34)
    hot_water_cost = hot_consumption * (45.67 if city == 'Геленджик' else 52.34)
    
    items.append({"Услуга": "❄️ Холодная вода", "Расчёт": f"{cold_consumption:.1f} м³ × {45.67 if city == 'Геленджик' else 52.34} руб", "Сумма": cold_water_cost})
    items.append({"Услуга": "🔥 Горячая вода", "Расчёт": f"{hot_consumption:.1f} м³ × {45.67 if city == 'Геленджик' else 52.34} руб", "Сумма": hot_water_cost})
    
    # Электричество
    if city == "Пыть-Ях" and stove_type == "Электрическая":
        elec_tariff = 2.86
        elec_note = "(электроплита)"
    else:
        elec_tariff = 5.23 if city == 'Геленджик' else 4.09
        elec_note = ""
    
    elec_cost = elec_consumption * elec_tariff
    items.append({"Услуга": "⚡ Электроэнергия", "Расчёт": f"{elec_consumption:.0f} кВт·ч × {elec_tariff} руб {elec_note}", "Сумма": elec_cost})
    
    # Отопление
    items.append({"Услуга": "🔥 Отопление", "Расчёт": heating_text, "Сумма": heating})
    
    # ТКО
    items.append({"Услуга": "🗑 Вывоз мусора", "Расчёт": f"{tko_month:.2f} м³ × 1010.75 руб", "Сумма": tko_cost})
    
    # НОВЫЕ: УК и СОИ
    items.append({"Услуга": "🏢 Обслуживание УК", "Расчёт": f"{area} м² × {uk_tariff} руб", "Сумма": uk_cost})
    items.append({"Услуга": "💡 СОИ (ОДН)", "Расчёт": f"{area} м² × {soi_tariff} руб", "Сумма": soi_cost})
    
    # Создаём таблицу
    df = pd.DataFrame(items)
    df["Сумма"] = df["Сумма"].apply(lambda x: f"{x:.2f} ₽")
    
    st.table(df)
    
    # Итог
    total = cold_water_cost + hot_water_cost + elec_cost + heating + tko_cost + uk_cost + soi_cost
    
    st.markdown("---")
    st.markdown(f'<div class="total-amount">ИТОГО: {total:.2f} ₽</div>', unsafe_allow_html=True)
    
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

Тарифы утверждены РСТ на 2026 год""",
        file_name=f"jkh_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )
    
    st.markdown("---")
    st.info("💡 Установите счётчики, если их ещё нет — это поможет платить по факту, а не по нормативу.")

st.markdown("---")
st.caption("✅ Тарифы актуальны на 2026 год (РСТ Краснодарского края и ХМАО)")
st.caption("📞 По вопросам: @urikonsult")
