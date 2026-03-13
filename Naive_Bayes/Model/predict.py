import joblib
import os

def classify_email(email_text):
    # Cargar modelos
    model = joblib.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'spam_model.pkl'))
    vec = joblib.load(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'vectorizer.pkl'))
    
    # Transformar y predecir
    email_vec = vec.transform([email_text.lower()])
    prediction = model.predict(email_vec)[0]
    
    prob = model.predict_proba(email_vec)[0] # Probabilidad de cada clase
    
    res = "SPAM" if prediction == 1 else "HAM (Seguro)"
    print(f"Resultado: {res} | Confianza: {max(prob)*100:.2f}%")

if __name__ == "__main__":
    email_usuario = input("Pega el contenido del correo: ")
    classify_email(email_usuario)