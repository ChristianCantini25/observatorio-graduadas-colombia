# Observatorio de Participación Femenina entre Graduados en Colombia (2020–2025)

Proyecto académico de la Universidad de los Andes.
**Asignatura:** Despliegue de Soluciones Analíticas.

## 1. Descripción del proyecto

### Problema y contexto

En Colombia las mujeres son mayoría entre los graduados de educación superior (56 % en 2020-2025), pero esa cifra agregada esconde brechas profundas. En Ingeniería, arquitectura y afines solo el 34 % de los graduados son mujeres, frente al 70 % en Ciencias de la salud. Además, en áreas como Economía y administración o Ciencias sociales la participación femenina cae con fuerza al pasar del pregrado al doctorado.

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

## 3. Estructura del repositorio

| Carpeta o archivo | Descripción |
|---|---|
| `data/raw/` | Seis archivos Excel originales |
| `data/processed/` | Base consolidada y procesada |
| `notebooks/01_exploracion_graduados.ipynb` | Exploración, limpieza y visualizaciones |
| `src/prepare_eda.py` | Script de preparación pendiente de validación |
| `docs/mockup.html` | Maqueta conceptual del dashboard |
| `data/raw.dvc` | Seguimiento de las bases originales |
| `data/processed.dvc` | Seguimiento de los datos procesados |

## 4. Análisis exploratorio

Se ha estudiado la participación femenina según año, área de conocimiento, departamento, nivel de formación, sector institucional y carácter de la institución.

### Principales hallazgos preliminares

| Dimensión | Participación femenina |
|---|---:|
| Colombia, 2020 | 55,92 % |
| Colombia, 2025 | 55,30 % |
| Ciencias de la salud | 70,08 % |
| Ingeniería y afines | 34,18 % |
| Doctorado | 41,79 % |
| Instituciones privadas | 59,03 % |
| Instituciones oficiales | 52,29 % |

Los resultados son descriptivos y no implican causalidad.

## 5. Preparación y calidad de datos

Las actividades realizadas incluyen:

- Consolidación de seis archivos anuales.
- Homologación de variables entre períodos.
- Normalización de departamentos, niveles de formación y sectores.
- Revisión de valores faltantes y conteos.
- Validación de duplicados exactos en las fuentes originales.

No se identificaron duplicados exactos en los seis archivos originales. Se conservaron los registros aparentemente repetidos en la base reducida, debido a que pueden corresponder a diferentes programas o sedes.

## 6. Herramientas y colaboración

**Git y GitHub:** control de versiones, documentación y contribuciones individuales.

**DVC:** seguimiento local de las versiones de datos. La configuración del almacenamiento remoto DVC continúa pendiente.

**OneDrive institucional:** almacenamiento compartido de las seis bases originales y el CSV consolidado, en `Proyecto DSA / Datos`.

Cada integrante trabaja con su propia cuenta de GitHub y registra sus contribuciones mediante commits.

## 7. Reproducibilidad

Para reproducir el análisis exploratorio:

1. Clonar el repositorio de GitHub.
2. Descargar los archivos originales desde OneDrive.
3. Guardarlos en `data/raw/` con los nombres `graduados_2020.xlsx` hasta `graduados_2025.xlsx`.
4. Abrir `notebooks/01_exploracion_graduados.ipynb` en Jupyter.
5. Ejecutar las celdas en orden.

El script `src/prepare_eda.py` requiere validación adicional para garantizar que reproduce los resultados del notebook.

## 8. Consideraciones metodológicas

- Los datos describen graduados, no trayectorias individuales.
- La asociación estadística no implica causalidad.
- La proporción femenina requiere una definición consistente del denominador.
- Se deben conservar los identificadores necesarios para distinguir programas y sedes.
- El modelo predictivo deberá evitar fuga de información.
- Se evaluará la posibilidad de validación temporal del modelo.

## 9. Estado y próximos pasos

**Estado actual:** exploración y consolidación inicial de datos, con GitHub y DVC configurados.

Actividades pendientes:

- Validar el script de procesamiento.
- Completar el análisis por programa académico.
- Definir la unidad de análisis predictiva.
- Desarrollar y evaluar el modelo supervisado.
- Construir y desplegar la solución analítica.
- Documentar los aportes de cada integrante.
