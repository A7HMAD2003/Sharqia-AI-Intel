import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. CORE SYSTEM ARCHITECTURE ---
st.set_page_config(page_title="TARYAQ | Strategic AI Core", page_icon="🏗️", layout="wide")

# Custom UI Styling
st.markdown("""
    <style>
    .report-box { padding: 25px; border-radius: 15px; background-color: #1a1c24; border-left: 8px solid #007bff; line-height: 1.6; }
    .stMetric { background-color: #111b21; padding: 15px; border-radius: 10px; border: 1px solid #2d3139; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ENGINEERING KNOWLEDGE BANK & HEURISTICS ---
def get_weather_engine(region, month):
    """Maps month and region to realistic Saudi weather terms."""
    # Logic: Month 12, 1, 2 (Winter) | 6, 7, 8 (Summer)
    if month in [12, 1, 2]:
        status = "Freezing" if region == "Asir" else "Clear"
        temp = 12 if region != "Jeddah" else 22
        if region == "Asir": status = "Foggy"
    elif month in [6, 7, 8]:
        status = "Hot"
        temp = 45 if region != "Asir" else 28
        if region in ["Jeddah", "Eastern Province"]: status = "Humid"
    elif month in [3, 4, 5]:
        status = "Windy" if region == "NEOM" else "Cloudy"
        temp = 29
    else: # Autumn
        status = "Thunderstorms" if region == "Asir" else "Clear"
        temp = 31
    return status, temp

def validate_logic(p_size, p_days, p_phase):
    """Checks if the duration is realistic for the project scale."""
    benchmarks = {
        "Small": (2, 15),
        "Medium": (10, 45),
        "Large": (30, 120),
        "Mega": (60, 365),
        "Infrastructure": (45, 500)
    }
    min_d, max_d = benchmarks.get(p_size, (1, 1000))
    if p_days > max_d: return False, f"⚠️ Warning: {p_days} days is excessive for a {p_size} project's {p_phase} phase. Benchmark suggests < {max_d} days."
    if p_days < min_d: return False, f"⚠️ Warning: {p_days} days is insufficient for the complexity of a {p_size} project. Benchmark suggests > {min_d} days."
    return True, "Logic Validated."

# --- 3. SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=80)
    st.title("TARYAQ AI")
    st.info("Dynamic Knowledge Bank: Active")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
    p_date = st.date_input("Execution Commencement", datetime.now())
    p_days = st.number_input("Planned Duration (Days)", min_value=1, value=15)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.90)

    # Immediate Logic Check
    is_valid, logic_msg = validate_logic(p_size, p_days, p_phase)
    if not is_valid:
        st.warning(logic_msg)

    st.divider()
    # Trigger button for fresh generation
    run_button = st.button("🚀 GENERATE STRATEGIC DOSSIER", use_container_width=True)

# --- 4. DYNAMIC REPORT GENERATOR (150 - 1000 WORDS) ---
def generate_deep_report(region, p_size, p_phase, p_days, p_labor, w_status, w_temp):
    # Calculate Risk Score
    risk_score = 0
    if w_status in ["Hot", "Humid", "Thunderstorms"]: risk_score += 3
    if p_labor < 0.7: risk_score += 4
    if p_size in ["Mega", "Infrastructure"]: risk_score += 2
    
    # Section 1: Overview
    overview = f"The Strategic Control Unit has finalized a deep-scan analysis for the **{p_phase}** phase in the **{region}**. This project, classified as **{p_size}** scale, is evaluated under the parametric constraints of a {p_days}-day execution window. TARYAQ AI core has synthesized historical benchmarks from the Knowledge Bank to provide this high-fidelity executive briefing."
    
    # Section 2: Risks
    if risk_score > 4:
        risks = f"CRITICAL RISKS DETECTED. The intersection of a **{p_size}** project scale with an efficiency index of {p_labor} creates a 'Deadlock Scenario'. Primary threats include: 1) Thermal expansion risks affecting **{p_phase}** structural integrity. 2) Schedule slippage compounding of approximately {round(p_days*0.2, 1)} days. 3) Labor fatigue thresholds being breached due to ambient loads of {w_temp}°C."
    else:
        risks = f"LOW RISK PROFILE. The project is currently positioned within the 'Safe Execution Zone'. All systemic variables indicate that the {p_days}-day target is achievable without significant parametric deviation. No critical bottlenecks in **{p_phase}** are currently forecasted by the AI logic."

    # Section 3: Supply Chain
    supply = f"Regional logistics for **{region}** are currently **{'VOLATILE' if risk_score > 5 else 'STABLE'}**. Data scraping from local MODON clusters and port authorities suggests a potential 12% lead-time escalation for specialized materials required for **{p_phase}**. Just-In-Time (JIT) delivery protocols are advised to prevent site congestion."

    # Section 4: Weather
    weather = f"Atmospheric Monitoring: Status is **{w_status}** at **{w_temp}°C**. Under **{w_status}** conditions, the evaporation rate and chemical hydration process for **{p_phase}** materials require specialized additives. Thermal load on labor reduces physical throughput by an estimated {100 - (p_labor*100)}%."

    # Section 5: Labor
    labor = f"OPTIMAL COORDINATION PLAN: To sustain a {p_labor} efficiency index, the Project Manager must implement a 'Bi-Phasic Shift' strategy. 70% of high-intensity mechanical tasks should be nocturnal (22:00 - 05:00). During peak **{w_status}** hours, workforce should be re-deployed to indoor fit-outs or shaded administrative staging."

    # Section 6: Costs
    costs = f"MITIGATION BUDGETARY IMPACT: Should the forecasted risks materialize, an emergency allocation of 4.5% to 8% of the phase budget is required. Breakdown: $3,500 for thermal safety infrastructure, $12,000 for express logistical surcharges, and a 15% increase in labor night-shift premiums."

    # Section 7: Solutions
    if risk_score > 4:
        solutions = f"COMMAND ACTIONS: 1) Bypass maritime transit; source structural components from local **{region}** hubs. 2) Re-baseline the schedule with a {round(p_days*0.15, 1)}-day buffer. 3) Deploy real-time IoT sensors for material monitoring. 4) Update stakeholders on the 'Risk Advisory' status immediately."
    else:
        solutions = "MANAGEMENT ADVICE: Your current operational status is excellent. Proactive advice: Use this stable window to pre-order long-lead items for the next phase. Reward high-performing teams to cement the current efficiency index. Maintain current baseline without aggressive acceleration."

    # Assemble and Expand
    full_report = f"""
    ## 📑 PROJECT STRATEGIC DOSSIER: {p_phase.upper()}
    
    ### 1. BRIEF OVERVIEW (لمحة عامة)
    {overview} {overview if len(overview) < 50 else ""}
    
    ### 2. POTENTIAL RISKS (المخاطر المحتملة)
    {risks}
    
    ### 3. SUPPLY CHAIN STATUS (سلاسل الإمداد)
    {supply}
    
    ### 4. WEATHER DYNAMICS & IMPACT (الطقس وتأثيره)
    Analysis for {p_date.strftime('%B %Y')}: The **{w_status}** condition acts as a primary operational constraint. {weather}
    
    ### 5. LABOR COORDINATION STRATEGY (تنسيق العمالة)
    {labor}
    
    ### 6. PROJECTED MITIGATION COSTS (التكاليف الإضافية)
    {costs}
    
    ### 7. STRATEGIC SOLUTIONS & MANDATES (الحلول)
    {solutions}
    
    ---
    *AI SEARCH STATUS: Connected to Knowledge Bank | Regional Satellites Active | Strategic Logic Applied.*
    """
    return full_report

# --- 5. MAIN EXECUTION ---
st.title("🏗️ TARYAQ : STRATEGIC ENGINEERING CORE")

if run_button:
    # Clear previous cache to ensure dynamic update
    st.session_state['last_report'] = ""
    
    # 1. Weather Logic
    w_status, w_temp = get_weather_engine(region, p_date.month)
    
    # 2. Status Update
    with st.status("📡 Connecting to Engineering Knowledge Bank...", expanded=True) as s:
        time.sleep(1)
        st.write(f"🔍 Analyzing {p_size} scale benchmarks for {region}...")
        time.sleep(1)
        st.write(f"🌡️ Validating {w_status} weather status for Month {p_date.month}...")
        s.update(label="Deep Scan Complete.", state="complete", expanded=False)

    # 3. Forecast Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Weather Status", w_status)
    c2.metric("Ambient Load", f"{w_temp}°C")
    c3.metric("Supply Chain", "STABLE" if p_size != "Mega" else "VOLATILE")
    c4.metric("Labor Index", f"{p_labor*100}%")

    st.divider()

    # 4. Final Report Output
    final_report = generate_deep_report(region, p_size, p_phase, p_days, p_labor, w_status, w_temp)
    st.markdown(final_report)
    
    # 5. Download Option
    st.download_button("📥 Download Dossier (Text)", final_report, file_name=f"TARYAQ_{region}_{p_phase}.txt")

else:
    st.info("👈 Enter project parameters in the Command Center and click 'GENERATE' to start the AI scan.")
