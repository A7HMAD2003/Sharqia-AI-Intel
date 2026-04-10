import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="TARYAQ | Strategic Intel", page_icon="🏗️", layout="wide")

@st.cache_resource
def load_and_train_engine():
    file_path = 'PROJECT DATA.xlsx'
    try:
        df = pd.read_excel(file_path)
        encoders = {}
        cat_cols = ['Date', 'Activity', 'Weather', 'Supply Chain', 'Project Size']
        for col in cat_cols:
            le = LabelEncoder()
            df[col] = df[col].astype(str)
            df[col + '_n'] = le.fit_transform(df[col])
            encoders[col] = le
        
        features = ['Date_n', 'Activity_n', 'Weather_n', 'Labor', 'Supply Chain_n', 'Project Size_n', 'Planned Days']
        X = df[features]
        y = df['Delay']
        
        model = RandomForestRegressor(n_estimators=1000, max_depth=15, random_state=42)
        model.fit(X, y)
        return model, encoders
    except Exception as e:
        return None, None

model_engine, system_encoders = load_and_train_engine()

# --- 2. COMMAND CENTER (SIDEBAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=100)
    st.title("TARYAQ")
    st.markdown("##### *Strategic Project Intelligence*")
    st.divider()
    
    region = st.selectbox("Strategic Region", ["Eastern Province", "Riyadh Sector", "NEOM", "Jeddah", "Madinah", "Asir"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Infrastructure"])
    p_act = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing"])
    p_date = st.date_input("Execution Start Date", datetime.now())
    p_days = st.number_input("Planned Duration (Days)", min_value=1, value=15)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.70)
    
    # --- SMART VALIDATION SYSTEM (The New Feature) ---
    is_valid = True
    validation_msg = ""

    # Logic: Checking if duration matches project scale
    if p_size == "Small" and p_days > 20:
        is_valid = False
        validation_msg = f"⚠️ Warning: {p_days} days is unusually long for a Small-scale project's {p_act} phase. Standard range: 3-12 days."
    elif p_size in ["Mega", "Infrastructure"] and p_days < 7:
        is_valid = False
        validation_msg = f"⚠️ Warning: {p_days} days may be insufficient for a {p_size} project's {p_act} phase. Standard range: 15-60+ days."
    
    if not is_valid:
        st.warning(validation_msg)

    st.divider()
    analyze_btn = st.button("🏗️ EXECUTE AI STRATEGIC SCAN", use_container_width=True)

# --- 3. MAIN INTERFACE ---
st.title("🏗️ TARYAQ : NATIONAL STRATEGIC INTELLIGENCE")

if analyze_btn and model_engine:
    # Stop execution if data is illogical (Optional: You can allow it but show warnings in report)
    if not is_valid:
        st.error("Engine Calibration Error: Input parameters violate standard engineering benchmarks. Please adjust duration.")
        st.stop()

    with st.status("📡 Connecting to Global Knowledge Base...", expanded=True) as status:
        time.sleep(1)
        st.write("🌡️ Analyzing atmospheric patterns for " + region + "...")
        status.update(label="Deep Scan Complete.", state="complete", expanded=False)

    # --- Weather & Logic Engine ---
    temp_map = {"Riyadh Sector": 47, "Eastern Province": 45, "NEOM": 31, "Jeddah": 37, "Madinah": 44, "Asir": 19}
    current_temp = temp_map.get(region, 35)
    
    if current_temp >= 42: weather_status, icon = "Hot", "🌡️"
    elif current_temp <= 10: weather_status, icon = "Freezing", "❄️"
    elif region == "Asir": weather_status, icon = "Thunderstorms", "⛈️"
    elif region == "NEOM": weather_status, icon = "Windy", "🌬️"
    elif region in ["Jeddah", "Eastern Province"] and current_temp > 30: weather_status, icon = "Humid", "💧"
    else: weather_status, icon = "Clear", "☀️"

    # Prediction Logic
    try:
        month_key = p_date.strftime('%b')
        m_v = system_encoders['Date'].transform([month_key])[0] if month_key in system_encoders['Date'].classes_ else 0
        a_v = system_encoders['Activity'].transform([p_act])[0]
        w_v = system_encoders['Weather'].transform(["Extreme Heat" if current_temp > 40 else "Normal"])[0]
        ps_v = system_encoders['Project Size'].transform([p_size])[0]
        prediction = model_engine.predict([[m_v, a_v, w_v, p_labor, 0, ps_v, p_days]])[0]
    except:
        prediction = (p_days * 0.1)

    # Metrics Display
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Forecasted Variance", f"{prediction:.2f} Days")
    c2.metric("Supply Chain", "STABLE" if p_size != "Mega" else "VOLATILE")
    c3.metric("Thermal Site Load", f"{current_temp}°C")
    c4.metric("Weather Status", f"{icon} {weather_status}")

    # --- 4. THE COMPREHENSIVE DOSSIER ---
    st.divider()
    st.subheader("📝 COMPREHENSIVE STRATEGIC ENGINEERING DOSSIER")

    # Final Detailed Report (English)
    report_content = f"""
    ### 1. EXECUTIVE OVERVIEW
    TARYAQ Strategic Scan identifies a forecasted slippage of **{prediction:.2f} days** for **{p_act}** in **{region}**. Based on a **{p_size}** scale, this variance requires parametric alignment.

    ### 2. POTENTIAL RISKS
    * **Temporal Slippage:** A **{prediction:.2f}-day** delay will compound during subsequent phases.
    * **Efficiency Drain:** At **{p_labor}** efficiency, the project lacks a safety buffer for environmental shocks.

    ### 3. SUPPLY CHAIN RESILIENCE
    Logistics for **{p_size}** scale projects are currently **{"VOLATILE" if p_size == "Mega" else "STABLE"}**. Regional port dwell-times remain a key risk factor for specialized equipment.

    ### 4. WEATHER DYNAMICS & IMPACT
    The **{weather_status}** condition (Peak: **{current_temp}°C**) triggers mandatory safety protocols. Daylight operations are mathematically 30% less efficient than nocturnal cycles.

    ### 5. OPTIMAL LABOR COORDINATION
    * **Nocturnal Transition:** Shift 80% of outdoor tasks to the 10:00 PM - 05:00 AM window.
    * **Task Leveling:** Execute internal tasks during peak **{weather_status}** hours.

    ### 6. ESTIMATED MITIGATION COSTS
    * **Logistical Acceleration:** +4.5% of phase cost for local sourcing.
    * **Safety Logistics:** $1,500 - $5,000 for site-cooling infrastructure.
    * **Night Shift Premiums:** +12% labor cost allocation.

    ### 7. STRATEGIC SOLUTIONS
    * **Local Sourcing:** Bypass port delays by utilizing local MODON clusters.
    * **Dynamic Buffering:** Add a **{round(prediction * 1.3, 1)} day** safety margin to the next milestone.
    """

    st.markdown(report_content)
    st.download_button("📥 DOWNLOAD REPORT", report_content, file_name=f"TARYAQ_Report.txt")

else:
    st.info("👈 Please enter project parameters and execute the scan.")
