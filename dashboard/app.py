
"""Tablero del Observatorio de Participación Femenina en Colombia."""

import pandas as pd
import plotly.express as px
import streamlit as st

from dashboard.datos import (
    cargar_base,
    cargar_brechas,
    cargar_importancia,
    calcular_indicadores,
    resumir_dimension,
    resumir_brechas,
)


st.set_page_config(
    page_title="Observatorio de Participación Femenina",
    layout="wide",
)

st.title("Observatorio de Participación Femenina")
st.caption(
    "Graduados de educación superior en Colombia | "
    "Fuente: SNIES, 2020–2025"
)

base = cargar_base()


def opciones(df, columna):
    """Devuelve categorías disponibles ordenadas."""
    return sorted(df[columna].dropna().unique().tolist())


def filtrar(df, selecciones):
    """Aplica los filtros seleccionados al conjunto de datos."""
    resultado = df.copy()

    for columna, valores in selecciones.items():
        if valores:
            resultado = resultado[
                resultado[columna].isin(valores)
            ]
        else:
            return resultado.iloc[0:0].copy()

    return resultado


# --------------------------------------------------
# FILTROS
# --------------------------------------------------

st.sidebar.header("Filtros del observatorio")
st.sidebar.caption(
    "Selecciona las características que deseas analizar."
)

anio = st.sidebar.selectbox(
    "Año de referencia",
    ["Todos"] + opciones(base, "anio"),
)

area = st.sidebar.multiselect(
    "Área de conocimiento",
    opciones(base, "area_conocimiento"),
    placeholder="Todas las áreas",
)

nivel = st.sidebar.multiselect(
    "Nivel de formación",
    opciones(base, "nivel_formacion_normalizado"),
    placeholder="Todos los niveles",
)

sector = st.sidebar.multiselect(
    "Sector institucional",
    opciones(base, "sector_normalizado"),
    placeholder="Todos los sectores",
)

caracter = st.sidebar.multiselect(
    "Carácter de la institución",
    opciones(base, "caracter_institucion"),
    placeholder="Todos los caracteres",
)

departamento = st.sidebar.multiselect(
    "Departamento",
    opciones(base, "departamento_normalizado"),
    placeholder="Todos los departamentos",
)

selecciones = {}

for columna, valores in {
    "area_conocimiento": area,
    "nivel_formacion_normalizado": nivel,
    "sector_normalizado": sector,
    "caracter_institucion": caracter,
    "departamento_normalizado": departamento,
}.items():
    selecciones[columna] = (
        valores if valores else opciones(base, columna)
    )

# La evolución utiliza todos los años.
# El año seleccionado solo afecta los indicadores y comparativos.
historico = filtrar(base, selecciones)

if anio == "Todos":
    filtrada = historico.copy()
else:
    filtrada = historico[historico["anio"] == anio].copy()

if filtrada.empty:
    st.warning(
        "No existen registros para la combinación seleccionada."
    )
    st.stop()


# --------------------------------------------------
# INDICADORES PRINCIPALES
# --------------------------------------------------

st.subheader("Panorama general")

indicadores = calcular_indicadores(filtrada)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Total de graduados",
    f"{indicadores['graduados']:,}",
)

c2.metric(
    "Mujeres graduadas",
    f"{indicadores['mujeres']:,}",
)

c3.metric(
    "Participación femenina",
    f"{indicadores['proporcion_mujeres']:.1%}",
)

st.caption(
    "Universo: programas con al menos 15 graduados "
    "en cada año. Los porcentajes se calculan "
    "ponderando por el número de graduados."
)

st.divider()


# --------------------------------------------------
# EVOLUCIÓN HISTÓRICA
# --------------------------------------------------

st.subheader("Evolución de la participación femenina")

evolucion = (
    historico.groupby("anio", as_index=False)[
        ["mujeres", "total"]
    ]
    .sum()
)

evolucion["proporcion_mujeres"] = (
    evolucion["mujeres"] / evolucion["total"]
)

fig_evolucion = px.line(
    evolucion,
    x="anio",
    y="proporcion_mujeres",
    markers=True,
    labels={
        "anio": "Año",
        "proporcion_mujeres": "Participación femenina",
    },
)

fig_evolucion.update_yaxes(
    tickformat=".1%",
)

fig_evolucion.update_xaxes(
    dtick=1,
)

fig_evolucion.update_layout(
    height=390,
    margin=dict(l=20, r=20, t=25, b=20),
)

st.plotly_chart(fig_evolucion, width="stretch")

st.caption(
    "La evolución muestra 2020–2025 para las "
    "características académicas, institucionales "
    "y territoriales seleccionadas, independientemente "
    "del año de referencia."
)

st.divider()


