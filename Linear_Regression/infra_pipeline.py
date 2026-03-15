import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

def setup_infra_project():
    # 1. Generar Datos (Facturación Cloud)
    np.random.seed(42)
    n_samples = 1000
    
    # Variables independientes (Features)
    usuarios_activos = np.random.randint(100, 10000, n_samples)
    almacenamiento_gb = np.random.uniform(50, 5000, n_samples)
    horas_cpu = np.random.uniform(100, 2000, n_samples)
    solicitudes_api = np.random.randint(1000, 1000000, n_samples)
    
    # Variable dependiente (Target: Costo en USD)
    # El costo tiene una relación lineal con las variables + un poco de ruido
    costo_usd = (usuarios_activos * 0.05) + (almacenamiento_gb * 0.1) + \
                (horas_cpu * 0.5) + (solicitudes_api * 0.00001) + \
                np.random.normal(0, 50, n_samples) # Ruido aleatorio

    df = pd.DataFrame({
        'usuarios': usuarios_activos,
        'almacenamiento': almacenamiento_gb,
        'cpu_horas': horas_cpu,
        'api_calls': solicitudes_api,
        'costo_total': costo_usd
    })
    df.to_csv('cloud_billing.csv', index=False)

    # 2. Entrenamiento
    X = df.drop('costo_total', axis=1)
    y = df['costo_total']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)

    # 3. Evaluación Profesional
    preds = model.predict(X_test)
    print(f"✅ R2 Score (Precisión): {r2_score(y_test, preds):.4f}")
    print(f"✅ Error Medio (MAE): ${mean_absolute_error(y_test, preds):.2f}")

    # 4. Guardar "Cerebro"
    joblib.dump(model, 'billing_model.pkl')

if __name__ == "__main__":
    setup_infra_project()