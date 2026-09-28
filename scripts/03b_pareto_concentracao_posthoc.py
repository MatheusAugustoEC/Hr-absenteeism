"""[I2] Pos-hoc (27/09/2026), a partir de achado da banca sobre a Fase 6/Entrega.
Holdout ja aberto (Fase 5) - este teste usa so a amostra de exploracao (34
identidades), no mesmo desenho da exclusao top-3 de H2 (Fase 3), mas aplicado
a concentracao de "consulta medica" no Pareto de horas/eventos administraveis,
nao a hipotese da distancia. Nao reabre nem reconfirma no holdout.
"""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
OUT_DIR = BASE / "fases" / "fase-3-analyze" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(QUALIDADE)

def classifica(reason):
    if reason in (0, 26):
        return "B1"
    if reason in (22, 23, 24, 25, 27, 28):
        return "B2"
    if 1 <= reason <= 21:
        return "CID"
    return "OUTRO"

df["cat"] = df["Reason for absence"].apply(classifica)
b2 = df[df["cat"] == "B2"]
evitavel = df[df["cat"].isin(["B1", "B2"])]

CONSULTA_MEDICA = 23

def pct_horas(b2_sub):
    tot = b2_sub["Absenteeism time in hours"].sum()
    cm = b2_sub[b2_sub["Reason for absence"] == CONSULTA_MEDICA]["Absenteeism time in hours"].sum()
    return round(100 * cm / tot, 2) if tot else None

def pct_eventos(evitavel_sub):
    tot = len(evitavel_sub)
    cm = len(evitavel_sub[evitavel_sub["Reason for absence"] == CONSULTA_MEDICA])
    return round(100 * cm / tot, 2) if tot else None

top3 = (
    b2[b2["Reason for absence"] == CONSULTA_MEDICA]
    .groupby("ID").size().sort_values(ascending=False).head(3).index.tolist()
)

baseline = {"pct_horas": pct_horas(b2), "pct_eventos": pct_eventos(evitavel)}

exclusoes = {}
for eid in top3:
    exclusoes[int(eid)] = {
        "pct_horas": pct_horas(b2[b2["ID"] != eid]),
        "pct_eventos": pct_eventos(evitavel[evitavel["ID"] != eid]),
    }

horas_vals = [v["pct_horas"] for v in exclusoes.values()]
eventos_vals = [v["pct_eventos"] for v in exclusoes.values()]

report = {
    "id_achado": "I2",
    "origem": "Fase 7 - Revisao por banca, pos-hoc a partir da Fase 2B/Analyze",
    "holdout": "nao tocado - so amostra de exploracao (34 identidades)",
    "desenho": "mesmo formato da exclusao top-3 de H2 (Fase 3): exclui, um de cada vez, os 3 funcionarios com mais eventos de consulta medica",
    "top3_ids_consulta_medica": [int(i) for i in top3],
    "baseline": baseline,
    "exclusoes": exclusoes,
    "faixa_pct_horas_com_exclusao": [min(horas_vals), max(horas_vals)],
    "faixa_pct_eventos_com_exclusao": [min(eventos_vals), max(eventos_vals)],
    "concentrado_em_poucos_funcionarios": bool(min(horas_vals) < 25 or min(eventos_vals) < 25),
}

with open(OUT_DIR / "pareto_concentracao_posthoc.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print(json.dumps(report, ensure_ascii=False, indent=2))
