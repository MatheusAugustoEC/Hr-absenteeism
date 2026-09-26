"""Fase 0 - Reconhecimento estrutural.

Regra F9 (metodo-dmaic): nesta fase so estrutura, procedencia e qualidade.
Nada de correlacao, cruzamento ou importancia de variavel entre colunas
distintas. Os testes abaixo verificam GRANULARIDADE (uma coluna repete
dentro do proprio ID / dentro do proprio mes?) e CIRCULARIDADE ARITMETICA
(BMI = Weight / Height^2), que sao checagens estruturais, nao relacionais.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "Absenteeism_at_work.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "fases" / "fase-0-reconhecimento" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW, sep=";")
df.columns = [c.strip() for c in df.columns]

report = {}

# 1. Forma bruta
report["shape"] = {"linhas": df.shape[0], "colunas": df.shape[1]}
report["colunas"] = list(df.columns)
report["dtypes"] = {c: str(t) for c, t in df.dtypes.items()}
report["nulos_por_coluna"] = df.isna().sum().to_dict()
report["duplicatas_exatas"] = int(df.duplicated().sum())

# 2. ID e granularidade
report["n_ids_distintos"] = int(df["ID"].nunique())
report["linhas_por_id"] = df.groupby("ID").size().describe().to_dict()

# colunas candidatas a "atributo fixo do funcionario"
attr_cols = [
    "Transportation expense", "Distance from Residence to Work", "Service time",
    "Age", "Education", "Son", "Social drinker", "Social smoker", "Pet",
    "Weight", "Height", "Body mass index",
]
constancia = {}
for c in attr_cols:
    nunique_por_id = df.groupby("ID")[c].nunique()
    constancia[c] = {
        "ids_com_mais_de_1_valor": int((nunique_por_id > 1).sum()),
        "total_ids": int(nunique_por_id.shape[0]),
    }
report["constancia_atributos_por_id"] = constancia

# 3. Work load Average/day e Hit target: repetem entre IDs diferentes no mesmo mes?
for c in ["Work load Average/day", "Hit target"]:
    if c not in df.columns:
        # nome pode vir com espaco extra no cabecalho original
        cand = [col for col in df.columns if col.strip().startswith(c.split(" ")[0])]
        continue
    grp = df.groupby("Month of absence")[c].nunique()
    report.setdefault("nivel_mes", {})[c] = {
        "valores_distintos_por_mes_describe": grp.describe().to_dict(),
        "meses_com_1_unico_valor": int((grp == 1).sum()),
        "total_meses": int(grp.shape[0]),
    }
    # quantos IDs distintos compartilham o mesmo valor dentro do mesmo mes (amostra mes 1)
    exemplo_mes = df[df["Month of absence"] == df["Month of absence"].mode()[0]]
    report["nivel_mes"][c]["exemplo_mes_valores_distintos"] = int(exemplo_mes[c].nunique())
    report["nivel_mes"][c]["exemplo_mes_n_linhas"] = int(exemplo_mes.shape[0])

# 4. Circularidade BMI = Weight / (Height/100)^2
bmi_calc = df["Weight"] / ((df["Height"] / 100) ** 2)
resid = (bmi_calc - df["Body mass index"]).abs()
report["circularidade_bmi"] = {
    "residuo_max": float(resid.max()),
    "residuo_medio": float(resid.mean()),
    "pct_residuo_menor_que_1": float((resid < 1).mean() * 100),
}

# 5. Reason for absence: distribuicao de categorias (capitulos CID = 1-21; 22-28 outros; 0 = ausente/nao especificado)
report["reason_for_absence_contagem"] = df["Reason for absence"].value_counts().sort_index().to_dict()

# 6. Month of absence: zeros (mes nao informado?) e cobertura
report["month_of_absence_contagem"] = df["Month of absence"].value_counts().sort_index().to_dict()

# 7. Day of the week e Seasons
report["day_of_week_contagem"] = df["Day of the week"].value_counts().sort_index().to_dict()
report["seasons_contagem"] = df["Seasons"].value_counts().sort_index().to_dict()

# 8. Disciplinary failure
report["disciplinary_failure_contagem"] = df["Disciplinary failure"].value_counts().to_dict()

# 9. Absenteeism time in hours: distribuicao bruta (forma, nao relacao)
ath = df["Absenteeism time in hours"]
report["absenteeism_hours_describe"] = ath.describe().to_dict()
report["absenteeism_hours_zeros"] = int((ath == 0).sum())
report["absenteeism_hours_valores_distintos"] = sorted(ath.unique().tolist())

# 10. Sinais de dado sintetico (F5): cardinalidade de continuas
for c in ["Transportation expense", "Distance from Residence to Work", "Weight", "Height", "Work load Average/day"]:
    report.setdefault("cardinalidade_continuas", {})[c] = int(df[c].nunique())

with open(OUT_DIR / "perfil_estrutural.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
