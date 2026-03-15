# Troubleshooting Guide / Guia de Solucion de Problemas

![Troubleshooting Banner](https://capsule-render.vercel.app/api?type=rect&height=120&text=Troubleshooting%20Playbook&fontSize=30&color=0:ef4444,100:f97316&fontColor=ffffff)

ES: Usa este playbook por sintoma.  
EN: Use this playbook by symptom.

## How to Use / Como Usar

1. Identify the exact symptom / Identifica el sintoma exacto.
2. Run the suggested fix block / Ejecuta el bloque sugerido.
3. Return to [WORKFLOWS.md](WORKFLOWS.md).

## 1) `streamlit` not recognized / `streamlit` no se reconoce

```powershell
& .\.venv\Scripts\Activate.ps1
python -m streamlit run .\Naive_Bayes\Model\app.py
```

## 2) `.venv` activation blocked / Activacion de `.venv` bloqueada

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\.venv\Scripts\Activate.ps1
```

## 3) Missing `spam_model.pkl` or `vectorizer.pkl`

```powershell
python .\Naive_Bayes\Model\trainer.py
```

## 4) `Linear_Regression/app_billing.py` model missing

```powershell
python .\Linear_Regression\infra_pipeline.py
python -m streamlit run .\Linear_Regression\app_billing.py --server.port 8517
```

## 5) `NameError: name 'pd' is not defined` in billing app

ES: Verifica que exista `import pandas as pd` en `Linear_Regression/app_billing.py`.  
EN: Ensure `import pandas as pd` exists in `Linear_Regression/app_billing.py`.

## 6) Wrong PCA Streamlit command / Comando incorrecto de PCA

```powershell
python -m streamlit run .\PCA\app_pca.py --server.port 8515
```

## 7) Missing `scaler.pkl` or `pca_model.pkl`

```powershell
python .\PCA\user_data_factory.py
python .\PCA\pca_pipeline.py
```

## 8) Missing `fpdf` module

```powershell
python -m pip install fpdf
```

## 9) Notebook `NameError`

- ES: Ejecuta celdas de arriba a abajo y usa kernel `.venv`.
- EN: Execute top-to-bottom and use the `.venv` kernel.

## 10) Streamlit port already in use / Puerto ocupado

```powershell
python -m streamlit run .\Naive_Bayes\Model\app.py --server.port 8518
```

## Quick Diagnostics / Diagnostico Rapido

```powershell
python --version
python -m pip list | Select-String "streamlit|scikit-learn|joblib|pandas|numpy|fpdf"
Test-Path .\spam_model.pkl
Test-Path .\vectorizer.pkl
Test-Path .\billing_model.pkl
Test-Path .\PCA\scaler.pkl
Test-Path .\PCA\pca_model.pkl
```
