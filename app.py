import streamlit as st
import pandas as pd
import io

# =========================
# 🔶 Multi-language dictionary
# =========================

lang_pack = {
    "ko": {
        "lang_label": "언어 선택",
        "lang_display": "한국어",
        "country_label": "국가 선택",
        "sidebar_basic": "기본 설정",
        "sidebar_hint": "현장에서 병원 담당자와 함께 값을 입력해보세요.",
        "title": "산소발생기 비즈니스 모델 계산기",
        "subtitle": "캄보디아 / 베트남 병원 대상 렌탈 vs 구매(ROI) vs 실린더 유지 비교 데모",
        "hospital_name_label": "병원 이름을 입력하세요",
        "print_button": "화면 인쇄하기 (Ctrl+P)",
        "save_button": "현재 시나리오를 파일로 저장 (CSV 다운로드)",
        "save_note": "※ 저장된 CSV 파일을 모아서 병원별 비교·관리 자료로 활용할 수 있습니다.",
        "sec1": "1. 현재 실린더 사용 비용",
        "sec2": "2. 산소발생기 운전 조건 및 전기요금",
        "sec2_1": "2-1. 산소발생기 산소 생산량 vs 실린더 용량 비교",
        "sec3": "3. 렌탈 모델",
        "sec4": "4. 구매 모델 (CAPEX + OPEX)",
        "sec5": "5. 결과 비교",
        "sec_roi": "6. ROI 분석 (렌탈 / 구매)",
        "cyl_mode_radio": "실린더 비용 입력 방식 선택",
        "cyl_mode_direct": "월간 총 비용 직접 입력",
        "cyl_mode_calc": "실린더 개수 × 단가로 계산",
        "days_per_month": "월 기준 일수 (일)",
        "cyl_monthly_direct": "현재 실린더 월간 총 비용 (USD)",
        "cyl_daily_qty": "하루 실린더 사용 개수 (EA)",
        "cyl_cost_per_unit": "실린더 1개당 비용 (충전+물류 포함, USD)",
        "usage_percent": "실제로 실린더(40L, 150BAR)를 몇 %까지 사용하고 교체하나요?",
        "usage_info_prefix": "100% 사용 기준 월 비용",
        "usage_info_mid": "사용 후 교체 시 실질 비용은",
        "usage_info_suffix": "입니다.",
        "energy_info": "📌 전기요금 기준 산소발생기 운영비 = 월",
        "gen_flow": "산소발생기 유량 (LPM)",
        "cyl_volume": "실린더 용적 (L)",
        "cyl_pressure": "실린더 충전 압력 (BAR)",
        "gen_vs_cyl_line": "👉 산소발생기 1대 = 하루 {day_cyl:.1f} 병/일, 약 {mon_cyl:.0f} 병/월 공급량과 동일",
        "rental_monthly_fee": "월 렌탈료 (USD)",
        "rental_includes_maint": "렌탈료에 유지보수 포함",
        "rental_extra_maint": "추가 유지보수비 (월, USD)",
        "purchase_price": "장비 구매 가격 (USD)",
        "maintenance_annual": "연간 유지보수 비용 (USD)",
        "amort_years": "투자 회수(감가) 기간 (년)",
        "colA_title": "실린더 유지",
        "colB_title": "렌탈 모델",
        "colC_title": "구매 모델",
        "metric_month": "월 비용 (USD)",
        "metric_year": "연간 비용 (USD)",
        "metric_5year": "5년 비용 (USD)",
        "roi_saving_success": "✔ 구매 시 실린더 대비 연간 {saving:,0f} USD 절감 예상",
        "roi_saving_warning": "❗ 구매 모델이 실린더보다 비용이 높거나 비슷합니다.",
        "roi_payback_info": "▶ 투자 회수 기간: 약 {years:.1f}년",
        "roi_payback_impossible": "투자 회수 계산이 불가능하거나 적자가 예상됩니다.",
        "footer": "※ 실제 데이터 기반 제안 시 입력값을 조정하세요."
    },
    "en": {
        "lang_label": "Language",
        "lang_display": "English",
        "country_label": "Country",
        "sidebar_basic": "Basic Settings",
        "sidebar_hint": "Enter hospital-specific values together with the client.",
        "title": "Oxygen Business Model Calculator",
        "subtitle": "Rental vs Purchase (ROI) vs Cylinder-only Cost Demo for Hospitals",
        "hospital_name_label": "Enter hospital name",
        "print_button": "Print this view (Ctrl+P)",
        "save_button": "Save current scenario as CSV",
        "save_note": "※ You can collect these CSVs to manage and compare hospitals.",
        "sec1": "1. Current Cylinder Oxygen Cost",
        "sec2": "2. Oxygen Generator Operation & Electricity Cost",
        "sec2_1": "2-1. Generator Oxygen Production vs Cylinder Capacity",
        "sec3": "3. Rental Model",
        "sec4": "4. Purchase Model (CAPEX + OPEX)",
        "sec5": "5. Cost Comparison",
        "sec_roi": "6. ROI Analysis (Rental & Purchase)",
        "cyl_mode_radio": "Cylinder cost input method",
        "cyl_mode_direct": "Enter monthly total cost directly",
        "cyl_mode_calc": "Calculate: quantity × unit price",
        "days_per_month": "Number of days per month",
        "cyl_monthly_direct": "Current monthly cylinder cost (USD)",
        "cyl_daily_qty": "Number of cylinders per day (EA)",
        "cyl_cost_per_unit": "Cost per cylinder (incl. refill & logistics, USD)",
        "usage_percent": "Up to what % of a cylinder (40L, 150BAR) is actually used before replacement?",
        "usage_info_prefix": "Monthly cost assuming 100% usage",
        "usage_info_mid": "→ with replacement at this % usage, effective monthly cost is",
        "usage_info_suffix": "",
        "energy_info": "📌 Electricity-based generator operating cost per month =",
        "gen_flow": "Generator flow rate (LPM)",
        "cyl_volume": "Cylinder water volume (L)",
        "cyl_pressure": "Cylinder charge pressure (BAR)",
        "gen_vs_cyl_line": "👉 One generator ≈ {day_cyl:.1f} cylinders/day, about {mon_cyl:.0f} cylinders/month",
        "rental_monthly_fee": "Monthly rental fee (USD)",
        "rental_includes_maint": "Maintenance included in rental fee",
        "rental_extra_maint": "Additional maintenance cost (per month, USD)",
        "purchase_price": "Generator purchase price (USD)",
        "maintenance_annual": "Annual maintenance cost (USD)",
        "amort_years": "Payback / depreciation period (years)",
        "colA_title": "Cylinder Only",
        "colB_title": "Rental Model",
        "colC_title": "Purchase Model",
        "metric_month": "Monthly cost (USD)",
        "metric_year": "Annual cost (USD)",
        "metric_5year": "5-year cost (USD)",
        "roi_saving_success": "✔ Purchase saves approx. {saving:,.0f} USD per year vs cylinders.",
        "roi_saving_warning": "❗ Purchase model is not cheaper than cylinders with current inputs.",
        "roi_payback_info": "▶ Estimated payback period: {years:.1f} years",
        "roi_payback_impossible": "Payback cannot be achieved or would be negative with current inputs.",
        "footer": "※ Adjust inputs to reflect the actual hospital situation."
    },
    "vi": {
        "lang_label": "Chọn ngôn ngữ",
        "lang_display": "Tiếng Việt",
        "country_label": "Quốc gia",
        "sidebar_basic": "Cài đặt cơ bản",
        "sidebar_hint": "Nhập số liệu theo thực tế của bệnh viện cùng với khách hàng.",
        "title": "Công cụ tính mô hình kinh doanh máy tạo oxy",
        "subtitle": "Demo so sánh Thuê vs Mua (ROI) so với dùng bình oxy cho bệnh viện",
        "hospital_name_label": "Nhập tên bệnh viện",
        "print_button": "In màn hình này (Ctrl+P)",
        "save_button": "Lưu kịch bản hiện tại thành file CSV",
        "save_note": "※ Có thể gom các file CSV để quản lý và so sánh theo từng bệnh viện.",
        "sec1": "1. Chi phí sử dụng bình oxy hiện tại",
        "sec2": "2. Điều kiện vận hành & chi phí điện của máy tạo oxy",
        "sec2_1": "2-1. Sản lượng oxy máy tạo vs dung tích bình oxy",
        "sec3": "3. Mô hình thuê",
        "sec4": "4. Mô hình mua (CAPEX + OPEX)",
        "sec5": "5. So sánh chi phí",
        "sec_roi": "6. Phân tích ROI (Thuê & Mua)",
        "cyl_mode_radio": "Cách nhập chi phí bình oxy",
        "cyl_mode_direct": "Nhập trực tiếp tổng chi phí/tháng",
        "cyl_mode_calc": "Tính: số bình × đơn giá",
        "days_per_month": "Số ngày trong tháng",
        "cyl_monthly_direct": "Tổng chi phí bình oxy/tháng (USD)",
        "cyl_daily_qty": "Số bình oxy sử dụng mỗi ngày (bình/ngày)",
        "cyl_cost_per_unit": "Chi phí 1 bình (gồm nạp & vận chuyển, USD)",
        "usage_percent": "Thực tế dùng khoảng bao nhiêu % dung tích bình (40L, 150BAR) trước khi thay?",
        "usage_info_prefix": "Chi phí/tháng nếu dùng 100%",
        "usage_info_mid": "→ với tỷ lệ sử dụng này, chi phí thực tế/tháng là",
        "usage_info_suffix": "",
        "energy_info": "📌 Chi phí điện vận hành máy tạo oxy/tháng ≈",
        "gen_flow": "Lưu lượng máy tạo oxy (LPM)",
        "cyl_volume": "Thể tích bình (L)",
        "cyl_pressure": "Áp suất nạp bình (BAR)",
        "gen_vs_cyl_line": "👉 1 máy tạo oxy ≈ {day_cyl:.1f} bình/ngày, khoảng {mon_cyl:.0f} bình/tháng",
        "rental_monthly_fee": "Phí thuê máy/tháng (USD)",
        "rental_includes_maint": "Đã bao gồm bảo trì trong phí thuê",
        "rental_extra_maint": "Chi phí bảo trì bổ sung/tháng (USD)",
        "purchase_price": "Giá mua máy (USD)",
        "maintenance_annual": "Chi phí bảo trì hàng năm (USD)",
        "amort_years": "Thời gian hoàn vốn/khấu hao (năm)",
        "colA_title": "Chỉ dùng bình oxy",
        "colB_title": "Mô hình thuê",
        "colC_title": "Mô hình mua",
        "metric_month": "Chi phí/tháng (USD)",
        "metric_year": "Chi phí/năm (USD)",
        "metric_5year": "Chi phí 5 năm (USD)",
        "roi_saving_success": "✔ Mua máy giúp tiết kiệm khoảng {saving:,0f} USD/năm so với chỉ dùng bình.",
        "roi_saving_warning": "❗ Với số liệu hiện tại, mô hình mua không rẻ hơn dùng bình.",
        "roi_payback_info": "▶ Thời gian hoàn vốn ước tính: {years:.1f} năm",
        "roi_payback_impossible": "Không thể hoàn vốn hoặc hoàn vốn âm với số liệu hiện tại.",
        "footer": "※ Cần điều chỉnh số liệu cho phù hợp với từng bệnh viện."
    },
    "km": {
        "lang_label": "ជ្រើសរើស​ភាសា",
        "lang_display": "ភាសាខ្មែរ",
        "country_label": "ប្រទេស",
        "sidebar_basic": "ការកំណត់មូលដ្ឋាន",
        "sidebar_hint": "សូមបញ្ចូលទិន្នន័យតាមស្ថានភាពពិតរបស់មន្ទីរពេទ្យជាមួយអតិថិជន។",
        "title": "គណនាម៉ូដែល​អាជីវកម្ម​ម៉ាស៊ីនផលិតអុកស៊ីសែន",
        "subtitle": "ការប្រៀបធៀបជួល និងទិញ (ROI) ប្រៀបធៀបនឹងប្រើស៊ីឡាំងតែប៉ុណ្ណោះ",
        "hospital_name_label": "បញ្ចូលឈ្មោះមន្ទីរពេទ្យ",
        "print_button": "បោះពុម្ពទំព័រនេះ (Ctrl+P)",
        "save_button": "រក្សាទុកសេណារីយ៉ូជា CSV",
        "save_note": "※ អ្នកអាចប្រមូល CSV ទាំងនេះដើម្បីគ្រប់គ្រង និងប្រៀបធៀបមន្ទីរពេទ្យ។",
        "sec1": "1. ចំណាយប្រើប្រាស់ស៊ីឡាំងអុកស៊ីសែនបច្ចុប្បន្ន",
        "sec2": "2. លក្ខខណ្ឌបើកបរ និងថ្លៃអគ្គិសនីរបស់ម៉ាស៊ីន",
        "sec2_1": "2-1. បរិមាណអុកស៊ីសែនពីម៉ាស៊ីន ប្រៀបធៀបនឹងស៊ីឡាំង",
        "sec3": "3. គំរូជួល",
        "sec4": "4. គំរូទិញ (CAPEX + OPEX)",
        "sec5": "5. សង្ខេបប្រៀបធៀបចំណាយ",
        "sec_roi": "6. វិភាគ ROI (ជួល / ទិញ)",
        "cyl_mode_radio": "របៀបបញ្ចូលថ្លៃស៊ីឡាំង",
        "cyl_mode_direct": "បញ្ចូលថ្លៃសរុបក្នុងមួយខែដោយផ្ទាល់",
        "cyl_mode_calc": "គណនា៖ ចំនួនស៊ីឡាំង × តម្លៃ",
        "days_per_month": "ចំនួនថ្ងៃក្នុងមួយខែ",
        "cyl_monthly_direct": "ថ្លៃប្រើស៊ីឡាំងក្នុងមួយខែ (USD)",
        "cyl_daily_qty": "ចំនួនស៊ីឡាំងប្រើក្នុងមួយថ្ងៃ (ប៊ូទុុង/ថ្ងៃ)",
        "cyl_cost_per_unit": "ថ្លៃស៊ីឡាំងមួយ (រួមទាំងបញ្ចូលឧស្ម័ន និងដឹកជញ្ជូន, USD)",
        "usage_percent": "ជាក់ស្តែងប្រើបានប្រហែលប៉ុន្មាន % នៃស៊ីឡាំង (40L, 150BAR) មុនពេលប្ដូរ?",
        "usage_info_prefix": "ចំណាយក្នុងមួយខែ ប្រសិនបើប្រើ 100%",
        "usage_info_mid": "→ ជាមួយតម្លៃភាគរយនេះ ចំណាយពិតក្នុងមួយខែ​គឺ",
        "usage_info_suffix": "",
        "energy_info": "📌 ចំណាយអគ្គិសនីបើកម៉ាស៊ីនក្នុងមួយខែ ≈",
        "gen_flow": "លំហូរអុកស៊ីសែនពីម៉ាស៊ីន (LPM)",
        "cyl_volume": "មាឌស៊ីឡាំង (L)",
        "cyl_pressure": "សម្ពាធបំពេញស៊ីឡាំង (BAR)",
        "gen_vs_cyl_line": "👉 ម៉ាស៊ីន 1 គ្រឿង ≈ {day_cyl:.1f} ស៊ីឡាំង/ថ្ងៃ ប្រហាក់ប្រហែល {mon_cyl:.0f} ស៊ីឡាំង/ខែ",
        "rental_monthly_fee": "ថ្លៃជួលក្នុងមួយខែ (USD)",
        "rental_includes_maint": "រួមបញ្ចូលថ្លៃថែទាំក្នុងថ្លៃជួលរួចហើយ",
        "rental_extra_maint": "ថ្លៃថែទាំបន្ថែមក្នុងមួយខែ (USD)",
        "purchase_price": "តម្លៃទិញម៉ាស៊ីន (USD)",
        "maintenance_annual": "ថ្លៃថែទាំប្រចាំឆ្នាំ (USD)",
        "amort_years": "រយៈពេលសងทุน/ចំណាយ (ឆ្នាំ)",
        "colA_title": "ប្រើតែស៊ីឡាំង",
        "colB_title": "គំរូជួល",
        "colC_title": "គំរូទិញ",
        "metric_month": "ចំណាយក្នុងមួយខែ (USD)",
        "metric_year": "ចំណាយក្នុងមួយឆ្នាំ (USD)",
        "metric_5year": "ចំណាយរយៈពេល 5 ឆ្នាំ (USD)",
        "roi_saving_success": "✔ ទិញម៉ាស៊ីនអាចសន្សំបានប្រហែល {saving:,0f} USD ក្នុងមួយឆ្នាំ ប្រៀបធៀបនឹងប្រើស៊ីឡាំងប៉ុណ្ណោះ។",
        "roi_saving_warning": "❗ ជាមួយទិន្នន័យបច្ចុប្បន្ន គំរូទិញមិនសន្សំចំណាយជាងប្រើស៊ីឡាំងទេ។",
        "roi_payback_info": "▶ រយៈពេលសងទុនប្រហែល {years:.1f} ឆ្នាំ",
        "roi_payback_impossible": "មិនអាចសងទុនឬអាចនឹងខាតបង់ទុនជាមួយទិន្នន័យបច្ចុប្បន្ន។",
        "footer": "※ សូមកែប្រែទិន្នន័យឲ្យសមរម្យតាមស្ថានភាពពិតនៃមន្ទីរពេទ្យ។"
    }
}

