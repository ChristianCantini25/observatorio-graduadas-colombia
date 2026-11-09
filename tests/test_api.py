
"""Pruebas automáticas de la API del Observatorio."""

import pytest
from fastapi.testclient import TestClient

from src.api import app


client = TestClient(app)

PROGRAMA_VALIDO = {
    "area_conocimiento": "Economía, administración, contaduría y afines",
    "nivel_formacion_normalizado": "ESPECIALIZACIÓN UNIVERSITARIA",
    "sector_normalizado": "OFICIAL",
    "caracter_institucion": (
        "Institución Universitaria/Escuela Tecnológica"
    ),
    "departamento_normalizado": "BOGOTA D C",
    "anio": 2024,
}


def test_health():
    """Verifica que el modelo está disponible."""
    respuesta = client.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.json()["status"] == "ok"


def test_prediccion_valida():
    """Reproduce la predicción de referencia de Lizeth."""
    respuesta = client.post("/predict", json=PROGRAMA_VALIDO)

    assert respuesta.status_code == 200

    datos = respuesta.json()

    assert datos["modelo"] == "Random Forest"
    assert datos["anio"] == 2024
    assert datos["proporcion_esperada"] == pytest.approx(
        0.3923479879803757,
        abs=1e-6,
    )
    assert datos["porcentaje_esperado"] == 39.23


def test_variable_faltante():
    """Rechaza una entrada sin área de conocimiento."""
    entrada = PROGRAMA_VALIDO.copy()
    del entrada["area_conocimiento"]

    respuesta = client.post("/predict", json=entrada)

    assert respuesta.status_code == 422


def test_anio_fuera_de_rango():
    """Rechaza años fuera del período del proyecto."""
    entrada = PROGRAMA_VALIDO.copy()
    entrada["anio"] = 2030

    respuesta = client.post("/predict", json=entrada)

    assert respuesta.status_code == 422


def test_variable_adicional():
    """Rechaza variables ajenas al contrato de la API."""
    entrada = PROGRAMA_VALIDO.copy()
    entrada["variable_inventada"] = "ejemplo"

    respuesta = client.post("/predict", json=entrada)

    assert respuesta.status_code == 422
