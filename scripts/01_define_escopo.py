"""Fase 1 - Define: contagens estruturais para o charter (D1, D3).

Regra 2 do contexto mestre / F9 da metodo-dmaic: nesta fase ainda nao se testa
relacao entre variaveis explicativas. O que segue e reagrupamento de UMA
coluna categorica (Reason for absence) em categorias mais grossas, e a
aplicacao dos criterios de exclusao decididos no relatorio - nao e teste de
hipotese nem cruzamento com outra variavel.
"""
import json
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw" / "Absenteeism_at_work.csv"
OUT_DIR = Path(__file__).resolve().parents[1] / "fases" / "fase-1-define" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(RAW, sep=";")
df.columns = [c.strip() for c in df.columns]

n_bruto = len(df)

# Criterios de exclusao decididos no Define
excl_administrativo = df[(df["Month of absence"] == 0) & (df["Absenteeism time in hours"] == 0)]
excl_id29 = df[(df["ID"] == 29) & (df["Age"] == 28)]

excluidos_idx = set(excl_administrativo.index) | set(excl_id29.index)
df_limpo = df.drop(index=excluidos_idx)

n_limpo = len(df_limpo)
n_ids = df_limpo["ID"].nunique()

def classifica(reason):
    if reason in (0, 26):
        return "B1_comportamental"
    if reason in (22, 23, 24, 25, 27, 28):
        return "B2_administravel"
    if 1 <= reason <= 21:
        return "CID"
    return "OUTRO"

df_limpo = df_limpo.copy()
df_limpo["categoria_defeito"] = df_limpo["Reason for absence"].apply(classifica)

contagem = df_limpo["categoria_defeito"].value_counts().to_dict()
proporcoes = (df_limpo["categoria_defeito"].value_counts(normalize=True) * 100).round(2).to_dict()

horas_por_categoria = df_limpo.groupby("categoria_defeito")["Absenteeism time in hours"].describe().to_dict()

# distribuicao de eventos por funcionario, apos limpeza (para citar a rival estrutural)
eventos_por_funcionario = df_limpo.groupby("ID").size().describe().to_dict()
top3_funcionarios = df_limpo.groupby("ID").size().sort_values(ascending=False).head(3).to_dict()

# NAO calcular aqui a concentracao por ID do subconjunto reason=0 (H3 do
# pre-registro): esse numero E o teste de H3. Computa-lo no Define, antes do
# pre-registro estar congelado, seria o proprio garimpo que a regra 3 do
# contexto mestre proibe. Fica só a contagem bruta (permitida - e a mesma
# natureza da contagem de "Reason for absence" ja feita na Fase 0).
b1_reason0_n = int((df_limpo["Reason for absence"] == 0).sum())

resumo = {
    "n_bruto": n_bruto,
    "excluidos": {
        "administrativos_month0_hours0": excl_administrativo[["ID", "Reason for absence", "Month of absence", "Disciplinary failure", "Absenteeism time in hours"]].to_dict(orient="records"),
        "id29_linha_minoritaria": excl_id29[["ID", "Reason for absence", "Age", "Height", "Weight", "Disciplinary failure", "Absenteeism time in hours"]].to_dict(orient="records"),
        "total_excluido": len(excluidos_idx),
    },
    "n_limpo": n_limpo,
    "n_identidades_funcionario": int(n_ids),
    "contagem_por_categoria": contagem,
    "proporcao_por_categoria_pct": proporcoes,
    "horas_describe_por_categoria": horas_por_categoria,
    "eventos_por_funcionario_describe": eventos_por_funcionario,
    "top3_funcionarios_mais_eventos": top3_funcionarios,
    "b1_reason0_n_apos_exclusao": b1_reason0_n,
}

with open(OUT_DIR / "escopo_define.json", "w", encoding="utf-8") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=2, default=str)

# grava tambem a base limpa (pos-exclusoes) para uso nas fases seguintes -
# ainda NAO e o holdout, e ainda NAO inclui relacoes entre variaveis
df_limpo.to_csv(Path(__file__).resolve().parents[1] / "data" / "processed" / "eventos_limpos.csv", index=False)

print(json.dumps(resumo, ensure_ascii=False, indent=2, default=str))
