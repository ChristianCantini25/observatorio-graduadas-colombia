# Resumen de la exploración

## Tamaño y calidad de los datos (para la sección 3)
- Filas: 273,485; columnas: 15
- AVISO: IES identificada por nombre (no hay código de la institución)
- AVISO: Programa identificado por nombre + nivel de formación + departamento (+ modalidad si existe); no hay código SNIES
- Años presentes: [2020, 2021, 2022, 2023, 2024, 2025]
- Columnas no encontradas (revisar nombres): ['ies_codigo', 'ies_padre', 'tipo_ies', 'dpto_ies', 'ies_acreditada', 'prog_codigo', 'prog_acreditado', 'modalidad', 'nbc', 'cine']
- Duplicados exactos: 5,477
- Porcentaje de nulos por columna (solo >0):
- GRADUADOS no numérico o nulo: 0
- GRADUADOS <= 0: 0

- Categorías de SEXO: FEMENINO (1,768,079.0), MASCULINO (1,383,678.0), NO BINARIO (12.0)
- Categorías distintas de area por año: {2020: 9, 2021: 9, 2022: 9, 2023: 9, 2024: 9, 2025: 9}
- Categorías distintas de nivel_formacion por año: {2020: 9, 2021: 9, 2022: 9, 2023: 9, 2024: 9, 2025: 9}
- Categorías distintas de sector por año: {2020: 2, 2021: 2, 2022: 2, 2023: 2, 2024: 2, 2025: 2}
- Graduados con área 'Sin clasificar' o 'Sin información': 2.3 % del total (decidir si se excluyen del análisis por área)

## Base programa x año
- Registros programa-año antes del umbral: 82,815
- Llaves (IES, programa, año) repetidas con atributos distintos: 235
- Umbral de 15 graduados: se excluye el 50.0 % de los registros programa-año y se conserva el 92.9 % de los graduados (→ completar X e Y en la sección 2)
    - umbral 5: excluye 25.8 % de registros, conserva 98.6 % de graduados
    - umbral 10: excluye 40.0 % de registros, conserva 96.0 % de graduados
    - umbral 15: excluye 50.0 % de registros, conserva 92.9 % de graduados
    - umbral 20: excluye 57.2 % de registros, conserva 89.7 % de graduados
    - umbral 30: excluye 67.8 % de registros, conserva 83.0 % de graduados
- Registros programa-año tras el umbral: 41,398

## Variable objetivo
- Proporción global de mujeres (ponderada por graduados): 56.6 %
- Proporción media por programa-año (sin ponderar): 54.5 %; mediana 57.8 %
- Percentiles 5/25/50/75/95: 11.1 / 40.0 / 57.8 / 71.2 / 88.2
- Programas-año con 0 % de mujeres: 359; con 100 %: 309

## Evolución 2020-2025
- Total por año: 2020: 56.5 %, 2021: 57.1 %, 2022: 57.4 %, 2023: 56.9 %, 2024: 55.8 %, 2025: 55.6 %
- POSGRADO: 2020: 57.1, 2021: 57.1, 2022: 58.9, 2023: 57.9, 2024: 57.8, 2025: 57.0
- PREGRADO: 2020: 56.4, 2021: 57.2, 2022: 57.0, 2023: 56.7, 2024: 55.2, 2025: 55.2

## Por área de conocimiento
- CIENCIAS DE LA SALUD: 71.3 % mujeres (176,895 graduados)
- CIENCIAS DE LA EDUCACIÓN: 66.2 % mujeres (240,531 graduados)
- SIN CLASIFICAR: 65.5 % mujeres (2,072 graduados)
- ECONOMÍA, ADMINISTRACIÓN, CONTADURÍA Y AFINES: 63.9 % mujeres (1,063,421 graduados)
- CIENCIAS SOCIALES Y HUMANAS: 59.2 % mujeres (593,802 graduados)
- BELLAS ARTES: 57.0 % mujeres (70,504 graduados)
- SIN INFORMACIÓN: 55.5 % mujeres (63,785 graduados)
- MATEMÁTICAS Y CIENCIAS NATURALES: 55.2 % mujeres (38,953 graduados)
- AGRONOMÍA, VETERINARIA Y AFINES: 53.7 % mujeres (39,783 graduados)
- INGENIERÍA, ARQUITECTURA, URBANISMO Y AFINES: 34.4 % mujeres (638,360 graduados)
- Rango: 34.4 % a 71.3 % (diferencia 36.9 puntos)

