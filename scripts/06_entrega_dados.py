"""Fase 6 - Entrega: consolida os agregados de todas as fases num unico JSON
que a pagina le em tempo de execucao. Nenhum numero e digitado a mao na
pagina - tudo vem daqui, que por sua vez le so os artefatos ja congelados
das fases (fases/*/artefatos/*.json, baseline-congelado.md) e a base final
data/processed/eventos_qualidade.csv (so estrutura, sem nenhuma relacao nova
sendo calculada - so reagrupamento para exibicao).
"""
import json
from pathlib import Path

import pandas as pd

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
OUT_DIR = BASE / "fases" / "fase-6-entrega" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def carrega(rel):
    with open(BASE / rel, encoding="utf-8") as f:
        return json.load(f)

baseline = carrega("fases/fase-2b-measure-baseline/artefatos/baseline.json")
analyze = carrega("fases/fase-3-analyze/artefatos/analyze.json")
improve = carrega("fases/fase-4-improve/artefatos/improve.json")
holdout = carrega("fases/fase-5-control/artefatos/holdout_confirmacao.json")

df = pd.read_csv(QUALIDADE)

# nomes descritivos - nunca B1/B2/CID/codigo numerico na pagina
MOTIVO_POR_REASON = {
    0: "Falta sem justificativa aceita",
    26: "Falta sem justificativa aceita",
    22: "Acompanhamento",
    23: "Consulta médica",
    24: "Doação de sangue",
    25: "Exame laboratorial",
    27: "Fisioterapia",
    28: "Consulta odontológica",
}
def tipo_de(reason):
    if reason in (0, 26):
        return 2  # sem justificativa aceita
    if reason in (22, 23, 24, 25, 27, 28):
        return 1  # administravel
    return 0  # atestado medico (CID 1-21)

def motivo_de(reason):
    if 1 <= reason <= 21:
        return "Atestado médico"
    return MOTIVO_POR_REASON[reason]

df["tipo"] = df["Reason for absence"].apply(tipo_de)
df["motivo"] = df["Reason for absence"].apply(motivo_de)

mediana_dist = df.groupby("ID")["Distance from Residence to Work"].first().median()
df["distancia_grp"] = (df["ID"].map(df.groupby("ID")["Distance from Residence to Work"].first()) > mediana_dist).astype(int)  # 0 perto, 1 longe

DIA_LABEL = {2: "Segunda", 3: "Terça", 4: "Quarta", 5: "Quinta", 6: "Sexta"}
df["dia_lbl"] = df["Day of the week"].map(DIA_LABEL)

TIPO_LABELS = ["Atestado médico", "Ausência administrável", "Falta sem justificativa aceita"]
MOTIVO_LABELS = ["Atestado médico", "Consulta médica", "Consulta odontológica", "Fisioterapia",
                  "Acompanhamento", "Exame laboratorial", "Doação de sangue", "Falta sem justificativa aceita"]
MOTIVO_IDX = {lab: i for i, lab in enumerate(MOTIVO_LABELS)}
DIST_LABELS = ["Mais perto (até a mediana)", "Mais longe (acima da mediana)"]
DIA_LABELS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
DIA_IDX = {lab: i for i, lab in enumerate(DIA_LABELS)}
ESTACAO_LABELS = ["Estação 1", "Estação 2", "Estação 3", "Estação 4"]

df["motivo_i"] = df["motivo"].map(MOTIVO_IDX)
df["dia_i"] = df["dia_lbl"].map(DIA_IDX)
df["estacao_i"] = df["Seasons"] - 1

cubo = (
    df.groupby(["tipo", "motivo_i", "distancia_grp", "dia_i", "estacao_i"])
    .agg(it=("Reason for absence", "size"), h=("Absenteeism time in hours", "sum"))
    .reset_index()
    .rename(columns={"distancia_grp": "di"})
)
cubo_rows = cubo.rename(columns={"tipo": "ti", "motivo_i": "mo", "dia_i": "da", "estacao_i": "es"})[
    ["ti", "mo", "di", "da", "es", "it", "h"]
].to_dict(orient="records")

