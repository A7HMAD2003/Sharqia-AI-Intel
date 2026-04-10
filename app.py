import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="TARYAQ | AI Control", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    /* Footer Style */
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #9ca3af; font-size: 13px; padding: 15px; background-color: rgba(14, 17, 23, 0.9); border-top: 1px solid #1f2937; z-index: 1000; }
    /* Metric Card Style */
    .stMetric { background-color: #1f2937 !important; padding: 15px !important; border-radius: 10px !important; border-bottom: 3px solid #3b82f6 !important; }
    /* Clean Titles */
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; }
    .risk-high { color: #ff4b4b; font-weight: bold; }
    .risk-stable { color: #00ff7f; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. INTELLIGENCE ENGINES ---

def get_precise_weather(region, date):
    """Accurate logic for Saudi weather terms requested."""
    month = date.month
    if month in [12, 1, 2]: # Winter
        status = "Freezing" if region in ["Riyadh Sector", "NEOM", "Asir"] else "Clear"
        temp = 12 if region != "Jeddah" else 22
        if region == "Asir": status = "Foggy"
    elif month in [6, 7, 8, 9]: # Summer
        status = "Hot"
        temp = 46 if region != "Asir" else 28
        if region in ["Jeddah", "Eastern Province"]: status = "Humid"
    elif month in [3, 4, 5]: # Spring
        status = "Thunderstorms" if region == "Asir" else "Cloudy"
        temp = 28
        if region == "NEOM": status = "Windy"
    else: # Autumn
        status = "Windy"
        temp = 32
    return status, temp

def analyze_supply_chain(region, p_size):
    """
    AI Logic to simulate search for supply chain disruptions 
    considering Geopolitics, Wars, and Disasters.
    """
    risk_level = "Stable"
    details = ""
    
    if region in ["NEOM", "Jeddah"]:
        risk_level = "Volatile"
        details = "Affected by maritime security tensions in the Red Sea. Potential 15% delay in heavy equipment shipping."
    elif region == "Eastern Province":
        risk_level = "Stable"
        details = "High resilience due to industrial proximity. Minimal impact from global shipping crises."
    elif region == "Riyadh Sector":
        risk_level = "Optimal"
        details = "Strategic inland reserves bypass maritime risks. Logistics hubs are fully operational."
    else:
        risk_level = "Monitoring"
        details = "Standard regional logistics flow with no active disaster alerts."

    if p_size in ["Mega", "Infrastructure"]:
        risk_level = "Strained"
        details += " High demand for specialized materials may trigger local market shortages."

    return risk_level, details

def calculate_operational_risk(p_size, p_days, p_labor, weather_status, sc_risk):
    """Engineering heuristics including supply chain risk."""
    base_friction = (1.0 - p_labor) * (p_days * 0.5)
    env_friction = 0
    if weather_status in ["Hot", "Humid", "Thunderstorms"]: env_friction = p_days * 0.3
    
    sc_impact = 0
    if sc_risk in ["Volatile", "Strained"]: sc_impact = p_days * 0.25
    
    if p_size == "Mega": env_friction += 10.0
    
    variance = base_friction + env_friction + sc_impact
    return round(variance, 2)

# --- 3. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.title("TARYAQ AI")
    st.markdown("##### *Advanced Engineering Control System*") # التعديل هنا
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
    p_date = st.date_input("Deployment Commencement", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=15)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85)

    is_valid = True
    if p_size == "Small" and p_days > 25:
        st.error(f"⚠️ LOGIC ERROR: {p_days} days is illogical for a Small scale phase.")
        is_valid = False
    elif p_size in ["Mega", "Infrastructure"] and p_days < 10:
        st.error(f"⚠️ LOGIC ERROR: Insufficient time for Mega scale phase.")
        is_valid = False

    st.divider()
    analyze_btn = st.button("🚀 EXECUTE STRATEGIC SCAN", use_container_width=True)

# --- 4. MAIN DISPLAY ---
st.title("🏗️ TARYAQ : ADVANCED ENGINEERING INTELLIGENCE") # التعديل هنا

if analyze_btn and is_valid:
    w_status, w_temp = get_precise_weather(region, p_date)
    sc_status, sc_details = analyze_supply_chain(region, p_size)
    p_var = calculate_operational_risk(p_size, p_days, p_labor, w_status, sc_status)
    
    with st.status("📡 Connecting to Global Knowledge Bank...", expanded=False) as s:
        time.sleep(0.8)
        st.write(f"🔍 Analyzing risks for {region}...")
        time.sleep(0.8)
        st.write("🚢 Checking maritime and land-based supply routes...")
        s.update(label="Strategic Analysis Complete!", state="complete")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Predicted Variance", f"{p_var} Days", delta="CRITICAL" if p_var > 4 else "STABLE")
    c2.metric("Supply Chain", sc_status)
    c3.metric("Weather Status", w_status)
    c4.metric("Ambient Load", f"{w_temp}°C")

    st.divider()
    
    is_safe = p_var < 2.5
    st.header("📑 STRATEGIC ENGINEERING DOSSIER")

    st.subheader("I. BRIEF OVERVIEW")
    st.write(f"TARYAQ AI has processed the operational parameters for the **{p_phase}** phase in **{region}**. Our analysis confirms a predicted variance of **{p_var} days**. The current project health is categorized as **{'OPTIMAL' if is_safe else 'AT RISK'}**, requiring alignment with the detected logistical and environmental frictions.")

    st.subheader("II. POTENTIAL RISKS")
    if is_safe:
        st.write(f"Minimal risks detected. Focus on maintaining the **{p_labor}** index. No systemic threats from global crises are currently affecting this window in **{region}**.")
    else:
        st.markdown(f"""
        * **Timeline Slippage:** High risk of a **{p_var} day** delay due to environmental and logistical friction.
        * **Operational Fatigue:** Thermal loads and supply chain stress may impact quality assurance.
        """)

    st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
    st.markdown(f"""
    * **Current Status:** **{sc_status}**
    * **AI Risk Analysis:** {sc_details}
    * **Strategic Note:** For **{region}**, local sourcing is **{'Highly Recommended' if sc_status != 'Optimal' else 'Stable'}**.
    """)

    st.subheader("IV. WEATHER IMPACT ANALYSIS")
    st.write(f"Forecasting **{w_status}** conditions at **{w_temp}°C**. Consistently verified with historical patterns for **{p_date.strftime('%B')}**.")

    st.subheader("V. WORKFORCE COORDINATION STRATEGY")
    if is_safe:
        st.markdown("* **Recommendation:** Maintain current patterns. Utilize this window for critical inspections.")
    else:
        st.markdown(f"* **Urgent Pivot:** Implement nocturnal rotation to maximize the **{p_labor}** efficiency index.")

    st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
    if is_safe:
        st.info("**$0.00**. No emergency budget allocation required.")
    else:
        st.warning(f"**Estimated +12% Budget Impact** due to volatility and hazard pay requirements.")

    st.subheader("VII. STRATEGIC SOLUTIONS")
    if is_safe:
        st.success("Proceed with baseline Gantt chart. Refresh AI scan in 7 days.")
    else:
        st.markdown(f"""
        * **Alternative Sourcing:** Utilize land-based suppliers to bypass maritime bottlenecks.
        * **Buffer Integration:** Inject a **{round(p_var * 1.2, 1)} day** safety buffer.
        """)

    full_report = f"TARYAQ REPORT - {region}\n" + "="*40 + f"\nSupply Chain: {sc_status}\nWeather: {w_status}\nVariance: {p_var} days\n"
    st.download_button("📥 DOWNLOAD FULL DOSSIER", full_report, file_name=f"TARYAQ_{region}_Report.txt")

else:
    st.info("👈 Please enter project parameters and click 'EXECUTE STRATEGIC SCAN'.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
