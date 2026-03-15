# Technical Reference

## Proposito

Este repositorio no esta estructurado como una libreria Python formal. Aun asi, si tiene interfaces claras en el subproyecto `Naive_Bayes/Model/` y una coleccion definida de notebooks exploratorios. Esta referencia resume ambos niveles.

## Modulos reproducibles en `Naive_Bayes/Model/`

### `data_factory.py`

#### Funcion: `generate_dataset(n_samples=1000)`

- Responsabilidad: generar un dataset sintetico de correos ham/spam.
- Entrada:
  - `n_samples` (`int`): cantidad de ejemplos a crear.
- Plantillas:
  - spam: premios, alertas de seguridad, descuentos, crypto, contenido adulto, ofertas de dinero rapido.
  - ham: reuniones, reportes, clases, tareas, recordatorios, actualizaciones.
- Salida:
  - `Naive_Bayes/Model/emails.csv`
- Contrato del archivo resultante:
  - `text` (`str`): contenido del correo.
  - `label` (`int`): `0` para ham, `1` para spam.

### `trainer.py`

#### Funcion: `clean_text(text)`

- Responsabilidad: normalizar texto antes del entrenamiento.
- Reglas actuales:
  - elimina caracteres no alfabeticos;
  - conserva espacios;
  - convierte a minusculas.

#### Funcion: `train_model()`

- Responsabilidad: entrenar y persistir un clasificador Naive Bayes multinomial.
- Pipeline:
  1. leer `Naive_Bayes/Model/emails.csv`;
  2. aplicar `clean_text`;
  3. dividir train/test con `test_size=0.2` y `random_state=42`;
  4. vectorizar con `TfidfVectorizer(stop_words='english')`;
  5. entrenar `MultinomialNB`;
  6. imprimir `classification_report`;
  7. guardar `spam_model.pkl` y `vectorizer.pkl` en la raiz del repo.

### `predict.py`

#### Funcion: `classify_email(email_text)`

- Responsabilidad: ejecutar inferencia de un unico texto por consola.
- Pasos:
  1. cargar `spam_model.pkl` y `vectorizer.pkl`;
  2. transformar el texto de entrada;
  3. predecir clase y probabilidades;
  4. imprimir etiqueta y confianza.
- Salida esperada:
  - `SPAM` o `HAM (Seguro)`;
  - porcentaje de confianza.

Observacion importante:

- `predict.py` actualmente convierte a minusculas, pero no replica toda la limpieza regex usada en `trainer.py` y `app.py`.

### `app.py`

#### Funcion: `clean_text(text)`

- Contrato: replica la logica de limpieza del entrenamiento.

#### Funcion: `load_assets()`

- Decorador: `st.cache_resource`.
- Responsabilidad: cargar y cachear el modelo y el vectorizador.
- Dependencia de artefactos:
  - `spam_model.pkl`
  - `vectorizer.pkl`

#### Comportamiento de la app

- framework UI: Streamlit;
- entrada: cuerpo de correo pegado por el usuario;
- salida:
  - mensaje visual de `SPAM` o `HAM`;
  - metrica de confianza;
  - texto explicativo breve.

### `visualizer.py`

#### Funcion: `plot_top_words(df, label_value, title, color)`

- Responsabilidad: graficar palabras frecuentes por clase.
- Dependencias:
  - `pandas`
  - `matplotlib`
  - `seaborn`
  - `nltk.stopwords`
- Flujo:
  1. descargar `stopwords` si hace falta;
  2. filtrar una clase del dataframe;
  3. contar terminos alfabeticos relevantes;
  4. construir grafico de barras horizontal.

## Catalogo de notebooks

| Notebook | Tema principal | Tecnicas o ideas |
| --- | --- | --- |
| `Algorimths/Bayesian_inference_engine.ipynb` | Inferencia bayesiana secuencial | prior, likelihood, sensibilidad, especificidad |
| `Algorimths/Digital_sensor.ipynb` | Sensor digital y deteccion de anomalias | distribucion normal, parametros, outliers |
| `Algorimths/Dinamic_campaign_optimizer.ipynb` | Optimizacion de campanas | Bernoulli, Binomial, Beta, Thompson sampling |
| `Algorimths/Multivariate_Analysis.ipynb` | Analisis multivariado | z-score, covarianza, correlacion, gaussianas multivariadas |
| `Algorimths/Naive_Bayes_Multinomial.ipynb` | Fraude financiero con Naive Bayes | independencia condicional, Laplace, clasificacion |
| `Algorimths/Simulator_physical_perfomance.ipynb` | Simulacion Monte Carlo | incertidumbre, probabilidad de logro, CDF |
| `Naive_Bayes/Scratch/Naive_Bayes.ipynb` | Naive Bayes desde cero | teoria, derivacion, implementacion manual |

## Contratos de datos y artefactos

### `Naive_Bayes/Model/emails.csv`

- columnas:
  - `text`
  - `label`
- clases:
  - `0` = ham
  - `1` = spam

### `spam_model.pkl`

- tipo esperado: clasificador scikit-learn compatible con `predict` y `predict_proba`.

### `vectorizer.pkl`

- tipo esperado: vectorizador TF-IDF ajustado con metodo `transform`.

## Dependencias funcionales entre componentes

- `trainer.py` depende de `Naive_Bayes/Model/emails.csv`.
- `predict.py` depende de `spam_model.pkl` y `vectorizer.pkl`.
- `app.py` depende de `spam_model.pkl` y `vectorizer.pkl`.
- `visualizer.py` depende de `Naive_Bayes/Model/emails.csv` y de recursos de NLTK.

## Caveats operativos

- Los notebooks no exponen API estable; son activos de aprendizaje.
- El preprocesamiento no esta perfectamente unificado entre todos los puntos de entrada.
- Los nombres de algunas carpetas y archivos contienen typos historicos, pero aqui se documentan sin corregirlos para no romper rutas reales.
