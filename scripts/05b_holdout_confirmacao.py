"""Fase 5 - Control: ANALISE da confirmacao. Roda depois de 05a, sobre o
sorteio ja fixado em data/holdout/split_ids.json. Nao mexe na semente nem
no sorteio - so calcula o efeito de H1 dentro do grupo de confirmacao.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
HOLDOUT_DIR = BASE / "data" / "holdout"
OUT_DIR = BASE / "fases" / "fase-5-control" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

with open(HOLDOUT_DIR / "split_ids.json", encoding="utf-8") as f:
    split = json.load(f)

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

# mediana de distancia usada na Fase 3 (calculada sobre TODAS as 34
# identidades, decisao ja travada no Analyze - nao recalcular so na
# exploracao, para manter a mesma definicao de "longe" usada em H1 e H2)
attr_completo = df.groupby("ID")["Distance from Residence to Work"].first()
mediana_dist_global = attr_completo.median()

df_confirmacao = df[df["ID"].isin(split["ids_confirmacao"])].copy()
df_confirmacao["longe"] = df_confirmacao["ID"].map(attr_completo) > mediana_dist_global

attr_confirmacao = attr_completo.loc[split["ids_confirmacao"]]

report = {
    "ids_confirmacao": split["ids_confirmacao"],
    "n_identidades_confirmacao": len(split["ids_confirmacao"]),
    "distancias_confirmacao": {int(i): float(d) for i, d in attr_confirmacao.items()},
    "mediana_distancia_global_34_identidades": float(mediana_dist_global),
    "n_longe_confirmacao": int((attr_confirmacao > mediana_dist_global).sum()),
    "n_perto_confirmacao": int((attr_confirmacao <= mediana_dist_global).sum()),
}

sub_h1 = df_confirmacao[df_confirmacao["cat"].isin(["B2", "CID"])].copy()
report["n_eventos_B2_confirmacao"] = int((sub_h1["cat"] == "B2").sum())
report["n_eventos_CID_confirmacao"] = int((sub_h1["cat"] == "CID").sum())

por_func = sub_h1.groupby("ID").agg(
    n_b2=("cat", lambda s: (s == "B2").sum()),
    n_cid=("cat", lambda s: (s == "CID").sum()),
).reset_index()
por_func["longe"] = por_func["ID"].map(attr_completo) > mediana_dist_global
report["n_funcionarios_com_evento_B2_ou_CID"] = int(len(por_func))
report["distribuicao_por_funcionario"] = por_func.to_dict(orient="records")

if len(por_func) >= 2 and por_func["longe"].nunique() == 2:
    n_b2_longe = por_func.loc[por_func["longe"], "n_b2"].sum()
    n_b2_perto = por_func.loc[~por_func["longe"], "n_b2"].sum()
    n_cid_longe = por_func.loc[por_func["longe"], "n_cid"].sum()
    n_cid_perto = por_func.loc[~por_func["longe"], "n_cid"].sum()
    tot_b2 = n_b2_longe + n_b2_perto
    tot_cid = n_cid_longe + n_cid_perto
    p_b2 = n_b2_longe / tot_b2 if tot_b2 > 0 else None
    p_cid = n_cid_longe / tot_cid if tot_cid > 0 else None
    efeito = (p_b2 - p_cid) * 100 if (p_b2 is not None and p_cid is not None) else None

    # bootstrap de cluster sobre os funcionarios do holdout (8, ou menos os
    # sem evento B2/CID) - IC amplo esperado dado n pequeno
    rng = np.random.default_rng(20260926)
    counts = por_func.set_index("ID")[["n_b2", "n_cid"]].to_numpy()
    longe_arr = por_func["longe"].to_numpy()
    n_emp = len(por_func)
    boots = []
    for _ in range(5000):
        idx = rng.integers(0, n_emp, size=n_emp)
        c = counts[idx]
        l = longe_arr[idx]
        tb2 = c[:, 0].sum()
        tcid = c[:, 1].sum()
        b2l = c[l, 0].sum() if l.any() else 0
        cidl = c[l, 1].sum() if l.any() else 0
        pb2 = b2l / tb2 if tb2 > 0 else np.nan
        pcid = cidl / tcid if tcid > 0 else np.nan
        boots.append((pb2 - pcid) * 100)
    boots = np.array(boots)
    boots_validos = boots[~np.isnan(boots)]
    ci = np.percentile(boots_validos, [2.5, 97.5]) if len(boots_validos) > 100 else [None, None]

    report["H1_confirmacao"] = {
        "n_b2_longe": int(n_b2_longe), "n_b2_perto": int(n_b2_perto),
        "n_cid_longe": int(n_cid_longe), "n_cid_perto": int(n_cid_perto),
        "proporcao_longe_entre_B2": round(float(p_b2), 4) if p_b2 is not None else None,
        "proporcao_longe_entre_CID": round(float(p_cid), 4) if p_cid is not None else None,
        "efeito_pp": round(float(efeito), 2) if efeito is not None else None,
        "ic_95_bootstrap_cluster": [round(float(ci[0]), 2), round(float(ci[1]), 2)] if ci[0] is not None else None,
        "n_replicas_bootstrap_validas": int(len(boots_validos)),
        "efeito_pre_registrado_exploracao_pp": 16.4,
        "mesma_direcao": bool(efeito is not None and efeito > 0),
    }
else:
    report["H1_confirmacao"] = {
        "calculavel": False,
        "motivo": "Grupo de confirmacao nao tem os dois estratos (longe/perto) com eventos B2 ou CID suficientes para o calculo.",
    }

with open(OUT_DIR / "holdout_confirmacao.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(report, ensure_ascii=False, indent=2, default=str))
