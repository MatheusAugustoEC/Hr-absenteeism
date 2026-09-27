"""Fase 2A - Measure: auditoria de procedencia e qualidade (M1-M5, M22 n/a
ainda). Trabalha sobre data/processed/eventos_limpos.csv (decisao travada do
Define) - nunca sobre o CSV bruto.
"""
import json
import math
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
LIMPOS = BASE / "data" / "processed" / "eventos_limpos.csv"
OUT_DIR = BASE / "fases" / "fase-2a-measure-qualidade" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(LIMPOS)
report = {}

# ---------------------------------------------------------------- 1. PERFIL
report["n_linhas"] = int(len(df))
report["n_ids"] = int(df["ID"].nunique())

def classifica(reason):
    if reason in (0, 26):
        return "B1_comportamental"
    if reason in (22, 23, 24, 25, 27, 28):
        return "B2_administravel"
    if 1 <= reason <= 21:
        return "CID"
    return "OUTRO"

df["categoria_defeito"] = df["Reason for absence"].apply(classifica)
report["contagem_por_categoria"] = df["categoria_defeito"].value_counts().to_dict()
report["eventos_por_id_describe"] = df.groupby("ID").size().describe().to_dict()

# confirma que as 4 linhas excluidas no Define nao sobrevivem
excl_check = {
    "id4_presente": bool((df["ID"] == 4).any()),
    "id35_presente": bool((df["ID"] == 35).any()),
    "id29_linha_jovem_presente": bool(((df["ID"] == 29) & (df["Age"] == 28)).any()),
    "linhas_month0_hours0_presentes": int(((df["Month of absence"] == 0) & (df["Absenteeism time in hours"] == 0)).sum()),
}
report["confirmacao_exclusoes_define"] = excl_check

# ---------------------------------------------------- 2. AS SEIS DIMENSOES

# --- Completude
nulos = df.isna().sum()
report["completude"] = {
    "nulos_por_coluna": nulos.to_dict(),
    "veredito": "APROVADO" if nulos.sum() == 0 else "REPROVADO",
    "nota": "Month of absence=0 e Reason for absence=0 sao categorias validas (codigos), nao nulos.",
}

# --- Unicidade: duplicatas de linha inteira, recalculadas na base limpa
dup_mask = df.duplicated(keep=False)
grupos_dup = (
    df[dup_mask]
    .groupby(list(df.columns))
    .size()
    .reset_index(name="tamanho_grupo")
)

# suporte empirico K_r: numero de combinacoes distintas de (Month, Day, Hours) por Reason
suporte_por_reason = (
    df.groupby("Reason for absence")[["Month of absence", "Day of the week", "Absenteeism time in hours"]]
    .apply(lambda g: g.drop_duplicates().shape[0])
    .to_dict()
)

veredito_grupos = []
for _, row in grupos_dup.iterrows():
    reason = row["Reason for absence"]
    id_ = row["ID"]
    tam = int(row["tamanho_grupo"])
    # n eventos deste ID com este Reason (para o calculo de colisao)
    n_i = int(((df["ID"] == id_) & (df["Reason for absence"] == reason)).sum())
    K_r = int(suporte_por_reason.get(reason, 1))
    K_r = max(K_r, 1)
    # probabilidade aproximada de pelo menos 1 colisao entre n_i sorteios uniformes em K_r valores
    p_colisao = 1 - math.exp(-n_i * (n_i - 1) / (2 * K_r)) if n_i > 1 else 0.0
    veredito = "PLAUSIVEL_POR_ACASO" if p_colisao >= 0.30 else "SUSPEITO_ERRO_DIGITACAO"
    veredito_grupos.append({
        "ID": int(id_),
        "Reason for absence": int(reason),
        "tamanho_grupo": tam,
        "n_eventos_deste_id_desta_reason": n_i,
        "K_r_suporte_empirico": K_r,
        "p_colisao_aproximada": round(p_colisao, 4),
        "veredito": veredito,
    })

report["unicidade"] = {
    "n_linhas_em_grupo_duplicado": int(dup_mask.sum()),
    "n_grupos_duplicados": int(len(grupos_dup)),
    "veredito_por_grupo": veredito_grupos,
    "n_grupos_plausiveis": sum(1 for v in veredito_grupos if v["veredito"] == "PLAUSIVEL_POR_ACASO"),
    "n_grupos_suspeitos": sum(1 for v in veredito_grupos if v["veredito"] == "SUSPEITO_ERRO_DIGITACAO"),
}

# --- Validade
validade = {}
validade["day_of_week_fora_dominio"] = int((~df["Day of the week"].isin([2, 3, 4, 5, 6])).sum())
validade["seasons_fora_dominio"] = int((~df["Seasons"].isin([1, 2, 3, 4])).sum())
validade["education_fora_dominio"] = int((~df["Education"].isin([1, 2, 3, 4])).sum())
validade["reason_fora_dominio"] = int((~df["Reason for absence"].between(0, 28)).sum())
for c in ["Disciplinary failure", "Social drinker", "Social smoker"]:
    validade[f"{c}_fora_dominio"] = int((~df[c].isin([0, 1])).sum())
validade["veredito"] = "APROVADO" if sum(v for k, v in validade.items() if isinstance(v, int)) == 0 else "REPROVADO"
report["validade"] = validade

