# Observatorio de Participación Femenina entre Graduados en Colombia (2020–2025)

Proyecto académico de la Universidad de los Andes.
**Asignatura:** Despliegue de Soluciones Analíticas.

## 1. Descripción del proyecto

### Problema y contexto

En Colombia las mujeres son mayoría entre los graduados de educación superior (56,6 % en 2020-2025, en programas con 15 o más graduados al año), pero esa cifra agregada esconde brechas profundas. En Ingeniería, arquitectura y afines solo el 34,4 % de los graduados son mujeres, frente al 71,3 % en Ciencias de la salud. Además, en áreas como Economía y administración o Ciencias sociales la participación femenina cae con fuerza al pasar del pregrado al doctorado.

Estas brechas importan porque la formación determina el acceso a los sectores de mayor crecimiento y mejor remuneración, y porque la equidad de género en educación hace parte de los compromisos de política pública del país (Objetivo de Desarrollo Sostenible 5). Hoy el Ministerio de Educación Nacional (MEN) publica los datos del SNIES, pero no cuenta con una herramienta que identifique, a nivel de programa, dónde la participación femenina es menor a la esperada.

Un modelo predictivo es útil porque permite estimar la participación femenina **esperada** de un programa según sus características (área, nivel, institución, sector y departamento) y compararla con la **observada**. Los programas que quedan muy por debajo de lo esperado son candidatos prioritarios para intervenciones de equidad. Un tablero descriptivo solo muestra promedios; el modelo permite comparar cada programa con sus pares.

### Pregunta de negocio

¿Qué programas, áreas y regiones debería priorizar el MEN para sus acciones de equidad de género en educación superior, según la brecha entre la participación femenina observada y la esperada de acuerdo con sus características académicas, institucionales y geográficas?

**Usuario principal:** Viceministerio de Educación Superior del MEN, área responsable de las políticas de equidad.
**Usuarios secundarios:** las instituciones de educación superior (IES), que pueden compararse con programas similares de otras instituciones.

**Pregunta analítica (para el modelo):** ¿En qué medida las características académicas, institucionales y geográficas permiten explicar y predecir la proporción de mujeres entre los graduados de educación superior en Colombia durante 2020-2025?

### Alcance del proyecto

**Incluye:**
- Datos de graduados del SNIES 2020-2025, agregados por programa-año (unidad de análisis).
- Variable objetivo: proporción de mujeres entre los graduados de cada programa-año.
- Umbral mínimo: se trabaja con programas-año de 15 o más graduados (el 50,0 % de los registros, que concentra el 92,9 % de los graduados), para evitar proporciones inestables en programas muy pequeños.
- Un modelo supervisado de regresión con validación temporal (entrenamiento con 2020-2023, evaluación con 2024-2025).
- Un tablero con un panorama descriptivo y un simulador que estima la participación femenina esperada de un programa y la compara con la observada.
- Despliegue del modelo como API, consumida por el tablero.

**No incluye:**
- Análisis de causalidad: el modelo identifica asociaciones, no explica por qué existen las brechas.
- Datos individuales de estudiantes, ni matrícula, deserción o empleabilidad (solo graduados).
- Diseño o evaluación de las intervenciones de política.

## 2. Fuentes de información

Se utilizan seis bases anuales del Ministerio de Educación Nacional (SNIES), correspondientes a 2020–2025.

Los datos representan conteos agregados de graduados, no registros individuales de estudiantes.

### Resumen de los datos

| Indicador | Resultado |
|---|---:|
| Período | 2020–2025 |
| Registros consolidados | 273.485 |
| Graduados contabilizados | 3.151.769 |
| Variables procesadas | 15 |
| Categorías territoriales | 33 |
| Niveles de formación | 9 |
| Sectores institucionales | 2 |

### Granularidad

En las bases originales, cada fila corresponde a una combinación de institución, programa, departamento de oferta, sexo, año y semestre, con el número de graduados. La base consolidada tiene 273.485 filas, 329 instituciones y 7.840 nombres de programa, sin valores faltantes. Para el modelo, los datos se agregan a una fila por **programa-año** (82.819 registros), en la que se suman los semestres y se separan los graduados por sexo. Se trabaja con los 41.399 registros que tienen 15 o más graduados (318 instituciones).

### Diccionario de datos - base consolidada (`graduados_2020_2025.csv`)

