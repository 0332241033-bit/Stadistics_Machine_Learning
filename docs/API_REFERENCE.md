# Technical Reference

## Module: Naive_Bayes/Model/data_factory.py

### Function: `generate_dataset(n_samples=1000)`

- Responsibility: creates synthetic spam/ham dataset.
- Input:
  - `n_samples` (int): number of generated rows.
- Output:
  - `emails.csv` file with columns:
    - `text` (str)
    - `label` (int, 0 for ham, 1 for spam)

## Module: Naive_Bayes/Model/trainer.py

### Function: `clean_text(text)`

- Responsibility: normalize text for model training.
- Rules:
  - keep letters and spaces
  - lowercase all text

### Function: `train_model()`

- Responsibility: train and persist a Naive Bayes classifier.
- Pipeline:
  1. Load `emails.csv`.
  2. Apply `clean_text`.
  3. Split train/test (`test_size=0.2`, `random_state=42`).
  4. Vectorize with TF-IDF.
  5. Train `MultinomialNB`.
  6. Print `classification_report`.
  7. Save model artifacts:
     - `spam_model.pkl`
     - `vectorizer.pkl`

## Module: Naive_Bayes/Model/predict.py

### Function: `classify_email(email_text)`

- Responsibility: run single-text inference from console.
- Steps:
  1. Load saved model and vectorizer.
  2. Transform text into vector space.
  3. Predict class and probabilities.
  4. Print label + confidence.

## Module: Naive_Bayes/Model/app.py

### Function: `clean_text(text)`

- Same normalization contract as training.

### Function: `load_assets()`

- Decorator: `st.cache_resource`.
- Responsibility: load and cache model/vectorizer for web app performance.

### App Behavior

- UI framework: Streamlit.
- Input: email body text.
- Output:
  - SPAM/HAM message
  - confidence metric

## Module: Naive_Bayes/Model/visualizer.py

### Function: `plot_top_words(df, label_value, title, color)`

- Responsibility: visualize top terms by label.
- Dependencies:
  - pandas
  - seaborn
  - matplotlib
  - nltk stopwords

## Data and Artifact Contracts

### Data File Contract (`emails.csv`)

- `text`: raw email content.
- `label`: binary target (`0`, `1`).

### Model Artifact Contract

- `spam_model.pkl`: scikit-learn classifier implementing `predict` and `predict_proba`.
- `vectorizer.pkl`: fitted TF-IDF vectorizer implementing `transform`.
