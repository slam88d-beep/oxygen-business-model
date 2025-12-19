import streamlit as st
import pandas as pd
import io

# =========================
# 다국어 텍스트 정의
# =========================

lang_pack = {
    "ko": {
        "lang_display": "한국어",
        "sidebar_basic": "기본 설정",
        "country_label": "국가 선택",
        "sidebar_hint": "현장에서 병원 담당자와 함께 값을 입력해보세요.",
        "title": "산소발생기 비즈니스 모델 계산기",
        "subtitle": "병원 대상 실린더 vs 렌탈 vs 구매(ROI) 비교",
        "hospital_name_label": "병원 이름을 입력하세요",
        "sec1": "1. 현재 실린더 사용 비용",
        "cyl_mode_radio": "실린더 비용 입력 방식 선택",
        "cyl_mode_direct": "월간 총 비용 직접 입력",
        "cyl_mode_calc": "실린더 개수 × 단가로 계산",
        "days_per_month": "월 기준 일수 (일)",
        "cyl_monthly_direct": "현재 실린더 월간 총 비용 (USD)",
        "cyl_daily_qty": "하루 실린더 사용 개수 (EA)",
        "cyl_cost_per_unit": "실린더 1개당 가스 비용 (USD)",
        "cyl_delivery_per_unit": "실린더 1개당 배송/물류 비용 (USD)",
        "usage_percent": "실제로 실린더(40L, 150BAR)를 몇 %까지 사용하고 교체하나요?",
        "usage_info_prefix": "100% 사용 기준 월 비용",
        "sec2": "2. 산소발생기 운전 조건 및 전기요금",
        "sec2_1": "2-1. 산소발생기 산소 생산량 vs 실린더 용량",
        "gen_flow": "산소발생기 유량 (LPM)",
        "cyl_volume": "실린더 용적 (L)",
        "cyl_pressure": "실린더 충전 압력 (BAR)",
        "sec3": "3. 렌탈 모델 (OPEX)",
        "rental_monthly_fee": "월 렌탈료 (USD)",
        "rental_includes_maint": "렌탈료에 유지보수 포함",
        "rental_extra_maint": "추가 유지보수비 (월, USD)",
        "sec4": "4. 구매 모델 (CAPEX + OPEX)",
        "purchase_price": "장비 구매 가격 (USD)",
        "maintenance_annual": "연간 유지보수 비용 (USD)",
        "amort_years": "감가 기간 (년, 회계용)",
        "sec5": "5. 결과 요약 및 비교",
        "colA_title": "실린더 유지",
        "colB_title": "렌탈 모델",
        "colC_title": "구매 모델",
        "metric_month": "월 비용 (USD)",
        "metric_year": "연간 비용 (USD)",
        "metric_5year": "5년 누적 비용 (USD)",
        "sec_roi": "6. ROI 분석 및 1~5년 비용 추이",
        "footer": "※ 실제 제안 시에는 각 병원의 실제 데이터에 맞게 조정해야 합니다.",
        "print_button": "현재 화면 인쇄하기 (브라우저 인쇄 기능 사용)",
        "save_button": "현재 병원 시나리오를 CSV로 저장",
        "save_note": "저장된 CSV 파일을 모아서 병원별 비교·관리 자료로 활용할 수 있습니다.",
    },
    "en": {
        "lang_display": "English",
        "sidebar_basic": "Basic settings",
        "country_label": "Country",
        "sidebar_hint": "Enter values together with the hospital staff.",
        "title": "Oxygen Business Model Calculator",
        "subtitle": "Cylinder vs Rental vs Purchase (ROI) for Hospitals",
        "hospital_name_label": "Hospital name",
        "sec1": "1. Current cylinder oxygen cost",
        "cyl_mode_radio": "Cylinder cost input mode",
        "cyl_mode_direct": "Enter monthly total cost directly",
        "cyl_mode_calc": "Calculate: cylinders × unit price",
        "days_per_month": "Number of days per month",
        "cyl_monthly_direct": "Current monthly cylinder cost (USD)",
        "cyl_daily_qty": "Number of cylinders per day (EA)",
        "cyl_cost_per_unit": "Gas cost per cylinder (USD)",
        "cyl_delivery_per_unit": "Delivery / logistics cost per cylinder (USD)",
        "usage_percent": "Up to what % of a 40L 150BAR cylinder is used before replacement?",
        "usage_info_prefix": "Monthly cost if 100% of each cylinder is used",
        "sec2": "2. Generator operation & electricity cost",
        "sec2_1": "2-1. Generator oxygen production vs cylinder capacity",
        "gen_flow": "Generator flow rate (LPM)",
        "cyl_volume": "Cylinder water volume (L)",
        "cyl_pressure": "Cylinder charge pressure (BAR)",
        "sec3": "3. Rental model (OPEX)",
        "rental_monthly_fee": "Monthly rental fee (USD)",
        "rental_includes_maint": "Maintenance included in rental fee",
        "rental_extra_maint": "Additional maintenance cost (per month, USD)",
        "sec4": "4. Purchase model (CAPEX + OPEX)",
        "purchase_price": "Generator purchase price (USD)",
        "maintenance_annual": "Annual maintenance cost (USD)",
        "amort_years": "Depreciation period (years, accounting view)",
        "sec5": "5. Summary and comparison",
        "colA_title": "Cylinder only",
        "colB_title": "Rental model",
        "colC_title": "Purchase model",
        "metric_month": "Monthly cost (USD)",
        "metric_year": "Annual cost (USD)",
        "metric_5year": "5-year total cost (USD)",
        "sec_roi": "6. ROI analysis and 1–5 year cost trend",
        "footer": "Adjust inputs to match the actual hospital situation.",
        "print_button": "Print this view (use browser print)",
        "save_button": "Download current hospital scenario as CSV",
        "save_note": "You can collect CSV files and compare hospitals.",
    }
    # 필요하면 vi, km 도 같은 구조로 나중에 추가 가능
}

