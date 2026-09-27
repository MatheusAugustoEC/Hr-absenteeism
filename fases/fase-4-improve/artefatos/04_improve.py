"""Fase 4 - Improve: simulacao de ganho (H1) e calculo de amostra do
experimento proposto. Ainda na janela de exploracao - holdout fechado.
"""
import json
from pathlib import Path

import pandas as pd
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
OUT_DIR = BASE / "fases" / "fase-4-improve" / "artefatos"
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

attr = df.groupby("ID")["Distance from Residence to Work"].first()
mediana_dist = attr.median()
longe_ids = attr[attr > mediana_dist].index

b2 = df[df["cat"] == "B2"]
b2_longe = b2[b2["ID"].isin(longe_ids)]

report = {
    "mediana_distancia_km": float(mediana_dist),
    "n_funcionarios_longe": int(len(longe_ids)),
    "n_funcionarios_perto": int(len(attr) - len(longe_ids)),
    "n_eventos_B2_total": int(len(b2)),
    "n_eventos_B2_longe": int(len(b2_longe)),
    "n_funcionarios_longe_com_evento_B2": int(b2_longe["ID"].nunique()),
    "horas_mediana_B2_longe": float(b2_longe["Absenteeism time in hours"].median()),
    "horas_mediana_B2_geral_fase2b": 2.0,
    "horas_total_B2_longe_janela": float(b2_longe["Absenteeism time in hours"].sum()),
}

MESES_APROX = 36
eventos_B2_longe_por_mes = report["n_eventos_B2_longe"] / MESES_APROX
horas_mediana = report["horas_mediana_B2_longe"]

cenarios = {}
for adesao in [0.20, 0.50, 0.80]:
    eventos_evitados_mes = eventos_B2_longe_por_mes * adesao
    horas_evitadas_mes = eventos_evitados_mes * horas_mediana
    cenarios[f"adesao_{int(adesao*100)}pct"] = {
        "eventos_evitados_por_mes": round(eventos_evitados_mes, 2),
        "horas_evitadas_por_mes": round(horas_evitadas_mes, 2),
    }
report["cenarios_ganho"] = cenarios
report["eventos_B2_longe_por_mes_aprox"] = round(eventos_B2_longe_por_mes, 3)

# ponto de indiferenca: custo assumido (PREMISSA DECLARADA) de coordenacao de RH
CUSTO_RH_HORAS_POR_MES = 8.0  # premissa declarada, nao medida - ver relatorio
fracao_indiferenca = CUSTO_RH_HORAS_POR_MES / (eventos_B2_longe_por_mes * horas_mediana)
report["ponto_de_indiferenca"] = {
    "custo_rh_assumido_horas_por_mes_PREMISSA": CUSTO_RH_HORAS_POR_MES,
    "fracao_de_adesao_para_empatar": round(fracao_indiferenca, 4),
    "interpretacao": "Se menos desta fracao dos eventos B2 elegiveis migrar para fora do expediente, a politica custa mais tempo de RH do que economiza em horas de ausencia evitada - dado o custo assumido acima.",
}

# ---------------------------------------------- calculo de n para o experimento
power_calc = NormalIndPower()
p1 = 0.40  # baseline ilustrativo, mesma convencao da Fase 2B
p2 = p1 + 0.10
h = proportion_effectsize(p2, p1)
n_por_grupo_80pct = power_calc.solve_power(effect_size=abs(h), power=0.80, alpha=0.0125, ratio=1.0, alternative="two-sided")

report["experimento"] = {
    "n_por_grupo_necessario_poder_80pct_alpha_0125": round(float(n_por_grupo_80pct), 1),
    "n_rotas_longas_disponiveis_aprox": int(len(longe_ids)),
    "viavel_com_operacao_atual": bool(n_por_grupo_80pct <= len(longe_ids)),
    "razao_necessario_vs_disponivel": round(float(n_por_grupo_80pct) / len(longe_ids), 1),
}

with open(OUT_DIR / "improve.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
