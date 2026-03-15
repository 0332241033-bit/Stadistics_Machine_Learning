# API Reference / Referencia de API

![API Banner](https://capsule-render.vercel.app/api?type=rect&height=120&text=Technical%20API%20Reference&fontSize=30&color=0:0f172a,100:334155&fontColor=ffffff)

ES: Contratos tecnicos de scripts, datos y artefactos.  
EN: Technical contracts for scripts, data, and artifacts.

## 1) Naive_Bayes Module / Modulo Naive_Bayes

### `Naive_Bayes/Model/data_factory.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Main function / Funcion principal | `generate_dataset(n_samples=1000)` |
| Input / Entrada | `n_samples` (`int`) |
| Output / Salida | `Naive_Bayes/Model/emails.csv` |
| CSV schema / Esquema CSV | `text` (`str`), `label` (`0 ham / 1 spam`) |

### `Naive_Bayes/Model/trainer.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Functions / Funciones | `clean_text(text)`, `train_model()` |
| Pipeline | regex cleaning, 80/20 split, TF-IDF, `MultinomialNB` |
| Artifacts / Artefactos | `spam_model.pkl`, `vectorizer.pkl` |
| Metrics / Metricas | `classification_report` |

### `Naive_Bayes/Model/predict.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Function / Funcion | `classify_email(email_text)` |
| Runtime dependencies / Dependencias runtime | `spam_model.pkl`, `vectorizer.pkl` |
| Output / Salida | label + confidence in console |

### `Naive_Bayes/Model/app.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Framework | Streamlit |
| Model loading / Carga de modelo | `@st.cache_resource` |
| Input / Entrada | email text |
| Output / Salida | SPAM/HAM + confidence metric |

## 2) Linear_Regression Module / Modulo Linear_Regression

### `Linear_Regression/infra_pipeline.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Main function / Funcion principal | `setup_infra_project()` |
| Generated dataset / Dataset generado | `cloud_billing.csv` |
| Features | `usuarios`, `almacenamiento`, `cpu_horas`, `api_calls` |
| Target | `costo_total` |
| Model / Modelo | `LinearRegression` |
| Metrics / Metricas | `R2`, `MAE` |
| Artifact / Artefacto | `billing_model.pkl` |

### `Linear_Regression/app_billing.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Framework | Streamlit |
| Requirement / Requisito | `billing_model.pkl` |
| Flow / Flujo | inputs -> prediction -> PDF download |
| Explainability / Explicabilidad | coefficient bar chart |
| Safe failure / Falla controlada | `st.stop()` if model missing |

### `Linear_Regression/billing_report.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Class / Clase | `BillingReport(FPDF)` |
| Function / Funcion | `generate_billing_pdf(inputs, prediction)` |
| Output / Salida | `proyeccion_costos.pdf` |

## 3) PCA Module / Modulo PCA

### `PCA/user_data_factory.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Main function / Funcion principal | `generate_user_data(n_users=1000)` |
| Generated dataset / Dataset generado | `PCA/user_behavior.csv` |
| Variables | 10 user behavior metrics |

### `PCA/pca_pipeline.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Main function / Funcion principal | `run_pca_pipeline()` |
| Process / Proceso | load -> scale (`StandardScaler`) -> PCA(2) |
| Outputs / Salidas | `PCA/scaler.pkl`, `PCA/pca_model.pkl`, `PCA/user_segments.csv` |
| Console output / Salida en consola | explained variance |

### `PCA/app_pca.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Framework | Streamlit |
| Required models / Modelos requeridos | `scaler.pkl`, `pca_model.pkl` |
| Input / Entrada | 10 user metrics |
| Output / Salida | projected coordinates `PC1`, `PC2` |

### `PCA/visualizer_pca.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Main function / Funcion principal | `visualize_clusters()` |
| Input / Entrada | `PCA/user_segments.csv` |
| Output / Salida | PC1 vs PC2 scatter plot |

## Dependency Graph / Grafo de Dependencias

```mermaid
flowchart LR
    DF[data_factory.py] --> T[trainer.py]
    T --> M[spam_model.pkl]
    T --> V[vectorizer.pkl]
    M --> NBAPP[Naive_Bayes app.py]
    V --> NBAPP

    INFRA[infra_pipeline.py] --> BILL[billing_model.pkl]
    BILL --> LRAPP[app_billing.py]
    LRAPP --> PDF[proyeccion_costos.pdf]

    UDF[user_data_factory.py] --> UP[PCA user_behavior.csv]
    UP --> PP[pca_pipeline.py]
    PP --> SC[scaler.pkl]
    PP --> PM[pca_model.pkl]
    PM --> PAPP[app_pca.py]
    SC --> PAPP

    CP[credit_pipeline.py] --> CD[credit_data.csv]
    CP --> CM[credit_model.pkl]
    CP --> CS[credit_scaler.pkl]
    CM --> LGAPP[app_credit.py]
    CS --> LGAPP
    LGAPP --> CPDF[dictamen_credito.pdf]
```

## 4) Logistic_regression Module / Modulo Logistic_regression

### `Logistic_regression/credit_pipeline.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Main function / Funcion principal | `setup_credit_project()` |
| Generated dataset / Dataset generado | `credit_data.csv` |
| Features | `ingresos_anuales`, `edad`, `puntaje_buro`, `deuda_actual`, `historial_atrasos` |
| Target | `riesgo` (`0 aprobado / 1 rechazado`) |
| Preprocessing / Preprocesamiento | `StandardScaler` |
| Model / Modelo | `LogisticRegression` |
| Metrics / Metricas | `classification_report`, `confusion_matrix` |
| Artifacts / Artefactos | `credit_model.pkl`, `credit_scaler.pkl` |

### `Logistic_regression/app_credit.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Framework | Streamlit |
| Requirement / Requisito | `credit_model.pkl`, `credit_scaler.pkl` |
| Flow / Flujo | inputs -> scale -> predict_proba -> decision -> PDF download |
| Decision logic / Logica de decision | `prediction == 1` -> RECHAZADO, `prediction == 0` -> APROBADO |
| Safe failure / Falla controlada | `st.stop()` if models missing |

### `Logistic_regression/credit_report.py`

| Field / Campo | Value / Valor |
| --- | --- |
| Class / Clase | `CreditReport(FPDF)` |
| Function / Funcion | `generate_credit_pdf(inputs, result, probability)` |
| Output / Salida | `dictamen_credito.pdf` |