# =================
# Streamlit 기본 설정
# =================

st.set_page_config(
    page_title="Oxygen Business Model Calculator",
    layout="wide"
)

# ---- 사이드바: 언어, 국가 ----
st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Language / 언어",
    ["ko", "en"],
    index=0,
    format_func=lambda x: lang_pack[x]["lang_display"]
)
L = lang_pack[language]

country = st.sidebar.selectbox(
    L["country_label"],
    ["Cambodia", "Vietnam", "Other"]
)

st.sidebar.subheader(L["sidebar_basic"])
st.sidebar.write(L["sidebar_hint"])

# ---- 탭 구성 ----
tab_hospital, tab_dealer = st.tabs(["병원용 ROI", "리테일러 ROI", "병원 규모 기반 추천"])

# ================================
# 병원용 ROI 계산기
# ================================
with tab_hospital:
    st.title(L["title"])
    st.caption(L["subtitle"])

    hospital_name = st.text_input(L["hospital_name_label"], "")

    st.markdown("---")

    # -----------------------------
    # 1. 현재 실린더 사용 비용
    # -----------------------------
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
            delivery_cost_per_unit = st.number_input(
                L["cyl_delivery_per_unit"],
                min_value=0.0,
                value=0.0,
                step=1.0
            )

        monthly_cylinder_cost_base = (
            daily_cylinder_qty * (cylinder_cost_per_unit + delivery_cost_per_unit) * days_per_month
        )

    usage_percent = st.selectbox(
        L["usage_percent"],
        [100, 95, 90, 85, 80, 75],
        index=0
    )

    # 실질 비용 (교체 퍼센트 반영)
    monthly_cylinder_cost = monthly_cylinder_cost_base * (100.0 / usage_percent)

    info_text = (
        f"{L['usage_info_prefix']}: {round(monthly_cylinder_cost_base)} USD, "
        f"{usage_percent}% 사용 시 실질 월 비용은 {round(monthly_cylinder_cost)} USD 입니다."
    )
    st.info(info_text)

    annual_cylinder_cost = monthly_cylinder_cost * 12
    five_year_cylinder_cost = annual_cylinder_cost * 5

    # -----------------------------
    # 2. 산소발생기 운전 조건 및 전기요금
    # -----------------------------
    st.header(L["sec2"])

    col1, col2, col3 = st.columns(3)

    with col1:
        power_kw = st.number_input(
            "산소발생기 소비전력 (kW) / Power (kW)",
            min_value=0.0,
            value=7.5,
            step=0.5
        )
    with col2:
        operating_hours_per_day = st.number_input(
            "하루 운전 시간 (시간) / Operating hours per day",
            min_value=0.0,
            max_value=24.0,
            value=24.0,
            step=1.0
        )
    with col3:
        elec_tariff = st.number_input(
            "전기요금 단가 (USD/kWh) / Electricity tariff",
            min_value=0.0,
            value=0.18,
            step=0.01
        )

    monthly_energy_cost = power_kw * operating_hours_per_day * days_per_month * elec_tariff
    annual_energy_cost = monthly_energy_cost * 12

    st.write(
        f"산소발생기 전기요금 기준 월 운영비는 약 {round(monthly_energy_cost)} USD, "
        f"연간 약 {round(annual_energy_cost)} USD 입니다."
    )

    # -----------------------------
    # 2-1. 산소발생기 vs 실린더 용량 비교
    # -----------------------------
    st.header(L["sec2_1"])

    col1, col2, col3 = st.columns(3)

    with col1:
        generator_flow_lpm = st.number_input(
            f"{L['gen_flow']} (기본값 60)",
            min_value=1.0,
            value=60.0,
            step=5.0
        )
    with col2:
        cylinder_volume_l = st.number_input(
            f"{L['cyl_volume']} (기본값 40)",
            min_value=1.0,
            value=40.0,
            step=1.0
        )
    with col3:
        cylinder_pressure_bar = st.number_input(
            f"{L['cyl_pressure']} (기본값 150)",
            min_value=1.0,
            value=150.0,
            step=10.0
        )

    daily_oxygen_m3 = generator_flow_lpm * 60.0 * operating_hours_per_day / 1000.0
    cylinder_oxygen_m3 = cylinder_volume_l * cylinder_pressure_bar / 1000.0
    cylinders_per_day_equiv = daily_oxygen_m3 / cylinder_oxygen_m3 if cylinder_oxygen_m3 > 0 else 0.0
    cylinders_per_month_equiv = cylinders_per_day_equiv * days_per_month

    st.success(
        f"산소발생기 1대는 하루 약 {cylinders_per_day_equiv:.1f}병, "
        f"한 달 약 {cylinders_per_month_equiv:.0f}병의 실린더 공급량과 비슷합니다."
    )

    # -----------------------------
    # 3. 렌탈 모델
    # -----------------------------
    st.header(L["sec3"])

    col1, col2, col3 = st.columns(3)

    with col1:
        rental_monthly_fee = st.number_input(
            L["rental_monthly_fee"],
            min_value=0.0,
            value=2500.0,
            step=100.0
        )
    with col2:
        rental_includes_maintenance = st.checkbox(
            L["rental_includes_maint"],
            value=True
        )
    with col3:
        rental_extra_maintenance = st.number_input(
            L["rental_extra_maint"],
            min_value=0.0,
            value=0.0,
            step=50.0
        )

    if rental_includes_maintenance:
        rental_maintenance_monthly = 0.0
    else:
        rental_maintenance_monthly = rental_extra_maintenance

    rental_monthly_total = rental_monthly_fee + rental_maintenance_monthly + monthly_energy_cost
    rental_annual_total = rental_monthly_total * 12
    rental_five_year_total = rental_annual_total * 5

    # -----------------------------
    # 4. 구매 모델 (CAPEX + OPEX)
    # -----------------------------
    st.header(L["sec4"])

    col1, col2, col3 = st.columns(3)

    with col1:
        purchase_price = st.number_input(
            L["purchase_price"],
            min_value=0.0,
            value=18000.0,
            step=1000.0
        )
    with col2:
        maintenance_annual = st.number_input(
            L["maintenance_annual"],
            min_value=0.0,
            value=1500.0,
            step=100.0
        )
    with col3:
        amortization_years = st.number_input(
            L["amort_years"],
            min_value=1,
            max_value=15,
            value=5,
            step=1
        )

    monthly_capex = purchase_price / (amortization_years * 12.0)
    monthly_maintenance = maintenance_annual / 12.0

    purchase_monthly_opex = monthly_maintenance + monthly_energy_cost
    purchase_annual_opex = purchase_monthly_opex * 12.0

    # 회계 관점에서 보여줄 월/연 비용 (CAPEX 분할 + OPEX)
    purchase_monthly_display = monthly_capex + purchase_monthly_opex
    purchase_annual_display = purchase_monthly_display * 12.0

    # 실제 5년 총 비용 = 초기 CAPEX + 5년 OPEX
    purchase_five_year_total = purchase_price + purchase_annual_opex * 5.0

    # ROI 계산: 실린더 vs "운영비(OPEX)" 기준
    annual_saving_purchase = annual_cylinder_cost - purchase_annual_opex
    payback_years = None
    if annual_saving_purchase > 0:
        payback_years = purchase_price / annual_saving_purchase

    annual_saving_rental = annual_cylinder_cost - rental_annual_total
    rental_5yr_saving = five_year_cylinder_cost - rental_five_year_total
    purchase_5yr_saving = five_year_cylinder_cost - purchase_five_year_total

    # -----------------------------
    # 5. 결과 요약 및 비교
    # -----------------------------
    st.header(L["sec5"])

    colA, colB, colC = st.columns(3)

    with colA:
        st.subheader(L["colA_title"])
        st.metric(L["metric_month"], f"{round(monthly_cylinder_cost):,}")
        st.metric(L["metric_year"], f"{round(annual_cylinder_cost):,}")
        st.metric(L["metric_5year"], f"{round(five_year_cylinder_cost):,}")

    with colB:
        st.subheader(L["colB_title"])
        st.metric(L["metric_month"], f"{round(rental_monthly_total):,}")
        st.metric(L["metric_year"], f"{round(rental_annual_total):,}")
        st.metric(L["metric_5year"], f"{round(rental_five_year_total):,}")

    with colC:
        st.subheader(L["colC_title"])
        st.metric(L["metric_month"], f"{round(purchase_monthly_display):,}")
        st.metric(L["metric_year"], f"{round(purchase_annual_display):,}")
        st.metric(L["metric_5year"], f"{round(purchase_five_year_total):,}")

    st.markdown("---")

    # -----------------------------
    # 6. ROI 분석 및 그래프
    # -----------------------------
    st.header(L["sec_roi"])

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("렌탈 ROI")
        st.write(f"실린더 대비 연간 절감액: {round(annual_saving_rental):,} USD")
        st.write(f"5년 누적 절감액: {round(rental_5yr_saving):,} USD")
        if annual_saving_rental > 0:
            st.success("렌탈이 실린더 유지보다 비용 절감 효과가 있습니다.")
        else:
            st.warning("렌탈이 실린더 유지보다 비싸거나 비슷한 수준입니다.")

    with col2:
        st.subheader("구매 ROI")
        st.write(f"실린더 대비 연간 운영비 절감액: {round(annual_saving_purchase):,} USD")
        st.write(f"5년 누적 절감액: {round(purchase_5yr_saving):,} USD")
        if annual_saving_purchase > 0 and payback_years is not None:
            st.success(
                f"초기 투자 {round(purchase_price):,} USD 기준 예상 투자 회수 기간은 "
                f"약 {payback_years:.1f}년입니다."
            )
        else:
            st.warning("현재 입력값 기준으로 구매 모델의 투자 회수 계산이 어렵습니다.")

    years = [1, 2, 3, 4, 5]
    cyl_costs = [annual_cylinder_cost * y for y in years]
    rental_costs = [rental_annual_total * y for y in years]
    purchase_costs = [purchase_price + purchase_annual_opex * y for y in years]

    df_years = pd.DataFrame(
        {
            "Year": years,
            "Cylinder": cyl_costs,
            "Rental": rental_costs,
            "Purchase": purchase_costs,
        }
    ).set_index("Year")

    st.subheader("1~5년 누적 비용 추이")
    st.line_chart(df_years)

    st.caption(L["footer"])

    st.markdown("---")

    # 인쇄 버튼 (브라우저 인쇄 기능 호출)
    if st.button(L["print_button"]):
        st.markdown(
            "<script>window.print();</script>",
            unsafe_allow_html=True,
        )

    # -----------------------------
    # 시나리오 CSV 저장
    # -----------------------------
    st.subheader(L["save_button"])

    summary = {
        "hospital_name": hospital_name,
        "country": country,
        "days_per_month": days_per_month,
        "monthly_cylinder_cost": round(monthly_cylinder_cost, 2),
        "annual_cylinder_cost": round(annual_cylinder_cost, 2),
        "five_year_cylinder_cost": round(five_year_cylinder_cost, 2),
        "rental_monthly_total": round(rental_monthly_total, 2),
        "rental_annual_total": round(rental_annual_total, 2),
        "rental_five_year_total": round(rental_five_year_total, 2),
        "purchase_monthly_display": round(purchase_monthly_display, 2),
        "purchase_annual_display": round(purchase_annual_display, 2),
        "purchase_five_year_total": round(purchase_five_year_total, 2),
        "annual_saving_rental_vs_cylinder": round(annual_saving_rental, 2),
        "annual_saving_purchase_vs_cylinder": round(annual_saving_purchase, 2),
        "rental_5year_saving_vs_cylinder": round(rental_5yr_saving, 2),
        "purchase_5year_saving_vs_cylinder": round(purchase_5yr_saving, 2),
        "payback_years_purchase": round(payback_years, 2) if payback_years else "",
        "generator_flow_lpm": generator_flow_lpm,
        "daily_cylinders_equiv": round(cylinders_per_day_equiv, 2),
        "monthly_cylinders_equiv": round(cylinders_per_month_equiv, 2),
    }

    df_out = pd.DataFrame([summary])
    csv_buffer = io.StringIO()
    df_out.to_csv(csv_buffer, index=False)

    default_filename = (hospital_name.strip() if hospital_name else "hospital") + "_oxygen_model.csv"

    st.download_button(
        label=L["save_button"],
        data=csv_buffer.getvalue(),
        file_name=default_filename,
        mime="text/csv",
    )

    st.caption(L["save_note"])


