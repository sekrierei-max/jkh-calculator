import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="Калькулятор ЖКХ",
    page_icon="🏠",
    layout="centered"
)

# Стили для единообразия шрифтов
st.markdown("""
<style>
    /* Единый базовый размер для всех текстов */
    .stApp, .stMarkdown, .stText, .stNumberInput, .stSelectbox, .stRadio {
        font-size: 16px !important;
    }
    
    /* Заголовки секций */
    .section-header {
        font-size: 20px !important;
        font-weight: 600;
        color: #2c3e50;
        margin-top: 25px;
        margin-bottom: 15px;
        border-bottom: 2px solid #3498db;
        padding-bottom: 5px;
    }
    
    /* Подзаголовки внутри секций */
    .subsection-header {
        font-size: 16px !important;
        font-weight: 600;
        color: #34495e;
        margin-top: 10px;
        margin-bottom: 5px;
    }
    
    /* Метки полей ввода */
    .input-label {
        font-size: 16px !important;
        font-weight: 500;
        color: #7f8c8d;
        margin-bottom: 2px;
    }
    
    /* Важная информация (результаты) */
    .result-value {
        font-size: 16px !important;
        font-weight: 700;
        color: #27ae60;
    }
    
    /* Информационные сообщения */
    .info-text {
        font-size: 16px !important;
        font-style: italic;
        color: #3498db;
        background-color: #f0f8ff;
        padding: 8px;
        border-radius: 5px;
    }
    
    /* Предупреждения */
    .warning-text {
        font-size: 16px !important;
        font-weight: 600;
        color: #e67e22;
        text-decoration: underline dotted;
    }
    
    /* Примечания внизу */
    .caption-text {
        font-size: 16px !important;
        color: #95a5a6;
        font-style: italic;
    }
    
    /* Таблица результатов */
    .dataframe {
        font-size: 16px !important;
    }
    
    .dataframe td, .dataframe th {
        font-size: 16px !important;
        padding: 8px !important;
    }
    
    /* Итоговая сумма */
    .total-amount {
        font-size: 24px !important;
        font-weight: 700;
        color: #27ae60;
        text-align: center;
        padding: 15px;
        background-color: #f1f8e9;
        border-radius: 10px;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

st.title("🏠 Калькулятор ЖКХ")
st.markdown(f'<p class="caption-text">📅 Актуально на {datetime.now().strftime("%d.%m.%Y")} | Тарифы утверждены РСТ</p>', unsafe_allow_html=True)
st.markdown("---")

# Боковая панель с настройками
with st.sidebar:
    st.markdown('<p class="section-header">⚙️ Параметры</p>', unsafe_allow_html=True)
    
    city = st.selectbox(
        "🏙️ **Город**",
        ["Геленджик", "Пыть-Ях"]
    )
    
    if city == "Пыть-Ях":
        stove_type = st.radio(
            "🔥 **Тип плиты**",
            ["Газовая", "Электрическая"],
            help="Для электроплит действует пониженный тариф"
        )
    
    st.markdown("---")
    st.markdown('<p class="caption-text">📊 Все тарифы соответствуют документам РСТ</p>', unsafe_allow_html=True)

# Основной интерфейс
st.markdown('<p class="section-header">👥 Данные проживания</p>', unsafe_allow_html=True)

col_people, col_area = st.columns(2)
with col_people:
    people = st.number_input("👨‍👩‍👧 Количество проживающих", min_value=1, value=2, step=1)
with col_area:
    area = st.number_input("🏠 Площадь квартиры (м²)", min_value=10.0, value=45.0, step=1.0)

# Водоснабжение
st.markdown('<p class="section-header">💧 Водоснабжение</p>', unsafe_allow_html=True)

col_cold, col_hot = st.columns(2)
with col_cold:
    st.markdown('<p class="subsection-header">❄️ Холодная вода</p>', unsafe_allow_html=True)
    cold_by_meter = st.checkbox("Есть счётчик ХВС", value=True, key="cold_meter")
    if cold_by_meter:
        cold_consumption = st.number_input("Показания (м³)", min_value=0.0, value=10.0, step=0.1, key="cold_input")
    else:
        cold_norm = 8.5 if city == 'Геленджик' else 9.2
        st.markdown(f'<p class="info-text">📋 Норматив: {cold_norm} м³/чел</p>', unsafe_allow_html=True)
        cold_consumption = cold_norm * people

with col_hot:
    st.markdown('<p class="subsection-header">🔥 Горячая вода</p>', unsafe_allow_html=True)
    hot_by_meter = st.checkbox("Есть счётчик ГВС", value=True, key="hot_meter")
    if hot_by_meter:
        hot_consumption = st.number_input("Показания (м³)", min_value=0.0, value=5.0, step=0.1, key="hot_input")
    else:
        hot_norm = 8.5 if city == 'Геленджик' else 9.2
        st.markdown(f'<p class="info-text">📋 Норматив: {hot_norm} м³/чел</p>', unsafe_allow_html=True)
        hot_consumption = hot_norm * people

# Электроснабжение
st.markdown('<p class="section-header">⚡ Электроснабжение</p>', unsafe_allow_html=True)

elec_by_meter = st.checkbox("Есть счётчик электроэнергии", value=True, key="elec_meter")
if elec_by_meter:
    if city == "Пыть-Ях" and stove_type == "Электрическая":
        st.markdown('<p class="info-text">💡 Для электроплит действует пониженный тариф 2.86 руб/кВт·ч</p>', unsafe_allow_html=True)
    elec_consumption = st.number_input("Показания (кВт·ч)", min_value=0.0, value=250.0, step=1.0, key="elec_input")
else:
    elec_norm = 180 if city == 'Геленджик' else 195
    st.markdown(f'<p class="info-text">📋 Норматив: {elec_norm} кВт·ч/чел</p>', unsafe_allow_html=True)
    elec_consumption = elec_norm * people

# Отопление
st.markdown('<p class="section-header">🔥 Отопление</p>', unsafe_allow_html=True)

if city == "Геленджик":
    st.markdown('<p class="info-text">📐 Отопление считается по площади квартиры</p>', unsafe_allow_html=True)
    heating = area * 35.89
    heating_text = f"{area} м² × 35.89 руб/м²"
else:  # Пыть-Ях
    st.markdown('<p class="info-text">🌡️ Отопление считается по фактическому потреблению тепла</p>', unsafe_allow_html=True)
    heating_consumption = st.number_input("Потребление тепла (Гкал)", min_value=0.0, value=2.5, step=0.1, key="heating_input")
    heating = heating_consumption * 2185.90
    heating_text = f"{heating_consumption} Гкал × 2185.90 руб/Гкал"

# ТКО (мусор)
st.markdown('<p class="section-header">🗑 ТКО (Вывоз мусора)</p>', unsafe_allow_html=True)

tko_year = 2.19  # норматив в год на человека
tko_month = (tko_year / 12) * people
tko_cost = tko_month * 1010.75

st.markdown(f'<p class="info-text">📊 Расчёт: {tko_month:.2f} м³ × 1010.75 руб = {tko_cost:.2f} ₽</p>', unsafe_allow_html=True)

# Кнопка расчёта
st.markdown("---")
if st.button("🧮 **РАССЧИТАТЬ**", type="primary", use_container_width=True):
    st.markdown("---")
    st.markdown('<p class="section-header">📊 ДЕТАЛЬНЫЙ РАСЧЁТ</p>', unsafe_allow_html=True)
    
    total = 0
    items = []
    
    # Вода
    cold_water_cost = cold_consumption * (45.67 if city == 'Геленджик' else 52.34)
    hot_water_cost = hot_consumption * (45.67 if city == 'Геленджик' else 52.34)
    
    items.append({
        "Услуга": "❄️ Холодная вода",
        "Расчёт": f"{cold_consumption:.1f} м³ × {45.67 if city == 'Геленджик' else 52.34} руб",
        "Сумма": cold_water_cost
    })
    
    items.append({
        "Услуга": "🔥 Горячая вода",
        "Расчёт": f"{hot_consumption:.1f} м³ × {45.67 if city == 'Геленджик' else 52.34} руб",
        "Сумма": hot_water_cost
    })
    
    # Электричество
    if city == "Пыть-Ях" and stove_type == "Электрическая":
        elec_tariff = 2.86
        elec_note = "(электроплита)"
    else:
        elec_tariff = 5.23 if city == 'Геленджик' else 4.09
        elec_note = ""
    
    elec_cost = elec_consumption * elec_tariff
    items.append({
        "Услуга": "⚡ Электроэнергия",
        "Расчёт": f"{elec_consumption:.0f} кВт·ч × {elec_tariff} руб {elec_note}",
        "Сумма": elec_cost
    })
    
    # Отопление
    items.append({
        "Услуга": "🔥 Отопление",
        "Расчёт": heating_text,
        "Сумма": heating
    })
    
    # ТКО
    items.append({
        "Услуга": "🗑 Вывоз мусора",
        "Расчёт": f"{tko_month:.2f} м³ × 1010.75 руб",
        "Сумма": tko_cost
    })
    
    # Создаём таблицу
    df = pd.DataFrame(items)
    df["Сумма"] = df["Сумма"].apply(lambda x: f"{x:.2f} ₽")
    
    st.table(df)
    
    # Итог
    total = cold_water_cost + hot_water_cost + elec_cost + heating + tko_cost
    
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

{'-'*40}
ИТОГО: {total:.2f} ₽

Тарифы утверждены РСТ на 2026 год""",
        file_name=f"jkh_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
        mime="text/plain"
    )
    
    # Совет по экономии
    st.markdown("---")
    st.markdown('<p class="info-text">💡 Установите счётчики, если их ещё нет — это поможет платить по факту, а не по нормативу.</p>', unsafe_allow_html=True)

# Нижняя часть
st.markdown("---")
st.markdown('<p class="caption-text">✅ Тарифы актуальны на 2026 год (РСТ Краснодарского края и ХМАО)</p>', unsafe_allow_html=True)
st.markdown('<p class="caption-text">📞 По вопросам: @urikonsult</p>', unsafe_allow_html=True)
