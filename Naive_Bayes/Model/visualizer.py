import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import nltk
from nltk.corpus import stopwords
import os

def plot_top_words(df, label_value, title, color):
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    
    # Filtrar y procesar palabras
    subset = df[df['label'] == label_value]['text'].str.lower().str.cat(sep=' ')
    words = [w for w in subset.split() if w.isalpha() and w not in stop_words]
    
    # Contar y graficar
    most_common = Counter(words).most_common(15)
    words_df = pd.DataFrame(most_common, columns=['Palabra', 'Frecuencia'])
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x='Frecuencia', y='Palabra', data=words_df, hue='Palabra', palette=color, legend=False)
    plt.title(title)
    plt.show()

if __name__ == "__main__":
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'emails.csv'))
    plot_top_words(df, 1, "Palabras más comunes en SPAM", "Reds_r")