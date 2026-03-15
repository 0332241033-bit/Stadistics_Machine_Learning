# Documentation Index

## Proposito

La carpeta `docs/` complementa al `README.md`. El README explica el proyecto en conjunto; estos archivos profundizan en instalacion, ejecucion, referencia tecnica y resolucion de problemas.

## Ruta de lectura recomendada

### Si quieres ejecutar el proyecto por primera vez

1. [SETUP_AND_ENV.md](SETUP_AND_ENV.md)
2. [WORKFLOWS.md](WORKFLOWS.md)
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Si quieres entender como esta construido

1. [README.md](../README.md)
2. [API_REFERENCE.md](API_REFERENCE.md)
3. [WORKFLOWS.md](WORKFLOWS.md)

### Si vienes por los notebooks

1. [README.md](../README.md)
2. [WORKFLOWS.md](WORKFLOWS.md)
3. [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

## Archivos y alcance

| Archivo | Alcance | Cuando usarlo |
| --- | --- | --- |
| [README.md](../README.md) | Vista global del repo | Cuando necesitas entender rapidamente que hay en el proyecto. |
| [SETUP_AND_ENV.md](SETUP_AND_ENV.md) | Preparacion del entorno | Cuando vas a instalar dependencias o configurar `.venv`. |
| [WORKFLOWS.md](WORKFLOWS.md) | Ejecucion por objetivos | Cuando quieres entrenar, predecir, abrir la app o recorrer notebooks. |
| [API_REFERENCE.md](API_REFERENCE.md) | Scripts, notebooks y contratos | Cuando necesitas revisar responsabilidades de modulos, datos y artefactos. |
| [TROUBLESHOOTING.md](TROUBLESHOOTING.md) | Fallos comunes | Cuando algo no corre, falta un archivo o un notebook da error. |

## Mapa rapido del repositorio

- `Algorimths/`: notebooks de estadistica, simulacion e inferencia.
- `Naive_Bayes/Model/`: scripts reproducibles del clasificador spam/ham.
- `Naive_Bayes/Scratch/`: version teorica y manual de Naive Bayes.
- `docs/`: soporte documental.

## Convenciones de esta documentacion

- Los comandos estan pensados para Windows PowerShell.
- Las rutas se expresan desde la raiz del repositorio.
- Se conservan los nombres reales del repo, incluyendo `Algorimths` y `requeriments.txt`.
- Los notebooks se tratan como material exploratorio; los scripts de `Naive_Bayes/Model/` se documentan como flujo reproducible.

## Checklist de mantenimiento

- [ ] Actualizar el README y este indice si cambian carpetas o propositos del repo.
- [ ] Revisar `SETUP_AND_ENV.md` cuando cambien dependencias o requisitos de Python.
- [ ] Revisar `API_REFERENCE.md` cuando cambien contratos de funciones o salidas.
- [ ] Anadir a `TROUBLESHOOTING.md` cualquier error que se repita mas de una vez.