# =================
# 🔶 Streamlit UI
# =================

st.set_page_config(
    page_title="Oxygen Business Model Calculator",
    layout="wide"
)

# ---- Sidebar: language & country ----
st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Language / 언어 / Ngôn ngữ / ភាសា",
    ["ko", "en", "vi", "km"],
    index=0,
    format_func=lambda x: lang_pack[x]["lang_display"]
)
L = lang_pack[language]

st.sidebar.subheader(L["sidebar_basic"])
country = st.sidebar.selectbox(
    L["country_label"],
    ["Cambodia", "Vietnam", "Other"]
)
st.sidebar.markdown("---")
st.sidebar.write(L["sidebar_hint"])

# ---- Tabs ----
tab_hospital, tab_dealer = st.tabs(["🏥 Hospital / 병원", "🤝 Dealer / 리테일러"])

# ================================
# 🏥 병원용 ROI 계산기 (기존 기능)
# ================================
with tab_hospital:
    # ---- Title ----
    st.title(L["title"])
    st.caption(L["subtitle"])

    # ---- Hospital name ----
    hospital_name = st.text_input(L["hospital_name_label"], "")

    st.markdown("---")

    # -----------------------------
    # 1. 현재 실린더 사용 비용 입력
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
            st.write("")

        monthly_cylinder_cost_base = daily_cylinder_qty * cylinder_cost_per_unit * days_per_month

    usage_percent = st.selectbox(
        L["usage_percent"],
        [100, 95, 90, 85, 80, 75],
        index=0
    )

    monthly_cylinder_cost = monthly_cylinder_cost_base * (100 / usage_percent)

    st.info(
        f"{L['usage_info_prefix']}: {monthly_cylinder_cost_base:,0f} USD → "
        f"{usage_percent}% {L['usage_info_mid']} **{monthly_cylinder_cost:,0f} USD** {L['usage_info_suffix']}"
    )

    annual_cylinder_cost = monthly_cylinder_cost * 12
    five_year_cylinder_cost = annual_cylinder_cost * 5

    # -----------------------------
    # 2. 산소발생기 공통 운전 조건 (전기/운전시간)
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
        f"{L['energy_info']} **{monthly_energy_cost:,0f} USD** "
        f"(≈ {annual_energy_cost:,0f} USD / year)"
    )

    # -----------------------------
    # 2-1. 산소발생기 vs 실린더 용량 비교
    # -----------------------------
    st.header(L["sec2_1"])

    col1, col2, col3 = st.columns(3)

    with col1:
        generator_flow_lpm = st.number_input(
            f"{L['gen_flow']} (기본값 60LPM)",
            min_value=1.0,
            value=60.0,
            step=5.0
        )

    with col2:
        cylinder_volume_l = st.number_input(
            f"{L['cyl_volume']} (기본값 40L)",
            min_value=1.0,
            value=40.0,
            step=1.0
        )

    with col3:
        cylinder_pressure_bar = st.number_input(
            f"{L['cyl_pressure']} (기본값 150BAR)",
            min_value=1.0,
            value=150.0,
            step=10.0
        )

    daily_oxygen_m3 = generator_flow_lpm * 60 * operating_hours_per_day / 1000
    cylinder_oxygen_m3 = cylinder_volume_l * cylinder_pressure_bar / 1000

    cylinders_per_day_equiv = daily_oxygen_m3 / cylinder_oxygen_m3 if cylinder_oxygen_m3 > 0 else 0
    cylinders_per_month_equiv = cylinders_per_day_equiv * days_per_month

    st.success(
        L["gen_vs_cyl_line"].format(
            day_cyl=cylinders_per_day_equiv,
            mon_cyl=cylinders_per_month_equiv
        )
    )

    # -----------------------------
    # 3. 렌탈 모델
    # -----------------------------
    st.header(L["sec3"])

    col1, col2, col3 = st.columns(3)

    with col1:
        rental_monthly_fee = st.number_input(
            f"{L['rental_monthly_fee']}",
            min_value=0.0,
            value=2500.0,
            step=100.0
        )

    with col2:
        rental_includes_maintenance = st.checkbox(
            L["rental_includes_maint"], value=True
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
    # 4. 구매 모델
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

    monthly_capex = purchase_price / (amortization_years * 12)
    monthly_maintenance = maintenance_annual / 12

    purchase_monthly_total = monthly_capex + monthly_maintenance + monthly_energy_cost
    purchase_annual_total = purchase_monthly_total * 12
    purchase_five_year_total = purchase_annual_total * 5

    # 연간/5년 절감, Payback 계산
    purchase_annual_saving = annual_cylinder_cost - purchase_annual_total
    annual_saving_vs_cylinder = purchase_annual_saving  # CSV 저장용 이름 유지
    if purchase_annual_saving > 0:
        payback_years = purchase_price / purchase_annual_saving
    else:
        payback_years = None

    rental_annual_saving = annual_cylinder_cost - rental_annual_total
    rental_5yr_saving = five_year_cylinder_cost - rental_five_year_total
    purchase_5yr_saving = five_year_cylinder_cost - purchase_five_year_total

    # -----------------------------
    # 5. 결과 비교
    # -----------------------------
    st.header(L["sec5"])

    colA, colB, colC = st.columns(3)

    with colA:
        st.subheader(L["colA_title"])
        st.metric(L["metric_month"], f"{monthly_cylinder_cost:,0f}")
        st.metric(L["metric_year"], f"{annual_cylinder_cost:,0f}")
        st.metric(L["metric_5year"], f"{five_year_cylinder_cost:,0f}")

    with colB:
        st.subheader(L["colB_title"])
        st.metric(L["metric_month"], f"{rental_monthly_total:,0f}")
        st.metric(L["metric_year"], f"{rental_annual_total:,0f}")
        st.metric(L["metric_5year"], f"{rental_five_year_total:,0f}")

    with colC:
        st.subheader(L["colC_title"])
        st.metric(L["metric_month"], f"{purchase_monthly_total:,0f}")
        st.metric(L["metric_year"], f"{purchase_annual_total:,0f}")
        st.metric(L["metric_5year"], f"{purchase_five_year_total:,0f}")

    st.markdown("---")

    # -----------------------------
    # 6. ROI 설명 + 1~5년 비용 그래프
    # -----------------------------
    st.header(L["sec_roi"])

    col1, col2 = st.columns(2)

    # 렌탈 ROI
    with col1:
        st.subheader("렌탈 ROI / Rental ROI")
        st.write(f"- 연간 절감액 / Annual saving vs Cylinder: **{rental_annual_saving:,.0f} USD**")
        st.write(f"- 5년 누적 절감 / 5-year saving vs Cylinder: **{rental_5yr_saving:,.0f} USD**")
        if rental_annual_saving > 0:
            st.success("✔ 렌탈이 실린더 유지보다 연간 기준으로 비용 절감 효과가 있습니다.")
        else:
            st.warning("❗ 렌탈이 실린더 유지보다 비싸거나 비슷한 수준입니다.")

    # 구매 ROI
    with col2:
        st.subheader("구매 ROI / Purchase ROI")
        st.write(f"- 연간 절감액 / Annual saving vs Cylinder: **{purchase_annual_saving:,0f} USD**")
        st.write(f"- 5년 누적 절감 / 5-year saving vs Cylinder: **{purchase_5yr_saving:,0f} USD**")
        if purchase_annual_saving > 0:
            st.success(L["roi_saving_success"].format(saving=purchase_annual_saving))
            if payback_years:
                st.info(L["roi_payback_info"].format(years=payback_years))
        else:
            st.warning(L["roi_saving_warning"])
            st.info(L["roi_payback_impossible"])

    # 1~5년 비용 추이 그래프
    years = [1, 2, 3, 4, 5]
    cyl_costs = [annual_cylinder_cost * y for y in years]
    rental_costs = [rental_annual_total * y for y in years]
    purchase_costs = [purchase_annual_total * y for y in years]

    df_years = pd.DataFrame({
        "Year": years,
        "Cylinder": cyl_costs,
        "Rental": rental_costs,
        "Purchase": purchase_costs,
    }).set_index("Year")

    st.subheader("1~5년 비용 추이 / Cost over 1–5 years")
    st.line_chart(df_years)

    st.caption(L["footer"])

    st.markdown("---")

    # -----------------------------
    # 🔶 인쇄 버튼
    # -----------------------------
    if st.button(L["print_button"]):
        st.markdown(
            """
            <script>
            window.print();
            </script>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------
    # 🔶 병원별 시나리오 저장 (CSV 다운로드)
    # -----------------------------
    st.subheader(L["save_button"])

    summary = {
        "hospital_name": hospital_name if hospital_name else "",
        "country": country,
        "days_per_month": days_per_month,
        "monthly_cylinder_cost": round(monthly_cylinder_cost, 2),
        "annual_cylinder_cost": round(annual_cylinder_cost, 2),
        "five_year_cylinder_cost": round(five_year_cylinder_cost, 2),
        "rental_monthly_total": round(rental_monthly_total, 2),
        "rental_annual_total": round(rental_annual_total, 2),
        "rental_five_year_total": round(rental_five_year_total, 2),
        "purchase_monthly_total": round(purchase_monthly_total, 2),
        "purchase_annual_total": round(purchase_annual_total, 2),
        "purchase_five_year_total": round(purchase_five_year_total, 2),
        "rental_annual_saving_vs_cylinder": round(rental_annual_saving, 2),
        "rental_5year_saving_vs_cylinder": round(rental_5yr_saving, 2),
        "purchase_annual_saving_vs_cylinder": round(purchase_annual_saving, 2),
        "purchase_5year_saving_vs_cylinder": round(purchase_5yr_saving, 2),
        "payback_years": round(payback_years, 2) if payback_years else "",
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
# 🤝 리테일러 / 파트너용 수익 모델 탭
# ====================================
with tab_dealer:
    st.title("리테일러 / 파트너 수익 모델 (Dealer ROI)")

    st.markdown(
        """
        병원에 장비를 공급하는 **리테일러(딜러)** 입장에서  
        ▶ 단순 판매 vs 렌탈 모델의 수익성과 회수기간을 계산합니다.
        """
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        factory_price = st.number_input(
            "제조사 공급가 / Factory price (USD)",
            min_value=0.0,
            value=12000.0,
            step=500.0,
        )
        dealer_sale_price = st.number_input(
            "병원 판매가 / Sale price to hospital (USD)",
            min_value=0.0,
            value=18000.0,
            step=500.0,
        )
        dealer_install_cost = st.number_input(
            "설치·교육 등 초기 비용 / Installation & training cost (USD, one-time)",
            min_value=0.0,
            value=500.0,
            step=100.0,
        )

    with col2:
        dealer_rental_fee = st.number_input(
            "병원 월 렌탈료 / Monthly rental fee to hospital (USD)",
            min_value=0.0,
            value=2500.0,
            step=100.0,
        )
        dealer_annual_service_cost = st.number_input(
            "연간 서비스·유지보수 비용 / Annual service cost (USD/year)",
            min_value=0.0,
            value=800.0,
            step=100.0,
        )
        rental_contract_years = st.number_input(
            "렌탈 계약기간 (년) / Rental contract period (years)",
            min_value=1,
            max_value=10,
            value=5,
            step=1,
        )

    st.markdown("---")

    # ① 단순 판매 모델
    st.subheader("① 단순 판매 모델 (One-off Sale)")

    unit_margin = dealer_sale_price - (factory_price + dealer_install_cost)
    margin_rate = (unit_margin / dealer_sale_price * 100) if dealer_sale_price > 0 else 0.0

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("한 대당 이익 / Margin per unit (USD)", f"{unit_margin:,.0f}")
    with col_s2:
        st.metric("마진율 / Margin rate (%)", f"{margin_rate:,.1f}%")

    st.markdown(
        f"- 리테일러는 한 대 판매 시 **약 {unit_margin:,.0f} USD** 이익을 얻습니다.\n"
        f"- 판매가 기준 마진율은 **약 {margin_rate:,.1f}%** 입니다."
    )

    st.markdown("---")

    # ② 렌탈 모델
    st.subheader("② 렌탈 모델 (Rental to Hospital)")

    initial_invest = factory_price + dealer_install_cost
    annual_profit = dealer_rental_fee * 12 - dealer_annual_service_cost

    if annual_profit > 0:
        payback_years_dealer = initial_invest / annual_profit
    else:
        payback_years_dealer = None

    total_profit_contract = annual_profit * rental_contract_years

    col_r1, col_r2, col_r3 = st.columns(3)
    with col_r1:
        st.metric("초기 투자금 / Initial investment (USD)", f"{initial_invest:,.0f}")
    with col_r2:
        st.metric("연간 순이익 / Annual net profit (USD)", f"{annual_profit:,.0f}")
    with col_r3:
        if payback_years_dealer:
            st.metric("투자 회수기간 / Payback (years)", f"{payback_years_dealer:,.1f}")
        else:
            st.metric("투자 회수기간 / Payback", "N/A")

    st.write(
        f"- 계약 {rental_contract_years}년 기준, 총 예상 순이익은 "
        f"**{total_profit_contract:,.0f} USD** 입니다."
    )

    st.markdown("---")

    # 📈 누적 현금흐름 그래프
    st.subheader("📈 누적 현금흐름 (Cumulative Cash Flow)")

    years_cf = list(range(0, rental_contract_years + 1))
    cash_flow = []
    for y in years_cf:
        if y == 0:
            cash_flow.append(-initial_invest)
        else:
            cash_flow.append(-initial_invest + annual_profit * y)

    df_cash = pd.DataFrame(
        {"Year": years_cf, "Cumulative Cash Flow (USD)": cash_flow}
    ).set_index("Year")

    st.line_chart(df_cash)

    # 📊 계약기간별 총 순이익 그래프
    st.subheader("📊 1년~계약기간까지 총 순이익 (Total Profit by Year)")

    years_profit = list(range(1, rental_contract_years + 1))
    total_profits = [annual_profit * y for y in years_profit]

    df_profit = pd.DataFrame(
        {"Year": years_profit, "Total Profit (USD)": total_profits}
    ).set_index("Year")

    st.bar_chart(df_profit)

    st.caption(
        "※ 이 탭은 리테일러(딜러) 입장에서의 수익성을 보여줍니다. "
        "병원 ROI는 왼쪽 탭에서 확인하세요."
    )
