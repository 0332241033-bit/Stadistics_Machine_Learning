# Setup and Environment Guide

## Purpose

This guide standardizes local setup for development, training, and app execution.

## Supported Platform

- Windows PowerShell (primary)
- Python 3.10+

## 1. Create Virtual Environment

```powershell
python -m venv .venv
```

## 2. Activate Virtual Environment

```powershell
& .\.venv\Scripts\Activate.ps1
```

If execution policy blocks scripts:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\.venv\Scripts\Activate.ps1
```

## 3. Install Dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\Naive_Bayes\requeriments.txt
```

## 4. Verify Environment

```powershell
python --version
python -m pip list
```

Expected key packages:

- pandas
- scikit-learn
- nltk
- matplotlib
- seaborn
- streamlit
- joblib

## 5. Validate End-to-End Readiness

```powershell
python .\Naive_Bayes\Model\trainer.py
python .\Naive_Bayes\Model\predict.py
python -m streamlit run .\Naive_Bayes\Model\app.py
```

## Environment Conventions

- Always run commands from repository root.
- Keep model artifacts (`spam_model.pkl`, `vectorizer.pkl`) in root unless project layout changes.
- Keep preprocessing logic aligned between training and inference.

## Optional Improvement

The file name `requeriments.txt` is non-standard; `requirements.txt` is recommended for broader tooling compatibility.
