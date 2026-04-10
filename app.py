import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
import os

# -------------------------------
# 1. PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="TARYAQ AI v2", layout="wide")

# -------------------------------
# 2. LOAD / CREATE DATASET
# -------------------------------
@st.cache_data
def load_data():
    if os.path.exists("project_data.csv"):
        df = pd.read_csv("project_data.csv")
    else:
        # Dataset مبدئي (تقدر تطوره لاحقًا)
        data = {
            "region": ["Riyadh Sector", "NEOM", "Jeddah", "Eastern Province"] * 20,
            "size": ["Small", "Medium", "Large", "Mega"] * 20,
            "phase": ["Excavation Works", "Concrete", "Finishing", "MEP"] * 20,
            "temp": np.random.randint(20, 50, 80),
            "labor": np.random.uniform(0.5, 1.0, 80),
            "delay": np.random.randint(1, 15, 80)
        }
        df = pd.DataFrame(data)
    return df

df = load_data()

# -------------------------------
# 3. ENCODING
# -------------------------------
le_region = LabelEncoder()
le_size = LabelEncoder()
le_phase = LabelEncoder()

df["region"] = le_region.fit_transform(df["region"])
df["size"] = le_size.fit_transform(df["size"])
df["phase"] = le_phase.fit_transform(df["phase"])

# -------------------------------
# 4. TRAIN MODEL
# -------------------------------
X = df[["region", "size", "phase", "temp", "labor"]]
y = df["delay"]

model = RandomForestRegressor(n_estimators=120, random_state=42)
model.fit(X, y)

# -------------------------------
# 5. WEATHER ENGINE
# -------------------------------
def get_weather(region, date):
    month = date.month
    if month in [6,7,8,9]:
        return "Extreme Heat", 45
    elif month in [12,1,2]:
        return "Cold", 15
    else:
        return "Moderate", 30

# -------------------------------
# 6. RISK ENGINE (محسن)
# -------------------------------
def calculate_risk(pred_delay, duration):
    risk_score = (pred_delay / duration) * 100
    
    if risk_score < 20:
        level = "LOW"
    elif risk_score < 50:
        level = "MEDIUM"
    else:
        level = "HIGH"
        
    return round(risk_score,2), level

# -------------------------------
# 7. UI
# -------------------------------
st.title("🏗️ TARYAQ AI ENGINE v2")

col1, col2, col3 = st.columns(3)

with col1:
    region = st.selectbox("Region", ["Riyadh Sector", "NEOM", "Jeddah", "Eastern Province"])
    size = st.selectbox("Project Size", ["Small", "Medium", "Large", "Mega"])

with col2:
    phase = st.selectbox("Phase", ["Excavation Works", "Concrete", "Finishing", "MEP"])
    duration = st.number_input("مدة المشروع (Days)", 1, 365, 30)

with col3:
    date = st.date_input("Start Date", datetime.now())
    labor = st.slider("Labor Efficiency", 0.1, 1.0, 0.8)

# -------------------------------
# 8. PREDICTION
# -------------------------------
if st.button("🚀 Run AI Analysis"):

    weather, temp = get_weather(region, date)

    # Encoding input
    r = le_region.transform([region])[0]
    s = le_size.transform([size])[0]
    p = le_phase.transform([phase])[0]

    input_data = np.array([[r, s, p, temp, labor]])

    pred_delay = model.predict(input_data)[0]

    risk_score, risk_level = calculate_risk(pred_delay, duration)

    # ---------------------------
    # DISPLAY
    # ---------------------------
    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Predicted Delay", f"{round(pred_delay,2)} Days")
    c2.metric("Risk Score", f"{risk_score}%")
    c3.metric("Risk Level", risk_level)
    c4.metric("Temperature", f"{temp}°C")

    st.divider()

    # ---------------------------
    # SMART ANALYSIS
    # ---------------------------
    st.subheader("📊 AI Insights")

    if risk_level == "HIGH":
        st.error("⚠️ High risk detected. Immediate intervention required.")
        st.write("""
        - Increase workforce efficiency
        - Shift work to night schedule
        - Secure local suppliers
        """)
    elif risk_level == "MEDIUM":
        st.warning("⚠️ متوسط المخاطر، يحتاج مراقبة")
        st.write("""
        - Monitor daily progress
        - Add buffer to schedule
        """)
    else:
        st.success("✅ المشروع في وضع آمن")
        st.write("""
        - Continue current plan
        - Optimize future phases
        """)

# -------------------------------
# 9. DATA UPLOAD (مهم جدًا)
# -------------------------------
st.divider()
st.subheader("📂 Upload Real Project Data")

uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    new_df = pd.read_csv(uploaded)
    new_df.to_csv("project_data.csv", index=False)
    st.success("تم تحديث بيانات الذكاء الاصطناعي بنجاح")
