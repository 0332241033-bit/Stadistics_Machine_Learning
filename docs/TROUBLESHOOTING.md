# Troubleshooting Guide

## 1) Error: `streamlit` is not recognized

### Cause

`streamlit` is installed inside virtual environment but not available in global PATH.

### Fix

```powershell
& .\.venv\Scripts\Activate.ps1
python -m streamlit run .\Naive_Bayes\Model\app.py
```

## 2) Error: FileNotFoundError for `emails.csv`

### Cause

Script executed from unexpected working directory and using fragile relative path.

### Fix

- Ensure scripts use paths derived from `__file__`.
- Run from repository root.

```powershell
python .\Naive_Bayes\Model\trainer.py
```

## 3) Error: FileNotFoundError for `.pkl` artifacts

### Cause

Model/vectorizer not generated yet or generated in another location.

### Fix

```powershell
python .\Naive_Bayes\Model\trainer.py
python .\Naive_Bayes\Model\predict.py
```

## 4) Warning in Seaborn about `palette`

### Cause

Future deprecation when using palette without hue.

### Fix

Use:

- `hue='<column>'`
- `legend=False` when legend is not required.

## 5) NLTK stopwords missing

### Cause

First run requires downloading corpora.

### Fix

Run visualization script once with internet access:

```powershell
python .\Naive_Bayes\Model\visualizer.py
```

## 6) Git push fails on new branch

### Cause

Branch has no upstream configured.

### Fix

```powershell
git push -u origin <branch_name>
```

## 7) Quick Diagnostic Commands

```powershell
python --version
python -m pip list
git branch
git status
```
