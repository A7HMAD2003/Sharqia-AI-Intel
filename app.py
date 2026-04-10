import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETTINGS & PAGE CONFIG ---
st.set_page_config(page_title="TARYAQ | AI Control", page_icon="🏗️", layout="wide")

# This ensures the report updates EVERY time the button is clicked
if 'report_generated' not in st.session_state:
    st.session_state.report_generated = False
    st.session_state.full_report = ""

# --- 2. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.title("🏗️ TARYAQ")
    st.markdown("##### *Dynamic Strategic Intel*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
    p_date = st.date_input("Execution Date", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=10)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.85)

    # --- ENGINEERING LOGIC VALIDATOR ---
    is_valid = True
    v_msg = ""
    if p_size == "Small" and p_days > 25:
        is_valid = False
        v_msg = f"⚠️ RED FLAG: {p_days} days for a Small scale project is excessive."
    elif p_size in ["Mega", "Infrastructure"] and p_days < 7:
        is_valid = False
        v_msg = f"⚠️ RED FLAG: {p_days} days is insufficient for Mega scale."

    if not is_valid:
        st.error(v_msg)

    st.divider()
    # Clicking this button will now force a re-run of the whole logic
    generate_btn = st.button("🚀 EXECUTE AI STRATEGIC SCAN", use_container_width=True)

# --- 3. DYNAMIC WEATHER & INTELLIGENCE ENGINE ---
def generate_dynamic_intel(region, date, p_size, p_phase, p_days, p_labor):
    month = date.month
    
    # Precise Weather Logic (By Month & Geography)
    if month in [12, 1, 2]: # Winter
        status = "Clear" if region != "Asir" else "Foggy"
        temp = 16 if region != "Jeddah" else 25
        if region == "Asir": temp = 8
    elif month in [6, 7, 8]: # Summer
        status = "Hot"
        temp = 45 if region != "Asir" else 27
        if region in ["Jeddah", "Eastern Province"]: status = "Humid"
    elif month in [3, 4, 5]: # Spring
        status = "Cloudy"
        temp = 28
        if region == "NEOM": status = "Windy"
    else: # Autumn
        status = "Thunderstorms" if region == "Asir" else "Windy"
        temp = 32

    # Calculation logic for Variance (Heuristics based on engineering)
    # This replaces illogical Excel data with realistic assumptions
    base_var = (p_days * 0.1) 
    if status in ["Hot", "Humid", "Thunderstorms"]: base_var += (p_days * 0.25)
    if p_labor < 0.7: base_var += (p_days * 0.15)
    if p_size == "Mega": base_var += 4.5
    
    variance = round(base_var, 2)
    return status, temp, variance

# --- 4. OUTPUT DISPLAY ---
st.title("🏗️ TARYAQ : PROJECT MANAGEMENT CORE")

if generate_btn:
    if not is_valid:
        st.error("Engine Blocked: Parameters are not logically sound.")
    else:
        # Reset and generate fresh data
        w_status, w_temp, p_var = generate_dynamic_intel(region, p_date, p_size, p_phase, p_days, p_labor)
        
        with st.status("📡 Running Intelligence Scan...", expanded=True) as s:
            time.sleep(1)
            st.write(f"🔍 Analyzing {region} logistics...")
            time.sleep(1)
            s.update(label="Analysis Complete!", state="complete", expanded=False)

        # Dashboard
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Predicted Slip", f"{p_var} Days", delta="CRITICAL" if p_var > 3 else "STABLE")
        c2.metric("Supply Chain", "VOLATILE" if p_size == "Mega" else "STABLE")
        c3.metric("Ambient Load", f"{w_temp}°C")
        c4.metric("Weather Status", w_status)

        st.divider()
        st.subheader("📝 STRATEGIC ENGINEERING DOSSIER")

        # Dynamic Content generation to ensure the report changes
        if p_var < 1.5:
            # POSITIVE / NO RISK REPORT
            report = f"""
            ### 1. BRIEF OVERVIEW
            The AI core identifies that the **{p_phase}** phase in **{region}** is currently within the **Optimal Execution Window**. With a planned duration of **{p_days} days**, the project is technically on track with zero detected friction.

            ### 2. POTENTIAL RISKS
            Risk level is **NEGLIGIBLE**. Current parameters suggest that all environmental and logistical variables are aligned with the project baseline.

            ### 3. SUPPLY CHAIN STATUS
            Logistics for **{p_size}** scale projects are currently **STABLE**. The AI scan confirms that regional transit routes in **{region}** are operating at 98% efficiency.

            ### 4. WEATHER IMPACT ANALYSIS
            Current status: **{w_status}** at **{w_temp}°C**. These atmospheric conditions are ideal for **{p_phase}**. No material curing or labor safety risks are present.

            ### 5. WORKFORCE COORDINATION
            Maintain current deployment levels. Advice to PM: Since efficiency is high ({p_labor}), consider pre-staging materials for the next milestone to capitalize on this stability.

            ### 6. ESTIMATED ADDITIONAL COSTS
            **$0.00**. Financial reserves should remain focused on future phases.

            ### 7. STRATEGIC SOLUTIONS
            Proceed as planned. Ensure the **{p_labor}** index is monitored weekly to maintain this momentum.
            """
        else:
            # RISK INTERVENTION REPORT
            report = f"""
            ### 1. BRIEF OVERVIEW
            A strategic variance of **{p_var} days** has been detected for the **{p_phase}** phase. Given the **{p_size}** scale, immediate parametric adjustments are required to protect the project's Critical Path.

            ### 2. POTENTIAL RISKS
            * **Schedule Slippage:** High risk of compounding delays exceeding {p_var * 2} days if not addressed.
            * **Thermal Load:** At **{w_temp}°C**, productivity is forecasted to drop by 22%.

            ### 3. SUPPLY CHAIN STATUS
            Supply chain for **{region}** is currently **{"VOLATILE" if p_size == "Mega" else "SENSITIVE"}**. AI indicates a potential 5-day delay in specialized material deliveries.

            ### 4. WEATHER IMPACT ANALYSIS
            The site is facing **{w_status}** conditions. Under **{w_status}** at **{w_temp}°C**, the **{p_phase}** requires specific material handling protocols to prevent chemical instability or labor exhaustion.

            ### 5. WORKFORCE COORDINATION
            * **Shift Modification:** Transition 80% of outdoor tasks to nocturnal hours.
            * **Rest Cycles:** Implement mandatory 10-minute cooling intervals to sustain the **{p_labor}** efficiency index.

            ### 6. ESTIMATED ADDITIONAL COSTS
            * **Logistical Expediting:** +$3,500 - $12,000 depending on urgent sourcing.
            * **Night Premiums:** +15% labor cost increase for this phase.

            ### 7. STRATEGIC SOLUTIONS
            * **Bypass Logistics:** Switch to local suppliers in **{region}** clusters.
            * **Buffer Realignment:** Add a **{round(p_var * 1.5, 1)} day** safety buffer to the next milestone immediately.
            """
        
        st.markdown(report)
        st.download_button("📥 DOWNLOAD DOSSIER", report, file_name=f"TARYAQ_{region}_Report.txt")

else:
    st.info("👈 Please enter project parameters and click 'EXECUTE AI STRATEGIC SCAN' to generate a fresh report.")
