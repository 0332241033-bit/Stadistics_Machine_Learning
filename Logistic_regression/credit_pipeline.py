import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, confusion_matrix

def setup_credit_project():
    # 1. Generar Datos Sintéticos (Comportamiento Financiero)
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'ingresos_anuales': np.random.normal(50000, 15000, n_samples),
        'edad': np.random.randint(18, 70, n_samples),
        'puntaje_buro': np.random.normal(600, 100, n_samples),
        'deuda_actual': np.random.normal(15000, 10000, n_samples),
        'historial_atrasos': np.random.randint(0, 5, n_samples)
    }
    
    df = pd.DataFrame(data)
    # Definir probabilidad de impago (Target) basada en una lógica oculta
    # Si puntaje es bajo y deuda es alta -> Riesgo (1)
    logit = (df['deuda_actual'] / df['ingresos_anuales'] * 5) + \
            (df['historial_atrasos'] * 2) - (df['puntaje_buro'] / 100)
    
    df['riesgo'] = (1 / (1 + np.exp(-logit)) > 0.5).astype(int)
    df.to_csv('credit_data.csv', index=False)

    # 2. Preprocesamiento Profesional
    X = df.drop('riesgo', axis=1)
    y = df['riesgo']
    
    # La Regresión Logística requiere escalado para converger correctamente
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
    
    # 3. Entrenamiento
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # 4. Guardar Modelos
    joblib.dump(model, 'credit_model.pkl')
    joblib.dump(scaler, 'credit_scaler.pkl')
    print("✅ Pipeline de Crédito completado y modelos guardados.")

if __name__ == "__main__":
    setup_credit_project()