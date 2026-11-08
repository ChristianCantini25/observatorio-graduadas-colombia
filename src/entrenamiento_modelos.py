"""Entrenamiento y evaluación de modelos - Observatorio de participación femenina.

Objetivo: predecir prop_mujeres por programa-año (ponderado por total de graduados).
Split temporal: train 2020-2023 / test 2024-2025. Ajuste de hiperparámetros con
validación interna (entrena 2020-2022, valida 2023) para no tocar el test.
Registra todo en MLflow si está instalado (en EC2 lo estará).

Uso:  python src/entrenamiento_modelos.py [--ruta data/derivado/programas_anio.xls]
                                         [--tracking-uri http://IP:5000] [--salida resultados/modelos]
"""
import argparse, itertools, json
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.inspection import permutation_importance
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

try:
    import mlflow, mlflow.sklearn
except ImportError:
    mlflow = None

CAT = ["area_conocimiento", "nivel_formacion_normalizado", "sector_normalizado",
       "caracter_institucion", "departamento_normalizado"]
NUM = ["anio"]
SEMILLA = 42


def cargar(ruta):
    df = pd.read_csv(ruta, encoding="utf-8-sig")
    return df.dropna(subset=["prop_mujeres", "total"]).reset_index(drop=True)


def metricas(y, p, w):
    return {"mae": mean_absolute_error(y, p), "rmse": mean_squared_error(y, p) ** 0.5,
            "r2": r2_score(y, p), "mae_pond": mean_absolute_error(y, p, sample_weight=w),
            "rmse_pond": mean_squared_error(y, p, sample_weight=w) ** 0.5,
            "r2_pond": r2_score(y, p, sample_weight=w)}


def pipeline(modelo, usa_rezago):
    num = NUM + (["prop_anio_anterior"] if usa_rezago else [])
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), CAT),
                             ("num", "passthrough", num)])
    return Pipeline([("pre", pre), ("m", modelo)]), CAT + num


def preparar(df, usa_rezago):
    X = df[CAT + NUM + (["prop_anio_anterior"] if usa_rezago else [])].copy()
    if usa_rezago:  # el rezago no existe para el primer año del programa
        X["prop_anio_anterior"] = X["prop_anio_anterior"].fillna(df["prop_mujeres"].mean())
    return X


def malla(nombre):
    if nombre == "random_forest":
        return [dict(n_estimators=150, max_depth=d, min_samples_leaf=l, n_jobs=-1, random_state=SEMILLA)
                for d, l in itertools.product([8, 16, None], [5, 20])]
    return [dict(n_estimators=n, max_depth=d, learning_rate=lr, subsample=0.8, random_state=SEMILLA)
            for n, d, lr in itertools.product([150, 300], [3, 5], [0.05, 0.1])]


def construir(nombre, params):
    return {"random_forest": RandomForestRegressor, "gradient_boosting": GradientBoostingRegressor,
            "baseline_lineal": Ridge}[nombre](**params)


