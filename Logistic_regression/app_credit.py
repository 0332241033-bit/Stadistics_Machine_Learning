import streamlit as st
import joblib
import numpy as np
from credit_report import generate_credit_pdf

st.set_page_config(page_title="AI Credit Scoring", page_icon="🏦")

try:
    model = joblib.load('credit_model.pkl')
    scaler = joblib.load('credit_scaler.pkl')
except:
    st.error("Corre primero 'python credit_pipeline.py'")
    st.stop()

st.title("🏦 Sistema de Evaluación de Crédito")

with st.form("credit_form"):
    col1, col2 = st.columns(2)
    with col1:
        ingresos = st.number_input("Ingresos Anuales ($)", 10000, 500000, 45000)
        edad = st.slider("Edad del Solicitante", 18, 80, 30)
        buro = st.number_input("Puntaje Buró (300-850)", 300, 850, 650)
    with col2:
        deuda = st.number_input("Deuda Actual ($)", 0, 1000000, 5000)
        atrasos = st.number_input("Historial de Atrasos (Meses)", 0, 24, 0)
    
    submitted = st.form_submit_button("Evaluar Solicitud")

if submitted:
    # 1. Preparar e Ingestar
    features = np.array([[ingresos, edad, buro, deuda, atrasos]])
    features_scaled = scaler.transform(features)
    
    # 2. Predicción y Probabilidad (Clave en Regresión Logística)
    prediction = model.predict(features_scaled)[0]
    probabilidad_riesgo = model.predict_proba(features_scaled)[0][1]
    
    # 3. Lógica de Decisión
    estatus = "RECHAZADO" if prediction == 1 else "APROBADO"
    
    if estatus == "APROBADO":
        st.success(f"✅ Solicitud APROBADA con {1-probabilidad_riesgo:.2%} de confianza.")
    else:
        st.error(f"🚨 Solicitud RECHAZADA por Riesgo de Impago ({probabilidad_riesgo:.2%}).")
    
    # 4. Reporte
    inputs_dict = {"ingresos": ingresos, "edad": edad, "buro": buro, "deuda": deuda, "atrasos": atrasos}
    path = generate_credit_pdf(inputs_dict, estatus, probabilidad_riesgo)
    
    with open(path, "rb") as f:
        st.download_button("📥 Descargar Dictamen Oficial", f, file_name=path)