# ====================================
# 리테일러 / 파트너용 ROI 계산기
# ====================================
with tab_dealer:
    # 언어별 텍스트 정의
    if language == "ko":
        t_title = "리테일러 / 파트너 수익 모델 (Dealer ROI)"
        t_intro = (
            "병원에 장비를 공급하는 리테일러(딜러) 입장에서 "
            "단순 판매 vs 렌탈 모델의 수익성과 회수기간을 비교합니다."
        )
        t_factory_price = "제조사 공급가 (USD)"
        t_import_cost = "수입·통관비용 (USD)"
        t_sale_price = "병원 판매가 (USD)"
        t_install_cost = "설치·교육 등 초기 비용 (USD, 일회성)"
        t_service_fee = "연간 서비스 계약 금액 (병원 청구, USD/년)"
        t_service_cost = "연간 서비스 제공 원가 (리테일러 비용, USD/년)"
        t_rental_fee = "병원 월 렌탈료 (USD)"
        t_contract_years = "렌탈 계약기간 (년)"
        t_sec_sale = "1) 단순 판매 모델"
        t_sec_rental = "2) 렌탈 모델"
        t_metric_initial_cost = "초기 총 원가 (USD)"
        t_metric_margin = "한 대당 초기 이익 (USD)"
        t_metric_margin_rate = "마진율 (%)"
        t_metric_service_net = "연간 서비스 순이익 (USD)"
        t_sale_text_1 = "공급가 + 통관 + 설치를 포함한 한 대당 총 원가입니다."
        t_sale_text_2 = "병원 판매 시 초기 이익과 마진율입니다."
        t_sale_text_3 = (
            "판매 후 2년차부터는 서비스 계약을 통해 매년 서비스 순이익이 발생한다고 가정합니다."
        )
        t_metric_initial_invest = "초기 투자금 (USD)"
        t_metric_annual_profit = "연간 순이익 (USD)"
        t_metric_payback = "투자 회수기간 (년)"
        t_rental_text_1 = "렌탈 1대 기준 초기 투자금과 연간 순이익을 기준으로 수익을 계산합니다."
        t_rental_text_2 = "계약 기간 전체에 대한 누적 순이익입니다."
        t_cashflow_title = "누적 현금흐름 (판매 vs 렌탈)"
        t_profit_title = "연도별 누적 순이익 (판매 vs 렌탈)"
        t_footer = (
            "이 탭은 리테일러(딜러) 입장에서 단순 판매와 렌탈의 장기 수익성을 "
            "비교하기 위한 도구입니다. 병원 관점의 ROI는 병원용 ROI 탭에서 확인하세요."
        )
    else:
        t_title = "Dealer / Partner Profit Model (Dealer ROI)"
        t_intro = (
            "From the dealer's perspective, compare the profitability and payback period "
            "of one-off sale vs rental to hospitals."
        )
        t_factory_price = "Factory price (USD)"
        t_import_cost = "Import & customs cost (USD)"
        t_sale_price = "Sales price to hospital (USD)"
        t_install_cost = "Installation & training cost (USD, one-time)"
        t_service_fee = "Annual service contract fee charged to hospital (USD/year)"
        t_service_cost = "Annual service delivery cost for dealer (USD/year)"
        t_rental_fee = "Monthly rental fee to hospital (USD)"
        t_contract_years = "Rental contract period (years)"
        t_sec_sale = "1) One-off sales model"
        t_sec_rental = "2) Rental model"
        t_metric_initial_cost = "Initial total cost (USD)"
        t_metric_margin = "Margin per unit (USD)"
        t_metric_margin_rate = "Margin rate (%)"
        t_metric_service_net = "Annual service net profit (USD)"
        t_sale_text_1 = "Total cost per unit including factory price, import and installation."
        t_sale_text_2 = "Initial margin and margin rate when selling to a hospital."
        t_sale_text_3 = (
            "From year 2, an annual service contract generates additional net profit."
        )
        t_metric_initial_invest = "Initial investment (USD)"
        t_metric_annual_profit = "Annual net profit (USD)"
        t_metric_payback = "Payback period (years)"
        t_rental_text_1 = "Rental profit is calculated from initial investment and annual net profit."
        t_rental_text_2 = "This is the cumulative net profit over the full contract period."
        t_cashflow_title = "Cumulative cash flow (Sale vs Rental)"
        t_profit_title = "Cumulative profit by year (Sale vs Rental)"
        t_footer = (
            "This tab is for comparing long-term profitability of sale vs rental "
            "from the dealer's point of view. Hospital-side ROI is in the first tab."
        )

    st.title(t_title)
    st.markdown(t_intro)
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        factory_price = st.number_input(
            t_factory_price,
            min_value=0.0,
            value=12000.0,
            step=500.0,
        )
        import_cost = st.number_input(
            t_import_cost,
            min_value=0.0,
            value=1000.0,
            step=100.0,
        )
        dealer_sale_price = st.number_input(
            t_sale_price,
            min_value=0.0,
            value=18000.0,
            step=500.0,
        )
        dealer_install_cost = st.number_input(
            t_install_cost,
            min_value=0.0,
            value=500.0,
            step=100.0,
        )

    with col2:
        service_fee_year = st.number_input(
            t_service_fee,
            min_value=0.0,
            value=1500.0,
            step=100.0,
        )
        service_cost_year = st.number_input(
            t_service_cost,
            min_value=0.0,
            value=800.0,
            step=100.0,
        )
        dealer_rental_fee = st.number_input(
            t_rental_fee,
            min_value=0.0,
            value=2500.0,
            step=100.0,
        )
        rental_contract_years = st.number_input(
            t_contract_years,
            min_value=1,
            max_value=10,
            value=5,
            step=1,
        )

    st.markdown("---")

    # 공통: 한 대 기준 초기 총 원가
    initial_unit_cost = factory_price + import_cost + dealer_install_cost

    # 서비스 계약 연간 순이익 (리테일러 입장)
    service_net_profit_year = service_fee_year - service_cost_year

    # ① 단순 판매 모델
    st.subheader(t_sec_sale)

    sale_initial_margin = dealer_sale_price - initial_unit_cost
    sale_margin_rate = (sale_initial_margin / dealer_sale_price * 100.0) if dealer_sale_price > 0 else 0.0

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric(t_metric_initial_cost, f"{round(initial_unit_cost):,}")
    with col_s2:
        st.metric(t_metric_margin, f"{round(sale_initial_margin):,}")
    with col_s3:
        st.metric(t_metric_margin_rate, f"{sale_margin_rate:.1f}")

    st.metric(t_metric_service_net, f"{round(service_net_profit_year):,}")

    st.markdown(
        f"- {t_sale_text_1} ≈ {round(initial_unit_cost):,} USD\n"
        f"- {t_sale_text_2} ≈ {round(sale_initial_margin):,} USD, {sale_margin_rate:.1f}%\n"
        f"- {t_sale_text_3}"
    )

    st.markdown("---")

       # ② 렌탈 모델
    st.subheader(t_sec_rental)

    initial_invest_rental = initial_unit_cost
    # 렌탈 연간 순이익 = 연간 렌탈료 - 연간 서비스 제공 원가
    annual_profit_rental = dealer_rental_fee * 12.0 - service_cost_year

    payback_years_dealer = None
    if annual_profit_rental > 0:
        payback_years_dealer = initial_invest_rental / annual_profit_rental

    total_profit_rental_contract = -initial_invest_rental + annual_profit_rental * rental_contract_years

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.metric(t_metric_initial_invest, f"{round(initial_invest_rental):,}")
    with col_r2:
        st.metric(t_metric_annual_profit, f"{round(annual_profit_rental):,}")
    with col_r3:
        if payback_years_dealer:
            st.metric(t_metric_payback, f"{payback_years_dealer:.1f}")
        else:
            st.metric(t_metric_payback, "N/A")

    st.markdown(
        f"- {t_rental_text_1}\n"
        f"- {t_rental_text_2} (≈ {round(total_profit_rental_contract):,} USD)"
    )

    st.markdown("---")

    # 누적 현금흐름 그래프 (판매 vs 렌탈)
    st.subheader(t_cashflow_title)

    years_cf = list(range(0, rental_contract_years + 1))
    cash_rental = []
    cash_sale = []

    for y in years_cf:
        if y == 0:
            # 연 0: 판매는 장비 판매 마진만, 렌탈은 초기 투자만
            cash_rental.append(-initial_invest_rental)
            cash_sale.append(sale_initial_margin)
        else:
            # 렌탈: 초기 투자 + 매년 렌탈 수익
            rental_cf = -initial_invest_rental + annual_profit_rental * y

            # 판매: 초기 마진 + (2년차부터 서비스 순이익 누적)
            service_years = max(0, y - 1)
            sale_cf = sale_initial_margin + service_net_profit_year * service_years

            cash_rental.append(rental_cf)
            cash_sale.append(sale_cf)

    df_cash = pd.DataFrame(
        {"Year": years_cf, "Rental": cash_rental, "Sale": cash_sale}
    ).set_index("Year")

    st.line_chart(df_cash)

    # 연도별 누적 순이익 (판매 vs 렌탈)
    st.subheader(t_profit_title)

    years_profit = list(range(1, rental_contract_years + 1))
    sale_profits = []
    rental_profits = []

    for y in years_profit:
        rental_total = -initial_invest_rental + annual_profit_rental * y
        rental_profits.append(rental_total)

        service_years = max(0, y - 1)
        sale_total = sale_initial_margin + service_net_profit_year * service_years
        sale_profits.append(sale_total)

    df_profit = pd.DataFrame(
        {"Year": years_profit, "Sale": sale_profits, "Rental": rental_profits}
    ).set_index("Year")

    st.bar_chart(df_profit)

    st.caption(t_footer)