# Paretos por motivo (so a parte evitavel) - taxa (7 motivos) e impacto em horas
# (6 motivos administraveis - falta sem justificativa tem sempre 0h, Fase 2B/2A)
evitavel = df[df["tipo"] != 0]
total_evitavel = len(evitavel)
pareto_taxa_motivo = (
    evitavel["motivo"].value_counts()
    .rename_axis("motivo").reset_index(name="n")
)
pareto_taxa_motivo["pct"] = (pareto_taxa_motivo["n"] / total_evitavel * 100).round(2)
pareto_taxa_motivo = pareto_taxa_motivo.sort_values("pct", ascending=False).to_dict(orient="records")

administraveis = df[df["tipo"] == 1]
total_horas_adm = administraveis["Absenteeism time in hours"].sum()
pareto_impacto_motivo = (
    administraveis.groupby("motivo")["Absenteeism time in hours"].sum()
    .rename("horas").reset_index()
)
pareto_impacto_motivo["pct"] = (pareto_impacto_motivo["horas"] / total_horas_adm * 100).round(2)
pareto_impacto_motivo = pareto_impacto_motivo.sort_values("pct", ascending=False).to_dict(orient="records")

# barra por funcionario, anonimizada, ordenada por proporcao evitavel crescente
df["evitavel"] = (df["tipo"] != 0).astype(int)
por_func = df.groupby("ID").agg(n=("evitavel", "size"), evit=("evitavel", "sum")).reset_index()
por_func["prop"] = por_func["evit"] / por_func["n"]
por_func = por_func.sort_values("prop").reset_index(drop=True)
por_func["rotulo"] = ["Funcionário " + str(i + 1) for i in range(len(por_func))]
funcionarios = por_func[["rotulo", "n", "prop"]].to_dict(orient="records")

# [I7, pos-hoc 27/09/2026] mes x tipo - mesma base nao-temporal do M11 (sem
# coluna de ano, mistura os 3 anos calendario), quebrada por tipo para o
# grafico exploratorio de padrao de calendario (Carnaval cai em fevereiro
# nos 3 anos cobertos - 2008, 2009, 2010 - verificado por calculo de Pascoa).
mes_por_tipo = (
    df.groupby(["Month of absence", "tipo"]).size().rename("it").reset_index()
    .pivot(index="Month of absence", columns="tipo", values="it")
    .reindex(columns=[0, 1, 2], fill_value=0)
    .fillna(0).astype(int).reset_index()
    .rename(columns={0: "atestado", 1: "administravel", 2: "sem_justificativa", "Month of absence": "mes"})
    .to_dict(orient="records")
)

