import os
import pandas as pd
import random

def generate_dataset(n_samples=1000):
    spam_templates = [
        "WINNER! Claim your {prize} now at {link}", "URGENT: {account} security alert. Click {link}",
        "Get {discount}% off {product}. Limited time!", "Invest in {crypto} and earn $10,000 weekly.",
        "Adult {content} for free. No credit card needed.", "Make money fast with this {job}."
    ]
    ham_templates = [
        "Hey, are we still meeting for {event}?", "Please find the {report} attached.",
        "The {topic} lecture is moved to {time}.", "Can you review the {task} for me?",
        "Don't forget the {event} tonight.", "Thanks for the update on the {subject}."
    ]
    
    data = []
    for _ in range(n_samples):
        is_spam = random.random() > 0.6 # 40% Spam, 60% Ham
        if is_spam:
            text = random.choice(spam_templates).format(
                prize="iPhone 15", link="bit.ly/fake", account="Bank", 
                discount=90, product="pills", crypto="Bitcoin", job="trading", content="video"
            )
            label = 1
        else:
            text = random.choice(ham_templates).format(
                event="lunch", report="PDF", topic="SQL", time="5 PM", 
                task="migration", subject="Data Science"
            )
            label = 0
        data.append([text, label])
    
    df = pd.DataFrame(data, columns=['text', 'label'])
    output_path = os.path.join(os.path.dirname(__file__), 'emails.csv')
    df.to_csv(output_path, index=False)
    print("Archivo 'emails.csv' generado en Naive_Bayes/Model.")

if __name__ == "__main__":
    generate_dataset()