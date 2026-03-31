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
    
    # ========== РЕДАКТИРОВАНИЕ ТАРИФОВ (ТОЛЬКО ДЛЯ АДМИНА) ==========
    with st.expander("🔒 Редактировать тарифы (для администратора)"):
        admin_password = st.text_input("Введите пароль:", type="password", key="admin_pass")
        
        if admin_password == "ваш_пароль":  # Замените на свой пароль
            st.success("✅ Доступ разрешён")
            
            st.markdown("**Водоснабжение**")
            cold_water = st.number_input(
                "Холодная вода (руб/м³)", 
                value=float(st.session_state.tariffs[city]['cold_water']),
                step=0.5,
                key="cold_water_input"
            )
            hot_water = st.number_input(
                "Горячая вода (руб/м³)", 
                value=float(st.session_state.tariffs[city]['hot_water']),
                step=0.5,
                key="hot_water_input"
            )
            
            st.markdown("**Электроснабжение**")
            electricity_gas = st.number_input(
                "Электричество (газовая плита, руб/кВт·ч)", 
                value=float(st.session_state.tariffs[city]['electricity_gas']),
                step=0.1,
                key="elec_gas_input"
            )
            if city == "Пыть-Ях":
                electricity_elec = st.number_input(
                    "Электричество (электроплита, руб/кВт·ч)", 
                    value=float(st.session_state.tariffs[city]['electricity_elec']),
                    step=0.1,
                    key="elec_elec_input"
                )
                st.session_state.tariffs[city]['electricity_elec'] = electricity_elec
            
            st.markdown("**Отопление**")
            if city == "Геленджик":
                heating = st.number_input(
                    "Отопление (руб/м²)", 
                    value=float(st.session_state.tariffs[city]['heating']),
                    step=0.5,
                    key="heating_input"
                )
                st.session_state.tariffs[city]['heating'] = heating
            else:
                heating_gcal = st.number_input(
                    "Отопление (руб/Гкал)", 
                    value=float(st.session_state.tariffs[city]['heating_gcal']),
                    step=10.0,
                    key="heating_gcal_input"
                )
                st.session_state.tariffs[city]['heating_gcal'] = heating_gcal
            
            st.markdown("**ТКО (мусор)**")
            tko = st.number_input(
                "ТКО (руб/м³)", 
                value=float(st.session_state.tariffs[city]['tko']),
                step=10.0,
                key="tko_input"
            )
            
            # Сохраняем изменённые значения
            st.session_state.tariffs[city]['cold_water'] = cold_water
            st.session_state.tariffs[city]['hot_water'] = hot_water
            st.session_state.tariffs[city]['electricity_gas'] = electricity_gas
            st.session_state.tariffs[city]['tko'] = tko
            
            st.caption("💡 Изменённые тарифы сохраняются до перезагрузки страницы")
        elif admin_password:
            st.error("❌ Неверный пароль")
        else:
            st.info("🔐 Введите пароль для редактирования тарифов")
    
    # ========== НОРМАТИВНЫЕ АКТЫ (ВИДИТ ВСЕ) ==========
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