def ajustar(pipe, X, y, w):
    pipe.fit(X, y, m__sample_weight=w)
    return pipe


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ruta", default="data/derivado/programas_anio.xls")
    ap.add_argument("--salida", default="resultados/modelos")
    ap.add_argument("--tracking-uri", default=None)
    ap.add_argument("--experimento", default="observatorio_prop_mujeres")
    a = ap.parse_args()
    out = Path(a.salida); out.mkdir(parents=True, exist_ok=True)

    if mlflow:
        if a.tracking_uri:
            mlflow.set_tracking_uri(a.tracking_uri)
        mlflow.set_experiment(a.experimento)
    else:
        print("MLflow no instalado: se omite el registro (los CSV sí se generan).")

    df = cargar(a.ruta)
    tr_int, va_int = df[df.anio <= 2022], df[df.anio == 2023]
    train, test = df[df.anio <= 2023], df[df.anio >= 2024]
    print(f"train={len(train)} test={len(test)} (validación interna 2023={len(va_int)})")

    filas, imp_all, mejor_por_variante = [], [], {}
    for rezago in (False, True):
        variante = "con_rezago" if rezago else "solo_caracteristicas"
        for nombre in ["baseline_lineal", "random_forest", "gradient_boosting"]:
            cands = [dict(alpha=1.0)] if nombre == "baseline_lineal" else malla(nombre)
            # 1) ajuste de hiperparámetros: entrena 2020-2022, valida 2023
            mejor, mejor_mae = None, np.inf
            for p in cands:
                pipe, _ = pipeline(construir(nombre, p), rezago)
                ajustar(pipe, preparar(tr_int, rezago), tr_int.prop_mujeres, tr_int.total)
                pv = pipe.predict(preparar(va_int, rezago))
                mae = mean_absolute_error(va_int.prop_mujeres, pv, sample_weight=va_int.total)
                if mae < mejor_mae:
                    mejor, mejor_mae = p, mae
            # 2) reentrena con 2020-2023 y evalúa en test 2024-2025
            pipe, cols = pipeline(construir(nombre, mejor), rezago)
            ajustar(pipe, preparar(train, rezago), train.prop_mujeres, train.total)
            Xt = preparar(test, rezago)
            pred = np.clip(pipe.predict(Xt), 0, 1)
            m = metricas(test.prop_mujeres, pred, test.total)
            m["mae_pond_validacion"] = mejor_mae
            print(f"{variante:22s}{nombre:18s} MAE_pond={m['mae_pond']:.4f} RMSE_pond={m['rmse_pond']:.4f} R2_pond={m['r2_pond']:.3f}")
            filas.append({"variante": variante, "modelo": nombre, **m, "params": json.dumps(mejor)})
            mejor_por_variante[(variante, nombre)] = (pipe, pred)

            # importancia por permutación (en test, ponderada por graduados) por variable original
            if nombre != "baseline_lineal":
                r = permutation_importance(pipe, Xt, test.prop_mujeres, n_repeats=5, random_state=SEMILLA,
                                           scoring="neg_mean_absolute_error",
                                           sample_weight=test.total.values, n_jobs=-1)
                imp = pd.DataFrame({"variable": cols, "importancia": r.importances_mean,
                                    "desv": r.importances_std}).sort_values("importancia", ascending=False)
                imp.insert(0, "modelo", nombre); imp.insert(0, "variante", variante)
                imp_all.append(imp)

            if mlflow:
                with mlflow.start_run(run_name=f"{nombre}__{variante}"):
                    mlflow.log_params({**mejor, "modelo": nombre, "variante": variante,
                                       "train": "2020-2023", "test": "2024-2025"})
                    mlflow.log_metrics({k: float(v) for k, v in m.items()})
                    mlflow.sklearn.log_model(pipe, name="modelo", serialization_format="cloudpickle")
                    if nombre != "baseline_lineal":
                        mlflow.log_table(imp, "importancia_variables.json")

    res = pd.DataFrame(filas); res.to_csv(out / "metricas.csv", index=False)
    pd.concat(imp_all).to_csv(out / "importancia_variables.csv", index=False)

    # modelo seleccionado: menor MAE ponderado en test, variante sin rezago (uso del tablero)
    sc = res[res.variante == "solo_caracteristicas"].sort_values("mae_pond")
    ganador = sc.iloc[0]["modelo"]
    pipe, pred = mejor_por_variante[("solo_caracteristicas", ganador)]
    joblib.dump(pipe, out / "modelo_seleccionado.joblib")

    # observado vs esperado: ajustar el modelo ganador sobre TODO el histórico no es válido (sesgo),
    # por eso el "esperado" de test sale del modelo entrenado en 2020-2023.
    ove = test[["anio", "institucion", "programa", "nivel_formacion_normalizado", "area_conocimiento",
                "departamento_normalizado", "sector_normalizado", "total", "prop_mujeres"]].copy()
    ove["esperado"] = pred
    ove["brecha"] = ove.prop_mujeres - ove.esperado
    ove.to_csv(out / "observado_vs_esperado.csv", index=False)
    if mlflow:
        with mlflow.start_run(run_name=f"seleccion__{ganador}"):
            mlflow.log_param("modelo_seleccionado", ganador)
            mlflow.log_artifacts(str(out))
    print("Modelo seleccionado (solo características):", ganador)


if __name__ == "__main__":
    main()
