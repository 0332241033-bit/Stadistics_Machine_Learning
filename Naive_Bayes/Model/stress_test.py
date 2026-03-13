import joblib
import pandas as pd

def run_stress_test():
    try:
        # 1. Cargar el cerebro del proyecto
        model = joblib.load('spam_model.pkl')
        vec = joblib.load('vectorizer.pkl')
    except FileNotFoundError:
        print("❌ Error: Primero debes ejecutar trainer.py para generar los modelos.")
        return

    # 2. Definir casos de prueba "difíciles"
    # Mezclamos palabras de spam en contextos reales y viceversa
    test_cases = [
        "Congratulations on winning the employee of the month award! Check the PDF for details.", # Difícil: Tiene 'Winning' y 'Check' pero es Ham.
        "Meeting at 3 PM to discuss the Bitcoin payment gateway integration for the bank.", # Difícil: Tiene 'Bitcoin' y 'Payment' pero es profesional.
        "Urgent: Your coffee is getting cold, come to the breakroom.", # Difícil: Tiene 'Urgent' pero es broma/Ham.
        "Get your free crypto now by clicking this link, no deposit needed fast money.", # Spam puro con frases de 3 palabras.
        "Can you send me the data architecture report by tonight? Thanks.", # Ham puro y corto.
        "Win a free vacation! Just click the link below to verify your account and claim prize." # Spam clásico.
    ]

    print(f"{'CORREO':<60} | {'PREDICCIÓN':<10} | {'CONFIANZA'}")
    print("-" * 85)

    for email in test_cases:
        # Transformar el texto usando el vectorizador de N-Grams
        vec_email = vec.transform([email.lower()])
        
        prediction = model.predict(vec_email)[0]
        prob = model.predict_proba(vec_email)[0]
        
        label = "🚨 SPAM" if prediction == 1 else "✅ HAM"
        confidence = prob[1] if prediction == 1 else prob[0]
        
        print(f"{email[:58]:<60} | {label:<10} | {confidence*100:.2f}%")

if __name__ == "__main__":
    run_stress_test()