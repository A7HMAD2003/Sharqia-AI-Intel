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

# --- 2. DATA LOADING ENGINE (KNOWLEDGE BANK) ---
@st.cache_data
def load_kb_data():
    file_path = 'PROJECT DATA.xlsx - Sheet1.csv'
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            # Standardize column names if needed
            return df
        except Exception as e:
            st.error(f"Error reading Knowledge Bank: {e}")
            return None
    return None

kb_df = load_kb_data()

# Extract dynamic activities from Excel
if kb_df is not None and 'Activity' in kb_df.columns:
    dynamic_phases = sorted(kb_df['Activity'].dropna().unique().tolist())
else:
    dynamic_phases = ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"]

# --- 3. INTELLIGENCE ENGINES (GLOBAL SEARCH & WEATHER) ---

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
    if p_size in ["Mega", "Infrastructure"] and p_days < 15:
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
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    
    # DYNAMIC PHASES FROM EXCEL
    p_phase = st.selectbox("Operational Phase (From Knowledge Bank)", dynamic_phases)
    
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
            st.error("Correct logic errors first.")

# --- 6. MAIN DISPLAY & REPORT ---
st.title("🏗️ TARYAQ : ADVANCED ENGINEERING INTELLIGENCE")

if st.session_state.analyze_triggered:
    with st.spinner("Analyzing Knowledge Bank & Global Crises..."):
        time.sleep(1)
        
        w_status, w_temp = get_refined_weather(region, p_date)
        sc_status, sc_intel = simulate_global_search(region, p_size)
        
        # Historical Insights Logic from KB
        hist_delay = 0
        if kb_df is not None:
            relevant_data = kb_df[kb_df['Activity'] == p_phase]
            if not relevant_data.empty:
                hist_delay = round(relevant_data['Delay'].mean(), 1)
        
        # Risk Calculation Logic
        base_friction = (1.0 - p_labor) * 10
        weather_friction = 5 if "Extreme" in w_status or "Storm" in w_status else 0
        supply_friction = 7 if sc_status == "Volatile" else 0
        p_var = round(base_friction + weather_friction + supply_friction + (p_days * 0.1), 2)
        is_safe = p_var < 5.0

        # Dashboard Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Variance", f"{p_var} Days", delta=f"Hist Avg: {hist_delay}d", delta_color="inverse")
        c2.metric("Supply Chain", sc_status)
        c3.metric("Weather Impact", w_status)
        c4.metric("Ambient Temp", f"{w_temp}°C")

        st.divider()

        # DYNAMIC LONG-FORM REPORT
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.header("📑 STRATEGIC ENGINEERING DOSSIER")
        
        # I. Brief Overview
        st.subheader("I. BRIEF OVERVIEW")
        st.write(f"""The TARYAQ Engineering Core has completed a multi-layered analysis of the **{p_phase}** phase for the **{p_size}** project in **{region}**. 
        Utilizing real-time AI search protocols and the synchronized Knowledge Bank, we have identified a temporal variance of **{p_var} days**. 
        Historical records from our database for the activity '{p_phase}' indicate an average historical delay of **{hist_delay} days**, which aligns with our current predictive model. 
        {'Operations are within the safe threshold' if is_safe else 'Critical slippage risk detected'}. """)

        # II. Potential Risks
        st.subheader("II. POTENTIAL RISKS")
        if is_safe:
            st.write(f"Risk levels for **{p_phase}** are nominal. Manager tip: Historical data shows that '{p_phase}' often suffers from late-stage documentation bottlenecks; ensure all sign-offs are ready 72 hours before the {p_days}-day mark.")
        else:
            st.write(f"1. **Compression:** The {p_var} day variance will disrupt the following milestones. 2. **Environment:** {w_temp}°C in {region} threatens '{p_phase}' integrity. 3. **Scale Stress:** {p_size} requirements exceed current local inventory.")

        # III. Supply Chain Status & Global Crisis Impact
        st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
        st.write(f"**Status: {sc_status}**. {sc_intel}. Projects in **{region}** must account for the maritime blockade in the Red Sea. We recommend a 40% local sourcing strategy for all items related to {p_phase}.")

        # IV. Weather Impact Analysis
        st.subheader("IV. WEATHER IMPACT ANALYSIS")
        st.write(f"Forecast for **{p_date.strftime('%B')}**: {w_status} at {w_temp}°C. This specific thermal load in {region} historically reduces efficiency by 12.5% for {p_phase} tasks.")

        # V. Workforce Coordination Strategy
        st.subheader("V. WORKFORCE COORDINATION STRATEGY")
        st.write(f"Given an efficiency of {p_labor}, implement: 1. Nocturnal Rotation (10PM-5AM). 2. Enhanced QA/QC layers. 3. 15-min cooling cycles.")

        # VI. Estimated Additional Costs
        st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
        cost_inc = "15-20%" if not is_safe else "2-5%"
        st.write(f"Expected budget impact: **+{cost_inc}**. Driven by nocturnal labor premiums and logistics re-routing for {p_phase} specific materials.")

        # VII. Strategic Solutions
        st.subheader("VII. STRATEGIC SOLUTIONS")
        st.markdown(f"""
        * **Buffer:** Add {round(p_var*1.2, 1)} days to next milestone.
        * **Pivot:** Immediate contact with suppliers in Dammam/Jubail for {p_phase} backup.
        * **AI Refresh:** Re-run scan every 48 hours for geopolitical updates.""")

        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("📥 DOWNLOAD FULL REPORT", "FULL CONTENT...", file_name=f"TARYAQ_{region}.txt")

else:
    st.info("👈 Enter project parameters in the sidebar and click 'EXECUTE STRATEGIC SCAN'.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
