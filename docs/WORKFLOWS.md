# Operational Workflows

## Objetivo

Esta guia traduce el repositorio a acciones concretas. En vez de listar solo comandos, organiza el trabajo segun lo que normalmente querras hacer: orientarte, entrenar, predecir, visualizar o revisar notebooks.

## Workflow 0: Elegir una ruta dentro del repo

Usa esta regla simple:

- si buscas teoria, simulacion o practica estadistica, empieza por `Algorimths/` y `Naive_Bayes/Scratch/`;
- si buscas algo ejecutable de punta a punta, empieza por `Naive_Bayes/Model/`;
- si buscas soporte operativo, usa `docs/`.

## Workflow 1: Entrenar el clasificador con el dataset incluido

Este es el camino mas corto para verificar que el proyecto aplicado funciona.

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\trainer.py
```

Que hace:

- carga `Naive_Bayes/Model/emails.csv`;
- limpia el texto;
- divide train/test;
- vectoriza con TF-IDF;
- entrena `MultinomialNB`;
- imprime metricas;
- guarda artefactos reutilizables.

Salidas esperadas:

- `spam_model.pkl` en la raiz del repo;
- `vectorizer.pkl` en la raiz del repo;
- `classification_report` en consola.

## Workflow 2: Regenerar el dataset y reentrenar

Usalo cuando quieras reiniciar el ejemplo sintetico o probar el pipeline desde cero.

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\data_factory.py
python .\Naive_Bayes\Model\trainer.py
```

Notas utiles:

- `generate_dataset(n_samples=1000)` produce por defecto un conjunto sintetico pequeno;
- la logica actual genera aproximadamente `60%` ham y `40%` spam;
- el archivo resultante se guarda como `Naive_Bayes/Model/emails.csv`.

## Workflow 3: Clasificar un correo por consola

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\predict.py
```

Entrada:

- cualquier texto pegado en consola.

Salida esperada:

- etiqueta `SPAM` o `HAM`;
- confianza basada en la mayor probabilidad de clase.

Requisito previo:

- `spam_model.pkl` y `vectorizer.pkl` ya deben existir.

## Workflow 4: Abrir la app web en Streamlit

```powershell
& .\.venv\Scripts\Activate.ps1
python -m streamlit run .\Naive_Bayes\Model\app.py
```

Que deberias ver:

- una interfaz para pegar el contenido de un correo;
- una prediccion con mensaje visual y metrica de confianza;
- carga cacheada del modelo para evitar recargas innecesarias.

## Workflow 5: Visualizar palabras frecuentes por clase

```powershell
& .\.venv\Scripts\Activate.ps1
python .\Naive_Bayes\Model\visualizer.py
```

Que hace:

- lee `emails.csv`;
- filtra por clase;
- elimina `stopwords` de NLTK;
- muestra un grafico de barras con las palabras mas frecuentes.

Observacion:

- si es la primera ejecucion, NLTK puede descargar recursos antes de graficar.

## Workflow 6: Recorrer los notebooks con un orden razonable

Si vas a estudiar el repositorio como laboratorio, este orden suele ser mas claro:

1. `Algorimths/Bayesian_inference_engine.ipynb`
2. `Algorimths/Digital_sensor.ipynb`
3. `Algorimths/Dinamic_campaign_optimizer.ipynb`
4. `Algorimths/Simulator_physical_perfomance.ipynb`
5. `Algorimths/Multivariate_Analysis.ipynb`
6. `Algorimths/Naive_Bayes_Multinomial.ipynb`
7. `Naive_Bayes/Scratch/Naive_Bayes.ipynb`

Recomendaciones para notebooks:

- ejecutalos de arriba a abajo;
- usa el kernel de `.venv` si quieres compartir dependencias con el resto del proyecto;
- si aparece un `NameError`, normalmente significa que se salto una celda previa.

## Workflow 7: Publicar cambios en una rama

Solo si estas versionando modificaciones del proyecto:

```powershell
git switch -c feature/documentation
git add .
git commit -m "docs: improve project documentation"
git push -u origin feature/documentation
```

## Checklist operativo rapido

- [ ] `.venv` activo antes de ejecutar Python.
- [ ] Dependencias instaladas desde `Naive_Bayes/Model/requeriments.txt`.
- [ ] `spam_model.pkl` y `vectorizer.pkl` generados antes de usar CLI o Streamlit.
- [ ] Comandos lanzados desde la raiz del repo.
- [ ] Notebooks ejecutados en orden cuando dependen de variables previas.
