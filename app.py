st.header(L["sec1"])

col1, col2, col3 = st.columns(3)

with col1:
    use_cylinder_mode = st.radio(
        L["cyl_mode_radio"],
        [L["cyl_mode_direct"], L["cyl_mode_calc"]],
        horizontal=False
    )

with col2:
    days_per_month = st.number_input(
        L["days_per_month"],
        min_value=1,
        max_value=31,
        value=30
    )

with col3:
    st.write("")

# 1) 기본 실린더 비용(배송비 제외)
if use_cylinder_mode == L["cyl_mode_direct"]:
    monthly_cylinder_cost_base = st.number_input(
        L["cyl_monthly_direct"],
        min_value=0.0,
        value=5000.0,
        step=100.0
    )
else:
    c1, c2, c3 = st.columns(3)
    with c1:
        daily_cylinder_qty = st.number_input(
            L["cyl_daily_qty"],
            min_value=0.0,
            value=20.0,
            step=1.0
        )
    with c2:
        cylinder_cost_per_unit = st.number_input(
            L["cyl_cost_per_unit"],
            min_value=0.0,
            value=15.0,
            step=1.0
        )
    with c3:
        st.write("")

    monthly_cylinder_cost_base = daily_cylinder_qty * cylinder_cost_per_unit * days_per_month

# 2) 🔹 배송비(월) 추가
cyl_delivery_monthly = st.number_input(
    "실린더 배송비 (월, USD) / Cylinder delivery cost per month (USD)",
    min_value=0.0,
    value=0.0,
    step=50.0
)

# 배송비를 포함한 총 기본비용
monthly_cylinder_cost_base += cyl_delivery_monthly

# 3) 사용 퍼센트(75~100%)에 따른 실질 비용
usage_percent = st.selectbox(
    L["usage_percent"],
    [100, 95, 90, 85, 80, 75],
    index=0
)

# 100% 기준 비용에 사용률을 반영한 실질 비용
monthly_cylinder_cost = monthly_cylinder_cost_base * (100 / usage_percent)

st.info(
    f"{L['usage_info_prefix']}: {monthly_cylinder_cost_base:,.0f} USD → "
    f"{usage_percent}% {L['usage_info_mid']} **{monthly_cylinder_cost:,.0f} USD** {L['usage_info_suffix']}"
)

annual_cylinder_cost = monthly_cylinder_cost * 12
five_year_cylinder_cost = annual_cylinder_cost * 5
