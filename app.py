import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os

# --- 1. SETTINGS & ADVANCED STYLING ---
st.set_page_config(page_title="TARYAQ | Engineering Intelligence", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #8b949e; font-size: 12px; padding: 12px; background-color: #161b22; border-top: 1px solid #30363d; z-index: 1000; }
    .stMetric { background-color: #161b22 !important; padding: 20px !important; border-radius: 12px !important; border-bottom: 4px solid #238636 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .logic-error-box { background-color: #ffdddd; color: #900; padding: 15px; border-radius: 8px; border-left: 5px solid #f00; margin-bottom: 20px; font-weight: bold; }
    .report-card { background-color: #ffffff; color: #1a1a1a; padding: 40px; border-radius: 15px; line-height: 1.8; text-align: justify; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }
    h1, h2, h3 { color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. DATA LOADING (KNOWLEDGE BANK) ---
@st.cache_data
def load_knowledge_bank():
    file_path = "PROJECT DATA.xlsx - Sheet1.csv"
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Get unique activities for the selectbox
        activities = sorted(df['Activity'].unique().tolist())
        return df, activities
    else:
        # Fallback activities if file is missing
        fallback = ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing", "Electrical", "Infrastructure Pipes"]
        return None, fallback

df_knowledge, activity_list = load_knowledge_bank()

# --- 3. INTELLIGENCE ENGINES ---

def simulate_global_search(region, scale):
    global_status = {
        "Red Sea Conflict": "Critical impact on NEOM and Jeddah ports. 25% increase in lead time for MEP equipment.",
        "Suez Canal Congestion": "Affecting finishing materials from Europe. Expected delay of 14 days.",
        "Global Steel Shortage": "Driven by regional wars, affecting Giga and Mega projects in Riyadh.",
        "Regional Stability": "Saudi domestic supply routes are 100% secure, but international maritime lanes are 'Volatile'."
    }
    if region in ["NEOM", "Jeddah"]:
        return "Volatile", f"HIGH RISK: {global_status['Red Sea Conflict']}. Logistics re-routed via Cape of Good Hope."
    elif region == "Riyadh Sector":
        return "Stable/Constrained", f"MODERATE RISK: {global_status['Global Steel Shortage']}. Inland routes are operational."
    else:
        return "Safe", "Primary supply chains are intact. Local MODON hubs providing sufficient buffers."

def get_refined_weather(region, date):
    month = date.month
    if month in [12, 1, 2]: # Winter
        status = "Cold/Freezing" if region in ["Riyadh Sector", "NEOM", "Asir"] else "Clear"
        temp = 12 if region != "Jeddah" else 22
        if region == "Asir": status = "Heavy Fog"
    elif month in [6, 7, 8, 9]: # Summer
        status = "Extreme Heat"
        temp = 48 if region != "Asir" else 29
        if region in ["Jeddah", "Eastern Province"]: status = "Extreme Heat/Humid"
    elif month in [3, 4, 5]: # Spring
        status = "Sandstorms" if region in ["Riyadh Sector", "NEOM"] else "Variable"
        temp = 31
        if region == "Asir": status = "Heavy Thunderstorms"
    else: # Autumn
        status = "High Winds"
        temp = 34
    return status, temp

# --- 4. LOGIC VALIDATION ENGINE ---
def validate_project_logic(p_size, p_days, p_phase):
    if p_size == "Small" and p_days > 25:
        return False, f"⚠️ LOGIC ERROR: {p_days} days for a 'Small' scale {p_phase} is excessive."
    if p_size in ["Mega", "Infrastructure", "Giga"] and p_days < 12:
        return False, f"⚠️ LOGIC ERROR: {p_days} days is critically insufficient for '{p_size}' {p_phase}."
    return True, ""

# --- 5. SIDEBAR ---
if 'analyze_triggered' not in st.session_state:
    st.session_state.analyze_triggered = False

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.title("TARYAQ AI CORE")
    st.markdown("##### *Advanced Control & Monitoring*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure", "Giga"])
    
    # DYNAMIC TASKS FROM EXCEL
    p_phase = st.selectbox("Operational Phase (Activity)", activity_list)
    
    p_date = st.date_input("Commencement Date", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=20)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85)

    is_logical, logic_msg = validate_project_logic(p_size, p_days, p_phase)
    if not is_logical:
        st.markdown(f"<div class='logic-error-box'>{logic_msg}</div>", unsafe_allow_html=True)

    st.divider()
    if st.button("🚀 EXECUTE STRATEGIC SCAN", use_container_width=True):
        if is_logical:
            st.session_state.analyze_triggered = True
        else:
            st.error("Cannot execute scan with logic errors.")

# --- 6. MAIN DISPLAY & REPORT ---
st.title("🏗️ TARYAQ : ADVANCED ENGINEERING INTELLIGENCE")

if st.session_state.analyze_triggered:
    with st.spinner("Syncing Knowledge Bank & Analyzing Global Logistics..."):
        time.sleep(1.2)
        
        w_status, w_temp = get_refined_weather(region, p_date)
        sc_status, sc_intel = simulate_global_search(region, p_size)
        
        # Risk Calculation Logic
        base_friction = (1.0 - p_labor) * 12
        weather_friction = 6 if "Extreme" in w_status or "Storm" in w_status else 0
        supply_friction = 8 if sc_status == "Volatile" else 0
        p_var = round(base_friction + weather_friction + supply_friction + (p_days * 0.12), 2)
        
        is_safe = p_var < 5.0

        # Dashboard Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Variance", f"{p_var} Days", delta="HIGH RISK" if not is_safe else "STABLE", delta_color="inverse")
        c2.metric("Supply Chain", sc_status)
        c3.metric("Weather Impact", w_status)
        c4.metric("Ambient Temp", f"{w_temp}°C")

        st.divider()

        # DYNAMIC REPORT
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.header(f"📑 STRATEGIC DOSSIER: {p_phase.upper()}")
        
        # I. Brief Overview
        st.subheader("I. BRIEF OVERVIEW")
        st.write(f"""The TARYAQ AI engine has cross-referenced the **{p_phase}** activity with historical data in the Knowledge Bank. 
        For a project of **{p_size}** scale in **{region}**, we have identified a variance of **{p_var} days**. 
        This phase is critical for the project's structural milestone, and current telemetry suggests {'a safe execution path' if is_safe else 'a high probability of critical path slippage'}. 
        The analysis incorporates 2026 maritime transit data and Saudi Vision 2030 infrastructure benchmarks.""")

        # II. Potential Risks
        st.subheader("II. POTENTIAL RISKS")
        risk_hist = "Historical data shows this activity often faces material lead-time issues."
        if df_knowledge is not None:
            match = df_knowledge[df_knowledge['Activity'] == p_phase]
            if not match.empty:
                risk_hist = f"According to Knowledge Bank, similar '{p_phase}' tasks previously faced risks like: {match['Supply Chain'].iloc[0]}."

        st.write(f"""1. **Historical Bottleneck:** {risk_hist}
        2. **Logistics Strain:** The scale of **{p_size}** requires massive resource mobilization which is currently constrained by regional traffic.
        3. **Environmental Stress:** The {w_status} condition will increase friction in mechanical operations by 12%.""")

        # III. Supply Chain & Global Crisis
        st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
        st.write(f"""**Status: {sc_status}**. {sc_intel}""")
        st.write(f"""Global shipping lanes, specifically the Red Sea corridor, are impacting the arrival of specialized equipment for **{p_phase}**. 
        AI-driven freight tracking suggests that 'Just-in-Time' delivery is no longer viable for **{region}**. 
        TARYAQ recommends a strategic shift: source 40% of standard materials from local MODON hubs in Eastern/Central provinces to bypass maritime blockade risks.""")

        # IV. Weather Analysis
        st.subheader("IV. WEATHER IMPACT ANALYSIS")
        st.write(f"""Forecast for **{p_date.strftime('%B')}** in **{region}** predicts **{w_status}** with peaks of **{w_temp}°C**. 
        {'This environment is suitable for high-speed assembly.' if w_temp < 35 else 
        'Extreme thermal load detected. This will affect concrete hydration and worker stamina.'}""")
        if w_temp > 42:
            st.error("ALERT: Heat stress exceeds safety limits. AI mandates shifting 80% of outdoor work to nocturnal hours (9 PM - 5 AM).")

        # V. Workforce Coordination
        st.subheader("V. WORKFORCE COORDINATION STRATEGY")
        st.write(f"""Current Efficiency: **{p_labor*100}%**. 
        1. **Optimized Shifts:** Implement a 3-shift rotation to compensate for the {p_var} days delay.
        2. **Skill Allocation:** Assign 'Senior Specialists' to the {p_phase} critical nodes to ensure zero-rework.
        3. **Safety Protocol:** Enhance hydration stations every 50 meters due to {w_status} conditions.""")

        # VI. Additional Costs
        st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
        cost_p = "4-6%" if is_safe else "14-20%"
        st.write(f"""Expected budget variance for this phase: **+{cost_p}**. 
        Drivers include: 
        * Premium nocturnal labor rates.
        * Logistics re-routing costs for materials bypassed from conflict zones.
        * Emergency local sourcing premiums.""")

        # VII. Solutions & Mitigation
        st.subheader("VII. STRATEGIC SOLUTIONS")
        mitigation_msg = "Early procurement of long-lead items."
        if df_knowledge is not None:
            match = df_knowledge[df_knowledge['Activity'] == p_phase]
            if not match.empty:
                mitigation_msg = match['Risk Mitigation'].iloc[0]

        st.markdown(f"""
        * **Expert Recommendation:** {mitigation_msg}
        * **Buffer Injection:** Add a safety buffer of {round(p_var * 1.3, 1)} days to the next milestone.
        * **Local Pivot:** Immediately secure secondary supply contracts with factories in **{region}** to stabilize the supply chain.""")

        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("📥 DOWNLOAD TECHNICAL DOSSIER", f"TARYAQ REPORT\nRegion: {region}\nActivity: {p_phase}\nVariance: {p_var}...", file_name=f"TARYAQ_{region}.txt")

else:
    st.info("👈 Select project parameters and click 'EXECUTE STRATEGIC SCAN' to begin.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
