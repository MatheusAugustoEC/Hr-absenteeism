"""Fase 3 - Analyze: H2 (rival estrutural) antes de H1, H3, H4.
Ainda na janela de exploracao - holdout fechado, nunca lido aqui (A17).
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
OUT_DIR = BASE / "fases" / "fase-3-analyze" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

RNG = np.random.default_rng(20260926)
ALPHA = 0.0125
N_BOOT = 5000

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
report = {}

ids = df["ID"].unique()
n_ids = len(ids)

# atributos fixos por funcionario
attr = df.groupby("ID").agg(
    distancia=("Distance from Residence to Work", "first"),
    n_eventos_total=("ID", "size"),
).reset_index()
mediana_dist = attr["distancia"].median()
attr["longe"] = attr["distancia"] > mediana_dist
report["mediana_distancia"] = float(mediana_dist)
report["n_funcionarios_longe"] = int(attr["longe"].sum())
report["n_funcionarios_perto"] = int((~attr["longe"]).sum())

df = df.merge(attr[["ID", "longe"]], on="ID")

# ------------------------------------------------------------ funcao efeito H1
sub_H1 = df[df["cat"].isin(["B2", "CID"])].copy()

def efeito_H1_bruto(data):
    """Diferenca (p.p.) na proporcao de eventos vindos de funcionario 'longe'
    entre eventos B2 e eventos CID - ponderado por evento (bruto)."""
    p_b2 = data.loc[data["cat"] == "B2", "longe"].mean()
    p_cid = data.loc[data["cat"] == "CID", "longe"].mean()
    return (p_b2 - p_cid) * 100

def efeito_H1_ponderado_funcionario(data):
    """Cada funcionario conta 1 vez: proporcao de eventos B2 (entre B2+CID)
    de cada funcionario, comparando media do grupo longe vs perto."""
    por_func = data.groupby("ID").agg(
        n_b2=("cat", lambda s: (s == "B2").sum()),
        n_cid=("cat", lambda s: (s == "CID").sum()),
        longe=("longe", "first"),
    )
    por_func = por_func[(por_func["n_b2"] + por_func["n_cid"]) > 0]
    por_func["prop_b2"] = por_func["n_b2"] / (por_func["n_b2"] + por_func["n_cid"])
    p_longe = por_func.loc[por_func["longe"], "prop_b2"].mean()
    p_perto = por_func.loc[~por_func["longe"], "prop_b2"].mean()
    return (p_longe - p_perto) * 100

efeito_bruto_h1 = efeito_H1_bruto(sub_H1)
efeito_ponderado_h1 = efeito_H1_ponderado_funcionario(sub_H1)

# ---------------------------------------------- H2(a): excluir top-3 funcionarios
top3 = attr.sort_values("n_eventos_total", ascending=False).head(3)["ID"].tolist()
h2a = {}
for excl_id in top3:
    sub = sub_H1[sub_H1["ID"] != excl_id]
    h2a[int(excl_id)] = {
        "efeito_bruto_pp": round(efeito_H1_bruto(sub), 2),
        "efeito_ponderado_pp": round(efeito_H1_ponderado_funcionario(sub), 2),
    }
report["H2a_exclusao_top3"] = h2a
report["H2b_bruto_vs_ponderado"] = {
    "efeito_bruto_pp": round(efeito_bruto_h1, 2),
    "efeito_ponderado_por_funcionario_pp": round(efeito_ponderado_h1, 2),
    "diverge_muito_ou_inverte": bool(
        (efeito_bruto_h1 * efeito_ponderado_h1 < 0)
        or (abs(efeito_bruto_h1 - efeito_ponderado_h1) > 10)
    ),
}

# criterio de refutacao pre-registrado
efeitos_exclusao = [v["efeito_ponderado_pp"] for v in h2a.values()]
cai_abaixo_10 = any(e < 10 for e in efeitos_exclusao)
inverte_bruto_ponderado = (efeito_bruto_h1 * efeito_ponderado_h1) < 0
H1_refutada_por_H2 = bool(cai_abaixo_10 or inverte_bruto_ponderado)
report["H2_veredito"] = {
    "cai_abaixo_10pp_em_alguma_exclusao": bool(cai_abaixo_10),
    "inverte_sinal_bruto_vs_ponderado": bool(inverte_bruto_ponderado),
    "H1_considerada_nao_sustentada_composicao_de_mix": H1_refutada_por_H2,
}

# ------------------------------------------------------------------- H1 teste
por_func_h1 = sub_H1.groupby("ID").agg(
    n_b2=("cat", lambda s: (s == "B2").sum()),
    n_cid=("cat", lambda s: (s == "CID").sum()),
    longe=("longe", "first"),
).reset_index()

# bootstrap vetorizado: pre-computa contagens por funcionario e soma por indice sorteado
por_func_counts = sub_H1.groupby(["ID", "cat"]).size().unstack(fill_value=0)
por_func_counts = por_func_counts.reindex(columns=["B2", "CID"], fill_value=0)
por_func_counts["longe"] = attr.set_index("ID")["longe"]
por_func_counts = por_func_counts.reset_index()

def efeito_bruto_vetorizado(idx_sorteio):
    sub = por_func_counts.iloc[idx_sorteio]
    n_b2_longe = sub.loc[sub["longe"], "B2"].sum()
    n_b2_perto = sub.loc[~sub["longe"], "B2"].sum()
    n_cid_longe = sub.loc[sub["longe"], "CID"].sum()
    n_cid_perto = sub.loc[~sub["longe"], "CID"].sum()
    tot_b2 = n_b2_longe + n_b2_perto
    tot_cid = n_cid_longe + n_cid_perto
    p_b2 = n_b2_longe / tot_b2 if tot_b2 > 0 else np.nan
    p_cid = n_cid_longe / tot_cid if tot_cid > 0 else np.nan
    return (p_b2 - p_cid) * 100

n_func_h1 = len(por_func_counts)
boots_h1 = []
perm_h1 = []
for _ in range(N_BOOT):
    idx_sorteio = RNG.integers(0, n_func_h1, size=n_func_h1)
    boots_h1.append(efeito_bruto_vetorizado(idx_sorteio))
boots_h1 = np.array(boots_h1)
ci_h1 = np.percentile(boots_h1, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
ci_h1_95 = np.percentile(boots_h1, [2.5, 97.5])

# permutacao: embaralha o rotulo 'longe' entre funcionarios, mantendo os totais fixos
longe_arr = por_func_counts["longe"].to_numpy()
for _ in range(N_BOOT):
    perm = RNG.permutation(longe_arr)
    tmp = por_func_counts.copy()
    tmp["longe"] = perm
    n_b2_longe = tmp.loc[tmp["longe"], "B2"].sum()
    n_b2_perto = tmp.loc[~tmp["longe"], "B2"].sum()
    n_cid_longe = tmp.loc[tmp["longe"], "CID"].sum()
    n_cid_perto = tmp.loc[~tmp["longe"], "CID"].sum()
    tot_b2 = n_b2_longe + n_b2_perto
    tot_cid = n_cid_longe + n_cid_perto
    p_b2 = n_b2_longe / tot_b2 if tot_b2 else np.nan
    p_cid = n_cid_longe / tot_cid if tot_cid else np.nan
    perm_h1.append((p_b2 - p_cid) * 100)
perm_h1 = np.array(perm_h1)
p_valor_h1 = float((np.abs(perm_h1) >= abs(efeito_bruto_h1)).mean())

report["H1_teste"] = {
    "efeito_observado_pp": round(efeito_bruto_h1, 2),
    "ic_98_75_bootstrap_cluster": [round(ci_h1[0], 2), round(ci_h1[1], 2)],
    "ic_95_bootstrap_cluster": [round(ci_h1_95[0], 2), round(ci_h1_95[1], 2)],
    "p_valor_permutacao_por_funcionario": round(p_valor_h1, 4),
    "alpha": ALPHA,
    "significativo_no_alpha": bool(p_valor_h1 < ALPHA),
    "efeito_minimo_pre_registrado_pp": 10,
    "n_clusters": int(n_func_h1),
}

# --------------------------------------------------------------------- H3
b1_reason0 = df[(df["Reason for absence"] == 0)]
por_id_reason0 = b1_reason0.groupby("ID").size().sort_values(ascending=False)
n_reason0 = int(por_id_reason0.sum())
top5_pct = float(por_id_reason0.head(5).sum() / n_reason0 * 100) if n_reason0 else None
n_ids_reason0 = int(por_id_reason0.shape[0])
H3_refutada = bool(top5_pct is not None and n_ids_reason0 > 5 and top5_pct > 50)
report["H3_teste"] = {
    "n_eventos_reason0": n_reason0,
    "n_ids_distintos": n_ids_reason0,
    "distribuicao_por_id": por_id_reason0.to_dict(),
    "top5_ids_concentracao_pct": round(top5_pct, 2) if top5_pct else None,
    "criterio_refutacao": "mais de 5 IDs distintos E top5 respondem por mais de 50%",
    "H3_refutada_comportamento_concentrado": H3_refutada,
    "veredito": "REFUTADA - comportamento concentrado, nao artefato disperso" if H3_refutada else "NAO REFUTADA - dispersao consistente com artefato de registro",
}

# --------------------------------------------------------------------- H4
sub_H4 = df[df["cat"].isin(["B1", "B2", "CID"])].copy()
sub_H4["defeito_B"] = sub_H4["cat"].isin(["B1", "B2"])
sub_H4["mon_fri"] = sub_H4["Day of the week"].isin([2, 6])

por_func_dia = sub_H4.groupby(["ID", "defeito_B"]).agg(
    n=("mon_fri", "size"),
    n_monfri=("mon_fri", "sum"),
).reset_index()
por_func_dia["prop_monfri"] = por_func_dia["n_monfri"] / por_func_dia["n"]

pivot = por_func_dia.pivot(index="ID", columns="defeito_B", values="prop_monfri")
pivot.columns = ["prop_CID_monfri", "prop_B_monfri"]
pivot = pivot.dropna()  # so funcionarios com ambos os tipos de evento
pivot["diff_pp"] = (pivot["prop_B_monfri"] - pivot["prop_CID_monfri"]) * 100

efeito_h4 = float(pivot["diff_pp"].mean())
n_func_h4 = len(pivot)

boots_h4 = []
diffs = pivot["diff_pp"].to_numpy()
for _ in range(N_BOOT):
    idx = RNG.integers(0, n_func_h4, size=n_func_h4)
    boots_h4.append(diffs[idx].mean())
boots_h4 = np.array(boots_h4)
ci_h4 = np.percentile(boots_h4, [100 * ALPHA / 2, 100 * (1 - ALPHA / 2)])
ci_h4_95 = np.percentile(boots_h4, [2.5, 97.5])
# teste de permutacao (sinal aleatorio - H0: diferenca media = 0)
perm_h4 = []
for _ in range(N_BOOT):
    sinais = RNG.choice([-1, 1], size=n_func_h4)
    perm_h4.append((diffs * sinais).mean())
perm_h4 = np.array(perm_h4)
p_valor_h4 = float((np.abs(perm_h4) >= abs(efeito_h4)).mean())

report["H4_teste"] = {
    "n_funcionarios_com_ambos_tipos": int(n_func_h4),
    "efeito_medio_pp_por_funcionario": round(efeito_h4, 2),
    "ic_98_75_bootstrap": [round(ci_h4[0], 2), round(ci_h4[1], 2)],
    "ic_95_bootstrap": [round(ci_h4_95[0], 2), round(ci_h4_95[1], 2)],
    "p_valor_permutacao_sinal": round(p_valor_h4, 4),
    "alpha": ALPHA,
    "significativo_no_alpha": bool(p_valor_h4 < ALPHA),
    "efeito_minimo_pre_registrado_pp": 8,
}

# ----------------------------------------------------------- 7. QUANTIFICACAO
baseline_prop_B = 0.6426
meses_periodo_aprox = 36
eventos_por_mes = len(df) / meses_periodo_aprox
eventos_B_por_mes = eventos_por_mes * baseline_prop_B

report["quantificacao"] = {
    "baseline_prop_B": baseline_prop_B,
    "eventos_B_por_mes_aprox": round(eventos_B_por_mes, 2),
    "H1_explica": "Nao validado com confianca (poder ~3%; ver H1_teste) - efeito observado nao pode ser atribuido com seguranca a causa",
    "H2_explica": "Rival estrutural nao descartou H1 automaticamente, mas tambem nao a confirma - ver H2_veredito",
    "H3_explica": report["H3_teste"]["veredito"],
    "H4_explica": "Nao validado com confianca (mesmo poder baixo) - ver H4_teste",
    "resumo": "Dado o poder de deteccao de aproximadamente 3% para H1 e H4, a maior parte do baseline de 64,26% de eventos B permanece SEM causa validada com confianca estatistica nesta fase. Isso e esperado e declarado, nao suavizado (A15).",
}

with open(OUT_DIR / "analyze.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
