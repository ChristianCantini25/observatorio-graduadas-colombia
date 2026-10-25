## \# Observatorio de Participación Femenina entre Graduados en Colombia (2020–2025)

## 

## \## 1. Descripción del proyecto

## 

## Proyecto académico desarrollado para la asignatura Despliegue de Soluciones Analíticas de la Universidad de los Andes.

## 

## El objetivo es analizar la participación femenina entre los graduados de educación superior en Colombia durante el período 2020–2025, identificar patrones asociados a características académicas, institucionales y geográficas, y desarrollar posteriormente un modelo predictivo.

## 

## \### Pregunta de investigación

## 

## ¿En qué medida las características académicas, institucionales y geográficas permiten explicar y predecir la proporción de mujeres entre los graduados de educación superior en Colombia durante 2020–2025?

## 

## \## 2. Fuentes de información

## 

## Se utilizan seis bases anuales de graduados del Ministerio de Educación Nacional de Colombia (SNIES), correspondientes a 2020, 2021, 2022, 2023, 2024 y 2025.

## 

## Los archivos contienen registros agregados de graduados por características académicas e institucionales. No corresponden a microdatos individuales de estudiantes.

## 

## \### Consolidación inicial

## 

## \- Período: 2020–2025.

## \- Registros consolidados: 273.485.

## \- Personas graduadas contabilizadas: 3.151.769.

## \- Variables de la base procesada: 15.

## \- Categorías territoriales normalizadas: 33.

## \- Categorías de nivel de formación normalizadas: 9.

## \- Categorías de sector institucional normalizadas: 2.

## 

## Los resultados corresponden al procesamiento exploratorio inicial y están sujetos a validaciones metodológicas adicionales.

## 

## \## 3. Estructura del repositorio

## 

## \- `data/raw/`: contiene los seis archivos originales denominados `graduados\_2020.xlsx` hasta `graduados\_2025.xlsx`.

## \- `data/processed/graduados\_2020\_2025.csv`: base consolidada y procesada.

## \- `notebooks/01\_exploracion\_graduados.ipynb`: notebook de exploración, limpieza y análisis descriptivo.

## \- `src/prepare\_eda.py`: script de preparación de datos, pendiente de validar frente al procesamiento final realizado en Jupyter.

## \- `docs/mockup.html`: primera maqueta conceptual del dashboard.

## \- `data/raw.dvc` y `data/processed.dvc`: archivos utilizados para registrar las versiones de los datos.

## \- `.gitignore`: configuración de exclusiones para Git.

## \- `.dvc/`: configuración de DVC.

## 

## \## 4. Análisis exploratorio realizado

## 

## Se desarrollaron análisis descriptivos de la participación femenina por:

## 

## \- Año de graduación.

## \- Área de conocimiento.

## \- Evolución temporal por área académica.

## \- Departamento de oferta del programa.

## \- Nivel de formación.

## \- Sector institucional.

## \- Carácter de la institución.

## 

## \### Principales hallazgos preliminares

## 

## \- La participación femenina nacional pasó de 55,92 % en 2020 a 55,30 % en 2025.

## \- Ciencias de la salud presentó una participación femenina acumulada de 70,08 %.

## \- Ingeniería, arquitectura, urbanismo y afines presentó una participación femenina acumulada de 34,18 %.

## \- En doctorado, la participación femenina acumulada fue de 41,79 %.

## \- En instituciones privadas, la participación femenina fue de 59,03 %, frente a 52,29 % en instituciones oficiales.

## 

## Estos resultados describen asociaciones observadas y no deben interpretarse como relaciones causales.

## 

## \## 5. Preparación y calidad de datos

## 

## Durante el procesamiento se realizaron las siguientes actividades:

## 

## \- Identificación de hojas y encabezados de los seis archivos.

## \- Selección y homologación de variables.

## \- Estandarización de categorías de sexo.

## \- Normalización de denominaciones territoriales.

## \- Homologación de niveles de formación.

## \- Normalización del sector institucional.

