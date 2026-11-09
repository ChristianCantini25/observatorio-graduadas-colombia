
"""API de predicción del Observatorio de Graduadas en Colombia."""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from src.predictor import cargar_modelo, predecir_proporcion


app = FastAPI(
    title="Observatorio de Participación Femenina",
    description=(
        "API para estimar la proporción esperada de mujeres "
        "entre los graduados de educación superior en Colombia."
    ),
    version="1.0.0",
)


class ProgramaEntrada(BaseModel):
    """Características utilizadas por el modelo supervisado."""

    model_config = ConfigDict(extra="forbid")

    area_conocimiento: str = Field(min_length=1)
    nivel_formacion_normalizado: str = Field(min_length=1)
    sector_normalizado: str = Field(min_length=1)
    caracter_institucion: str = Field(min_length=1)
    departamento_normalizado: str = Field(min_length=1)
    anio: int = Field(ge=2020, le=2025)


class PrediccionSalida(BaseModel):
    proporcion_esperada: float
    porcentaje_esperado: float
    modelo: str
    anio: int


@app.get("/")
def inicio():
    return {
        "servicio": "Observatorio de Participación Femenina",
        "estado": "disponible",
        "documentacion": "/docs",
    }


@app.get("/health")
def health():
    """Comprueba que el modelo puede cargarse."""
    try:
        cargar_modelo()
        return {"status": "ok", "modelo": "Random Forest"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="El modelo predictivo no está disponible.",
        )


@app.post("/predict", response_model=PrediccionSalida)
def predict(programa: ProgramaEntrada):
    """Predice la proporción femenina esperada."""
    try:
        return predecir_proporcion(programa.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No fue posible generar la predicción.",
        )