# --------------------------------------------------
# COMPARACIÓN POR ÁREA
# --------------------------------------------------

st.subheader("Participación femenina por área de conocimiento")

resumen_area = resumir_dimension(
    filtrada,
    "area_conocimiento",
)

fig_area = px.bar(
    resumen_area,
    x="proporcion_mujeres",
    y="area_conocimiento",
    orientation="h",
    text="proporcion_mujeres",
    labels={
        "proporcion_mujeres": "Participación femenina",
        "area_conocimiento": "Área de conocimiento",
    },
)

fig_area.update_traces(
    texttemplate="%{text:.1%}",
    textposition="outside",
)

fig_area.update_xaxes(
    tickformat=".0%",
    range=[0, 1],
)

fig_area.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=520,
    margin=dict(l=20, r=50, t=20, b=20),
)

st.plotly_chart(fig_area, width="stretch")


# --------------------------------------------------
# COMPARACIÓN TERRITORIAL
# --------------------------------------------------

st.divider()

st.subheader("Participación femenina por departamento")

resumen_depto = resumir_dimension(
    filtrada,
    "departamento_normalizado",
)

fig_depto = px.bar(
    resumen_depto,
    x="proporcion_mujeres",
    y="departamento_normalizado",
    orientation="h",
    text="proporcion_mujeres",
    labels={
        "proporcion_mujeres": "Participación femenina",
        "departamento_normalizado": "Departamento",
    },
)

fig_depto.update_traces(
    texttemplate="%{text:.1%}",
    textposition="outside",
)

fig_depto.update_xaxes(
    tickformat=".0%",
    range=[0, 1],
)

fig_depto.update_layout(
    yaxis={"categoryorder": "total ascending"},
    height=850,
    margin=dict(l=20, r=50, t=20, b=20),
)

st.plotly_chart(fig_depto, width="stretch")

st.caption(
    "Los resultados descriptivos no implican relaciones "
    "causales ni permiten atribuir las diferencias "
    "a una característica individual."
)

# --------------------------------------------------
# ANÁLISIS DE BRECHAS: OBSERVADO VS. ESPERADO
# --------------------------------------------------

st.divider()

st.subheader("Participación observada frente a esperada")

st.caption(
    "Predicciones fuera de muestra del Random Forest para "
    "2024–2025. Una brecha negativa indica una participación "
    "femenina inferior a la esperada según las características "
    "académicas, institucionales y territoriales."
)

brechas = cargar_brechas()

# Aplicar los mismos filtros del tablero.
# El archivo de brechas no incluye caracter_institucion,
# por lo que esa dimensión se recuperará posteriormente.
filtros_brechas = {
    "area_conocimiento": area,
    "nivel_formacion_normalizado": nivel,
    "sector_normalizado": sector,
    "caracter_institucion": caracter,
    "departamento_normalizado": departamento,
}

for columna, valores in filtros_brechas.items():
    if valores:
        brechas = brechas[brechas[columna].isin(valores)]

if anio in [2024, 2025]:
    brechas = brechas[brechas["anio"] == anio]
elif anio != "Todos":
    brechas = brechas.iloc[0:0].copy()

if brechas.empty:
    st.info(
        "No hay predicciones fuera de muestra disponibles "
        "para la selección realizada. La evaluación del "
        "modelo comprende 2024 y 2025."
    )
else:
    dimension = st.selectbox(
        "Comparar brechas por",
        [
            "area_conocimiento",
            "departamento_normalizado",
            "nivel_formacion_normalizado",
            "sector_normalizado",
        ],
        format_func=lambda x: {
            "area_conocimiento": "Área de conocimiento",
            "departamento_normalizado": "Departamento",
            "nivel_formacion_normalizado": "Nivel de formación",
            "sector_normalizado": "Sector",
        }[x],
    )

    resumen = resumir_brechas(brechas, dimension)

    fig_brechas = px.bar(
        resumen,
        x="brecha",
        y=dimension,
        orientation="h",
        color="brecha",
        color_continuous_scale="RdBu",
        color_continuous_midpoint=0,
        labels={
            "brecha": "Brecha (proporción)",
            dimension: "Categoría",
        },
    )

    fig_brechas.update_xaxes(tickformat="+.0%")
    fig_brechas.update_layout(height=550)

    st.plotly_chart(fig_brechas, width="stretch")

    tabla = resumen[
        [dimension, "total", "observado", "esperado", "brecha"]
    ].copy()

    tabla["observado"] *= 100
    tabla["esperado"] *= 100
    tabla["brecha"] *= 100

    st.dataframe(
        tabla,
        column_config={
            "total": st.column_config.NumberColumn(
                "Graduados", format="%d"
            ),
            "observado": st.column_config.NumberColumn(
                "Observado (%)", format="%.1f"
            ),
            "esperado": st.column_config.NumberColumn(
                "Esperado (%)", format="%.1f"
            ),
            "brecha": st.column_config.NumberColumn(
                "Brecha (pp)", format="%+.1f"
            ),
        },
        hide_index=True,
        width="stretch",
    )

    st.caption(
        "Las brechas son señales exploratorias, no evidencia "
        "causal ni una clasificación definitiva. El modelo "
        "presenta un RMSE ponderado aproximado de 16 puntos "
        "porcentuales y sus resultados individuales deben "
        "interpretarse con precaución."
    )

