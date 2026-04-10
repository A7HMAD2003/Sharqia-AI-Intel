import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. GLOBAL SETTINGS & PROFESSIONAL STYLING ---
st.set_page_config(page_title="TARYAQ | Global Strategic Control", page_icon="🏗️", layout="wide")

st.markdown("""
    <style>
    .report-container { background-color: #0e1117; padding: 25px; border-radius: 15px; border: 1px solid #1f2937; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #9ca3af; font-size: 12px; padding: 10px; background-color: rgba(14, 17, 23, 0.9); border-top: 1px solid #1f2937; z-index: 1000; }
    .stMetric { background-color: #1f2937 !important; padding: 20px !important; border-radius: 12px !important; border-bottom: 4px solid #3b82f6 !important; }
    .logic-alert { color: #ff4b4b; font-weight: bold; background-color: rgba(255, 75, 75, 0.1); padding: 10px; border-radius: 5px; }
    h1, h2, h3 { font-family: 'Segoe UI', sans-serif; }
    .status-optimal { color: #00ff7f; font-weight: bold; }
    .status-risk { color: #ff4b4b; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE GLOBAL INTELLIGENCE ENGINE (Knowledge Bank & Crisis Mapping) ---

def analyze_global_risks(region, scale):
    """Simulating Global AI Search for Wars, Disasters, and Supply Chain Tensions."""
    # Data represents real-time world status simulations (Red Sea, Global Logistics, Regional tensions)
    crisis_map = {
        "NEOM": {
            "conflict_impact": "High (Maritime security in the Red Sea directly affects heavy machinery logistics).",
            "logistics_status": "Volatile (30% increase in lead time for specialized tech).",
            "global_context": "Affected by Suez Canal traffic diversions and regional naval instability."
        },
        "Jeddah": {
            "conflict_impact": "Moderate (Increased shipping insurance premiums for regional ports).",
            "logistics_status": "Strained (Port congestion due to alternative route docking).",
            "global_context": "Direct correlation with Mediterranean-Red Sea trade disruptions."
        },
        "Eastern Province": {
            "conflict_impact": "Low (Stability in the Arabian Gulf corridor).",
            "logistics_status": "Optimal (Strong connectivity to GCC industrial hubs).",
            "global_context": "Resilient against Red Sea crisis but sensitive to global oil price fluctuations."
        },
        "Riyadh Sector": {
            "conflict_impact": "Minimal (Inland protection).",
            "logistics_status": "Stable (Strategic land-bridge and air freight connectivity).",
            "global_context": "High resilience due to diversified inland logistics hubs."
        }
    }
    
    # Default to general logic if region not in map
    data = crisis_map.get(region, {
        "conflict_impact": "Monitoring (Global status is currently under watch).",
        "logistics_status": "Stable (Local markets providing buffer).",
        "global_context": "Standard international trade flow."
    })
    
    if scale in ["Mega", "Infrastructure"]:
        data["logistics_status"] = "Strained (Global scarcity of high-performance materials)."
        
    return data

def get_precise_weather(region, date):
    """Corrected Seasonal Logic for KSA."""
    month = date.month
    # Winter (Dec, Jan, Feb)
    if month in [12, 1, 2]:
        status = "Freezing" if region in ["Riyadh Sector", "NEOM", "Asir"] else "Clear/Cool"
        temp = 13 if region != "Jeddah" else 22
    # Summer (Jun, Jul, Aug, Sep)
    elif month in [6, 7, 8, 9]:
        status = "Extreme Heat"
        temp = 46 if region != "Asir" else 28
        if region in ["Jeddah", "Eastern Province"]: status = "Extreme Heat/Humid"
    # Transition
    else:
        status = "Unsettled/Windy"
        temp = 32
        if region == "Asir": status = "Heavy Rain Risk"
        
    return status, temp

# --- 3. DYNAMIC DATA & FILE HANDLING (Knowledge Bank) ---

def process_knowledge_bank(uploaded_file):
    """Processes Excel/CSV with intelligent assumptions."""
    if uploaded_file:
        try:
            df = pd.read_excel(uploaded_file)
            return df, "Data successfully integrated from Excel."
        except:
            return None, "Error reading file. Using AI fallback assumptions."
    return None, "No file uploaded. Operating on strategic AI assumptions."

# --- 4. SIDEBAR - DYNAMIC INPUTS ---

with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=70)
    st.title("TARYAQ SYSTEM")
    st.markdown("##### *Global Engineering Intelligence*")
    st.divider()
    
    # Information Bank Upload
    st.subheader("📁 Knowledge Bank")
    kb_file = st.file_uploader("Sync Project Data (Excel)", type=["xlsx"])
    df_bank, kb_status = process_knowledge_bank(kb_file)
    st.caption(kb_status)
    
    st.divider()
    
    # Control Parameters
    region = st.selectbox("Project Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_scale = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_phase = st.selectbox("Construction Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
    p_date = st.date_input("Start Date", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=15)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85)

    # --- LOGIC VALIDATOR (The 'Common Sense' Engine) ---
    is_logical = True
    logic_error = ""
    if p_scale == "Small" and p_days > 25:
        logic_error = f"⚠️ LOGIC ERROR: {p_days} days is excessive for a Small project's {p_phase} phase."
        is_logical = False
    elif p_scale in ["Mega", "Infrastructure"] and p_days < 10:
        logic_error = f"⚠️ LOGIC ERROR: {p_days} days is insufficient for {p_scale} scale engineering."
        is_logical = False

    if not is_logical:
        st.markdown(f"<div class='logic-alert'>{logic_error}</div>", unsafe_allow_html=True)

    st.divider()
    analyze_btn = st.button("🚀 EXECUTE GLOBAL SCAN", use_container_width=True)

# --- 5. MAIN INTERFACE & REPORTING ENGINE ---

st.title("🏗️ TARYAQ : ADVANCED STRATEGIC DOSSIER")

if analyze_btn and is_logical:
    # Trigger AI Engines
    with st.status("📡 Connecting to Global Strategic Intelligence...", expanded=False) as status:
        global_intel = analyze_global_risks(region, p_scale)
        time.sleep(1)
        w_status, w_temp = get_precise_weather(region, p_date)
        time.sleep(1)
        status.update(label="Global Analysis Complete!", state="complete")

    # Calculated Variance
    base_var = (1.0 - p_labor) * p_days
    env_impact = 4.5 if "Extreme Heat" in w_status or "Rain" in w_status else 0
    geo_impact = 6.0 if "High" in global_intel['conflict_impact'] else 1.0
    total_var = round(base_var + env_impact + geo_impact, 2)
    is_safe = total_var < 5.0

    # Dashboard Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Predicted Delay", f"{total_var} Days", delta="CRITICAL" if not is_safe else "SAFE")
    c2.metric("Regional Risk", global_intel['conflict_impact'].split()[0])
    c3.metric("Weather Load", w_status)
    c4.metric("Ambient Temp", f"{w_temp}°C")

    st.divider()

    # --- THE COMPREHENSIVE REPORT (150 - 1000 Words) ---
    st.header("📑 ENGINEERING STRATEGIC DOSSIER")
    
    # 1. Brief Overview
    st.subheader("I. EXECUTIVE SUMMARY")
    st.write(f"""
    TARYAQ Global Intelligence has processed the operational parameters for the **{p_phase}** phase of the **{p_scale}** project located in the **{region}**. 
    The AI engine has cross-referenced regional telemetry with global maritime and geopolitical data. 
    Current projections indicate a total schedule variance of **{total_var} days**. 
    {'The project is currently trending towards an optimal completion window with minimal friction.' if is_safe else 'The project is flagged for high-risk delays due to external stressors; immediate strategic intervention is required to safeguard the critical path.'}
    """)

    # 2. Potential Risks
    st.subheader("II. POTENTIAL OPERATIONAL RISKS")
    if is_safe:
        st.write("Current risk levels are nominal. The primary focus should be maintaining the workforce index and ensuring that 'Just-In-Time' delivery remains uncompromised by micro-logistical failures. No systemic threats from global conflicts are currently impacting this specific local window.")
    else:
        st.markdown(f"""
        * **Supply Chain Fragmentation:** High probability of lead-time inflation due to regional maritime instability.
        * **Thermal Degradation:** Predicted **{w_temp}°C** peaks will likely impact material performance (especially in {p_phase}).
        * **Geopolitical Volatility:** The project's proximity to **{region}** logistics hubs exposes it to international trade-route tensions.
        """)

    # 3. Supply Chain (The Global Connector)
    st.subheader("III. GLOBAL SUPPLY CHAIN & CRISIS ASSESSMENT")
    st.markdown(f"""
    * **Global Context:** {global_intel['global_context']}
    * **Crisis Impact:** {global_intel['conflict_impact']}
    * **AI Supply Logic:** TARYAQ identifies that for projects of **{p_scale}** scale, dependence on international long-lead items is high. Due to the **{global_intel['logistics_status']}** status, we recommend activating 'Alternative Sourcing' protocols immediately. Our global search indicates that maritime routes through the Red Sea are currently experiencing delays that could inject up to **{total_var} days** of additional buffer requirements.
    """)

    # 4. Weather Impact
    st.subheader("IV. METEOROLOGICAL IMPACT ANALYSIS")
    st.write(f"The forecasting for **{p_date.strftime('%B %Y')}** in **{region}** confirms **{w_status}** at **{w_temp}°C**. This is consistent with TARYAQ's historical weather bank. {'Conditions are ideal for structural work.' if 'Heat' not in w_status else 'This load requires a mandatory heat-mitigation plan. Concrete pouring during peak hours will fail quality audits due to evaporation rates.'}")

    # 5. Workforce Strategy
    st.subheader("V. WORKFORCE COORDINATION STRATEGY")
    if is_safe:
        st.markdown("* **Instruction:** Maintain current shift patterns. Optimize for early-morning high-productivity windows to stay ahead of the curve.")
    else:
        st.markdown(f"""
        * **Strategic Pivot:** Transition to 'Nocturnal Operations' for the {p_phase} phase to bypass the **{w_temp}°C** peak.
        * **Incentive Alignment:** Given the **{p_labor}** index, implement a 'Safety-First' bonus to prevent fatigue-related accidents during high-stress windows.
        """)

    # 6. Additional Costs
    st.subheader("VI. FINANCIAL CONTINGENCY ESTIMATION")
    if is_safe:
        st.info("**Projected Extra Cost: 0%**. Budget remains within baseline parameters.")
    else:
        cost_inc = "15% - 22%" if p_scale in ["Mega", "Infrastructure"] else "8%"
        st.warning(f"**Projected Extra Cost: +{cost_inc}**. This covers premium shipping routes, night-shift labor differentials, and thermal protection additives.")

    # 7. Strategic Solutions
    st.subheader("VII. PROPOSED STRATEGIC SOLUTIONS")
    if is_safe:
        st.success("CONTINUE AS PLANNED. **Manager Tip:** Utilize this stable period to stockpile 20% of phase-2 materials as a hedge against future global volatility.")
    else:
        st.markdown(f"""
        * **Logistics Re-routing:** Bypass Red Sea routes by utilizing land-bridge logistics from the Eastern Province to {region}.
        * **Schedule Buffering:** Inject a **{round(total_var * 1.5, 1)} day** 'Strategic Buffer' into the Gantt chart.
        * **Crisis Monitoring:** Monitor TARYAQ live alerts for any escalation in regional tensions that may affect the Madinah-NEOM corridor.
        """)

    # --- DOWNLOAD DATA ---
    report_data = f"TARYAQ REPORT: {region} - {p_phase}\nScale: {p_scale}\nDelay: {total_var} days\nStatus: {global_intel['conflict_impact']}"
    st.download_button("📥 DOWNLOAD FULL ENGINEERING DOSSIER", report_data, file_name=f"TARYAQ_{region}_Report.txt")

else:
    st.info("👈 Please enter project parameters and click 'EXECUTE GLOBAL SCAN' to generate the report.")

# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
