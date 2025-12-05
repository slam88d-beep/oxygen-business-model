import streamlit as st
import pandas as pd
import io
import math

# PDF 라이브러리 (reportlab) 로드 시도
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    PDF_ENABLED = True
except Exception:
    PDF_ENABLED = False

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
        "pdf_button": "PDF 요약 리포트 다운로드",
        "save_button": "현재 시나리오를 파일로 저장 (CSV 다운로드)",
        "save_note": "※ 저장된 CSV 파일을 모아서 병원별 비교·관리 자료로 활용할 수 있습니다.",
        "sec1": "1. 현재 실린더 사용 비용",
        "sec2": "2. 산소발생기 운전 조건 및 전기요금",
        "sec2_1": "2-1. 산소발생기 산소 생산량 vs 실린더 용량 비교",
        "sec2_2": "2-2. 병상 기준 산소 사용량 & 권장 장비 대수",
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
        "beds_total": "총 병상 수",
        "bed_occupancy": "평균 병상 가동률 (%)",
        "oxy_bed_ratio": "산소 사용 병상 비율 (%)",
        "avg_flow_per_bed": "산소 사용 병상 1개당 평균 유량 (LPM)",
        "bed_use_hours": "산소 사용 평균 시간 (시간/일)",
        "bed_estimate_line": "👉 산소 사용 병상(유효 병상 수): 약 {eff_beds:.1f}개\n"
                             "   예상 실린더 사용량: 하루 {day_cyl:.1f}병, 월 {mon_cyl:.0f}병",
        "gen_recommend_line": "✅ 위 사용량 기준 권장 60LPM 산소발생기 수량: {gen}대 (백업 포함 N+1 구성: {gen_backup}대 권장)",
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
        "roi_saving_success": "✔ 구매 시 실린더 대비 연간 {saving:,.0f} USD 절감 예상",
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
        "pdf_button": "Download PDF Summary Report",
        "save_button": "Save current scenario as CSV",
        "save_note": "※ You can collect these CSVs to manage and compare hospitals.",
        "sec1": "1. Current Cylinder Oxygen Cost",
        "sec2": "2. Oxygen Generator Operation & Electricity Cost",
        "sec2_1": "2-1. Generator Oxygen Production vs Cylinder Capacity",
        "sec2_2": "2-2. Bed-based Oxygen Usage & Generator Count",
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
        "beds_total": "Total number of beds",
        "bed_occupancy": "Average bed occupancy (%)",
        "oxy_bed_ratio": "Ratio of beds using oxygen (%)",
        "avg_flow_per_bed": "Avg oxygen flow per oxygen bed (LPM)",
        "bed_use_hours": "Avg oxygen usage time (hours/day)",
        "bed_estimate_line": "👉 Effective oxygen beds: approx. {eff_beds:.1f}\n"
                             "   Estimated cylinder usage: {day_cyl:.1f} cylinders/day, {mon_cyl:.0f} cylinders/month",
        "gen_recommend_line": "✅ Recommended 60 LPM generators: {gen} units (with N+1 backup: {gen_backup} units)",
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
    # vi / km 는 앞에서 쓰던 것과 동일하게 두면 됩니다.
    # (길어지니까 여기서는 생략하지만, 종찬님 파일에는 이미 들어있으니 그대로 두시면 돼요)
}

# =================
# 🔶 Streamlit UI 기본 설정
# =================

st.set_page_config(
    page_title="Oxygen Business Model Calculator",
    layout="wide"
)

# ---- Sidebar: language & country ----
st.sidebar.header("Settings")

language = st.sidebar.selectbox(
    "Language / 언어 / Ngôn ngữ / ភាសា",
    ["ko", "en"],  # 일단 두 가지만 써도 되고, vi/km도 추가 가능
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

# ---- Title ----
st.title(L["title"])
st.caption(L["subtitle"])

hospital_name = st.text_input(L["hospital_name_label"], "")

st.markdown("---")

# -----------------------------
# 1. 실린더 비용 + 배송비
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

# 배송비 추가
cyl_delivery_monthly = st.number_input(
    "실린더 배송비 (월, USD) / Cylinder delivery cost per month (USD)",
    min_value=0.0,
    value=0.0,
    step=50.0
)
monthly_cylinder_cost_base += cyl_delivery_monthly

usage_percent = st.selectbox(
    L["usage_percent"],
    [100, 95, 90, 85, 80, 75],
    index=0
)

monthly_cylinder_cost = monthly_cylinder_cost_base * (100 / usage_percent)

st.info(
    f"{L['usage_info_prefix']}: {monthly_cylinder_cost_base:,.0f} USD → "
    f"{usage_percent}% {L['usage_info_mid']} **{monthly_cylinder_cost:,.0f} USD** {L['usage_info_suffix']}"
)

annual_cylinder_cost = monthly_cylinder_cost * 12
five_year_cylinder_cost = annual_cylinder_cost * 5

# -----------------------------
# 2. 전기요금 + 발전량, 병상 기반 사용량, 렌탈/구매, ROI
# -----------------------------
# 👉 이 아래 부분은 어제 쓰던 코드 그대로 두셔도 되고,
#    문제되던 건 PDF 부분뿐이라, PDF 부분만 아래처럼 바꾸면 됩니다.
#    (답변이 너무 길어져서 여기서는 생략하지만, 종찬님 app.py에 있던 나머지 계산/그래프/CSV 부분 그대로 사용하셔도 됩니다.)


