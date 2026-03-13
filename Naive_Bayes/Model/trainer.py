import pandas as pd
import re
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()
    return text

def train_model():
    # 1. Cargar y Limpiar
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'emails.csv'))
    df['text'] = df['text'].apply(clean_text)
    
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )
    
    # 2. Vectorización con N-Grams (Aquí está el cambio clave)
    # ngram_range=(1, 3) significa que usará palabras sueltas, pares y tríos.
    # max_features=5000 limita el vocabulario para que el modelo no sea muy pesado.
    vectorizer = TfidfVectorizer(
        stop_words='english', 
        ngram_range=(1, 3), 
        max_features=5000
    )
    
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 3. Entrenar
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    # 4. Evaluación
    y_pred = model.predict(X_test_vec)
    print("\n--- PERFORMANCE CON N-GRAMS (1-3) ---")
    print(classification_report(y_test, y_pred))
    
    # 5. Guardar el "Cerebro" actualizado
    joblib.dump(model, 'spam_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("\n✅ Modelo actualizado con reconocimiento de frases.")

if __name__ == "__main__":
    train_model()