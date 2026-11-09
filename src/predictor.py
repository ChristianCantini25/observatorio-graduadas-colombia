
"""Servicio de predicción del Observatorio de Graduadas.

Utiliza el modelo Random Forest seleccionado en la Entrega 2.
"""

from functools import lru_cache
from pathlib import Path

import joblib
import pandas as pd


MODEL_PATH = (
    Path(__file__).resolve().parents[1]
    / "resultados"
    / "modelos"
    / "modelo_seleccionado.joblib"
)

FEATURES = [
    "area_conocimiento",
    "nivel_formacion_normalizado",
    "sector_normalizado",
    "caracter_institucion",
    "departamento_normalizado",
    "anio",
]


@lru_cache(maxsize=1)
def cargar_modelo():
    """Carga el modelo una sola vez por proceso."""
    if not MODEL_PATH.is_file():
        raise FileNotFoundError(
            f"No se encontró el modelo: {MODEL_PATH}"
        )

    return joblib.load(MODEL_PATH)


def predecir_proporcion(caracteristicas: dict) -> dict:
    """Estima la proporción femenina esperada de un programa."""
    faltantes = [
        variable
        for variable in FEATURES
        if variable not in caracteristicas
    ]

    if faltantes:
        raise ValueError(
            f"Faltan variables obligatorias: {faltantes}"
        )

    for variable in FEATURES[:-1]:
        valor = caracteristicas[variable]
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                f"Valor inválido para {variable}"
            )

    anio = caracteristicas["anio"]
    if type(anio) is not int or not 2020 <= anio <= 2025:
        raise ValueError(
            "El año debe ser un entero entre 2020 y 2025."
        )

    entrada = pd.DataFrame(
        [{variable: caracteristicas[variable] for variable in FEATURES}]
    )

    modelo = cargar_modelo()
    prediccion = float(modelo.predict(entrada)[0])

    proporcion = max(0.0, min(1.0, prediccion))

    return {
        "proporcion_esperada": proporcion,
        "porcentaje_esperado": round(proporcion * 100, 2),
        "modelo": "Random Forest",
        "anio": anio,
    }
