import pandas as pd
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'user_behavior.csv'

def generate_user_data(n_users=1000):
    np.random.seed(42)
    data = {
        'tiempo_sesion': np.random.normal(15, 5, n_users),
        'paginas_vistas': np.random.poisson(5, n_users),
        'clics_ofertas': np.random.poisson(2, n_users),
        'dias_desde_registro': np.random.randint(1, 365, n_users),
        'compras_realizadas': np.random.poisson(1, n_users),
        'monto_gastado': np.random.normal(100, 40, n_users),
        'scroll_depth': np.random.uniform(20, 100, n_users),
        'rebotes': np.random.randint(0, 10, n_users),
        'tiempo_en_checkout': np.random.normal(5, 2, n_users),
        'dispositivo_mobile': np.random.choice([0, 1], n_users)
    }
    
    df = pd.DataFrame(data)
    # Asegurar que no haya valores negativos
    df[df < 0] = 0
    df.to_csv(DATA_PATH, index=False)
    print(f"Archivo '{DATA_PATH.name}' generado con 10 variables por usuario.")

if __name__ == "__main__":
    generate_user_data()