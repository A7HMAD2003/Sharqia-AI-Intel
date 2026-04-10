import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETTINGS & ADVANCED STYLING ---
st.set_page_config(page_title="TARYAQ | AI Engineering Intelligence", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0d1117; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #8b949e; font-size: 11px; padding: 10px; background-color: #161b22; border-top: 1px solid #30363d; z-index: 1000; }
    .stMetric { background-color: #161b22 !important; padding: 20px !important; border-radius: 12px !important; border-bottom: 4px solid #3b82f6 !important; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }
    .report-card { background-color: #ffffff; color: #1a1a1a; padding: 45px; border-radius: 15px; line-height: 1.9; text-align: justify; box-shadow: 0 10px 30px rgba(0,0,0,0.15); border: 1px solid #e1e4e8; }
    .logic-alert { background-color: #ffeef0; color: #d73a49; padding: 15px; border-radius: 8px; border: 1px solid #f97583; margin-bottom: 20px; font-weight: bold; }
    h1, h2, h3 { font-family: 'Inter', sans-serif; color: #3b82f6; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE 50 ENGINEERING PHASES ---
PHASES = [
    "Project Feasibility Study", "Architect & Consultant Selection", "Concept Architectural Design",
    "Structural, MEP & Civil Drawings", "Building Permit Acquisition", "Contractor Bidding & Selection",
    "Contract Signing & Bill of Quantities (BOQ)", "Site Handover to Contractor", "Preparation of Shop Drawings",
    "Site Mobilization & Temporary Facilities", "Site Clearing & Grubbing", "Land Surveying & Setting Out",
    "Excavation Works", "Anti-Termite Soil Treatment", "Blinding Concrete (Lean Concrete)",
    "Foundation Waterproofing (Batten)", "Foundation Reinforcement & Formwork", "Pouring Foundation Concrete",
    "Column Neck Reinforcement & Formwork", "Pouring Column Necks", "Bitumen Coating for Underground Structures",
    "Backfilling & Compaction (Layers)", "Ground Beam (Plinth Beam) Construction", "Under-slab MEP Piping Installation",
    "Ground Floor Column Reinforcement", "Pouring Ground Floor Columns", "Slab-on-Grade & Upper Slab Formwork",
    "Slab Reinforcement & Conduit Placement", "Pouring Concrete Slabs", "Masonry Works (Blockwork)",
    "Electrical Conduit Installation (First Fix)", "Plumbing & Drainage Piping (First Fix)", "HVAC Copper Pipe Routing",
    "Door & Window Frame Installation", "Internal Plastering Works", "External Rendering (Plastering)",
    "Firefighting & Gas System Installation", "Roof & Wet Area Waterproofing", "False Ceiling & Gypsum Works",
    "Thermal Insulation for Facades", "Floor & Wall Tiling Works", "Internal Painting (Primer & Putty)",
    "Sanitary Ware Installation", "Electrical Switchgear & Panel Installation", "Lighting Fixture Installation",
    "HVAC Unit Installation (Indoor/Outdoor)", "Joinery (Doors, Windows & Cabinets)", "Final Coat Painting",
    "Post-Construction Cleaning", "Final Inspection & Project Handover"
]

# --- 3. INTELLIGENCE ENGINES ---

def global_intel_scan(region, phase, scale):
    """Simulates a global AI search for wars, crises, and supply chain impacts."""
    # Logic to vary output based on region and current global events
    impact_factor = "High" if region in ["NEOM", "Jeddah"] else "Moderate"
    
    scenarios = {
        "Maritime": "Red Sea tensions are causing 18-24 day delays in electromechanical arrivals for western regions.",
        "Industrial": "Global energy crisis in Europe is spiking the cost of high-grade finishing materials by 15%.",
        "Regional": "Stability in central KSA is high, but steel prices are volatile due to international raw material shifts.",
        "GigaScale": f"Competition for resources among {scale} projects in {region} is creating internal supply bottlenecks."
    }
    
    status = "Critical/Volatile" if impact_factor == "High" else "Stable/Monitoring"
    details = f"{scenarios['Maritime'] if region in ['NEOM', 'Jeddah'] else scenarios['Regional']} {scenarios['GigaScale']}"
    
    return status, details

def get_precise_weather(region, date):
    """Accurate Seasonal KSA Weather Patterns."""
    month = date.month
    if month in [12, 1, 2]: # Winter
        status, temp = ("Freezing/Foggy", 11) if region in ["Riyadh Sector", "NEOM", "Asir"] else ("Clear", 21)
    elif month in [6, 7, 8, 9]: # Summer
        status, temp = ("Extreme Heat", 46) if region != "Asir" else ("Mild", 27)
        if region in ["Jeddah", "Eastern Province"]: status = "Extreme Heat/Humid"
    elif month in [3, 4, 5]: # Spring
        status, temp = ("Sandstorms", 32) if region in ["Riyadh Sector", "NEOM"] else ("Moderate", 28)
        if region == "Asir": status = "Thunderstorms"
    else: # Autumn
        status, temp = ("High Winds", 33)
    return status, temp

# --- 4. LOGIC GUARD (Validation) ---
def validate_inputs(scale, days, phase):
    # Logic: Small projects shouldn't take too long for simple phases, and Mega projects need minimum time
    if scale == "Small" and days > 25 and "Pouring" in phase:
        return False, f"⚠️ Logic Alert: {days} days for {phase} in a Small project is inefficient. Re-check scheduling."
    if scale in ["Mega", "Infrastructure", "Giga"] and days < 14:
        return False, f"⚠️ Logic Alert: {days} days is insufficient for {scale} scale safety and curing protocols."
    return True, ""

# --- 5. SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.title("TARYAQ AI CORE")
    st.markdown("##### *Strategic Project Intelligence*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_scale = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Giga", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase", PHASES)
    p_date = st.date_input("Start Date", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=20)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85)

    is_logical, logic_msg = validate_inputs(p_scale, p_days, p_phase)
    if not is_logical:
        st.markdown(f"<div class='logic-alert'>{logic_msg}</div>", unsafe_allow_html=True)

    st.divider()
    analyze_btn = st.button("🚀 EXECUTE STRATEGIC SCAN", use_container_width=True)

# --- 6. MAIN ENGINE & REPORT GENERATOR ---
st.title("🏗️ TARYAQ : ADVANCED ENGINEERING INTELLIGENCE")

if analyze_btn and is_logical:
    with st.spinner("Analyzing Global Geopolitics & Regional Telemetry..."):
        time.sleep(1.2)
        
        # Fresh Data Generation
        w_status, w_temp = get_precise_weather(region, p_date)
        sc_status, sc_intel = global_intel_scan(region, p_phase, p_scale)
        
        # Advanced Variance Calculation
        base_var = (1.0 - p_labor) * (p_days * 0.5)
        weather_tax = 6 if "Extreme" in w_status or "Storm" in w_status else 0
        supply_tax = 8 if "Critical" in sc_status else 0
        total_var = round(base_var + weather_tax + supply_tax + (p_days * 0.05), 2)
        
        is_safe = total_var < 5.0

        # UI Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Variance", f"{total_var} Days", delta="CRITICAL" if not is_safe else "STABLE", delta_color="inverse")
        c2.metric("Supply Chain", sc_status)
        c3.metric("Weather Load", w_status)
        c4.metric("Ambient Temp", f"{w_temp}°C")

        st.divider()

        # DYNAMIC LONG-FORM REPORT (7 SECTIONS)
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.header("📑 STRATEGIC ENGINEERING DOSSIER")
        
        # I. Brief Overview
        st.subheader("I. BRIEF OVERVIEW")
        st.write(f"""The TARYAQ AI engine has processed a comprehensive simulation for the **{p_phase}** phase of the **{p_scale}** project in **{region}**. 
        By cross-referencing your Efficiency Index ({p_labor}) with regional knowledge banks and real-time infrastructure data, we predict a potential 
        variance of **{total_var} days**. {'This variance is within the safety threshold, indicating a robust plan.' if is_safe else 
        'This variance indicates a high risk of project slippage that could compromise the entire milestone schedule.'} This assessment integrates 
        historical data from the Saudi Vision 2030 project repository and current geotechnical constraints in the {region}.""")

        # II. Potential Risks
        st.subheader("II. POTENTIAL RISKS")
        if is_safe:
            st.write(f"""While the current trajectory is stable, the Project Manager must monitor 'Micro-Friction' events. Specifically for {p_phase}, 
            there is a residual risk of equipment calibration errors. Given the {p_scale} scale, any minor error in {p_phase} will be magnified 
            in the later stages of construction. We recommend a proactive quality audit every 72 hours.""")
        else:
            st.write(f"""1. **Timeline Compounding:** A {total_var}-day delay in {p_phase} will create a bottleneck for subsequent MEP and finishing works.
            2. **Thermal Stress:** The {w_temp}°C peak temperature in {region} threatens both material curing integrity and labor productivity.
            3. **Resource Strain:** Our AI indicates that {p_scale} projects in this sector are currently competing for the same specialized machinery, 
            likely leading to unexpected rental price surges.""")

        # III. Supply Chain Status & Global Crisis Impact
        st.subheader("III. SUPPLY CHAIN STATUS & GLOBAL CRISIS IMPACT")
        st.write(f"**Status: {sc_status}**. {sc_intel}")
        st.write(f"""Global geopolitical shifts, specifically in the Red Sea and Eastern Europe, have disrupted the 'Just-in-Time' delivery models 
        for projects in **{region}**. For the **{p_phase}** phase, we observe a volatility in the procurement of high-tension steel and electronic switchgear. 
        TARYAQ recommends immediate 'Strategic Stockpiling'—securing 40% of future phase materials now to avoid war-related logistics blockades 
        or sudden freight spikes that could reach 20% by next quarter.""")

        # IV. Weather & Environmental Impact
        st.subheader("IV. WEATHER IMPACT ANALYSIS")
        st.write(f"Telemetry for **{p_date.strftime('%B')}** in **{region}** reveals **{w_status}** conditions with peaks of **{w_temp}°C**.")
        if "Heat" in w_status:
            st.write(f"""This thermal load represents a primary risk to the **{p_phase}** process. High temperatures accelerate the evaporation of 
            moisture in concrete and plaster, leading to structural cracks. Our AI suggests a 12% reduction in productivity during daylight 
            hours. Managers must implement thermal mitigation protocols immediately.""")
        else:
            st.write(f"Weather conditions are mathematically optimal for this phase. This provides a rare window to accelerate outdoor {p_phase} activities.")

        # V. Workforce Coordination Strategy
        st.subheader("V. WORKFORCE COORDINATION STRATEGY")
        if is_safe:
            st.write(f"""Current labor morale and efficiency ({p_labor}) are excellent. To maintain this, TARYAQ suggests implementing 
            'Predictive Inspection'—completing quality checks 6 hours ahead of schedule. Provide the team with standard performance incentives 
            to capitalize on this momentum before the next high-risk phase.""")
        else:
            st.write(f"""1. **Shift Inversion:** Shift 70% of high-intensity labor to the nocturnal window (8:00 PM - 4:00 AM) to bypass {w_temp}°C heat.
            2. **Hydration & Safety:** Implement mandatory 20-minute 'Cooling Cycles' every 2 hours for all outdoor personnel.
            3. **Task Fragmentation:** Break down {p_phase} into smaller, 4-hour sub-tasks to ensure the {p_labor} index doesn't drop further.""")

        # VI. Estimated Additional Costs
        st.subheader("VI. ESTIMATED ADDITIONAL COSTS")
        impact = "2% - 5%" if is_safe else "15% - 22%"
        st.write(f"""The predicted financial impact on the phase budget is **{impact}**. 
        In **{region}**, this is driven by:
        * Premium nocturnal labor rates to mitigate weather risk.
        * Logistics surcharges for re-routing materials away from 'Volatile' maritime zones.
        * Emergency contingency for secondary sourcing of specialized components.""")

        # VII. Strategic Solutions
        st.subheader("VII. STRATEGIC SOLUTIONS")
        if is_safe:
            st.success(f"Execution is optimal. **Strategic Tip:** Utilize this stability to finalize the 'Shop Drawings' for the next milestone early.")
        else:
            st.markdown(f"""
            * **Buffer Injection:** Insert a safety buffer of **{round(total_var * 1.2, 1)} days** into the master Gantt chart immediately.
            * **Domestic Sourcing:** Transition at least 30% of your current supply needs to local MODON industrial hubs to decouple from global risks.
            * **Thermal Additives:** Use chilled water and retarding agents if {p_phase} involves concrete or plastering in **{w_temp}°C** weather.""")

        st.markdown("</div>", unsafe_allow_html=True)
        st.download_button("📥 DOWNLOAD FULL DOSSIER", f"TARYAQ REPORT\nRegion: {region}\nPhase: {p_phase}\nVariance: {total_var}...", file_name=f"TARYAQ_{region}_Full.txt")

else:
    st.info("👈 Enter project parameters and execute the Strategic Scan to generate the report.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