# --------------------------------------------------
# IMPORTANCIA DE VARIABLES DEL MODELO
# --------------------------------------------------

st.divider()

st.subheader("¿Qué variables influyen en las predicciones?")

st.caption(
    "Importancia por permutación del Random Forest seleccionado. "
    "Muestra cuánto aumenta el error MAE ponderado cuando "
    "se altera una variable del modelo."
)

importancia = cargar_importancia()

nombres = {
    "area_conocimiento": "Área de conocimiento",
    "nivel_formacion_normalizado": "Nivel de formación",
    "sector_normalizado": "Sector institucional",
    "caracter_institucion": "Carácter de la institución",
    "departamento_normalizado": "Departamento",
    "anio": "Año",
}

importancia["variable_mostrar"] = (
    importancia["variable"].map(nombres)
)

importancia = importancia.sort_values(
    "importancia",
    ascending=True,
)

fig_importancia = px.bar(
    importancia,
    x="importancia",
    y="variable_mostrar",
    orientation="h",
    text="importancia",
    labels={
        "importancia": "Aumento del MAE ponderado",
        "variable_mostrar": "Variable",
    },
)

fig_importancia.update_traces(
    texttemplate="%{text:.3f}",
    textposition="outside",
)

fig_importancia.update_layout(
    height=430,
    margin=dict(l=20, r=65, t=20, b=20),
)

st.plotly_chart(fig_importancia, width="stretch")

st.info(
    "El área de conocimiento es la variable más importante "
    "del modelo. Estas importancias describen la capacidad "
    "predictiva y no demuestran relaciones causales."
)

# --------------------------------------------------
# SIMULADOR PREDICTIVO - INTEGRACION CON FASTAPI
# --------------------------------------------------

import requests

st.divider()
st.subheader("Simulador de participación femenina esperada")

st.caption(
    "Selecciona las características de un programa para "
    "estimar la participación femenina esperada mediante "
    "el Random Forest entrenado con datos del SNIES."
)

API_URL = "http://127.0.0.1:8001/predict"

c1, c2 = st.columns(2)

with c1:
    sim_area = st.selectbox(
        "Área de conocimiento del programa",
        opciones(base, "area_conocimiento"),
        key="sim_area",
    )

    sim_nivel = st.selectbox(
        "Nivel de formación del programa",
        opciones(base, "nivel_formacion_normalizado"),
        key="sim_nivel",
    )

    sim_sector = st.selectbox(
        "Sector de la institución",
        opciones(base, "sector_normalizado"),
        key="sim_sector",
    )

with c2:
    sim_caracter = st.selectbox(
        "Carácter de la institución",
        opciones(base, "caracter_institucion"),
        key="sim_caracter",
    )

    sim_departamento = st.selectbox(
        "Departamento del programa",
        opciones(base, "departamento_normalizado"),
        key="sim_departamento",
    )

    sim_anio = st.selectbox(
        "Año de referencia",
        [2020, 2021, 2022, 2023, 2024, 2025],
        index=5,
        key="sim_anio",
    )

if st.button(
    "Calcular participación esperada",
    type="primary",
):
    entrada = {
        "area_conocimiento": sim_area,
        "nivel_formacion_normalizado": sim_nivel,
        "sector_normalizado": sim_sector,
        "caracter_institucion": sim_caracter,
        "departamento_normalizado": sim_departamento,
        "anio": sim_anio,
    }

    try:
        respuesta = requests.post(
            API_URL,
            json=entrada,
            timeout=30,
        )

        respuesta.raise_for_status()
        resultado = respuesta.json()

        st.success("Predicción generada correctamente.")

        st.metric(
            "Participación femenina esperada",
            f"{resultado['porcentaje_esperado']:.2f}%",
        )

        st.caption(
            "Estimación estadística, no una meta normativa "
            "ni una predicción causal. El modelo fue evaluado "
            "fuera de muestra en 2024–2025."
        )

    except requests.RequestException:
        st.error(
            "No fue posible conectar con la API predictiva. "
            "Verifica que FastAPI esté ejecutándose "
            "en el puerto 8001."
        )
