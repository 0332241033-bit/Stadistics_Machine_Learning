import streamlit as st
import joblib
import re
import os

# Configuración de la página
st.set_page_config(page_title="Detector de Spam Pro", page_icon="📧")

# Función de limpieza (debe ser igual a la del entrenamiento)
def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()
    return text

# Cargar el modelo y el vectorizador
@st.cache_resource # Esto hace que la app sea rápida al no recargar el modelo cada vez
def load_assets():
    model = joblib.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'spam_model.pkl'))
    vec = joblib.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'vectorizer.pkl'))
    return model, vec

try:
    model, vec = load_assets()

    # Interfaz de Usuario
    st.title("📧 Clasificador de Correos con Naive Bayes")
    st.markdown("""
    Esta aplicación utiliza un modelo de **Machine Learning** entrenado para detectar patrones 
    en el texto y decidir si un correo es seguro o es Spam.
    """)

    email_input = st.text_area("Pega el contenido del correo aquí:", height=200, placeholder="Ej: Win a free iPhone now!")

    if st.button("Analizar Correo"):
        if email_input.strip() == "":
            st.warning("Por favor, escribe algo primero.")
        else:
            # Procesar
            cleaned = clean_text(email_input)
            vectorized = vec.transform([cleaned])
            
            # Predecir
            prediction = model.predict(vectorized)[0]
            probabilities = model.predict_proba(vectorized)[0]
            
            # Mostrar resultado
            st.divider()
            if prediction == 1:
                st.error(f"🚨 **RESULTADO: ESTO ES SPAM**")
                st.metric("Confianza de Spam", f"{probabilities[1]*100:.2f}%")
            else:
                st.success(f"✅ **RESULTADO: CORREO SEGURO (HAM)**")
                st.metric("Confianza de Seguridad", f"{probabilities[0]*100:.2f}%")
            
            st.info("El algoritmo analizó la probabilidad de cada palabra basándose en el dataset de 1000 correos.")

except FileNotFoundError:
    st.error("No se encontraron los archivos 'spam_model.pkl' o 'vectorizer.pkl'. ¡Ejecuta primero el script de entrenamiento!")