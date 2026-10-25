"""
Exploración de datos - Graduados de educación superior en Colombia (SNIES 2020-2025)
Pregunta de negocio: ¿en qué medida las características académicas, institucionales y
geográficas explican y predicen la proporción de mujeres entre los graduados?

Uso:
    python exploracion_graduados.py RUTA_BASE_UNIFICADA [--umbral 15] [--salida resultados]

RUTA_BASE_UNIFICADA: archivo .csv, .parquet o .xlsx con las bases 2020-2025 ya unidas
(una fila por institución x programa x sexo x año x semestre, con la columna GRADUADOS).

Salida (carpeta --salida):
    resumen.md          cifras para completar los espacios marcados del reporte
    tabla_agregada.csv  base programa x año con la proporción de mujeres
    fig_*.png           figuras (usar de 4 a 6 en el reporte)
"""
import argparse
import re
import sys
import unicodedata
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Lectura y normalización de nombres de columnas
# ---------------------------------------------------------------------------

def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Z0-9]+", "_", s.upper()).strip("_")


# nombre canónico -> posibles patrones (sobre el nombre normalizado)
CANDIDATAS = {
    "ies_codigo": [r"^CODIGO_DE_LA_INSTITUCION$", r"^CODIGO_INSTITUCION$"],
    "ies_padre": [r"^IES_PADRE$"],
    "ies_nombre": [r"^INSTITUCION_DE_EDUCACION_SUPERIOR_IES$", r"^NOMBRE_INSTITUCION$", r"^INSTITUCION$"],
    "tipo_ies": [r"^PRINCIPAL_O_SECCIONAL$"],
    "sector": [r"^SECTOR_NORMALIZADO$", r"^SECTOR_IES$", r"^SECTOR$"],
    "caracter": [r"^CARACTER_IES$", r"^CARACTER$", r"^CARACTER_INSTITUCION$"],
    "dpto_ies": [r"^DEPARTAMENTO_DE_DOMICILIO_DE_LA_IES$", r"^DEPARTAMENTO_IES$"],
    "ies_acreditada": [r"^IES_ACREDITADA$"],
    "prog_codigo": [r"^CODIGO_SNIES_DEL_PROGRAMA$", r"^CODIGO_SNIES_PROGRAMA$"],
    "prog_nombre": [r"^PROGRAMA_ACADEMICO$", r"^PROGRAMA$"],
    "prog_acreditado": [r"^PROGRAMA_ACREDITADO$"],
    "nivel_academico": [r"^NIVEL_ACADEMICO$"],
    "nivel_formacion": [r"^NIVEL_FORMACION_NORMALIZADO$", r"^NIVEL_DE_FORMACION$", r"^NIVEL_FORMACION$"],
    "modalidad": [r"^MODALIDAD$", r"^METODOLOGIA$"],
    "area": [r"^AREA_DE_CONOCIMIENTO$", r"^AREA_CONOCIMIENTO$"],
    "nbc": [r"^NUCLEO_BASICO_DEL_CONOCIMIENTO_NBC$", r"^NBC$"],
    "cine": [r"^DESC_CINE_CAMPO_AMPLIO$", r"^CINE_CAMPO_AMPLIO$"],
    "dpto_prog": [r"^DEPARTAMENTO_NORMALIZADO$", r"^DEPARTAMENTO_DE_OFERTA_DEL_PROGRAMA$", r"^DEPARTAMENTO_PROGRAMA$", r"^DEPARTAMENTO$"],
    "sexo": [r"^SEXO$", r"^GENERO$"],
    "anio": [r"^ANO$", r"^ANIO$"],
    "semestre": [r"^SEMESTRE$"],
    "graduados": [r"^GRADUADOS$"],
}


