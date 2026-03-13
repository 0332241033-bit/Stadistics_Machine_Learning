# Operational Workflows

## Objective

Provide repeatable command sequences for the most common project operations.

## Workflow 1: Full Training Cycle

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\data_factory.py
python .\Naive_Bayes\Model\trainer.py
```

Outputs:

- `Naive_Bayes/Model/emails.csv`
- `spam_model.pkl`
- `vectorizer.pkl`

## Workflow 2: Console Prediction

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\predict.py
```

Input:

- Any email text pasted in console.

Output:

- Label: SPAM or HAM.
- Confidence score (max class probability).

## Workflow 3: Web Prediction with Streamlit

```powershell
& .\.venv\Scripts\Activate.ps1
python -m streamlit run .\Naive_Bayes\Model\app.py
```

Expected behavior:

- Loads cached model/vectorizer once.
- Allows text input and returns prediction with confidence metrics.

## Workflow 4: Exploratory Visualization

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\visualizer.py
```

Expected behavior:

- Downloads NLTK stopwords if needed.
- Displays bar chart for top frequent terms by class.

## Workflow 5: Branch and Publish Changes

```powershell
git switch -c feature/documentation
git add .
git commit -m "docs: add full project documentation"
git push -u origin feature/documentation
```

## Runtime Checklist

- [ ] Virtual environment activated.
- [ ] Dependencies installed.
- [ ] Artifacts present before inference (`spam_model.pkl`, `vectorizer.pkl`).
- [ ] Commands executed from repository root.