with tab_sizing:
    # -----------------------------
    # 병원 규모 기반 수요 추정 & 모델 추천 (30 LPM / 60 LPM)
    # -----------------------------
    if language == "ko":
        title = "병원 규모 기반 산소발생기 필요 수량 계산"
        intro = "병원의 아울렛/ICU/수술실(OR) 규모를 바탕으로 예상 산소 수요(LPM)를 추정하고, 30LPM/60LPM 모델 필요 대수를 추천합니다."
        sec1 = "1) 병원 규모 입력"
        sec2 = "2) 수요 가정(조정 가능)"
        sec3 = "3) 결과 및 추천"
        outlets_label = "일반 병동 아울렛 개수 (개)"
        icu_label = "ICU 베드(또는 ICU 아울렛) 개수 (개)"
        or_label = "OR(수술실) 개수 (개)"
        avg_outlet_lpm_label = "일반 아울렛 평균 사용량 (LPM/아울렛)"
        avg_icu_lpm_label = "ICU 평균 사용량 (LPM/ICU)"
        avg_or_lpm_label = "OR 평균 사용량 (LPM/OR)"
        simult_label = "동시 사용률(%)"
        safety_label = "안전계수(%)"
        redundancy_label = "N+예비 대수 (대)"
        u03_cap_label = "RAK-U03M2E 용량 (LPM)"
        u06_cap_label = "RAK-U06M2E 용량 (LPM)"
        demand_text = "예상 필요 유량"
        rec_text = "추천"
        explain_text = "계산 방식: (아울렛×가정LPM + ICU×가정LPM + OR×가정LPM) × 동시사용률 × 안전계수"
    else:
        title = "Sizing Recommendation by Hospital Scale"
        intro = "Estimate oxygen demand (LPM) from outlets/ICU/OR and recommend required units for 30 LPM and 60 LPM models."
        sec1 = "1) Hospital scale inputs"
        sec2 = "2) Assumptions (adjustable)"
        sec3 = "3) Results & recommendation"
        outlets_label = "General ward outlets (count)"
        icu_label = "ICU beds/outlets (count)"
        or_label = "OR rooms (count)"
        avg_outlet_lpm_label = "Avg usage per general outlet (LPM)"
        avg_icu_lpm_label = "Avg usage per ICU (LPM)"
        avg_or_lpm_label = "Avg usage per OR (LPM)"
        simult_label = "Simultaneous usage rate (%)"
        safety_label = "Safety factor (%)"
        redundancy_label = "N+ standby units"
        u03_cap_label = "RAK-U03M2E capacity (LPM)"
        u06_cap_label = "RAK-U06M2E capacity (LPM)"
        demand_text = "Estimated required flow"
        rec_text = "Recommendation"
        explain_text = "Formula: (Outlets×LPM + ICU×LPM + OR×LPM) × simult. rate × safety factor"

    st.title(title)
    st.caption(intro)

    st.markdown("---")
    st.subheader(sec1)

    c1, c2, c3 = st.columns(3)
    with c1:
        outlets = st.number_input(outlets_label, min_value=0, value=50, step=1)
    with c2:
        icu = st.number_input(icu_label, min_value=0, value=10, step=1)
    with c3:
        or_rooms = st.number_input(or_label, min_value=0, value=2, step=1)

    st.markdown("---")
    st.subheader(sec2)

    a1, a2, a3 = st.columns(3)
    with a1:
        avg_outlet_lpm = st.number_input(avg_outlet_lpm_label, min_value=0.0, value=3.0, step=0.5)
        simult_rate = st.number_input(simult_label, min_value=1.0, max_value=100.0, value=40.0, step=5.0) / 100.0
    with a2:
        avg_icu_lpm = st.number_input(avg_icu_lpm_label, min_value=0.0, value=10.0, step=1.0)
        safety_factor = st.number_input(safety_label, min_value=100.0, max_value=250.0, value=120.0, step=5.0) / 100.0
    with a3:
        avg_or_lpm = st.number_input(avg_or_lpm_label, min_value=0.0, value=15.0, step=1.0)
        redundancy_n = st.number_input(redundancy_label, min_value=0, max_value=5, value=1, step=1)

    # 모델 용량 (고정값이지만 수정 가능하게 열어둠)
    b1, b2 = st.columns(2)
    with b1:
        cap_u03 = st.number_input(u03_cap_label, min_value=1.0, value=30.0, step=1.0)
    with b2:
        cap_u06 = st.number_input(u06_cap_label, min_value=1.0, value=60.0, step=1.0)

    st.caption(explain_text)

    # -----------------------------
    # 계산
    # -----------------------------
    base_demand = outlets * avg_outlet_lpm + icu * avg_icu_lpm + or_rooms * avg_or_lpm
    required_lpm = base_demand * simult_rate * safety_factor

    # 필요 대수(예비 N대 추가)
    import math
    units_u03 = math.ceil(required_lpm / cap_u03) + int(redundancy_n)
    units_u06 = math.ceil(required_lpm / cap_u06) + int(redundancy_n)

    st.markdown("---")
    st.subheader(sec3)

    colA, colB, colC = st.columns(3)
    with colA:
        st.metric(demand_text + " (LPM)", f"{required_lpm:,.1f}")
        st.caption(f"Base (no factors): {base_demand:,.1f} LPM")

    with colB:
        st.metric("RAK-U03M2E (30 LPM) 필요 수량" if language == "ko" else "RAK-U03M2E units needed", f"{units_u03} 대" if language == "ko" else f"{units_u03} units")

    with colC:
        st.metric("RAK-U06M2E (60 LPM) 필요 수량" if language == "ko" else "RAK-U06M2E units needed", f"{units_u06} 대" if language == "ko" else f"{units_u06} units")

    # 추천 로직: "대수 최소" 기준으로 추천 (현장 설명에 단순/명확)
    # (원하면 향후 CAPEX, 설치공간, 예비품, MTBF 등으로 가중치 확장 가능)
    if units_u06 < units_u03:
        rec_model = "RAK-U06M2E (60 LPM)"
        rec_qty = units_u06
    elif units_u03 < units_u06:
        rec_model = "RAK-U03M2E (30 LPM)"
        rec_qty = units_u03
    else:
        # 동일하면 60 LPM을 기본 추천(설치/운영 단순성)
        rec_model = "RAK-U06M2E (60 LPM)"
        rec_qty = units_u06

    if language == "ko":
        st.success(f"추천하는 제품의 종류 및 수량은 **{rec_model} {rec_qty}대** 입니다.")
        st.write(
            "참고: 실제 현장에서는 배관압력(MGPS), 피크 사용 패턴, 산소 순도/압력 요구, "
            "백업 실린더/LOX 운용 여부, 전원 안정성 등을 함께 반영해 최종 설계를 확정하는 것을 권장합니다."
        )
    else:
        st.success(f"Recommended model & quantity: **{rec_model} × {rec_qty}**.")
        st.write(
            "Note: Final sizing should consider peak usage profile, MGPS pressure requirement, "
            "backup source strategy (cylinder/LOX), and power stability."
        )


