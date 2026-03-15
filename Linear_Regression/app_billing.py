import streamlit as st
import joblib
import numpy as np
import pandas as pd
from billing_report import generate_billing_pdf

st.set_page_config(page_title="Cloud Cost Predictor", page_icon="💰")

try:
    model = joblib.load('billing_model.pkl')
except Exception:
    st.error("Corre primero 'python infra_pipeline.py'")
    st.stop()

st.title("💰 Predicción de Gastos de Infraestructura")
st.markdown("Estima el costo mensual de tu arquitectura cloud usando Regresión Lineal.")

col1, col2 = st.columns(2)

with col1:
    u = st.number_input("Usuarios Activos", 100, 100000, 1000)
    a = st.number_input("Almacenamiento (GB)", 1, 10000, 500)

with col2:
    c = st.number_input("Horas de CPU", 1, 5000, 750)
    api = st.number_input("Solicitudes API", 1000, 10000000, 50000)

if st.button("Calcular Presupuesto"):
    # Preparar datos
    features = np.array([[u, a, c, api]])
    prediction = model.predict(features)[0]
    
    # Mostrar en pantalla
    st.subheader(f"Costo Estimado: ${prediction:,.2f} USD")
    
    # Generar PDF
    inputs_dict = {
        "Usuarios": u, "Almacenamiento GB": a,
        "Horas CPU": c, "API Calls": api
    }
    path = generate_billing_pdf(inputs_dict, prediction)
    
    with open(path, "rb") as f:
        st.download_button("📩 Descargar Proyección en PDF", f, file_name=path)

# Gráfico de Coeficientes (Explicabilidad)
if st.checkbox("Mostrar importancia de variables"):
    import matplotlib.pyplot as plt
    coefs = pd.DataFrame({'Feature': ['Usuarios', 'Storage', 'CPU', 'API'], 
                          'Peso': model.coef_})
    st.bar_chart(coefs.set_index('Feature'))