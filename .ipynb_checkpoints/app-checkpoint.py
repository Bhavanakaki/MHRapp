import streamlit as st
import pandas as pd
import joblib
import json
from pathlib import Path

# Paths
ROOT         = Path(__file__).parent
DATA_PATH    = ROOT / "data"   / "cleaned_survey.csv"
MODEL_PATH   = ROOT / "models" / "rf_model.pkl"
SCALER_PATH  = ROOT / "models" / "scaler.pkl"
RES_PATH     = ROOT / "resources.json"

# Load artifacts
rf     = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
resources = json.loads(RES_PATH.read_text())

# Fixed features
FEATURES = [
  'Age','Gender','self_employed','family_history','no_employees',
  'remote_work','tech_company','benefits','mental_health_consequence'
]

df = pd.read_csv(DATA_PATH)
dummies = pd.get_dummies(df[FEATURES], drop_first=True).columns.tolist()
FEATURE_COLUMNS = ['Age'] + dummies

st.title("🌟 Mental Health Risk Detector")
st.write("Enter a few details for your risk assessment.")

age = st.slider("Age (20–65)", 20, 65, 30)
gender = st.selectbox("Gender", ["Male","Female"])
self_emp = st.selectbox("Self-employed?", df.self_employed.unique())
family_hist = st.selectbox("Family history?", df.family_history.unique())
company_sz = st.selectbox("Company size?", df.no_employees.unique())
remote = st.selectbox("Remote work?", df.remote_work.unique())
tech_comp = st.selectbox("Tech company?", df.tech_company.unique())
benefits = st.selectbox("Benefits offered?", df.benefits.unique())
mh_conseq = st.selectbox("MH discussion consequence?", df.mental_health_consequence.unique())

# Build input
data = {c: 0 for c in FEATURE_COLUMNS}
data['Age'] = age

def set_dummy(pref, val):
    key = f"{pref}_{val}"
    if key in data:
        data[key] = 1

for pref,val in {
    'Gender': gender,
    'self_employed': self_emp,
    'family_history': family_hist,
    'no_employees': company_sz,
    'remote_work': remote,
    'tech_company': tech_comp,
    'benefits': benefits,
    'mental_health_consequence': mh_conseq
}.items():
    set_dummy(pref, val)

inp = pd.DataFrame([data], columns=FEATURE_COLUMNS)
inp[['Age']] = scaler.transform(inp[['Age']])

if st.button("Assess My Risk"):
    r = rf.predict(inp)[0]
    st.subheader(f"🩺 Your Risk Level: {r}")
    st.markdown("**Resources:**")
    for tip in resources.get(r, []):
        st.write(f"- {tip}")