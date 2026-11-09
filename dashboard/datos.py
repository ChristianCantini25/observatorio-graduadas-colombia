
"""Carga y preparación de datos para el tablero del Observatorio."""

from pathlib import Path

import pandas as pd
import streamlit as st
import json
import re
import unicodedata


RAIZ = Path(__file__).resolve().parents[1]

RUTA_BASE = RAIZ / "data" / "derivado" / "programas_anio.xls"
RUTA_BRECHAS = (
    RAIZ / "resultados" / "modelos" / "observado_vs_esperado.csv"
)
RUTA_IMPORTANCIA = (
    RAIZ / "resultados" / "modelos" / "importancia_variables.csv"
)


@st.cache_data
def cargar_base():
    """Carga la base descriptiva de programas-año (2020-2025)."""
    df = pd.read_csv(RUTA_BASE, encoding="utf-8-sig")

    columnas = [
        "anio",
        "institucion",
        "programa",
        "area_conocimiento",
        "nivel_formacion_normalizado",
        "sector_normalizado",
        "caracter_institucion",
        "departamento_normalizado",
        "mujeres",
        "hombres",
        "no_binario",
        "total",
        "prop_mujeres",
    ]

    return df[columnas].copy()




@st.cache_data
def cargar_brechas():
    """Carga brechas y recupera el carácter institucional."""
    brechas = pd.read_csv(RUTA_BRECHAS, encoding="utf-8-sig")
    base = cargar_base()

    claves = [
        "anio",
        "institucion",
        "programa",
        "nivel_formacion_normalizado",
        "area_conocimiento",
        "departamento_normalizado",
        "sector_normalizado",
    ]

    referencia = base[
        claves + ["caracter_institucion"]
    ].copy()

    resultado = brechas.merge(
        referencia,
        on=claves,
        how="left",
        validate="one_to_one",
        indicator=True,
    )

    if len(resultado) != len(brechas):
        raise ValueError(
            "El cruce modificó la cantidad de registros."
        )

    if not resultado["_merge"].eq("both").all():
        raise ValueError(
            "Existen registros sin carácter institucional."
        )

    return resultado.drop(columns="_merge")




@st.cache_data
def cargar_importancia():
    """Carga las importancias por permutación del modelo seleccionado."""
    df = pd.read_csv(RUTA_IMPORTANCIA, encoding="utf-8-sig")

    return df[
        (df["variante"] == "solo_caracteristicas")
        & (df["modelo"] == "random_forest")
    ].copy()


def calcular_indicadores(df):
    """Calcula indicadores agregados ponderados por graduados."""
    total = int(df["total"].sum())
    mujeres = int(df["mujeres"].sum())

    proporcion = mujeres / total if total > 0 else 0.0

    return {
        "graduados": total,
        "mujeres": mujeres,
        "proporcion_mujeres": proporcion,
        "programas_anio": len(df),
    }


def resumir_dimension(df, dimension):
    """Agrupa los graduados por una dimensión académica o territorial."""
    resumen = (
        df.groupby(dimension, dropna=False)[
            ["mujeres", "total"]
        ]
        .sum()
        .reset_index()
    )

    resumen["proporcion_mujeres"] = (
        resumen["mujeres"] / resumen["total"]
    )

    return resumen.sort_values(
        "proporcion_mujeres",
        ascending=False,
    )


def resumir_brechas(df, dimension):
    """Calcula observado, esperado y brecha ponderados por graduados."""
    trabajo = df.copy()

    trabajo["mujeres_estimadas"] = (
        trabajo["esperado"] * trabajo["total"]
    )

    trabajo["mujeres_observadas"] = (
        trabajo["prop_mujeres"] * trabajo["total"]
    )

    resumen = (
        trabajo.groupby(dimension, dropna=False)[
            ["mujeres_estimadas", "mujeres_observadas", "total"]
        ]
        .sum()
        .reset_index()
    )

    resumen["observado"] = (
        resumen["mujeres_observadas"] / resumen["total"]
    )

    resumen["esperado"] = (
        resumen["mujeres_estimadas"] / resumen["total"]
    )

    resumen["brecha"] = (
        resumen["observado"] - resumen["esperado"]
    )

    return resumen.sort_values("brecha")

RUTA_GEOJSON = RAIZ / "data" / "geo" / "departamentos_colombia.geojson"


def normalizar_departamento(texto):
    """Normaliza tildes y puntuación para cruzar nombres territoriales."""
    texto = str(texto).upper().strip()
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(
        caracter for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )
    texto = re.sub(r"[^A-Z0-9]+", " ", texto)
    return " ".join(texto.split())


@st.cache_data
def cargar_geografia():
    """Carga polígonos GeoJSON y añade una llave normalizada."""
    with open(RUTA_GEOJSON, encoding="utf-8") as archivo:
        geojson = json.load(archivo)

    for figura in geojson["features"]:
        figura["properties"]["departamento_clave"] = (
            normalizar_departamento(
                figura["properties"]["dpto_nombre"]
            )
        )

    return geojson
