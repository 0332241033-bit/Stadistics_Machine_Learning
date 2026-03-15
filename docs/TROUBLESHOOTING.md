# Troubleshooting Guide

## Como usar esta guia

Empieza por el sintoma que ves y luego verifica la causa mas probable. La mayoria de problemas en este repo caen en una de estas categorias:

- entorno Python no activado o mal seleccionado;
- artefactos del modelo que todavia no existen;
- notebooks ejecutados fuera de orden;
- rutas correctas, pero desde un punto de ejecucion distinto al esperado.

## 1) `streamlit` is not recognized

### Sintoma

PowerShell no reconoce `streamlit` como comando.

### Causa probable

`streamlit` esta instalado dentro de `.venv`, pero el entorno virtual no esta activo o el comando se esta lanzando fuera de ese entorno.

### Que hacer

```powershell
& .\.venv\Scripts\Activate.ps1
python -m streamlit run .\Naive_Bayes\Model\app.py
```

## 2) PowerShell bloquea `Activate.ps1`

### Sintoma

La terminal muestra un error de execution policy al intentar activar el entorno virtual.

### Causa probable

La politica de ejecucion del proceso actual no permite scripts locales.

### Que hacer

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
& .\.venv\Scripts\Activate.ps1
```

## 3) `spam_model.pkl` o `vectorizer.pkl` no existen

### Sintoma

`predict.py` o `app.py` fallan al cargar artefactos.

### Causa probable

Todavia no se ejecuto el entrenamiento o se entreno en otra ubicacion.

### Que hacer

```powershell
python .\Naive_Bayes\Model\trainer.py
python .\Naive_Bayes\Model\predict.py
```

Verifica despues que ambos archivos quedaron en la raiz del repositorio.

## 4) `emails.csv` no se encuentra o esta desactualizado

### Sintoma

El entrenamiento no encuentra datos o estas viendo un dataset viejo.

### Causa probable

No se regeneraron los datos o el archivo no esta en `Naive_Bayes/Model/`.

### Que hacer

```powershell
python .\Naive_Bayes\Model\data_factory.py
python .\Naive_Bayes\Model\trainer.py
```

Confirma que `Naive_Bayes/Model/emails.csv` exista despues del primer comando.

## 5) Los imports funcionan en terminal, pero fallan en notebooks

### Sintoma

El notebook marca `ModuleNotFoundError` aunque ya instalaste paquetes.

### Causa probable

El notebook esta usando un kernel distinto a `.venv`.

### Que hacer

- Selecciona el kernel de Python asociado a `.venv`.
- Reinicia el kernel si acabas de instalar paquetes.
- Reejecuta el notebook desde la primera celda.

## 6) Faltan `nltk stopwords`

### Sintoma

`visualizer.py` falla al cargar `stopwords`.

### Causa probable

Es la primera ejecucion y NLTK aun no descargo ese recurso.

### Que hacer

```powershell
python .\Naive_Bayes\Model\visualizer.py
```

Hazlo con conexion a internet al menos una vez.

## 7) `Naive_Bayes/Scratch/Naive_Bayes.ipynb` lanza `NameError`

### Sintoma

El notebook de scratch falla en una celda de evaluacion o uso del clasificador.

### Causa probable

Se salto la celda donde se define la clase o la estructura principal del modelo.

### Que hacer

- Ejecuta el notebook de arriba hacia abajo.
- Asegurate de correr primero la celda de definicion de la clase `Naive_Bayes`.

## 8) `Simulator_physical_perfomance.ipynb` falla en la visualizacion

### Sintoma

La celda final de graficos o resumen muestra variables no definidas.

### Causa probable

Se omitio una celda intermedia que calculaba valores auxiliares para la visualizacion.

### Que hacer

- Ejecuta el notebook completo en orden.
- Si trabajas por bloques, confirma que existan las variables analiticas necesarias antes de la celda final.

## 9) Warning de Seaborn sobre `palette`

### Sintoma

Seaborn muestra una advertencia de deprecacion o uso futuro respecto a `palette`.

### Causa probable

Se esta pasando `palette` sin el contexto de `hue` en ciertos graficos.

### Que hacer

- usa `hue='<columna>'` si el grafico lo necesita;
- usa `legend=False` cuando el color no requiera leyenda.

## 10) `git push` falla en una rama nueva

### Sintoma

Git rechaza el push porque la rama no tiene upstream.

### Que hacer

```powershell
git push -u origin <branch_name>
```

## Diagnostico rapido

Si no tienes claro por donde empezar, ejecuta esto:

```powershell
python --version
python -m pip list
git branch
git status
```

Y, si el problema es del pipeline de spam/ham, verifica tambien:

```powershell
Test-Path .\Naive_Bayes\Model\emails.csv
Test-Path .\spam_model.pkl
Test-Path .\vectorizer.pkl
```