| Variable | Tipo | Descripción |
|---|---|---|
| `institucion` | Categórica | Nombre de la institución de educación superior (IES). 329 valores |
| `sector` | Categórica | Sector de la IES tal como aparece en la fuente (con diferencias de mayúsculas entre años) |
| `sector_normalizado` | Categórica | Sector homologado: OFICIAL o PRIVADO |
| `caracter_institucion` | Categórica | Universidad; Institución Universitaria/Escuela Tecnológica; Institución Tecnológica; Institución Técnica Profesional |
| `departamento` | Categórica | Departamento de oferta del programa tal como aparece en la fuente (37 valores) |
| `departamento_normalizado` | Categórica | Departamento homologado (33 categorías territoriales) |
| `programa` | Categórica | Nombre del programa académico. 7.840 valores |
| `nivel_academico` | Categórica | Pregrado o Posgrado (pendiente homologar mayúsculas) |
| `nivel_formacion` | Categórica | Nivel de formación tal como aparece en la fuente (11 valores) |
| `nivel_formacion_normalizado` | Categórica | Nivel homologado (9 niveles): Formación técnica profesional, Tecnológico, Universitario, Especialización técnico profesional, Especialización tecnológica, Especialización universitaria, Especialización médico quirúrgica, Maestría y Doctorado |
| `area_conocimiento` | Categórica | Área de conocimiento del programa: 8 áreas, más «Sin información» y «Sin clasificar» |
| `sexo` | Categórica | MASCULINO, FEMENINO o NO BINARIO |
| `anio` | Numérica | Año de graduación (2020-2025) |
| `semestre` | Numérica | Semestre de graduación (1 o 2) |
| `graduados` | Numérica | Número de graduados en la combinación de la fila |

### Variables derivadas - base programa-año (`programas_anio.csv`)

| Variable | Descripción |
|---|---|
| `mujeres` / `hombres` / `no_binario` | Graduados de cada sexo en el programa-año |
| `total` | Total de graduados del programa-año (suma de las tres categorías) |
| `prop_mujeres` | **Variable objetivo:** mujeres / total |
| `prop_anio_anterior` | Proporción de mujeres del mismo programa en el año inmediatamente anterior (vacía si no hay registro previo) |

**Nota sobre la categoría «No binario»:** suma 12 graduados (1 en 2023 y 11 en 2025). Se mantiene en el total del programa y no se analiza por separado por su bajo volumen.

## 3. Estructura del repositorio

| Carpeta o archivo | Descripción |
|---|---|
| `data/raw/` | Seis archivos Excel originales |
| `data/processed/` | Base consolidada y procesada |
| `notebooks/01_exploracion_graduados.ipynb` | Exploración, limpieza y visualizaciones |
| `notebooks/02_eda_variable_objetivo.ipynb` | Base programa-año, variable objetivo, asociación entre variables y estabilidad temporal |
| `src/exploracion_graduados.py` | Script de exploración sobre la base procesada |
| `resultados/` | Figuras y resumen de la exploración |
| `src/prepare_eda.py` | Script de preparación pendiente de validación |
| `docs/mockup.html` | Maqueta conceptual del dashboard |
| `data/raw.dvc` | Seguimiento de las bases originales |
| `data/processed.dvc` | Seguimiento de los datos procesados |

## 4. Análisis exploratorio

Se ha estudiado la participación femenina según año, área de conocimiento, departamento, nivel de formación, sector institucional y carácter de la institución.

### Principales hallazgos preliminares

Cifras calculadas sobre los programas-año con 15 o más graduados (41.399 registros), ponderadas por número de graduados.

| Dimensión | Participación femenina |
|---|---:|
| Colombia, 2020 | 56,5 % |
| Colombia, 2025 | 55,6 % |
| Ciencias de la salud | 71,3 % |
| Ingeniería y afines | 34,4 % |
| Doctorado | 44,6 % |
| Instituciones privadas | 59,5 % |
| Instituciones oficiales | 52,7 % |

Los resultados son descriptivos y no implican causalidad.

Asociación con la proporción de mujeres (eta² ponderado): el área de conocimiento explica el 29,8 % de la variación entre programas; la institución, el 19,7 % (inflado por su número de categorías); el sector, el nivel de formación y el departamento, cerca del 2 % cada uno; y el año, el 0,1 %. La proporción de un programa se correlaciona 0,84 con la del año anterior. El detalle está en `notebooks/02_eda_variable_objetivo.ipynb` y en `resultados/`.

## 5. Preparación y calidad de datos

Las actividades realizadas incluyen:

- Consolidación de seis archivos anuales.
- Homologación de variables entre períodos.
- Normalización de departamentos, niveles de formación y sectores.
- Revisión de valores faltantes y conteos.
- Validación de duplicados exactos en las fuentes originales.
- Agregación a programa-año y aplicación del umbral mínimo de 15 graduados.

No se identificaron duplicados exactos en los seis archivos originales. Se conservaron los registros aparentemente repetidos en la base reducida, debido a que pueden corresponder a diferentes programas o sedes.

## 6. Herramientas y colaboración

**Git y GitHub:** control de versiones, documentación y contribuciones individuales.

**DVC:** seguimiento de las versiones de datos con almacenamiento remoto en Amazon S3 (AWS Academy). Los datos originales y procesados se descargan con `dvc pull`.

**OneDrive institucional:** almacenamiento compartido de las seis bases originales y el CSV consolidado, en `Proyecto DSA / Datos`.