def leer(ruta):
    p = Path(ruta)
    if p.suffix == ".parquet":
        return pd.read_parquet(p)
    if p.suffix in (".xlsx", ".xls"):
        return pd.read_excel(p)
    for enc in ("utf-8", "latin-1"):
        try:
            return pd.read_csv(p, encoding=enc, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise ValueError("No se pudo leer el archivo")


def mapear_columnas(df):
    originales = {norm(c): c for c in df.columns}
    mapa, faltan = {}, []
    for canon, pats in CANDIDATAS.items():
        hit = None
        for pat in pats:
            for n, orig in originales.items():
                if re.match(pat, n):
                    hit = orig
                    break
            if hit:
                break
        if hit:
            mapa[hit] = canon
        else:
            faltan.append(canon)
    # Si el nombre original de una columna no elegida coincide con un nombre canónico
    # (p. ej. 'sector' y 'sector_normalizado'), se descarta para evitar columnas duplicadas
    elegidas = set(mapa.keys())
    chocan = [c for c in df.columns if c not in elegidas and c in set(mapa.values())]
    df = df.drop(columns=chocan)
    return df.rename(columns=mapa), faltan


# ---------------------------------------------------------------------------
# 2. Utilidades de graficación
# ---------------------------------------------------------------------------
AZUL, GRIS, ROSA = "#2b5c8a", "#8c8c8c", "#c2547a"
plt.rcParams.update({"figure.dpi": 130, "axes.spines.top": False,
                     "axes.spines.right": False, "font.size": 9})


def prop_ponderada(g):
    """Proporción de mujeres del grupo = total mujeres / total graduados."""
    return g["mujeres"].sum() / g["total"].sum()


def barras(serie, titulo, archivo, salida, ref=None, top=None):
    s = serie.sort_values()
    if top:
        s = s.tail(top)
    fig, ax = plt.subplots(figsize=(7, max(2.5, 0.28 * len(s) + 1)))
    ax.barh(s.index.astype(str), s.values * 100, color=AZUL)
    if ref is not None:
        ax.axvline(ref * 100, color=ROSA, ls="--", lw=1)
        ax.text(ref * 100, len(s) - 0.4, f" global {ref*100:.1f} %", color=ROSA, fontsize=8)
    ax.set_xlabel("% de mujeres entre los graduados")
    ax.set_title(titulo, loc="left", fontsize=10)
    fig.tight_layout()
    fig.savefig(salida / archivo)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3. Análisis
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("ruta")
    ap.add_argument("--umbral", type=int, default=15)
    ap.add_argument("--salida", default="resultados")
    a = ap.parse_args()
    salida = Path(a.salida)
    salida.mkdir(exist_ok=True)
    out = []  # líneas del resumen

    def w(txt=""):
        out.append(txt)
        print(txt)

    raw = leer(a.ruta)
    df, faltan = mapear_columnas(raw)
    obligatorias = {"sexo", "anio", "graduados"}
    if obligatorias & set(faltan):
        sys.exit(f"Faltan columnas obligatorias: {sorted(obligatorias & set(faltan))}\n"
                 f"Columnas encontradas: {list(raw.columns)}")
    # Si la base no trae códigos, se construyen llaves con los nombres
    # (aproximación: dos programas con igual nombre, IES y nivel se tratan como uno)
    aviso_llaves = []
    if "ies_codigo" not in df.columns:
        if "ies_nombre" not in df.columns:
            sys.exit("Se necesita el código o el nombre de la institución")
        df["ies_codigo"] = df["ies_nombre"].astype(str).str.strip().str.upper()
        aviso_llaves.append("IES identificada por nombre (no hay código de la institución)")
    if "prog_codigo" not in df.columns:
        if "prog_nombre" not in df.columns:
            sys.exit("Se necesita el código SNIES o el nombre del programa")
        partes = [df["prog_nombre"].astype(str).str.strip().str.upper()]
        for extra in ("nivel_formacion", "dpto_prog", "modalidad"):
            if extra in df.columns:
                partes.append(df[extra].astype(str).str.strip().str.upper())
        df["prog_codigo"] = partes[0].str.cat(partes[1:], sep="|")
        aviso_llaves.append("Programa identificado por nombre + nivel de formación + departamento"
                            " (+ modalidad si existe); no hay código SNIES")

    w("# Resumen de la exploración\n")
    w("## Tamaño y calidad de los datos (para la sección 3)")
    w(f"- Filas: {len(raw):,}; columnas: {raw.shape[1]}")
    for av in aviso_llaves:
        w(f"- AVISO: {av}")
    w(f"- Años presentes: {sorted(df['anio'].dropna().unique().tolist())}")
    if faltan:
        w(f"- Columnas no encontradas (revisar nombres): {faltan}")
    w(f"- Duplicados exactos: {df.duplicated().sum():,}")
    nulos = (df.isna().mean() * 100).round(2)
    nulos = nulos[nulos > 0].sort_values(ascending=False)
    w("- Porcentaje de nulos por columna (solo >0):")
    for c, v in nulos.items():
        w(f"    - {c}: {v} %")

    df["graduados"] = pd.to_numeric(df["graduados"], errors="coerce")
    w(f"- GRADUADOS no numérico o nulo: {df['graduados'].isna().sum():,}")
    w(f"- GRADUADOS <= 0: {(df['graduados'] <= 0).sum():,}")
    df = df[df["graduados"] > 0].copy()

    # categorías de texto: espacios y mayúsculas, y consistencia entre años
    cat_cols = [c for c in ["sexo", "sector", "caracter", "nivel_academico", "nivel_formacion",
                            "modalidad", "area", "cine", "tipo_ies", "dpto_ies", "dpto_prog",
                            "ies_acreditada", "prog_acreditado"] if c in df.columns]
    for c in cat_cols:
        df[c] = df[c].astype(str).str.strip().str.upper().replace({"NAN": np.nan})
    w("\n- Categorías de SEXO: " + ", ".join(
        f"{k} ({v:,})" for k, v in df.groupby("sexo")["graduados"].sum().items()))
    for c in ["area", "nivel_formacion", "sector", "modalidad"]:
        if c in df.columns:
            por_anio = df.groupby("anio")[c].nunique()
            w(f"- Categorías distintas de {c} por año: {por_anio.to_dict()}")

    # --- construcción de la base programa x año --------------------------------
    sexo = df["sexo"].str.upper()
    df["es_mujer"] = sexo.isin(["FEMENINO", "MUJER", "F"])
    llaves = [c for c in ["ies_codigo", "prog_codigo", "anio", "nivel_academico", "nivel_formacion",
                          "modalidad", "area", "nbc", "cine", "sector", "caracter", "tipo_ies",
                          "ies_acreditada", "prog_acreditado", "dpto_ies", "dpto_prog"]
              if c in df.columns]
    # se rellenan nulos de llaves para no perder filas en el groupby
    base = df[llaves + ["graduados", "es_mujer"]].copy()
    for c in llaves:
        if base[c].dtype == object:
            base[c] = base[c].fillna("SIN DATO")
    base["mujeres"] = base["graduados"] * base["es_mujer"]
    agg = (base.groupby(llaves, as_index=False)
           .agg(total=("graduados", "sum"), mujeres=("mujeres", "sum")))
    agg["prop_mujeres"] = agg["mujeres"] / agg["total"]

    if "area" in df.columns:
        sin = df["area"].astype(str).str.upper().str.contains("SIN CLASIFICAR|SIN INFORMACION|SIN INFORMACIÓN")
        w(f"- Graduados con área 'Sin clasificar' o 'Sin información': "
          f"{100*df.loc[sin,'graduados'].sum()/df['graduados'].sum():.1f} % del total "
          f"(decidir si se excluyen del análisis por área)")
    w("\n## Base programa x año")
    w(f"- Registros programa-año antes del umbral: {len(agg):,}")
    n_prog_dup = agg.duplicated(["ies_codigo", "prog_codigo", "anio"]).sum()
    w(f"- Llaves (IES, programa, año) repetidas con atributos distintos: {n_prog_dup:,}")

    # --- umbral -----------------------------------------------------------------
    mantiene = agg["total"] >= a.umbral
    pct_reg_excl = 100 * (~mantiene).mean()
    pct_grad_cons = 100 * agg.loc[mantiene, "total"].sum() / agg["total"].sum()
    w(f"- Umbral de {a.umbral} graduados: se excluye el {pct_reg_excl:.1f} % de los registros "
      f"programa-año y se conserva el {pct_grad_cons:.1f} % de los graduados "
      f"(→ completar X e Y en la sección 2)")
    for u in (5, 10, 15, 20, 30):
        m = agg["total"] >= u
        w(f"    - umbral {u}: excluye {100*(~m).mean():.1f} % de registros, "
          f"conserva {100*agg.loc[m,'total'].sum()/agg['total'].sum():.1f} % de graduados")
    agg_all = agg.copy()
    agg = agg[mantiene].copy()
    agg.to_csv(salida / "tabla_agregada.csv", index=False)
    w(f"- Registros programa-año tras el umbral: {len(agg):,}")

    glob = prop_ponderada(agg)
    w(f"\n## Variable objetivo")
    w(f"- Proporción global de mujeres (ponderada por graduados): {glob*100:.1f} %")
    w(f"- Proporción media por programa-año (sin ponderar): {agg['prop_mujeres'].mean()*100:.1f} %; "
      f"mediana {agg['prop_mujeres'].median()*100:.1f} %")
    q = agg["prop_mujeres"].quantile([.05, .25, .5, .75, .95]) * 100
    w("- Percentiles 5/25/50/75/95: " + " / ".join(f"{v:.1f}" for v in q))
    w(f"- Programas-año con 0 % de mujeres: {(agg['prop_mujeres']==0).sum():,}; con 100 %: "
      f"{(agg['prop_mujeres']==1).sum():,}")

    # Fig 1: distribución objetivo
    fig, ax = plt.subplots(figsize=(6, 3))
    ax.hist(agg["prop_mujeres"] * 100, bins=40, color=AZUL, edgecolor="white")
    ax.axvline(glob * 100, color=ROSA, ls="--", lw=1)
    ax.set_xlabel("% de mujeres en el programa-año")
    ax.set_ylabel("Programas-año")
    ax.set_title("Distribución de la proporción de mujeres", loc="left", fontsize=10)
    fig.tight_layout(); fig.savefig(salida / "fig_1_distribucion_objetivo.png"); plt.close(fig)

    # Fig 2: evolución
    w("\n## Evolución 2020-2025")
    ev = agg.groupby("anio").apply(prop_ponderada)
    w("- Total por año: " + ", ".join(f"{int(k)}: {v*100:.1f} %" for k, v in ev.items()))
    fig, ax = plt.subplots(figsize=(6, 3))
    if "nivel_academico" in agg.columns:
        for nivel, g in agg.groupby("nivel_academico"):
            s = g.groupby("anio").apply(prop_ponderada) * 100
            ax.plot(s.index, s.values, marker="o", lw=1, label=nivel, alpha=.8)
            w(f"- {nivel}: " + ", ".join(f"{int(k)}: {v:.1f}" for k, v in s.items()))
    ax.plot(ev.index, ev.values * 100, color="black", lw=2.2, marker="o", label="Total")
    ax.set_ylabel("% de mujeres"); ax.legend(fontsize=7, frameon=False)
    ax.set_title("Evolución de la proporción de mujeres", loc="left", fontsize=10)
    fig.tight_layout(); fig.savefig(salida / "fig_2_evolucion.png"); plt.close(fig)

    # análisis por dimensión
    dims = [("area", "Por área de conocimiento", "fig_3_area.png"),
            ("cine", "Por campo amplio CINE", "fig_3b_cine.png"),
            ("nivel_formacion", "Por nivel de formación", "fig_4_nivel_formacion.png"),
            ("sector", "Por sector", None),
            ("caracter", "Por carácter de la IES", None),
            ("tipo_ies", "Por tipo de IES", None),
            ("modalidad", "Por modalidad", None),
            ("ies_acreditada", "Por acreditación de la IES", None),
            ("prog_acreditado", "Por acreditación del programa", None)]
    for col, titulo, arch in dims:
        if col not in agg.columns:
            continue
        s = agg.groupby(col).apply(prop_ponderada)
        n = agg.groupby(col)["total"].sum()
        w(f"\n## {titulo}")
        for k in s.sort_values(ascending=False).index:
            w(f"- {k}: {s[k]*100:.1f} % mujeres ({int(n[k]):,} graduados)")
        w(f"- Rango: {s.min()*100:.1f} % a {s.max()*100:.1f} % (diferencia {100*(s.max()-s.min()):.1f} puntos)")
        if arch:
            barras(s, titulo + " (% de mujeres)", arch, salida, ref=glob)

    # Fig 5: sector/carácter/acreditación en cajas
    cajas = [c for c in ["sector", "caracter", "ies_acreditada", "prog_acreditado"] if c in agg.columns]
    if cajas:
        fig, axs = plt.subplots(1, len(cajas), figsize=(3 * len(cajas), 3), sharey=True)
        axs = np.atleast_1d(axs)
        for ax, c in zip(axs, cajas):
            grupos = [g["prop_mujeres"].values * 100 for _, g in agg.groupby(c)]
            etiquetas = [str(k)[:14] for k, _ in agg.groupby(c)]
            ax.boxplot(grupos, showfliers=False)
            ax.set_xticks(range(1, len(etiquetas) + 1)); ax.set_xticklabels(etiquetas)
            ax.set_title(c, fontsize=9); ax.tick_params(axis="x", rotation=30)
        axs[0].set_ylabel("% de mujeres")
        fig.tight_layout(); fig.savefig(salida / "fig_5_cajas_institucional.png"); plt.close(fig)

    # departamento y comparación IES vs oferta
    for col, nombre in [("dpto_prog", "departamento de oferta del programa"),
                        ("dpto_ies", "departamento de la IES")]:
        if col in agg.columns:
            s = agg.groupby(col).apply(prop_ponderada)
            n = agg.groupby(col)["total"].sum()
            w(f"\n## Por {nombre}")
            w(f"- Mayores: " + "; ".join(f"{k} {s[k]*100:.1f} %" for k in s.sort_values(ascending=False).index[:5]))
            w(f"- Menores: " + "; ".join(f"{k} {s[k]*100:.1f} %" for k in s.sort_values().index[:5]))
            if col == "dpto_prog":
                grandes = s[n >= n.quantile(.25)]  # evita departamentos con muy pocos graduados
                barras(grandes, "Por departamento de oferta (% de mujeres)",
                       "fig_6_departamento.png", salida, ref=glob, top=33)
    if {"dpto_ies", "dpto_prog"} <= set(agg.columns):
        distinto = agg["dpto_ies"] != agg["dpto_prog"]
        w(f"- Registros donde el departamento de la IES difiere del de oferta: {100*distinto.mean():.1f} % "
          f"({100*agg.loc[distinto,'total'].sum()/agg['total'].sum():.1f} % de los graduados)")
        w(f"- Proporción de mujeres cuando difieren: {prop_ponderada(agg[distinto])*100:.1f} %; "
          f"cuando coinciden: {prop_ponderada(agg[~distinto])*100:.1f} %")

    # Interacción nivel x área
    if {"area", "nivel_formacion"} <= set(agg.columns):
        piv = (agg.groupby(["area", "nivel_formacion"]).apply(prop_ponderada).unstack() * 100)
        cnt = agg.groupby(["area", "nivel_formacion"])["total"].sum().unstack()
        piv = piv.where(cnt >= 1000)  # se oculta si hay muy pocos graduados
        fig, ax = plt.subplots(figsize=(7, 3.8))
        im = ax.imshow(piv.values, cmap="RdBu", vmin=20, vmax=80, aspect="auto")
        ax.set_xticks(range(piv.shape[1])); ax.set_xticklabels([str(c)[:18] for c in piv.columns], rotation=35, ha="right", fontsize=7)
        ax.set_yticks(range(piv.shape[0])); ax.set_yticklabels([str(i)[:30] for i in piv.index], fontsize=7)
        for i in range(piv.shape[0]):
            for j in range(piv.shape[1]):
                v = piv.values[i, j]
                if not np.isnan(v):
                    ax.text(j, i, f"{v:.0f}", ha="center", va="center", fontsize=6)
        fig.colorbar(im, ax=ax, label="% de mujeres")
        ax.set_title("Área x nivel de formación", loc="left", fontsize=10)
        fig.tight_layout(); fig.savefig(salida / "fig_7_area_x_nivel.png"); plt.close(fig)
        # combinaciones más extremas
        st = piv.stack().dropna().sort_values()
        w("\n## Interacciones área x nivel (combinaciones con >=1000 graduados)")
        w("- Menor proporción de mujeres: " + "; ".join(f"{a_} / {b_}: {v:.0f} %" for (a_, b_), v in st.head(4).items()))
        w("- Mayor proporción de mujeres: " + "; ".join(f"{a_} / {b_}: {v:.0f} %" for (a_, b_), v in st.tail(4).items()))

    # Cardinalidad e inestabilidad (implicaciones para el modelo)
    w("\n## Implicaciones para el modelo")
    for c in [c for c in ["ies_codigo", "prog_codigo", "nbc", "dpto_prog", "dpto_ies", "area", "cine"] if c in agg.columns]:
        w(f"- Cardinalidad de {c}: {agg[c].nunique():,}")
    pesos = agg["total"].describe()
    w(f"- Graduados por programa-año: mediana {pesos['50%']:.0f}, media {pesos['mean']:.0f}, máx {pesos['max']:.0f}")
    pequenos = agg["total"] < 30
    w(f"- Programas-año con 15-29 graduados: {100*pequenos.mean():.1f} % de los registros "
      f"(varianza alta de la proporción → usar peso = total de graduados)")
    # sd de la proporción esperada solo por azar para n pequeño
    w(f"- Desviación por azar de la proporción con n=15 y p=0.5: {np.sqrt(.25/15)*100:.1f} puntos; con n=100: {np.sqrt(.25/100)*100:.1f} puntos")

    # asociación rápida de cada variable con el objetivo (R² ponderado de ANOVA)
    w("\n## Asociación de cada variable con la proporción de mujeres (R² ponderado, indicativo)")
    y = agg["prop_mujeres"].values; wts = agg["total"].values
    ybar = np.average(y, weights=wts)
    sst = np.sum(wts * (y - ybar) ** 2)
    res = {}
    for c in [c for c in ["area", "cine", "nbc", "nivel_academico", "nivel_formacion", "modalidad", "sector",
                          "caracter", "tipo_ies", "ies_acreditada", "prog_acreditado", "dpto_ies",
                          "dpto_prog", "anio"] if c in agg.columns]:
        medias = agg.groupby(c).apply(lambda g: np.average(g["prop_mujeres"], weights=g["total"]))
        pred = agg[c].map(medias).values
        res[c] = 1 - np.sum(wts * (y - pred) ** 2) / sst
    for c, v in sorted(res.items(), key=lambda kv: -kv[1]):
        w(f"- {c}: R² = {v:.3f}")
    fig, ax = plt.subplots(figsize=(5.5, 3))
    s = pd.Series(res).sort_values()
    ax.barh(s.index, s.values, color=AZUL)
    ax.set_xlabel("R² ponderado (variable sola)")
    ax.set_title("Asociación individual con la proporción de mujeres", loc="left", fontsize=10)
    fig.tight_layout(); fig.savefig(salida / "fig_8_asociacion_variables.png"); plt.close(fig)

    (salida / "resumen.md").write_text("\n".join(out), encoding="utf-8")
    print(f"\nListo. Resultados en: {salida.resolve()}")


if __name__ == "__main__":
    main()
