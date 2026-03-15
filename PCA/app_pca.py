import streamlit as st
import joblib
import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCALER_PATH = BASE_DIR / 'scaler.pkl'
PCA_MODEL_PATH = BASE_DIR / 'pca_model.pkl'

st.set_page_config(page_title="Analizador de Usuarios PCA", layout="wide")

@st.cache_resource
def load_models():
    if not SCALER_PATH.exists() or not PCA_MODEL_PATH.exists():
        missing = [str(path.name) for path in [SCALER_PATH, PCA_MODEL_PATH] if not path.exists()]
        raise FileNotFoundError(f"Faltan archivos del modelo: {', '.join(missing)}")
    scaler = joblib.load(SCALER_PATH)
    pca = joblib.load(PCA_MODEL_PATH)
    return scaler, pca

try:
    scaler, pca = load_models()
except FileNotFoundError as exc:
    st.error(f"{exc}. Ejecuta primero pca_pipeline.py para generarlos.")
    st.stop()

st.title("🧩 Reducción de Dimensionalidad con PCA")
st.write("Ingresa las métricas del usuario para proyectarlo en el mapa de comportamiento.")

# Crear columnas para los inputs
col1, col2 = st.columns(2)

with col1:
    tiempo = st.slider("Tiempo Sesión (min)", 0, 60, 15)
    paginas = st.number_input("Páginas Vistas", 0, 50, 5)
    clics = st.number_input("Clics en Ofertas", 0, 20, 2)
    monto = st.number_input("Monto Gastado ($)", 0, 1000, 100)
    dias = st.slider("Días desde Registro", 1, 365, 30)

with col2:
    compras = st.number_input("Compras", 0, 10, 1)
    scroll = st.slider("Scroll Depth %", 0, 100, 50)
    rebotes = st.number_input("Rebotes", 0, 10, 1)
    checkout = st.number_input("Tiempo Checkout (min)", 0, 15, 5)
    mobile = st.selectbox("¿Es Mobile?", [0, 1])

if st.button("Proyectar Usuario"):
    # Preparar datos
    input_data = np.array([[tiempo, paginas, clics, dias, compras, monto, scroll, rebotes, checkout, mobile]], dtype=float)
    
    # 1. Escalar (OBLIGATORIO)
    scaled = scaler.transform(input_data)
    # 2. Transformar con PCA
    projected = pca.transform(scaled)
    
    st.success(f"El usuario ha sido proyectado a las coordenadas: PC1: {projected[0][0]:.2f}, PC2: {projected[0][1]:.2f}")
    
    # Explicación profesional
    st.info("""
    **Interpretación para Arquitectura de Datos:**
    PCA ha tomado tus 10 entradas y las ha 'comprimido'. 
    - Si el valor de PC1 es alto, el usuario es muy activo.
    - Si el valor de PC2 es alto, el usuario tiene alta probabilidad de conversión.
    """)