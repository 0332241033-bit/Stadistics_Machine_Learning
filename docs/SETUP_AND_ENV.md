# Setup and Environment Guide

## Proposito

Esta guia deja preparado el entorno local para tres tipos de uso:

- ejecutar notebooks desde VS Code;
- entrenar y probar el clasificador spam/ham;
- lanzar la app web en Streamlit.

## Plataforma objetivo

- Windows PowerShell
- Python 3.10 o superior

## Prerrequisitos

Antes de empezar, verifica que tienes:

- Python accesible desde terminal;
- permisos para crear un entorno virtual local;
- conectividad basica si vas a instalar dependencias o descargar recursos de NLTK.

## 1. Crear el entorno virtual

Ejecuta desde la raiz del repositorio:

```powershell
python -m venv .venv
```

## 2. Activar el entorno virtual

```powershell
& .\.venv\Scripts\Activate.ps1
```

Si PowerShell bloquea la ejecucion del script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\.venv\Scripts\Activate.ps1
```

## 3. Instalar dependencias del proyecto

```powershell
python -m pip install --upgrade pip
python -m pip install -r .\Naive_Bayes\Model\requeriments.txt
```

Dependencias principales incluidas actualmente:

- `pandas`
- `scikit-learn`
- `nltk`
- `matplotlib`
- `seaborn`
- `streamlit`
- `joblib`

Nota: el archivo se llama `requeriments.txt` porque asi existe hoy en el repositorio. La documentacion conserva ese nombre real.

## 4. Verificar que el entorno quedo funcional

```powershell
python --version
python -m pip list
python -c "import pandas, sklearn, nltk, matplotlib, seaborn, streamlit, joblib; print('Entorno OK')"
```

Si este ultimo comando falla, revisa [TROUBLESHOOTING.md](TROUBLESHOOTING.md) antes de continuar.

## 5. Recomendar el mismo entorno para notebooks

Si trabajas desde VS Code con archivos `.ipynb`:

- selecciona `.venv` como kernel de Python;
- ejecuta los notebooks de arriba hacia abajo para evitar variables no inicializadas;
- usa el mismo entorno para notebooks y scripts si quieres resultados coherentes.

## 6. Validar el pipeline reproducible de spam/ham

El dataset de ejemplo ya viene incluido en el repo, asi que puedes probar el flujo minimo asi:

```powershell
python .\Naive_Bayes\Model\trainer.py
python .\Naive_Bayes\Model\predict.py
python -m streamlit run .\Naive_Bayes\Model\app.py
```

Si quieres regenerar el dataset sintetico antes de entrenar:

```powershell
python .\Naive_Bayes\Model\data_factory.py
python .\Naive_Bayes\Model\trainer.py
```

## 7. Archivos que deberian aparecer o actualizarse

Despues de entrenar deberias tener:

- `spam_model.pkl` en la raiz del repositorio;
- `vectorizer.pkl` en la raiz del repositorio.

Si regeneras datos, tambien se actualiza:

- `Naive_Bayes/Model/emails.csv`

## Convenciones del entorno

- Ejecuta comandos desde la raiz del repo salvo que una guia diga lo contrario.
- `trainer.py` consume `Naive_Bayes/Model/emails.csv`.
- `predict.py` y `app.py` cargan los artefactos entrenados desde la raiz del repo.
- `visualizer.py` puede pedir la descarga de `stopwords` de NLTK en el primer uso.

## Recomendaciones practicas

- Si solo quieres leer notebooks, el entorno no tiene que estar perfecto desde el minuto uno.
- Si quieres reproducibilidad, usa siempre la misma `.venv`.
- Si trabajas en mejoras del codigo, reentrena el modelo tras tocar limpieza o vectorizacion.
