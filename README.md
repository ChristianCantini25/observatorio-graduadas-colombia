# Observatorio de Participación Femenina entre Graduados en Colombia (2020–2025)

Proyecto académico de la Universidad de los Andes.
**Asignatura:** Despliegue de Soluciones Analíticas.

## 1. Descripción del proyecto

Este proyecto analiza la participación femenina entre los graduados de educación superior en Colombia durante 2020–2025, identificando patrones asociados a características académicas, institucionales y geográficas.

**Pregunta de investigación:**

¿En qué medida las características académicas, institucionales y geográficas permiten explicar y predecir la proporción de mujeres entre los graduados de educación superior en Colombia durante 2020–2025?

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
