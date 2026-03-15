# Setup and Environment Guide / Guia de Entorno

![Setup Banner](https://capsule-render.vercel.app/api?type=rect&height=120&text=Setup%20%26%20Environment&fontSize=32&color=0:2563eb,100:16a34a&fontColor=ffffff)

ES: Guia unificada para dejar listo todo el repositorio.  
EN: Unified guide to prepare the entire repository.

## Goal / Objetivo

- ES: Ejecutar notebooks en `Algorimths/`.
- EN: Run notebooks in `Algorimths/`.
- ES: Entrenar y servir `Naive_Bayes/`.
- EN: Train and serve `Naive_Bayes/`.
- ES: Correr prediccion de costos en `Linear_Regression/`.
- EN: Run cloud cost prediction in `Linear_Regression/`.
- ES: Evaluar riesgo crediticio en `Logistic_regression/`.
- EN: Run credit risk scoring in `Logistic_regression/`.
- ES: Ejecutar pipeline y app de `PCA/`.
- EN: Run pipeline and app in `PCA/`.

## Requirements / Requisitos

- Python 3.10+
- PowerShell
- VS Code (recommended / recomendado)

## 1) Create and Activate venv / Crear y Activar venv

```powershell
python -m venv .venv
& .\.venv\Scripts\Activate.ps1
```

If script execution is blocked / Si la ejecucion de scripts esta bloqueada:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\.venv\Scripts\Activate.ps1
```

## 2) Install Dependencies / Instalar Dependencias

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\Naive_Bayes\Model\requeriments.txt
python -m pip install numpy fpdf jupyter
```

## 3) Environment Validation / Validacion de Entorno

```powershell
python --version
python -m pip list
python -c "import numpy, pandas, sklearn, matplotlib, seaborn, streamlit, joblib, nltk, fpdf; print('Environment OK / Entorno OK')"
```

## 4) Quick Validation by Module / Validacion Rapida por Modulo

### Naive Bayes

```powershell
python .\Naive_Bayes\Model\trainer.py
python .\Naive_Bayes\Model\predict.py
```

### Linear Regression

```powershell
python .\Linear_Regression\infra_pipeline.py
python -m streamlit run .\Linear_Regression\app_billing.py --server.port 8517
```

### PCA

```powershell
python .\PCA\user_data_factory.py
python .\PCA\pca_pipeline.py
python -m streamlit run .\PCA\app_pca.py --server.port 8515
```

### Logistic Regression

```powershell
python .\Logistic_regression\credit_pipeline.py
python -m streamlit run .\Logistic_regression\app_credit.py --server.port 8518
```

## 5) Notebook Kernel / Kernel de Notebooks

- ES: Selecciona `.venv` como interprete del notebook.
- EN: Select `.venv` as notebook interpreter.
- ES: Ejecuta de arriba a abajo para evitar `NameError`.
- EN: Execute top-to-bottom to avoid `NameError`.

## 6) Expected Artifacts / Artefactos Esperados

| Module / Modulo | Expected files / Archivos esperados |
| --- | --- |
| Naive_Bayes | `spam_model.pkl`, `vectorizer.pkl` |
| Linear_Regression | `billing_model.pkl`, `cloud_billing.csv` |
| Linear_Regression app | `proyeccion_costos.pdf` |
| Logistic_regression | `credit_model.pkl`, `credit_scaler.pkl`, `credit_data.csv` |
| Logistic_regression app | `dictamen_credito.pdf` |
| PCA | `PCA/scaler.pkl`, `PCA/pca_model.pkl`, `PCA/user_segments.csv` |
