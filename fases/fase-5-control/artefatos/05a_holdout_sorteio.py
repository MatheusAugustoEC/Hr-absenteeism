"""Fase 5 - Control: SORTEIO do holdout. Executado uma unica vez.

Regra do contexto mestre / C5: o holdout e aberto uma unica vez, e o
resultado e registrado qualquer que seja. Este script SO faz o sorteio das
34 identidades em exploracao (75%) e confirmacao (25%) com semente fixa - ele
NAO calcula nenhum efeito, nenhuma proporcao, nenhum teste. Isso e proposital:
separa o momento do sorteio (que fixa quem esta em cada grupo) do momento da
analise (script 05b), para que a semente e a composicao dos grupos fiquem
registradas ANTES de qualquer numero de confirmacao ser visto.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import SEMENTE_HOLDOUT, PROPORCAO_EXPLORACAO

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"
HOLDOUT_DIR = BASE / "data" / "holdout"
HOLDOUT_DIR.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(QUALIDADE)
ids = np.sort(df["ID"].unique())
n = len(ids)

rng = np.random.default_rng(SEMENTE_HOLDOUT)
ids_embaralhados = rng.permutation(ids)
n_exploracao = round(n * PROPORCAO_EXPLORACAO)

ids_exploracao = sorted(ids_embaralhados[:n_exploracao].tolist())
ids_confirmacao = sorted(ids_embaralhados[n_exploracao:].tolist())

resultado = {
    "semente": SEMENTE_HOLDOUT,
    "n_total_identidades": int(n),
    "proporcao_exploracao": PROPORCAO_EXPLORACAO,
    "n_exploracao": len(ids_exploracao),
    "n_confirmacao": len(ids_confirmacao),
    "ids_exploracao": [int(i) for i in ids_exploracao],
    "ids_confirmacao": [int(i) for i in ids_confirmacao],
}

with open(HOLDOUT_DIR / "split_ids.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, ensure_ascii=False, indent=2)

print(f"Sorteio realizado com semente {SEMENTE_HOLDOUT}.")
print(f"Exploracao: {len(ids_exploracao)} identidades -> {ids_exploracao}")
print(f"Confirmacao: {len(ids_confirmacao)} identidades -> {ids_confirmacao}")
print("Gravado em data/holdout/split_ids.json. Nenhum efeito foi calculado ainda.")
