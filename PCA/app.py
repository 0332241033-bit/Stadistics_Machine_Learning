import streamlit as st
import joblib
import numpy as np
import pandas as pd
from report_engine import generate_pdf

# Configuración y Carga
st.set_page_config(page_title="AI Customer Segments", layout="wide")

try:
    scaler = joblib.load('scaler.pkl')
    pca = joblib.load('pca.pkl')
    kmeans = joblib.load('kmeans.pkl')
except Exception:
    st.error("⚠️ Ejecuta primero 'python pipeline.py' para generar los modelos.")

SEGMENTOS = {
    0: ("💎 VIP", "Usuario de alto valor, mucha actividad y compras."),
    1: ("🌱 NUEVO", "Usuario recién llegado con actividad exploratoria."),
    2: ("⚠️ RIESGO", "Usuario con muchos rebotes, posible abandono."),
    3: ("📈 RECURRENTE", "Usuario estándar con comportamiento estable.")
}

FEATURE_COLUMNS = [
    "tiempo_sesion",
    "paginas_vistas",
    "clics_ofertas",
    "monto_gastado",
    "scroll_depth",
    "dias_registro",
    "compras",
    "rebotes",
    "tiempo_checkout",
    "mobile",
]

st.title("🧩 Segmentación de Usuarios con PCA + K-Means")

with st.sidebar:
    st.header("Métricas de Entrada")
    t = st.slider("Tiempo Sesión", 0, 60, 15)
    p = st.number_input("Páginas Vistas", 0, 50, 5)
    c = st.number_input("Clics Ofertas", 0, 20, 2)
    g = st.number_input("Gasto Total", 0, 1000, 100)
    sc = st.slider("Scroll Depth %", 0, 100, 50)
    d = st.number_input("Días Registro", 0, 365, 30)
    co = st.number_input("Compras", 0, 15, 1)
    r = st.number_input("Rebotes", 0, 10, 1)
    ch = st.slider("Tiempo Checkout", 0, 15, 5)
    m = st.selectbox("Mobile", [0, 1])

if st.button("Analizar y Generar Reporte"):
    # 1. Procesar
    input_data = pd.DataFrame(
        [[t, p, c, g, sc, d, co, r, ch, m]],
        columns=FEATURE_COLUMNS,
    )
    scaled = scaler.transform(input_data)
    coords = pca.transform(scaled)
    cluster = kmeans.predict(coords)[0]
    
    # 2. Resultados
    nombre, desc = SEGMENTOS[cluster]
    st.subheader(f"Categoría Detectada: {nombre}")
    st.info(desc)
    
    # 3. PDF
    pdf_path = generate_pdf(nombre, desc, coords[0])
    
    with open(pdf_path, "rb") as f:
        st.download_button("📥 Descargar Reporte PDF", f, file_name=pdf_path)