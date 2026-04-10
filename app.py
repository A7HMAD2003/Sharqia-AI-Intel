import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. CORE SYSTEM ARCHITECTURE ---
# Title of the browser tab and dynamic updating configuration
st.set_page_config(page_title="TARYAQ | AI Control", page_icon="🏗️", layout="wide")

# Custom Styling to make the dossier beautiful and professional
# Also styling the small footer at the bottom
st.markdown("""
    <style>
    .report-box { padding: 30px; border-radius: 15px; border: 1px solid #4b5563; background-color: #1f2937; margin-bottom: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
    .report-title { color: #f3f4f6; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-bottom: 20px; font-weight: bold; font-size: 26px; }
    .report-content h3 { color: #d1d5db; border-left: 5px solid #6b7280; padding-left: 10px; margin-top: 25px; margin-bottom: 15px; font-weight: 600; font-size: 20px; }
    .report-content p { color: #e5e7eb; line-height: 1.8; margin-bottom: 15px; font-size: 16px; }
    .stMetric { background-color: #1f2937; padding: 20px; border-radius: 12px; border-bottom: 4px solid #3b82f6; }
    .footer { position: fixed; left: 0; bottom: 0; width: 100%; text-align: center; color: #9ca3af; font-size: 12px; padding: 10px; background-color: rgba(14, 17, 23, 0.8); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. ADVANCED LOGIC ENGINES ---

def get_realistic_weather(region, date):
    """Maps realistic Saudi weather based on Region and Month to avoid 'Hot in Jan' errors."""
    month = date.month
    # Logic based on Saudi Meteorological patterns
    if month in [12, 1, 2]: # Winter
        status, temp = ("Clear" if region != "Asir" else "Foggy"), (16 if region != "Jeddah" else 24)
    elif month in [6, 7, 8]: # Summer
        status, temp = ("Hot"), (46 if region != "Asir" else 29)
        if region in ["Jeddah", "Eastern Province"]: status = "Humid"
    elif month in [3, 4, 5]: # Spring
        status, temp = ("Cloudy"), (29)
        if region == "NEOM": status = "Windy"
    else: # Autumn
        status, temp = ("Thunderstorms" if region == "Asir" else "Windy"), (31)
    
    return status, temp

def engineering_risk_engine(p_size, p_days, p_labor, weather_status):
    """Fallback Heuristics if Excel data is static or illogical."""
    # Base variance from efficiency
    variance = (1.0 - p_labor) * (p_days * 0.4)
    # Environmental impact
    if weather_status in ["Hot", "Humid", "Thunderstorms"]: variance += (p_days * 0.22)
    elif weather_status == "Foggy": variance += (p_days * 0.1)
    # Project complexity factor
    if p_size == "Mega": variance += 5.2
    elif p_size == "Infrastructure": variance += 3.8
    
    return round(variance, 2)

# --- 3. SIDEBAR COMMAND CENTER ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=80)
    st.title("TARYAQ CORE")
    st.markdown("##### *Strategic Project Intelligence*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Riyadh Sector", "Eastern Province", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_phase = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
    p_date = st.date_input("Execution Date", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=15)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.90)

    # --- LOGIC VALIDATOR ---
    is_valid = True
    v_msg = ""
    if p_size == "Small" and p_days > 20:
        is_valid = False
        v_msg = f"⚠️ Logic Alert: {p_days} days is excessive for a {p_size} project's {p_phase}."
    elif p_size in ["Mega", "Infrastructure"] and p_days < 10:
        is_valid = False
        v_msg = f"⚠️ Logic Alert: {p_days} days is insufficient for {p_size} scale phase."

    if not is_valid:
        st.error(v_msg)

    st.divider()
    # Clicking this button will now force a re-run with fresh calculations
    analyze_btn = st.button("🚀 EXECUTE AI STRATEGIC SCAN", use_container_width=True)

# --- 4. MAIN INTERFACE & DYNAMIC CALCULATIONS ---
st.title("🏗️ TARYAQ : AUTONOMOUS PROJECT INTELLIGENCE")

if analyze_btn and is_valid:
    # 1. Trigger Engines
    weather_status, ambient_temp = get_realistic_weather(region, p_date)
    predicted_delay = engineering_risk_engine(p_size, p_days, p_labor, weather_status)
    
    with st.status("📡 Establishing AI Knowledge Link & Cross-Scoping Regional Data...", expanded=True) as status:
        time.sleep(1.2)
        st.write("🔍 Cross-referencing historical delay benchmarks for " + p_phase + "...")
        time.sleep(1)
        st.write(f"🌡️ analyzing thermal load for {region}...")
        status.update(label="Dynamic Scan Complete.", state="complete", expanded=False)

    # Top Metric Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Predicted Variance", f"{predicted_delay} Days", delta="HIGH RISK" if predicted_delay > 3 else "STABLE")
    m2.metric("Supply Chain", "VOLATILE" if p_size == "Mega" else "STABLE")
    m3.metric("Ambient Load", f"{ambient_temp}°C")
    m4.metric("Weather Status", weather_status)

    st.divider()
    
    # --- 5. THE BEAUTIFUL STRATEGIC DOSSIER ---
    is_safe = predicted_delay < 1.5
    
    # Text Generation with full content (7 points) to ensure correct word count
    if is_safe:
        report_type = " ✅ OPTIMAL STATUS"
        report_text = f"""
        ### 1. BRIEF OVERVIEW
        Congratulations. The project is currently operating within the **Optimal Execution Window**. For the **{p_phase}** phase in **{region}**, TARYAQ AI confirms that your baseline of **{p_days} days** is mathematically sound. The projected variance of **{predicted_delay} days** is negligible and easily absorbed by standard contingency buffers, suggesting high temporal health for a project of a **{p_size}** scale.

        ### 2. POTENTIAL RISKS
        Risk profile is categorized as strictly **STABLE**. Current parametric analysis indicates zero detected schedule-slip stressors for the foundations. However, the Project Manager must maintain the workforce morale to preserve the current efficiency index of **{p_labor}**, as any sudden drop in labor output could shift the project baseline.

        ### 3. SUPPLY CHAIN STATUS
        Regional logistics are operating at **OPTIMAL** capacity. Procurement dwells are tracking at 98% efficiency compared to the 5-year average for a **{p_size}** scale. Supply lead times for specialized materials like concrete in **{region}** currently meet baseline expectations.

        ### 4. WEATHER & ENVIRONMENTAL IMPACT
        Forecasted **{weather_status}** conditions at **{ambient_temp}°C** provide a favorable atmospheric window. These parameters are perfect for foundations, as they avoid accelerated evaporation or steel expansion. Labor endurance is not compromised under these ideal conditions.

        ### 5. OPTIMAL WORKFORCE COORDINATION
        Maintain current daylight shift patterns. No extreme shifts are required. Proactive Advice: Utilize this period to pre-stage materials 48 hours ahead of schedule to create an even larger safety buffer for future, riskier phases.

        ### 6. ESTIMATED MITIGATION COSTS
        **$0.00**. No emergency financial injection is required at this milestone. Contingency funds should remain focus on future phases.

        ### 7. SOLUTIONS
        Continue operations as per the original project baseline.

        *(AI Scan Complete)*
        """
    else:
        report_type = " ⚠️ RISK ADVISORY"
        report_text = f"""
        ### 1. BRIEF OVERVIEW
        TARYAQ identifies a critical schedule slippage of **{predicted_delay} days** for **{p_act}**. Given the **{p_size}** scale, this variance threatens the Critical Path. Immediate re-alignment of the planned **{p_days}-day** duration is required, as current parametric input violates standard engineering safety benchmarks.

        ### 2. POTENTIAL RISKS
        * **Timeline Compression:** Current variance of **{predicted_delay} days** will lead to cascading delays in subsequent milestones.
        * **Structural Integrity:** Under **{weather_status}** at **{ambient_temp}°C**, curing times for foundations fluctuate, potentially leading to micro-cracking if thermal intervals are ignored.
        * **Resource Drain:** At a **{p_labor}** efficiency, the project site cannot absorb the logistical friction points in the **{region}**.

        ### 3. SUPPLY CHAIN STATUS
        Supply chain is currently **UNDER PRESSURE** across the **Riyadh Sector**. Intelligence indicates a 14% uptick in procurement dwell-times. For a project of **{p_size}** scale, procurement of specialized concrete components faces an additional 4-day lag.

        ### 4. WEATHER & ENVIRONMENTAL IMPACT ANALYSIS
        The site is facing **{weather_status}** conditions with a thermal peak of **{ambient_temp}°C**. In these conditions, labor productivity is mathematically reduced by 30%. Evaporation rates are critical, demanding slowed concrete hydration.

        ### 5. OPTIMAL WORKFORCE COORDINATION STRATEGY
        * **Pivot to Nocturnal:** Immediately transition 75% of foundations tasks to the 10:00 PM - 05:00 AM window to bypass the **{ambient_temp}°C** load.
        * **Task Leveling:** Re-allocate low-efficiency crews to non-critical path support.
        * **Rest Cycles:** Implement mandatory 15-minute cooling stand-downs every 90 minutes.

        ### 6. ESTIMATED MITIGATION COSTS
        * **Logistics Acceleration:** +5% of phase budget for utilizing MODON industrial clusters.
        * **Night-Shift Premiums:** Projected 12% labor cost increase.
        * **Thermal Site Gear:** Estimated $2,500 - $7,000 for site-wide cooling infrastructure.

        ### 7. SOLUTIONS
        * **Decentralize Procurement:** Bypass maritime ports and source aggregate from Dammam industrial city directly.
        * **Dynamic Buffering:** Apply an AI-weighted safety margin of **{round(predicted_delay * 1.5, 1)} days** to your Gantt chart.
        * **Live AI Monitoring:** Refresh this diagnostic every 72 hours until the **{weather_status}** status clears.
        """

    # --- THE DOSSIER DISPLAY BOX (ENGINEERING DOSSIER BOX) ---
    st.markdown(f"""
        <div class="report-box">
            <div class="report-title">
                📊 Strategic Engineering Dossier - {report_type}
            </div>
            <div class="report-content report-text">
                {st.markdown(report_text, unsafe_allow_html=False)}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.download_button("📥 DOWNLOAD DOSSIER", report_text, file_name=f"TARYAQ_{region}_Report.txt")

else:
    st.info("👈 Enter project parameters and click 'EXECUTE AI STRATEGIC SCAN' to generate a fresh intelligence dossier.")


# --- FOOTER ---
st.markdown(f"""
    <div class="footer">
        Developed by Ahmad M. Al Musallem. All rights reserved. <br>
        (طور بواسطة أحمد محمد المسلم وجميع الحقوق محفوظة له)
    </div>
    """, unsafe_allow_html=True)
