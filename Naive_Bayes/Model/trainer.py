import pandas as pd
import re
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix

def clean_text(text):
    text = re.sub(r'[^a-zA-Z\s]', '', str(text)).lower()
    return text

def train_model():
    # 1. Cargar y Limpiar
    df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'emails.csv'))
    df['text'] = df['text'].apply(clean_text)
    
    # 2. Dividir datos
    X_train, X_test, y_train, y_test = train_test_split(
        df['text'], df['label'], test_size=0.2, random_state=42
    )
    
    # 3. Vectorización Profesional (TF-IDF)
    # Convertimos texto a números considerando la importancia de la palabra
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 4. Naive Bayes Multinomial
    model = MultinomialNB()
    model.fit(X_train_vec, y_train)
    
    # 5. Evaluación
    y_pred = model.predict(X_test_vec)
    print("\n--- PERFORMANCE DEL MODELO ---")
    print(classification_report(y_test, y_pred))
    
    # 6. Guardar el "Cerebro" del proyecto
    joblib.dump(model, 'spam_model.pkl')
    joblib.dump(vectorizer, 'vectorizer.pkl')
    print("\n✅ Modelo y Vectorizador guardados.")

if __name__ == "__main__":
    train_model()