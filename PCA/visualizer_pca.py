import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SEGMENTS_PATH = BASE_DIR / 'user_segments.csv'

def visualize_clusters():
    df_pca = pd.read_csv(SEGMENTS_PATH)
    
    plt.figure(figsize=(10, 7))
    sns.scatterplot(x='PC1', y='PC2', data=df_pca, alpha=0.6, color='purple')
    
    plt.title('Mapa de Usuarios (Reducción PCA)', fontsize=15)
    plt.xlabel('Componente Principal 1 (Comportamiento General)')
    plt.ylabel('Componente Principal 2 (Intención de Compra)')
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.show()

if __name__ == "__main__":
    visualize_clusters()