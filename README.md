# Observatorio de participación femenina entre graduados, Colombia 2020–2025

**Pregunta:** ¿En qué medida las características académicas, institucionales y geográficas permiten explicar y predecir la proporción de mujeres entre los graduados de educación superior en Colombia durante 2020–2025?

**Fuente:** Ministerio de Educación Nacional, SNIES. Seis libros Excel originales proporcionados por el equipo. Son datos agregados de graduados, no microdatos individuales.

## Estructura
- `data/raw/2020.xlsx` ... `2025.xlsx`: archivos originales, no versionarlos en Git ordinario.
- `src/prepare_eda.py`: extracción, armonización y exploración inicial reproducible.
- `data/processed/graduados_normalizados.csv`: se genera con el script (una fila por observación fuente).
- `data/processed/modelo_agregado.csv`: se genera con el script (una fila por combinación de características y período).
- `reports/resumen_eda.json`: métricas descriptivas generadas.
- `docs/mockup.html`: maqueta del futuro tablero, no sistema operativo.

## Cómo ejecutar
```bash
python src/prepare_eda.py
```
La extracción puede tardar varios minutos por el tamaño de los seis archivos Excel. Verificar `reports/resumen_eda.json` antes de reportar números. La participación femenina se calcula como `mujeres / total graduados`, incluyendo en el total otras categorías reportadas. Comprobar si existen registros de sexo sin clasificar antes de definir el denominador definitivo.

## Git + DVC (comandos para ejecutar desde la carpeta del proyecto)
```bash
git init
git checkout -b main
python -m pip install dvc
dvc init
dvc add data/raw/2020.xlsx data/raw/2021.xlsx data/raw/2022.xlsx data/raw/2023.xlsx data/raw/2024.xlsx data/raw/2025.xlsx
# Definir y configurar un almacenamiento remoto autorizado (DVC) antes de hacer push de los datos.
git add .gitignore .dvcignore data/raw/*.dvc src README.md docs reports/.gitkeep
git commit -m "Inicio: fuentes SNIES 2020-2025, pipeline EDA y mockup"
# Crear un repo privado en GitHub y enlazarlo con su URL real
# git remote add origin <URL_REAL_DEL_REPOSITORIO>
# git push -u origin main
```
Cada integrante debe realizar sus propios commits; no se debe simular participación. No se ha creado remotamente un repositorio GitHub ni un almacenamiento DVC desde este paquete.

## Precauciones metodológicas
- El análisis de asociaciones no implica causalidad.
- Los datos solo describen personas graduadas; no permiten estimar probabilidades individuales de graduación.
- Para evitar fuga de información, las variables `sexo`, `mujeres`, `hombres`, `graduados` no serán predictores de la proporción observada; `total` puede usarse para ponderación, pero no como variable disponible para predecir escenarios futuros sin una estimación independiente.
- Evaluar validación temporal (entrenar con años anteriores, probar con el año final) y métricas ponderadas por número de graduados.
- La columna `área de conocimiento` presenta categorías `Sin clasificar`; complementar con CINE si resulta necesario.
- La entrega exige informe <=10 páginas y reporte individual/equipo <=1 página, capturas reales de repositorios y commits.
