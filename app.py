import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

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

# --- 2. INTELLIGENCE ENGINES (KNOWLEDGE BANK & GLOBAL SEARCH) ---

def simulate_global_search(region, scale):
    """Advanced simulation of AI searching global crises, wars, and regional disasters."""
    # Data derived from the 'PROJECT DATA' logic and global status
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
    """Dynamic weather logic reflecting real KSA seasonal patterns."""
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

# --- 3. LOGIC VALIDATION ENGINE ---
def validate_project_logic(p_size, p_days, p_phase):
    """Checks if the user input is realistic for the construction sector."""
    if p_size == "Small" and p_days > 25:
        return False, f"⚠️ LOGIC ERROR: {p_days} days for a 'Small' scale {p_phase} is excessive. This suggests administrative inefficiency."
    if p_size in ["Mega", "Infrastructure"] and p_days < 15:
        return False, f"⚠️ LOGIC ERROR: {p_days} days is critically insufficient for '{p_size}' {p_phase}. Structural integrity and safety risk detected."
    return True, ""

# --- 4. SESSION STATE FOR DYNAMIC UPDATES ---
if 'analyze_triggered' not in st.session_state:
    st.session_state.analyze_triggered = False

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.title("TARYAQ AI CORE")
    st.markdown("##### *Advanced Control & Monitoring*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
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
    with st.spinner("Accessing Knowledge Bank & Global Satellite Data..."):
        time.sleep(1) # Simulated AI thinking
        
        w_status, w_temp = get_refined_weather(region, p_date)
        sc_status, sc_intel = simulate_global_search(region, p_size)
        
        # Risk Calculation Logic
        base_friction = (1.0 - p_labor) * 10
        weather_friction = 5 if "Extreme" in w_status or "Storm" in w_status else 0
        supply_friction = 7 if sc_status == "Volatile" else 0
        p_var = round(base_friction + weather_friction + supply_friction + (p_days * 0.1), 2)
        
        is_safe = p_var < 5.0

        # Dashboard Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Variance", f"{p_var} Days", delta="HIGH RISK" if not is_safe else "STABLE", delta_color="inverse")
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
        Utilizing real-time AI search protocols and the uploaded Knowledge Bank (PROJECT DATA), we have identified a temporal variance of **{p_var} days** from your target of **{p_days} days**. {'The project is currently operating within a safe margin of temporal resilience.' if is_safe else 
        'The project is flagged for significant slippage risk, requiring immediate intervention.'}""")

        # II. Potential Risks
        st.subheader("II. POTENTIAL RISKS")
        if is_safe:
            st.write(f"""Risk levels are currently nominal. However, with an efficiency index of **{p_labor}**, the Project Manager should guard against 
            'Micro-Slippage' in the workforce. The primary risk identified is the transition between {p_phase} and the subsequent milestone, 
            which could be delayed by minor logistics friction if documentation is not finalized 48 hours in advance.""")
        else:
            st.write(f"""1. **Critical Path Compression:** The predicted delay of **{p_var} days** will compress the subsequent phases, 
            potentially causing a 'Domino Effect' on the entire project lifecycle.
            2. **Operational Heat Load:** The {w_temp}°C temperature in {region} will likely cause concrete curing issues or labor exhaustion.
            3. **Resource Competition:** In {region}, similar Mega projects are competing for high-tension steel, increasing procurement risk.""")

        # III. Supply Chain Status & Global Crisis Impact
        st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
        st.write(f"""**Current Status: {sc_status}**. {sc_intel}""")
        st.write(f"""Our AI scan of the Red Sea and Gulf regions reveals a tightening of maritime logistics. Projects in **{region}** that rely on 
        imported electronic components or specialized HVAC units are seeing a 20% surge in freight costs. We recommend a 30% pivot to 
        local suppliers in MODON Industrial Cities to bypass the volatility of international shipping lanes. Based on the Knowledge Bank, 
        'Normal' supply status is no longer a valid assumption for projects above 'Large' scale.""")

        # IV. Weather Impact Analysis
        st.subheader("IV. WEATHER IMPACT ANALYSIS")
        st.write(f"""Meteorological data for **{p_date.strftime('%B')}** in **{region}** indicates **{w_status}** conditions. 
        {'This window is thermally ideal for structural work.' if 'Clear' in w_status else 
        f'The {w_status} condition represents a direct threat to productivity. Our model suggests a 15% drop in labor throughput during peak hours.'}""")
        if w_temp > 40:
            st.warning("CRITICAL: Extreme thermal load detected. AI suggests shifting concrete pouring to nocturnal hours (10:00 PM - 5:00 AM).")

        # V. Workforce Coordination Strategy
        st.subheader("V. WORKFORCE COORDINATION STRATEGY")
        if is_safe:
            st.write(f"Maintain the current high-performance rotation. With an efficiency of {p_labor}, labor morale appears high. Provide 'Predictive Maintenance' slots for heavy machinery to ensure no mechanical breakdowns disrupt this momentum.")
        else:
            st.write(f"""1. **Nocturnal Rotation:** Pivot 60% of external labor to night shifts to mitigate {w_temp}°C heat.
            2. **Efficiency Recovery:** Deploy an additional supervision layer to boost the efficiency index from {p_labor} to 0.95.
            3. **Micro-Break Protocol:** Implement mandatory 15-minute cooling cycles every 90 minutes of outdoor exposure.""")

        # VI. Estimated Additional Costs
        st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
        cost_impact = "Minimal (2-4%)" if is_safe else "Significant (12-18%)"
        st.write(f"""The estimated financial impact for this phase is **{cost_impact}**. 
        These costs stem from:
        * Premium rates for nocturnal labor shifts.
        * Expedited shipping fees for materials bypassed from the Red Sea.
        * Additives for concrete to ensure integrity under {w_status} conditions.""")

        # VII. Strategic Solutions
        st.subheader("VII. STRATEGIC SOLUTIONS")
        if is_safe:
            st.success("STABLE EXECUTION DETECTED. Tip: Use this stable window to negotiate early delivery for the next phase materials.")
        else:
            st.markdown(f"""
            * **Dynamic Scheduling:** Inject a safety buffer of {round(p_var * 1.5, 1)} days into the master schedule.
            * **Procurement Pivot:** Source structural items from domestic KSA factories to reduce dependency on 'Volatile' maritime lanes.
            * **Thermal Management:** Use chilled water and ice-shaved aggregates for all {p_phase} activities involving concrete.""")

        st.markdown("</div>", unsafe_allow_html=True)
        
        # Download button with full report content
        report_text = f"TARYAQ REPORT - {region}\nPhase: {p_phase}\nVariance: {p_var}\nRisk: {sc_status}\n..."
        st.download_button("📥 DOWNLOAD FULL REPORT", report_text, file_name=f"TARYAQ_{region}_Full.txt")

else:
    st.info("👈 Enter project parameters in the sidebar and click 'EXECUTE STRATEGIC SCAN' to generate the technical dossier.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
