"""Fase 2B - Measure: baseline, capabilidade, Paretos e poder.

Trabalha SO na janela de exploracao (holdout fechado). Base:
data/processed/eventos_qualidade.csv (733 eventos, 34 identidades).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from statsmodels.stats.proportion import proportion_confint
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
OUT_DIR = BASE / "fases" / "fase-2b-measure-baseline" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(20260926)

df = pd.read_csv(QUALIDADE)

def classifica(reason):
    if reason in (0, 26):
        return "B1_comportamental"
    if reason in (22, 23, 24, 25, 27, 28):
        return "B2_administravel"
    if 1 <= reason <= 21:
        return "CID"
    return "OUTRO"

df["categoria_defeito"] = df["Reason for absence"].apply(classifica)
df["e_defeito_B"] = df["categoria_defeito"].isin(["B1_comportamental", "B2_administravel"])
df["e_B1"] = df["categoria_defeito"] == "B1_comportamental"
df["e_B2"] = df["categoria_defeito"] == "B2_administravel"

N = len(df)
ids = df["ID"].unique()
n_ids = len(ids)
report = {"n_total_eventos": int(N), "n_identidades": int(n_ids)}

# --------------------------------------------------- 1. BASELINE (proporcao)

def cluster_bootstrap_ci(flag_col, n_boot=5000, alpha=0.05):
    """Reamostra funcionarios inteiros (nao eventos) com reposicao.
    Vetorizado: para cada ID, pre-computa n_eventos e n_flag; o bootstrap so
    soma esses vetores para os IDs sorteados em cada replica.
    """
    por_id = df.groupby("ID").agg(n_eventos=(flag_col, "size"), n_flag=(flag_col, "sum"))
    n_eventos_arr = por_id["n_eventos"].to_numpy()
    n_flag_arr = por_id["n_flag"].to_numpy()
    n_emp = len(por_id)

    idx_sorteados = RNG.integers(0, n_emp, size=(n_boot, n_emp))
    boots = n_flag_arr[idx_sorteados].sum(axis=1) / n_eventos_arr[idx_sorteados].sum(axis=1)
    lo, hi = np.percentile(boots, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi), boots

baseline = {}
for nome, col in [("B_total", "e_defeito_B"), ("B1", "e_B1"), ("B2", "e_B2")]:
    p_hat = float(df[col].mean())
    n_eventos = int(df[col].sum())
    wilson_lo, wilson_hi = proportion_confint(n_eventos, N, alpha=0.05, method="wilson")
    boot_lo, boot_hi, _ = cluster_bootstrap_ci(col)
    baseline[nome] = {
        "n_eventos": n_eventos,
        "proporcao": round(p_hat, 4),
        "wilson_ic95_naive_733_eventos_independentes": [round(wilson_lo, 4), round(wilson_hi, 4)],
        "bootstrap_cluster_ic95_34_funcionarios": [round(boot_lo, 4), round(boot_hi, 4)],
        "dpmo": round(p_hat * 1_000_000, 1),
    }
    # nivel sigma (aprox., processo de atributo - defeito por unidade=evento)
    dpmo = p_hat if p_hat > 0 else 1e-9
    z_sem_deslocamento = stats.norm.ppf(1 - dpmo) if dpmo < 1 else None
    baseline[nome]["nivel_sigma_sem_deslocamento"] = round(float(z_sem_deslocamento), 3) if z_sem_deslocamento is not None else None
    baseline[nome]["nivel_sigma_com_deslocamento_1_5"] = round(float(z_sem_deslocamento) + 1.5, 3) if z_sem_deslocamento is not None else None

report["baseline_proporcoes"] = baseline

# horas por subcategoria - distribuicao inteira
horas = {}
for cat in ["B1_comportamental", "B2_administravel", "CID"]:
    sub = df[df["categoria_defeito"] == cat]["Absenteeism time in hours"]
    horas[cat] = {
        "n": int(sub.shape[0]),
        "media": round(float(sub.mean()), 2),
        "mediana": round(float(sub.median()), 2),
        "desvio_padrao": round(float(sub.std()), 2),
        "min": float(sub.min()),
        "p25": float(sub.quantile(0.25)),
        "p75": float(sub.quantile(0.75)),
        "max": float(sub.max()),
    }
report["horas_por_subcategoria"] = horas

# ----------------------------------------------- 2. TABELA DESCRITIVA POR MES (nao temporal)
por_mes = df.groupby("Month of absence").agg(
    n_eventos=("e_defeito_B", "size"),
    n_B=("e_defeito_B", "sum"),
).reset_index()
por_mes["proporcao_B"] = (por_mes["n_B"] / por_mes["n_eventos"]).round(4)
report["tabela_nao_temporal_por_mes"] = por_mes.to_dict(orient="records")

# ----------------------------------------------------------- 3. CAPABILIDADE
prop_por_func = df.groupby("ID")["e_defeito_B"].mean().sort_values()
n_func = len(prop_por_func)
tam_quartil = max(1, n_func // 4)
quartil_superior = prop_por_func.iloc[:tam_quartil]  # menor proporcao B = melhor desempenho
meta_interna = float(quartil_superior.mean())
baseline_agregado = float(df["e_defeito_B"].mean())

# traducao em eventos/mes: eventos B observados / (36 meses aprox, 3 anos) vs eventos B se todos no nivel do quartil superior
eventos_totais_periodo = N
meses_periodo_aprox = 36  # jul/2007-jul/2010 ~ 36 meses corridos (aproximacao, sem coluna de ano exata)
eventos_por_mes_observado = eventos_totais_periodo / meses_periodo_aprox
eventos_B_por_mes_observado = eventos_por_mes_observado * baseline_agregado
eventos_B_por_mes_meta = eventos_por_mes_observado * meta_interna
reducao_eventos_B_por_mes = eventos_B_por_mes_observado - eventos_B_por_mes_meta

report["capabilidade"] = {
    "baseline_agregado_prop_B": round(baseline_agregado, 4),
    "n_funcionarios_no_quartil_superior": int(tam_quartil),
    "meta_interna_prop_B_quartil_superior": round(meta_interna, 4),
    "prop_por_funcionario_describe": prop_por_func.describe().to_dict(),
    "eventos_B_por_mes_observado_aprox": round(eventos_B_por_mes_observado, 2),
    "eventos_B_por_mes_na_meta_aprox": round(eventos_B_por_mes_meta, 2),
    "reducao_eventos_B_por_mes_aprox": round(reducao_eventos_B_por_mes, 2),
    "nota_meses_periodo": "36 meses e aproximacao (jul/2007-jul/2010); sem coluna de ano exata, o denominador de meses e estimado, nao contado.",
}

# ------------------------------------------------- 4. ESTRATIFICACAO / PARETO
codigos_B = [0, 22, 23, 24, 25, 26, 27, 28]
sub_B = df[df["Reason for absence"].isin(codigos_B)].copy()
total_eventos_B = len(sub_B)
total_horas_B2 = sub_B[sub_B["Reason for absence"].isin([22, 23, 24, 25, 27, 28])]["Absenteeism time in hours"].sum()

pareto_taxa = (
    sub_B["Reason for absence"].value_counts().sort_values(ascending=False)
)
pareto_taxa_pct = (pareto_taxa / total_eventos_B * 100).round(2)

pareto_impacto_horas = (
    sub_B[sub_B["Reason for absence"].isin([22, 23, 24, 25, 27, 28])]
    .groupby("Reason for absence")["Absenteeism time in hours"].sum()
    .sort_values(ascending=False)
)
pareto_impacto_horas_pct = (pareto_impacto_horas / total_horas_B2 * 100).round(2)

report["pareto"] = {
    "total_eventos_B": int(total_eventos_B),
    "total_horas_B2": float(total_horas_B2),
    "pareto_taxa_pct_por_codigo": pareto_taxa_pct.to_dict(),
    "pareto_impacto_horas_pct_por_codigo_B2_apenas": pareto_impacto_horas_pct.to_dict(),
    "nota_B1": "Reason 0 e 26 (B1) tem Absenteeism time in hours = 0 em 100% dos eventos - nao entram no Pareto de impacto em horas. Regua alternativa para B1: o proprio Pareto de taxa (contagem de eventos), ja reportado acima.",
}

# ------------------------------------------------------- 5. TAMANHO DE AMOSTRA
# poder aproximado com n efetivo = clusters (funcionarios), nao eventos
alpha_bonferroni = 0.0125
power_calc = NormalIndPower()

def poder_dois_grupos(n_por_grupo, p1, effect_pp, alpha):
    p2 = p1 + effect_pp
    h = proportion_effectsize(p2, p1)
    return float(power_calc.power(effect_size=abs(h), nobs1=n_por_grupo, ratio=1.0, alpha=alpha, alternative="two-sided"))

n_por_grupo_aprox = n_func // 2  # divisao por mediana de distancia, ~17 funcionarios por grupo
poder_h1 = poder_dois_grupos(n_por_grupo_aprox, 0.40, 0.10, alpha_bonferroni)  # H1: 10 p.p., baseline ~40% arbitrario p/ calculo
poder_h4 = poder_dois_grupos(n_por_grupo_aprox, 0.20, 0.08, alpha_bonferroni)  # H4: 8 p.p., baseline ~20% arbitrario p/ calculo

contagem_por_codigo = sub_B["Reason for absence"].value_counts().to_dict()
recortes_sem_n = {int(k): int(v) for k, v in contagem_por_codigo.items() if v < 15}

report["poder"] = {
    "n_clusters_total": int(n_func),
    "n_por_grupo_aprox_split_mediana": int(n_por_grupo_aprox),
    "alpha_bonferroni": alpha_bonferroni,
    "poder_aproximado_H1_10pp": round(poder_h1, 3),
    "poder_aproximado_H4_8pp": round(poder_h4, 3),
    "nota": "Poder calculado com n efetivo = numero de FUNCIONARIOS por grupo (~17), nao o numero de eventos - a unidade de aleatorizacao/comparacao e o funcionario para H1 (Distance e constante por funcionario). Baseline de proporcao usado no calculo de h e ilustrativo (Cohen's h depende do nivel base), nao e o baseline real da hipotese.",
    "recortes_sem_n_suficiente_menos_de_15_eventos": recortes_sem_n,
}

with open(OUT_DIR / "baseline.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