## \- Validación de valores faltantes y conteos.

## \- Revisión de duplicados exactos utilizando todas las columnas de las fuentes originales.

## 

## No se identificaron duplicados exactos en las seis fuentes revisadas.

## 

## Los registros aparentemente duplicados en la base reducida se conservaron, debido a que pueden diferenciarse mediante variables adicionales presentes en los archivos originales, como identificadores de programa o municipio de oferta.

## 

## \## 6. Control de versiones y colaboración

## 

## \### Git y GitHub

## 

## El proyecto utiliza Git para el control de versiones del código, notebooks y documentación.

## 

## Repositorio principal:

## 

## https://github.com/ChristianCantini25/observatorio-graduadas-colombia

## 

## El repositorio es privado y se ha invitado a las integrantes del equipo como colaboradoras.

## 

## Cada integrante debe realizar sus propios commits y documentar sus contribuciones.

## 

## \### DVC

## 

## Se utiliza DVC para registrar las versiones de las bases originales y procesadas.

## 

## DVC se encuentra inicializado y los archivos están registrados localmente.

## 

## La configuración de un almacenamiento remoto DVC compartido todavía está pendiente.

## 

## \### Almacenamiento compartido

## 

## Las bases se encuentran disponibles en la carpeta institucional compartida de OneDrive:

## 

## `Proyecto DSA / Datos`

## 

## Organización:

## 

## \- `Datos/`: seis archivos Excel originales.

## \- `Datos/Procesados/`: archivo CSV consolidado.

## 

## El almacenamiento compartido de OneDrive es independiente de la configuración actual de DVC.

## 

## \## 7. Reproducción del análisis

## 

## Para consultar el análisis ejecutado:

## 

## 1\. Clonar el repositorio de GitHub.

## 2\. Obtener las bases originales desde la carpeta compartida de OneDrive.

## 3\. Guardarlas en `data/raw/` con los nombres establecidos.

## 4\. Instalar las dependencias de Python necesarias.

## 5\. Abrir `notebooks/01\_exploracion\_graduados.ipynb` en Jupyter.

## 6\. Ejecutar las celdas en orden para reproducir el procesamiento y las visualizaciones.

## 

## El script `src/prepare\_eda.py` está pendiente de validación y ajuste para garantizar que reproduzca los resultados del notebook con los archivos actuales.

## 

## \## 8. Consideraciones metodológicas

## 

## \- Los datos describen personas graduadas y no permiten calcular probabilidades individuales de graduación.

## \- Los análisis de asociación no implican causalidad.

## \- La participación femenina se calcula como mujeres graduadas divididas entre el total de graduados.

## \- Deben conservarse categorías de sexo adicionales que estén presentes en las fuentes.

## \- Para el modelo predictivo se deberán evitar variables que produzcan fuga de información.

## \- Se evaluará la pertinencia de una validación temporal del modelo.

## \- La unidad de análisis definitiva deberá considerar las diferencias entre programas y sedes.

## \- Las categorías académicas sin clasificar deberán tratarse de manera explícita.

## 

## \## 9. Próximas actividades

## 

## \- Revisar y ajustar la reproducibilidad del script de preparación.

## \- Completar las validaciones metodológicas del EDA.

## \- Explorar la participación femenina por programa académico.

## \- Definir la unidad de análisis para el modelo supervisado.

## \- Desarrollar y evaluar el modelo predictivo.

## \- Construir la aplicación analítica y su interfaz.

## \- Preparar el despliegue de la solución.

## \- Documentar las contribuciones individuales del equipo.

## 

## \## 10. Estado del proyecto

## 

## \*\*Etapa actual:\*\* Entrega 1 — Exploración de datos, preparación inicial y configuración de herramientas de versionamiento.

## 

## El proyecto cuenta con una primera base consolidada, análisis exploratorio en Jupyter, repositorio GitHub y seguimiento local de datos mediante DVC.

## 

## El modelo predictivo, la aplicación funcional y su despliegue se desarrollarán en las siguientes etapas.

