# Linear_Regression - Cloud Cost Forecasting / Prediccion de Costos Cloud

![Linear Regression Banner](https://capsule-render.vercel.app/api?type=rect&height=110&text=Cloud%20Cost%20Forecasting%20Module&fontSize=24&color=0:22c55e,100:15803d&fontColor=ffffff)

ES: Modulo orientado a control financiero de infraestructura cloud mediante regresion lineal y reporte descargable.

EN: Module focused on cloud financial control through linear regression and downloadable reporting.

## Business Objective / Objetivo de Negocio

- ES: Estimar costo mensual de infraestructura para planificacion presupuestaria.
- EN: Estimate monthly infrastructure cost for budget planning.

## Delivery Flow / Flujo de Entrega

```mermaid
flowchart LR
    A[infra_pipeline.py] --> B[cloud_billing.csv]
    A --> C[billing_model.pkl]
    C --> D[app_billing.py]
    D --> E[proyeccion_costos.pdf]
```

## Technical Components / Componentes Tecnicos

| File | Role |
| --- | --- |
| `infra_pipeline.py` | synthetic data generation, training, and model evaluation |
| `app_billing.py` | Streamlit interface for interactive forecasting |
| `billing_report.py` | PDF export for management-ready output |

## Run Demo / Demo de Ejecucion

```powershell
python .\Linear_Regression\infra_pipeline.py
python -m streamlit run .\Linear_Regression\app_billing.py --server.port 8517
```

## Portfolio Value / Valor para Portfolio

- ES: Conecta modelo predictivo con entrega ejecutiva (PDF) y UI de negocio.
- EN: Connects predictive modeling with executive delivery (PDF) and business UI.

## Related Links / Enlaces Relacionados

- [../README.md](../README.md)
- [../docs/WORKFLOWS.md](../docs/WORKFLOWS.md)
- [../docs/TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md)
