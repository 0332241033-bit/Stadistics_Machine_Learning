import pandas as pd
import joblib
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'user_behavior.csv'
SCALER_PATH = BASE_DIR / 'scaler.pkl'
PCA_MODEL_PATH = BASE_DIR / 'pca_model.pkl'
SEGMENTS_PATH = BASE_DIR / 'user_segments.csv'

def run_pca_pipeline():
    # 1. Cargar datos
    df = pd.read_csv(DATA_PATH)
    
    # 2. Escalar los datos (PCA es sensible a las escalas de los números)
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(df)
    
    # 3. Aplicar PCA (Reducir de 10 variables a 2 componentes principales)
    # Queremos ver si podemos resumir todo en 2 ejes para graficar
    pca = PCA(n_components=2, random_state=42)
    pca_data = pca.fit_transform(data_scaled)
    
    # Crear un nuevo DF con los componentes
    df_pca = pd.DataFrame(data=pca_data, columns=['PC1', 'PC2'])
    
    # 4. Ver varianza explicada (¿Cuánta info guardamos?)
    print(f"Varianza explicada por cada componente: {pca.explained_variance_ratio_}")
    print(f"Total de info retenida: {sum(pca.explained_variance_ratio_)*100:.2f}%")
    
    # 5. Guardar el transformador para producción
    joblib.dump(scaler, SCALER_PATH)
    joblib.dump(pca, PCA_MODEL_PATH)
    df_pca.to_csv(SEGMENTS_PATH, index=False)
    print("\nPCA completado y modelos guardados.")

if __name__ == "__main__":
    run_pca_pipeline()