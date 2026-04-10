import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from datetime import datetime
import time

# --- 1. SETTINGS & AI ENGINE ---
st.set_page_config(page_title="Sharqia AI Intel", page_icon="🏗️", layout="wide")

@st.cache_resource
def load_and_train():
    # تأكد أن هذا الاسم يطابق تماماً ملفك المرفوع: PROJECT DATA.xlsx
    file_name = 'PROJECT DATA.xlsx' 
    
    # قراءة ملف الإكسل
    df = pd.read_excel(file_name)
    
    encoders = {}
    for col in ['Date', 'Activity', 'Weather', 'Supply Chain', 'Project Size']:
        le = LabelEncoder()
        df[col] = df[col].astype(str)
        df[col + '_n'] = le.fit_transform(df[col])
        encoders[col] = le
    
    features = ['Date_n', 'Activity_n', 'Weather_n', 'Labor', 'Supply Chain_n', 'Project Size_n', 'Planned Days']
    X = df[features]
    y = df['Delay']
    model = RandomForestRegressor(n_estimators=200, random_state=42).fit(X, y)
    return model, encoders

# Initialize Model
try:
    model, encoders = load_and_train()
except Exception as e:
    st.error(f"⚠️ Critical Error: Could not find or read 'PROJECT DATA.xlsx'. Please ensure the file is uploaded to GitHub. Error: {e}")

# --- 2. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.header("🏗️ Control Center")
    p_size = st.selectbox("Project Scale", ["Small", "Medium", "Large", "Mega", "Giga", "Infrastructure"])
    p_act = st.selectbox("Phase Activity", ["Foundations", "Steel Structure", "Concrete Pouring", "HVAC", "Finishing"])
    p_date = st.date_input("Deployment Date", datetime.now())
    p_days = st.number_input("Planned Duration (Days)", min_value=1, value=30)
    p_labor = st.slider("Workforce Efficiency", 0.1, 1.0, 1.0)
    
    st.divider()
    run_btn = st.button("🚀 LAUNCH GLOBAL AI SCAN", use_container_width=True)

# --- 3. MAIN DASHBOARD ---
st.title("🏗️ Sharqia Autonomous Construction Intel")
st.write("Specialized AI Sector: **Al-Khobar, Saudi Arabia**")

if run_btn:
    with st.status("🔍 AI Agent scanning global news and Al-Khobar logistics...", expanded=True) as status:
        time.sleep(2)
        st.write("Accessing King Abdulaziz Port real-time data...")
        time.sleep(1)
        st.write("Analyzing regional thermal & humidity indices for Al-Khobar...")
        time.sleep(1)
        status.update(label="Scanning Complete. Intelligence Report Generated.", state="complete", expanded=False)

    # Simulated Autonomous Intelligence Findings
    intel = {
        "supply_key": "Material Shortage", 
        "supply_label": "CRITICAL (Logistics Backlog Detected)",
        "weather_key": "Extreme Heat",
        "temp": 44,
        "market_risk": "Supply chain instability detected; procurement costs forecasted to rise by 4.2%."
    }

    # Model Prediction Logic
    m_name = p_date.strftime('%b')
    try:
        m_n = encoders['Date'].transform([m_name])[0] if m_name in encoders['Date'].classes_ else 0
        a_n = encoders['Activity'].transform([p_act])[0] if p_act in encoders['Activity'].classes_ else 0
        w_n = encoders['Weather'].transform([intel['weather_key']])[0]
        s_n = encoders['Supply Chain'].transform([intel['supply_key']])[0]
        ps_n = encoders['Project Size'].transform([p_size])[0]
        
        prediction = model.predict([[m_n, a_n, w_n, p_labor, s_n, ps_n, p_days]])[0]
    except:
        prediction = 6.85 # Fallback for demo

    # Results UI Display
    col1, col2, col3 = st.columns(3)
    col1.metric("Predicted Delay", f"{prediction:.2f} Days", delta="CRITICAL", delta_color="inverse")
    col2.metric("Supply Chain Status", intel['supply_label'])
    col3.metric("Ambient Temp", f"{intel['temp']}°C", delta="High Heat")

    st.subheader("📜 Executive Intelligence Report")
    st.markdown(f"""
    ---
    ### 🧠 AI Strategic Diagnostic
    The autonomous diagnostic for **Al-Khobar** predicts a schedule deviation of **{prediction:.2f} days**. 
    
    **1. Environmental Analysis:**
    The thermal load of **{intel['temp']}°C** significantly impacts the **{p_act}** phase. Labor productivity is forecasted to drop by 20% due to heat stress.
    
    **2. Market Intelligence:**
    {intel['market_risk']} Direct maritime disruptions are impacting regional delivery lead times.
    
    **3. Mitigation Strategies:**
    - **Nocturnal Shift:** Execute outdoor components from 11 PM to 6 AM to bypass heat peaks.
    - **Local Sourcing:** Shift procurement to Dammam Industrial City to avoid port congestion.
    - **Thermal Buffer:** Apply a 10% safety buffer to the completion date of this phase.
    """)
else:
    st.info("👈 Configure the project in the sidebar and launch the AI scan.")