Cada integrante trabaja con su propia cuenta de GitHub y registra sus contribuciones mediante commits.

## 7. Reproducibilidad

Para reproducir el análisis exploratorio:

1. Clonar el repositorio de GitHub.
2. Instalar las librerías: pandas, numpy, matplotlib, openpyxl, jupyter y DVC con soporte para S3.
3. Descargar los datos con `dvc pull` (requiere credenciales de AWS configuradas). Alternativa: descargar las seis bases desde OneDrive y guardarlas en `data/raw/` con los nombres `graduados_2020.xlsx` hasta `graduados_2025.xlsx`.
4. Ejecutar `notebooks/01_exploracion_graduados.ipynb`, que genera `data/processed/graduados_2020_2025.csv`.
5. Copiar `graduados_2020_2025.csv` a la carpeta `notebooks/` y ejecutar `notebooks/02_eda_variable_objetivo.ipynb`, que lo lee desde su propia carpeta y genera `programas_anio.csv` (base programa-año con 15 o más graduados).
6. El script `src/exploracion_graduados.py` genera las figuras y el resumen de la carpeta `resultados/`.

El script `src/prepare_eda.py` requiere validación adicional para garantizar que reproduce los resultados del notebook 01.

## 8. Consideraciones metodológicas

- Los datos describen graduados, no trayectorias individuales. La asociación estadística no implica causalidad.
- La variable objetivo es la proporción de mujeres por programa-año (mujeres / total de graduados). La categoría «No binario» (12 graduados) se mantiene en el total.
- Los programas muy pequeños producen proporciones inestables. Un umbral de 10 graduados excluye el 40,0 % de los registros y conserva el 96,0 % de los graduados; uno de 15 excluye el 50,0 % y conserva el 92,9 %; uno de 30 excluye el 67,8 % y conserva el 83,0 %. Se adopta 15 y el modelo se pondera por número de graduados.
- Con ese umbral, solo 359 registros tienen 0 % de mujeres y 309 tienen 100 %.
- El área de conocimiento es la variable que más se asocia con la proporción (eta² = 29,8 %). El eta² de `institucion` está inflado por su alto número de categorías.
- El efecto del nivel de formación depende del área (por ejemplo, la caída hacia el doctorado en Economía y Ciencias sociales no ocurre en Ingeniería), lo que justifica modelos que capturen interacciones. El doctorado tiene pocos graduados y sus cifras se interpretan con cautela.
- La proporción de un programa se correlaciona 0,84 con la del año anterior. El modelo debe validarse con partición temporal (entrenamiento 2020-2023, evaluación 2024-2025) para evitar fuga de información, y no puede depender solo del año anterior porque los programas nuevos no tienen historial.
- El panel es desbalanceado: 2.917 series aparecen en los seis años y 3.695 en uno solo.
- Se conservan los identificadores necesarios para distinguir programas y sedes.
- La columna `nivel_academico` conserva diferencias de mayúsculas de la fuente; el análisis usa `nivel_formacion_normalizado`.

## 9. Estado y próximos pasos

**Estado actual:** exploración completa sobre la base programa-año (15 o más graduados), DVC con almacenamiento remoto en S3, maqueta conceptual del tablero y reporte de la Entrega 1.

Actividades pendientes:

- Versionar en DVC la base programa-año (`programas_anio.csv`). Para esta entrega se subió directamente al repositorio en `data/derivado/`; en la siguiente se versionará con DVC junto con los datos procesados.
- Entrenar la línea base (regresión lineal ponderada por graduados) con partición temporal.
- Entrenar el modelo principal (Random Forest y Gradient Boosting) y registrar los experimentos en MLflow.
- Ajustar hiperparámetros, comparar modelos y analizar la importancia de variables.
- Construir el tablero: filtros, indicadores, gráficas descriptivas, módulo predictivo vía API y comparación observado vs. esperado.
- Validar el script `src/prepare_eda.py` frente a los notebooks.

## 10. Reporte de trabajo en equipo

| Integrante | Actividades | Evidencia |
|---|---|---|
| Christian Cantini | Creación del repositorio y su estructura inicial, configuración inicial de DVC, descarga y consolidación de las bases del SNIES, revisión de calidad y normalización de datos, redacción y mantenimiento del README | Commits de `ChristianCantini25`; `notebooks/01_exploracion_graduados.ipynb` |
| Lizeth Daniela Ortiz Perdomo | Configuración del remoto de DVC en Amazon S3, script de exploración y resultados, elaboración de la maqueta del tablero, integración del reporte | Commits «Configurar remoto DVC en S3» y «Agregar script de exploración y resultados» (pull request #1); `src/exploracion_graduados.py`; `resultados/` |
| Natalia Cantini | Definición del problema, la pregunta de negocio y el alcance; diccionario de datos; exploración de la variable objetivo (base programa-año, asociación entre variables, estabilidad temporal) | Commits de `nataliacantinic`; `notebooks/02_eda_variable_objetivo.ipynb` |