dados = {
    "TIPO_LABELS": TIPO_LABELS,
    "mes_por_tipo": mes_por_tipo,
    "MOTIVO_LABELS": MOTIVO_LABELS,
    "DIST_LABELS": DIST_LABELS,
    "DIA_LABELS": DIA_LABELS,
    "ESTACAO_LABELS": ESTACAO_LABELS,
    "cubo": cubo_rows,
    "funcionarios": funcionarios,
    "pareto_taxa_motivo": pareto_taxa_motivo,
    "pareto_impacto_motivo": pareto_impacto_motivo,
    "mediana_distancia_km": float(mediana_dist),

    "baseline": {
        "n_total": baseline["n_total_eventos"],
        "n_identidades": baseline["n_identidades"],
        "prop_evitavel": baseline["baseline_proporcoes"]["B_total"]["proporcao"],
        "prop_evitavel_ic95": baseline["baseline_proporcoes"]["B_total"]["bootstrap_cluster_ic95_34_funcionarios"],
        "prop_administravel": baseline["baseline_proporcoes"]["B2"]["proporcao"],
        "prop_administravel_ic95": baseline["baseline_proporcoes"]["B2"]["bootstrap_cluster_ic95_34_funcionarios"],
        "prop_sem_justificativa": baseline["baseline_proporcoes"]["B1"]["proporcao"],
        "prop_sem_justificativa_ic95": baseline["baseline_proporcoes"]["B1"]["bootstrap_cluster_ic95_34_funcionarios"],
        "meta_interna": baseline["capabilidade"]["meta_interna_prop_B_quartil_superior"],
        "eventos_evitaveis_mes_atual": baseline["capabilidade"]["eventos_B_por_mes_observado_aprox"],
        "eventos_evitaveis_mes_meta": baseline["capabilidade"]["eventos_B_por_mes_na_meta_aprox"],
        "reducao_potencial_mes": baseline["capabilidade"]["reducao_eventos_B_por_mes_aprox"],
        "tabela_nao_temporal_por_mes": baseline["tabela_nao_temporal_por_mes"],
    },

    "achados": {
        "H1_efeito_pp": analyze["H1_teste"]["efeito_observado_pp"],
        "H1_ic": analyze["H1_teste"]["ic_95_bootstrap_cluster"],
        "H1_p": analyze["H1_teste"]["p_valor_permutacao_por_funcionario"],
        "H1_alpha": analyze["H1_teste"]["alpha"],
        "H1_n_clusters": analyze["H1_teste"]["n_clusters"],
        "H1_n_longe": analyze["n_funcionarios_longe"],
        "H1_n_perto": analyze["n_funcionarios_perto"],
        "H2_nao_refuta": not analyze["H2_veredito"]["H1_considerada_nao_sustentada_composicao_de_mix"],
        "H3_n_casos": analyze["H3_teste"]["n_eventos_reason0"],
        "H3_n_ids": analyze["H3_teste"]["n_ids_distintos"],
        "H3_top5_pct": analyze["H3_teste"]["top5_ids_concentracao_pct"],
        "H3_refutada": analyze["H3_teste"]["H3_refutada_comportamento_concentrado"],
        "H4_efeito_pp": analyze["H4_teste"]["efeito_medio_pp_por_funcionario"],
        "H4_p": analyze["H4_teste"]["p_valor_permutacao_sinal"],
        "H2_bruto_pp": analyze["H2b_bruto_vs_ponderado"]["efeito_bruto_pp"],
        "H2_ponderado_pp": analyze["H2b_bruto_vs_ponderado"]["efeito_ponderado_por_funcionario_pp"],
        "H2_exclusoes": [v["efeito_ponderado_pp"] for v in analyze["H2a_exclusao_top3"].values()],
    },

    "holdout": {
        "n_confirmacao": holdout["n_identidades_confirmacao"],
        "n_longe": holdout["n_longe_confirmacao"],
        "n_perto": holdout["n_perto_confirmacao"],
        "efeito_pp": holdout["H1_confirmacao"]["efeito_pp"],
        "ic95": holdout["H1_confirmacao"]["ic_95_bootstrap_cluster"],
        "mesma_direcao": holdout["H1_confirmacao"]["mesma_direcao"],
    },

    "improve": {
        "n_funcionarios_longe_com_evento_administravel": improve["n_funcionarios_longe_com_evento_B2"],
        "n_eventos_administravel_longe": improve["n_eventos_B2_longe"],
        "horas_mediana_administravel_longe": improve["horas_mediana_B2_longe"],
        "cenarios": improve["cenarios_ganho"],
        "custo_rh_assumido_horas_mes": improve["ponto_de_indiferenca"]["custo_rh_assumido_horas_por_mes_PREMISSA"],
        "fracao_indiferenca": improve["ponto_de_indiferenca"]["fracao_de_adesao_para_empatar"],
        "n_necessario_experimento": improve["experimento"]["n_por_grupo_necessario_poder_80pct_alpha_0125"],
        "n_disponivel_experimento": improve["experimento"]["n_rotas_longas_disponiveis_aprox"],
        "razao_necessario_disponivel": improve["experimento"]["razao_necessario_vs_disponivel"],
    },
}

with open(OUT_DIR / "dados_pagina.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2, default=str)

print(f"n linhas cubo: {len(cubo_rows)}")
print(f"n funcionarios: {len(funcionarios)}")
print("Gravado em", OUT_DIR / "dados_pagina.json")