## Por nivel de formación
- ESPECIALIZACIÓN UNIVERSITARIA: 58.7 % mujeres (478,740 graduados)
- UNIVERSITARIO: 58.5 % mujeres (1,488,211 graduados)
- MAESTRÍA: 55.3 % mujeres (145,452 graduados)
- TECNOLÓGICO: 52.5 % mujeres (652,973 graduados)
- ESPECIALIZACIÓN MÉDICO QUIRÚRGICA: 52.0 % mujeres (1,254 graduados)
- FORMACIÓN TÉCNICA PROFESIONAL: 49.8 % mujeres (144,224 graduados)
- ESPECIALIZACIÓN TECNOLÓGICA: 47.3 % mujeres (16,030 graduados)
- DOCTORADO: 44.6 % mujeres (978 graduados)
- ESPECIALIZACIÓN TÉCNICO PROFESIONAL: 16.0 % mujeres (244 graduados)
- Rango: 16.0 % a 58.7 % (diferencia 42.7 puntos)

## Por sector
- PRIVADO: 59.5 % mujeres (1,654,541 graduados)
- OFICIAL: 52.7 % mujeres (1,273,565 graduados)
- Rango: 52.7 % a 59.5 % (diferencia 6.8 puntos)

## Por carácter de la IES
- INSTITUCIÓN TÉCNICA PROFESIONAL: 58.7 % mujeres (100,999 graduados)
- INSTITUCIÓN UNIVERSITARIA/ESCUELA TECNOLÓGICA: 58.3 % mujeres (887,140 graduados)
- UNIVERSIDAD: 56.4 % mujeres (1,421,974 graduados)
- INSTITUCIÓN TECNOLÓGICA: 53.5 % mujeres (517,993 graduados)
- Rango: 53.5 % a 58.7 % (diferencia 5.2 puntos)

## Por departamento de oferta del programa
- Mayores: ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA 75.4 %; GUAVIARE 66.8 %; ARAUCA 66.1 %; LA GUAJIRA 65.0 %; CHOCO 63.6 %
- Menores: CUNDINAMARCA 44.8 %; ATLANTICO 53.6 %; CALDAS 53.8 %; AMAZONAS 54.2 %; GUAINIA 54.2 %

## Interacciones área x nivel (combinaciones con >=1000 graduados)
- Menor proporción de mujeres: CIENCIAS DE LA EDUCACIÓN / TECNOLÓGICO: 27 %; INGENIERÍA, ARQUITECTURA, URBANISMO Y AFINES / ESPECIALIZACIÓN TECNOLÓGICA: 29 %; INGENIERÍA, ARQUITECTURA, URBANISMO Y AFINES / FORMACIÓN TÉCNICA PROFESIONAL: 30 %; INGENIERÍA, ARQUITECTURA, URBANISMO Y AFINES / TECNOLÓGICO: 31 %
- Mayor proporción de mujeres: ECONOMÍA, ADMINISTRACIÓN, CONTADURÍA Y AFINES / TECNOLÓGICO: 68 %; CIENCIAS DE LA SALUD / UNIVERSITARIO: 72 %; CIENCIAS DE LA SALUD / ESPECIALIZACIÓN UNIVERSITARIA: 73 %; CIENCIAS DE LA SALUD / FORMACIÓN TÉCNICA PROFESIONAL: 74 %

## Implicaciones para el modelo
- Cardinalidad de ies_codigo: 318
- Cardinalidad de prog_codigo: 9,036
- Cardinalidad de dpto_prog: 33
- Cardinalidad de area: 10
- Graduados por programa-año: mediana 40, media 71, máx 11772
- Programas-año con 15-29 graduados: 35.6 % de los registros (varianza alta de la proporción → usar peso = total de graduados)
- Desviación por azar de la proporción con n=15 y p=0.5: 12.9 puntos; con n=100: 5.0 puntos

## Asociación de cada variable con la proporción de mujeres (R² ponderado, indicativo)
- area: R² = 0.298
- sector: R² = 0.023
- nivel_formacion: R² = 0.019
- dpto_prog: R² = 0.019
- caracter: R² = 0.006
- anio: R² = 0.001
- nivel_academico: R² = 0.001