# --- Consistencia
# (a) work load / hit target nivel-mes, recheck na base limpa
consist_periodo = {}
for c in ["Work load Average/day", "Hit target"]:
    grp = df.groupby("Month of absence")[c].nunique()
    consist_periodo[c] = {
        "media_valores_distintos_por_mes": round(float(grp.mean()), 3),
        "meses_com_1_unico_valor": int((grp == 1).sum()),
        "total_meses": int(grp.shape[0]),
    }
# (b) BMI circularidade recheck
bmi_calc = df["Weight"] / ((df["Height"] / 100) ** 2)
resid = (bmi_calc - df["Body mass index"]).abs()
consist_bmi = {
    "residuo_max": float(resid.max()),
    "residuo_medio": float(resid.mean()),
    "pct_residuo_menor_que_1": float((resid < 1).mean() * 100),
    "regra_operacional": "Weight e Height sao as colunas-fonte; Body mass index e derivada (IMC=Weight/(Height/100)^2, arredondado). Nas fases seguintes, tratar as tres como UMA evidencia - nunca usar Body mass index como preditor concorrente de Weight/Height na mesma analise.",
}
report["consistencia"] = {"nivel_periodo": consist_periodo, "circularidade_bmi": consist_bmi}

# --- Acuracia
report["acuracia"] = {
    "veredito": "NAO_AUDITAVEL",
    "motivo": "Nao ha valor total independente (ex.: soma de horas de um sistema de ponto) para conferir contra a base. Nenhuma regra de fechamento e auditavel aqui - declarado, nao forcado.",
}

# --- Pontualidade
# concentracao de eventos por mes (sem timestamp de registro, so podemos olhar concentracao)
por_mes = df["Month of absence"].value_counts().sort_index()
report["pontualidade"] = {
    "eventos_por_mes": por_mes.to_dict(),
    "veredito": "NAO_AUDITAVEL_PARA_ATRASO",
    "motivo": "Sem timestamp de registro nao ha como medir atraso. A concentracao por mes ja e coberta pela checagem de duplicata (dimensao Unicidade); nenhum mes mostra contagem que sugira lote fora do que a duplicata ja capturou.",
}

# ---------------------------------------------------------------- 3. VIESES
report["vieses"] = {
    "selecao": "Populacao = funcionarios com >=1 evento no periodo. Funcionarios sem nenhuma ausencia nao aparecem - nao ha denominador para taxa de funcionarios que faltam.",
    "vazamento": "Disciplinary failure e Absenteeism time in hours sao pos-evento - nao usar como preditor de Reason for absence nem um do outro.",
    "nao_representado": "Funcionarios sem ausencia no periodo inteiro existem na empresa mas nao na base.",
}

# --------------------------------------------------------- 4. ERRO INDETECTAVEL
report["erro_indetectavel"] = (
    "Reason for absence registrado incorretamente por conveniencia "
    "(ex.: falta sem justificativa lancada como consulta medica) nao deixa "
    "rastro estrutural - so seria visivel com o atestado fisico, que nao "
    "existe nesta base."
)

# -------------------------------------- RESOLUCAO: remove duplicatas suspeitas
# Criterio (M5, com regra escrita): grupo duplicado com p_colisao_aproximada <
# 0.30 (menos de 30% de chance de coincidir por acaso dado o suporte empirico
# da categoria) e tratado como erro de digitacao provavel - mantem-se a
# primeira ocorrencia, descartam-se as demais linhas do grupo. Grupo com
# p_colisao_aproximada >= 0.30 e mantido inteiro (coincidencia plausivel de
# evento real).
suspeitos = [v for v in veredito_grupos if v["veredito"] == "SUSPEITO_ERRO_DIGITACAO"]
idx_remover = []
for s in suspeitos:
    mask = (df["ID"] == s["ID"]) & (df["Reason for absence"] == s["Reason for absence"])
    # restringe aos membros exatos deste grupo duplicado (mesmas colunas completas)
    sub = df[mask]
    # dentro do subconjunto ID+Reason, agrupa por todas as colunas p/ achar o grupo exato
    grp_cols = list(df.columns)
    dup_sub = sub[sub.duplicated(subset=grp_cols, keep=False)]
    if dup_sub.empty:
        continue
    # mantem a primeira ocorrencia (menor indice), remove as demais
    manter = dup_sub.index.min()
    idx_remover.extend([i for i in dup_sub.index if i != manter])

idx_remover = sorted(set(idx_remover))
df_qualidade = df.drop(index=idx_remover).drop(columns=["categoria_defeito"])
report["resolucao_duplicatas"] = {
    "criterio": "p_colisao_aproximada < 0.30 => remover extras, manter 1a ocorrencia",
    "linhas_removidas_indices_originais": idx_remover,
    "n_linhas_removidas": len(idx_remover),
    "n_linhas_final": int(len(df_qualidade)),
}

df_qualidade.to_csv(BASE / "data" / "processed" / "eventos_qualidade.csv", index=False)

with open(OUT_DIR / "auditoria_qualidade.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2, default=str)

print(json.dumps(report["resolucao_duplicatas"], ensure_ascii=False, indent=2, default=str))
print("n_linhas_final:", len(df_qualidade), "n_ids_final:", df_qualidade["ID"].nunique())
