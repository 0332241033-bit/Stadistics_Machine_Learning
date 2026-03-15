import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

def setup_project():
    # 1. Generar Datos Sintéticos (1000 usuarios)
    np.random.seed(42)
    data = {
        'tiempo_sesion': np.random.normal(15, 5, 1000),
        'paginas_vistas': np.random.poisson(5, 1000),
        'clics_ofertas': np.random.poisson(2, 1000),
        'monto_gastado': np.random.normal(100, 40, 1000),
        'scroll_depth': np.random.uniform(20, 100, 1000),
        'dias_registro': np.random.randint(1, 365, 1000),
        'compras': np.random.poisson(1, 1000),
        'rebotes': np.random.randint(0, 10, 1000),
        'tiempo_checkout': np.random.normal(5, 2, 1000),
        'mobile': np.random.choice([0, 1], 1000)
    }
    df = pd.DataFrame(data)
    df[df < 0] = 0
    df.to_csv('usuarios.csv', index=False)

    # 2. Pipeline de Machine Learning
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    pca = PCA(n_components=2)
    pca_data = pca.fit_transform(scaled_data)

    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    kmeans.fit(pca_data)

    # 3. Guardar Modelos
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(pca, 'pca.pkl')
    joblib.dump(kmeans, 'kmeans.pkl')
    print("✅ Sistema de IA entrenado y modelos guardados.")

if __name__ == "__main__":
    setup_project()