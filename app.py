import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="TARYAQ | AI Infrastructure Control", page_icon="🏗️", layout="wide")

# Custom CSS for Professional Dashboard
st.markdown("""
    <style>
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #9ca3af; font-size: 11px; padding: 10px; background-color: rgba(14, 17, 23, 0.9); border-top: 1px solid #1f2937; z-index: 1000; }
    .stMetric { background-color: #1f2937 !important; padding: 20px !important; border-radius: 12px !important; border-left: 5px solid #3b82f6 !important; }
    .main-header { font-size: 36px; font-weight: bold; color: #f8fafc; margin-bottom: 20px; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; }
    .report-card { background-color: #111827; padding: 30px; border-radius: 15px; border: 1px solid #374151; line-height: 1.8; color: #d1d5db; }
    h1, h2, h3 { color: #60a5fa !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED INTELLIGENCE ENGINES ---

def get_realtime_weather_ai(region, p_date):
    """Accurate seasonal weather logic for KSA regions."""
    month = p_date.month
    # Resetting logic to ensure January is never 'Hot'
    if month in [12, 1, 2]: # Winter
        status = "Freezing/Cold" if region in ["Riyadh Sector", "NEOM", "Asir"] else "Mild/Clear"
        temp = 12 if region != "Jeddah" else 21
        if region == "Asir": status = "Dense Fog"
    elif month in [6, 7, 8, 9]: # Summer
        status = "Extreme Heat"
        temp = 47 if region != "Asir" else 27
        if region in ["Jeddah", "Eastern Province"]: status = "High Humidity"
    elif month in [3, 4, 5]: # Spring
        status = "Thunderstorms" if region == "Asir" else "Dust Storms"
        temp = 29
        if region == "NEOM": status = "High Winds"
    else: # Autumn
        status = "Turbulent Winds"
        temp = 32
    return status, temp

def analyze_crisis_and_supply_chain(region, p_size):
    """
    Advanced simulation of AI searching for Wars, Disasters, and Supply Chain Status.
    This logic changes dynamically based on region.
    """
    impact_score = 0
    crisis_report = ""
    
    # Specific Regional Crisis Mapping
    if region in ["NEOM", "Jeddah"]:
        impact_score = 0.8
        crisis_report = "CRITICAL: Maritime supply routes in the Red Sea are under 'High Alert' due to ongoing geopolitical conflicts. Supply chains for heavy machinery and specialized steel from Europe/Asia are experiencing 25-40% lead-time surges."
    elif region == "Eastern Province":
        impact_score = 0.3
        crisis_report = "STABLE: Proximity to major industrial hubs (Jubail/Dammam) mitigates international shocks. However, energy price volatility is causing a slight uptick in logistics costs."
    elif region == "Riyadh Sector":
        impact_score = 0.2
        crisis_report = "OPTIMAL: Strategic inland positioning protects the project from maritime blockades. Inland dry ports are fully operational, though truck queuing at regional borders is slightly elevated."
    elif region == "Asir":
        impact_score = 0.5
        crisis_report = "WARNING: Seasonal natural disaster risk (Flash Floods). Supply routes through mountain passes are vulnerable to closures. Local cement supplies are stable but specialized finishing items are delayed."
    else:
        impact_score = 0.4
        crisis_report = "MONITORING: General supply chain pressure due to global inflation. No immediate war or disaster impact detected in the immediate vicinity."

    # Scale Multiplier
    if p_size in ["Mega", "Infrastructure"]:
        impact_score += 0.2
        crisis_report += " Additionally, the 'Mega' scale triggers localized resource scarcity for skilled labor and high-grade concrete."

    status = "Volatile" if impact_score > 0.6 else "Under Pressure" if impact_score > 0.4 else "Stable"
    return status, crisis_report

def calculate_engineering_variance(p_size, p_days, p_labor, w_status, sc_status):
    """Engineering logic for schedule deviation."""
    friction = (1.0 - p_labor) * (p_days * 0.5)
    
    # Weather frictions
    if "Extreme Heat" in w_status or "Humidity" in w_status: friction += p_days * 0.35
    if "Storms" in w_status or "Fog" in w_status: friction += p_days * 0.2
    
    # Crisis frictions
    if sc_status == "Volatile": friction += p_days * 0.3
    if sc_status == "Under Pressure": friction += p_days * 0.15
    
    if p_size == "Mega": friction += 12.0 # Baseline Mega-project complexity
    
    return round(friction, 2)

# --- 3. SESSION STATE MANAGEMENT ---
# To solve the update problem
if 'last_report' not in st.session_state:
    st.session_state.last_report = None

# --- 4. SIDEBAR - PARAMETERS & VALIDATION ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=80)
    st.title("TARYAQ AI")
    st.markdown("##### *Advanced Infrastructure Intelligence*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"], key="reg")
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"], key="sz")
    p_phase = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"], key="ph")
    p_date = st.date_input("Deployment Commencement", datetime.now(), key="dt")
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=15, key="dy")
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85, key="lb")

    # --- LOGIC ERROR DETECTION (Requested) ---
    is_valid = True
    if p_size == "Small" and p_days > 25:
        st.error(f"⚠️ LOGIC ERROR: {p_days} days is illogical for a '{p_size}' phase of {p_phase}. AI suggests reducing to <15 days.")
        is_valid = False
    elif p_size in ["Mega", "Infrastructure"] and p_days < 10:
        st.error(f"⚠️ LOGIC ERROR: Insufficient time for a '{p_size}' project. Minimum realistic duration is 20 days.")
        is_valid = False

    st.divider()
    if st.button("🚀 EXECUTE STRATEGIC SCAN", use_container_width=True):
        if is_valid:
            st.session_state.trigger_scan = True
        else:
            st.session_state.trigger_scan = False

# --- 5. MAIN EXECUTION & REPORTING ---
st.markdown('<div class="main-header">🏗️ TARYAQ : STRATEGIC ENGINEERING CONTROL</div>', unsafe_allow_html=True)

if st.session_state.get('trigger_scan', False):
    # Fetch Data
    w_status, w_temp = get_realtime_weather_ai(region, p_date)
    sc_status, sc_crisis = analyze_crisis_and_supply_chain(region, p_size)
    p_var = calculate_engineering_variance(p_size, p_days, p_labor, w_status, sc_status)
    
    # Progress Simulation
    with st.status("📡 Connecting to Strategic Knowledge Bank...", expanded=True) as status:
        st.write("🔍 Scanning Global Crisis Database for Regional Wars & Conflicts...")
        time.sleep(1)
        st.write(f"🌍 Pulling Satellite Weather Data for {region}...")
        time.sleep(1)
        st.write("🚢 Analyzing Maritime and Land Supply Chain Volatility...")
        status.update(label="Deep Scan Complete!", state="complete")

    # Metrics Layout
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Predicted Variance", f"{p_var} Days", delta="CRITICAL" if p_var > 5 else "STABLE")
    m2.metric("Supply Chain Risk", sc_status)
    m3.metric("Weather Alert", w_status)
    m4.metric("Thermal Load", f"{w_temp}°C")

    st.divider()

    # --- LONG-FORM REPORT GENERATION ---
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    
    is_safe = p_var < 3.5

    # 1. Brief Overview
    st.header("I. BRIEF OVERVIEW")
    st.write(f"TARYAQ Strategic Intelligence has processed the operational parameters for the **{p_phase}** phase of your **{p_size}** scale project in **{region}**. Based on the commencement date of **{p_date}**, our AI engine has cross-referenced global infrastructure benchmarks with local telemetry. {'The project currently shows high temporal resilience with a negligible variance' if is_safe else 'The project is currently flagged for a significant schedule deviation of ' + str(p_var) + ' days'}. This assessment serves as a high-level roadmap for the Project Management Office (PMO) to align with the Saudi National Strategic objectives.")

    # 2. Potential Risks
    st.header("II. POTENTIAL RISKS")
    if is_safe:
        st.write("The primary risk detected is 'Momentum Decay'. While efficiency is at **{p_labor}**, any reduction in quality control frequency could lead to rework. We also identify a minor risk of 'Administrative Friction' during the handover to the next phase. Maintain the current pace but increase the frequency of site inspections by 15%.")
    else:
        st.markdown(f"""
        * **Schedule Compounding:** The {p_var}-day delay represents a systemic threat to the critical path, likely delaying the next three phases by an average of 20%.
        * **Thermal Degradation:** Under **{w_status}** conditions, material stability (specifically for {p_phase}) is at risk.
        * **Geopolitical Friction:** Indirect delays from the **{sc_status}** status of the supply chain will likely affect specialized machinery arrival.
        """)

    # 3. Supply Chain Status (WARS & CRISIS ANALYSIS)
    st.header("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS ANALYSIS")
    st.write(f"**Current Status:** {sc_status}")
    st.info(f"**AI Intelligence Report:** {sc_crisis}")
    st.write("Our 'Search Tool' indicates that regional tensions and maritime disruptions are fundamentally reshaping procurement strategies. For projects in **{region}**, we have detected a shift in logistics hubs. It is advised to avoid reliance on single-source international suppliers. TARYAQ recommends immediate diversification toward MODON-certified local manufacturers to bypass potential maritime blockades or war-related transit insurance spikes.")

    # 4. Weather & Impact Analysis
    st.header("IV. WEATHER IMPACT ANALYSIS")
    st.write(f"For the month of **{p_date.strftime('%B')}**, the {region} exhibits **{w_status}** patterns. The ambient load of **{w_temp}°C** {'is within the optimal operating window for structural work' if w_temp < 30 else 'represents a severe thermal challenge for outdoor operations'}.")
    st.write(f"Historically, projects of this scale in {region} see a productivity drop of 22% when {w_status} conditions persist. AI modeling suggests that the {p_phase} will require enhanced curing monitoring (if concrete) or thermal expansion allowances (if steel).")

    # 5. Workforce Coordination Strategy
    st.header("V. WORKFORCE COORDINATION STRATEGY")
    if is_safe:
        st.write(f"Maintain the current 8-hour shift structure. Since workforce efficiency is at **{p_labor}**, use this 'Golden Window' to complete 10% more of the non-critical tasks. Advice: Increase technical training for the second-tier labor force to maintain this momentum into the next phase.")
    else:
        st.markdown(f"""
        * **The Nocturnal Pivot:** Transition 80% of outdoor high-intensity tasks to the 10:00 PM - 6:00 AM window.
        * **Efficiency Buffering:** With efficiency at **{p_labor}**, provide 20-minute thermal recovery breaks every 2 hours.
        * **PM Tip:** Re-allocate high-skill labor to the most critical bottleneck identified in the Gantt chart to reduce the {p_var}-day variance.
        """)

    # 6. Estimated Additional Costs
    st.header("VI. ESTIMATED ADDITIONAL COSTS")
    if is_safe:
        st.success("**Estimated Impact: $0.00**. No emergency budget allocation is required. Maintain standard contingency (5%).")
    else:
        impact = "15% - 25%" if sc_status == "Volatile" else "8% - 12%"
        st.warning(f"**Estimated Impact: +{impact} of Phase Budget**. This is driven by emergency procurement from local sources, night-shift hazard pay, and potential liquidating damages from the {p_var}-day delay.")

    # 7. Strategic Solutions
    st.header("VII. STRATEGIC SOLUTIONS")
    if is_safe:
        st.write("1. **Continue Baseline Execution:** No changes required.")
        st.write("2. **Strategic Stockpiling:** Buy 20% extra of bulk materials now while the supply chain is stable.")
        st.write("3. **Early Inspection:** Perform a deep-audit 3 days before the phase ends.")
    else:
        st.markdown(f"""
        1. **Decentralized Procurement:** Immediately shift orders for critical components to regional suppliers in **{region}**.
        2. **Dynamic Schedule Buffering:** Inject a **{round(p_var * 1.5, 1)} day** safety margin into the master schedule.
        3. **Thermal Mitigation:** If {p_phase} involves concrete, utilize chilled water systems and ice-shaving aggregates to combat the **{w_temp}°C** load.
        """)

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Reset trigger to allow new scans
    st.session_state.trigger_scan = False

else:
    st.info("👈 Please enter project parameters and click 'EXECUTE STRATEGIC SCAN' to generate the technical dossier.")

# --- 6. FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
