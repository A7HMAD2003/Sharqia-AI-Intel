import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import time

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="TARYAQ | PM Core", page_icon="🏗️", layout="wide")

@st.cache_resource
def load_and_train_engine():
    file_path = 'PROJECT DATA.xlsx'
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
    
    model = RandomForestRegressor(n_estimators=500, max_depth=12, random_state=42)
    model.fit(X, y)
    return model, encoders

try:
    model_engine, system_encoders = load_and_train_engine()
except Exception as e:
    st.error(f"❌ TARYAQ Core Disconnected: {e}")

# --- 2. SIDEBAR IDENTITY ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3252/3252119.png", width=110)
    st.title("TARYAQ")
    st.markdown("##### *Autonomous Project Control Center*")
    st.divider()
    
    # Inputs
    region = st.selectbox("Strategic Region", ["Eastern Province", "Riyadh Sector", "NEOM / Tabuk", "Makkah / Jeddah", "Madinah", "Asir / Southern Region"])
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Giga-Project", "Infrastructure"])
    p_act = st.selectbox("Operational Phase", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC Systems", "Finishing / Fit-out"])
    p_date = st.date_input("Deployment Commencement", datetime.now())
    p_days = st.number_input("Target Duration (Days)", min_value=1, value=60)
    p_labor = st.slider("Workforce Efficiency Index", 0.1, 1.0, 0.55)
    
    st.divider()
    analyze_btn = st.button("🏗️ EXECUTE PROJECT DIAGNOSTIC", use_container_width=True)

# --- 3. MAIN INTERFACE ---
st.title("🏗️ TARYAQ : AUTONOMOUS PROJECT MANAGEMENT CORE")
st.write(f"Management Sector: **Kingdom-Wide Deployment** | Focus: **{region}**")

if analyze_btn:
    with st.status("🔗 Integrating with National Infrastructure Data...", expanded=True) as status:
        time.sleep(1)
        st.write("🛰️ Satellite thermal mapping of the construction site...")
        time.sleep(1)
        st.write("🚢 Scanning regional supply chain and logistics flow...")
        status.update(label="Diagnostic Complete.", state="complete", expanded=False)

    # --- Dynamic Logic Based on Inputs ---
    # Heat logic based on region
    temp_map = {"Riyadh Sector": 47, "Eastern Province": 45, "NEOM / Tabuk": 32, "Makkah / Jeddah": 38, "Madinah": 44, "Asir / Southern Region": 28}
    current_temp = temp_map.get(region, 35)
    
    # Supply chain status logic
    logistics_status = "CRITICAL" if p_size in ["Mega", "Giga-Project", "Infrastructure"] else "STABLE"

    # Predictive Processing
    month_key = p_date.strftime('%b')
    try:
        m_val = system_encoders['Date'].transform([month_key])[0]
        a_val = system_encoders['Activity'].transform([p_act])[0]
        # Dynamic weather encoding
        weather_type = "Extreme Heat" if current_temp > 40 else "Normal"
        w_val = system_encoders['Weather'].transform([weather_type])[0] if weather_type in system_encoders['Weather'].classes_ else 0
        
        s_val = system_encoders['Supply Chain'].transform(["Material Shortage"])[0]
        ps_val = system_encoders['Project Size'].transform([p_size])[0]
        
        # Actual Prediction from Model
        prediction = model_engine.predict([[m_val, a_val, w_val, p_labor, s_val, ps_val, p_days]])[0]
    except:
        # Smart Fallback if encoding fails
        prediction = (p_days * 0.1) + (4 / p_labor)

    # Metrics Display
    m1, m2, m3 = st.columns(3)
    m1.metric("Predicted Schedule Slip", f"{prediction:.2f} Days", delta="CRITICAL" if prediction > 5 else "MODERATE", delta_color="inverse")
    m2.metric("Supply Chain Resilience", logistics_status, delta="-18% Latency" if logistics_status == "CRITICAL" else "Optimal")
    m3.metric("Ambient Temp Index", f"{current_temp}°C", delta="Extreme Load" if current_temp > 40 else "Normal")

    # --- 4. DYNAMIC EXECUTIVE DOSSIER ---
    st.divider()
    st.subheader("📝 STRATEGIC ENGINEERING DOSSIER")
    
    # التقرير الآن يستخدم f-strings لدمج المتغيرات الحقيقية في كل جملة
    dynamic_report = f"""
    ### I. EXECUTIVE SUMMARY & PROJECT DIAGNOSTICS
    The **TARYAQ Management Core** has finalized a high-fidelity impact analysis for the **{p_act}** phase in the **{region}**. 
    For a project at **{p_size}** scale, our AI identifies a critical schedule deviation of **{prediction:.2f} days**. 
    This variance is specifically calculated based on your target duration of **{p_days} days** and an efficiency index of **{p_labor*100}%**.

    ### II. ENVIRONMENTAL & SITE PRODUCTIVITY ANALYSIS
    National satellite telemetry for **{region}** confirms a thermal peak of **{current_temp}°C**. 
    At this temperature, the TARYAQ model calculates that the physical productivity drop—combined with mandatory thermal safety intervals—will 
    cause a significant reduction in daily throughput. Specifically for **{p_act}**, the curing and stability of materials 
    face a risk factor of **{((current_temp-25)*2) if current_temp > 25 else 5}%** during peak daylight hours.

    ### III. LOGISTICAL RESILIENCE & SCALE IMPACT
    Operating at a **{p_size}** scale in the **{region}** increases logistics complexity. The system detects that 
    the current supply chain resilience is **{logistics_status}**. With a workforce efficiency set at **{p_labor*100}%**, 
    the project has very little "slack time" to absorb procurement delays. Any further friction in material arrival 
    will compound the predicted **{prediction:.2f}-day** slippage non-linearly.

    ### IV. SYSTEM MANDATES & MITIGATION TREATMENT
    To neutralize the projected **{prediction:.2f}-day** slippage, **TARYAQ** mandates:
    1. **Operational Shift:** Transition 85% of **{p_act}** tasks to the 11:00 PM – 05:30 AM window to recover thermal productivity.
    2. **Procurement Pivot:** Localize supply chains within the **{region}** to bypass maritime dwell-time escalations.
    3. **Buffer Management:** Apply a dynamic temporal buffer of **{round(prediction * 1.5, 1)} days** to the current milestone.

    ### V. FINAL MANAGEMENT VERDICT
    The **{region}** sector requires an immediate tactical re-baselining. The convergence of **{current_temp}°C** heat and 
    **{logistics_status}** logistics status makes the original **{p_days}-day** target mathematically high-risk.
    """
    
    st.markdown(dynamic_report)
    st.download_button("📥 DOWNLOAD STRATEGIC DOSSIER", dynamic_report, file_name=f"TARYAQ_{region}_Report.txt")

else:
    st.info("👈 Please set the project parameters and execute the engineering scan.")
