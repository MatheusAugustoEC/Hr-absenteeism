"""Fase 2B - graficos do baseline: proporcao com IC, os dois Paretos, e a
tabela por mes rotulada como NAO TEMPORAL diretamente na legenda.
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]
OUT_DIR = BASE / "fases" / "fase-2b-measure-baseline" / "artefatos"
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"

with open(OUT_DIR / "baseline.json", encoding="utf-8") as f:
    report = json.load(f)

COR_B1 = "#c0392b"
COR_B2 = "#2b6cb0"
COR_CID = "#5a8f5a"
COR_NEUTRA = "#555555"

plt.rcParams.update({"font.size": 10.5, "axes.edgecolor": "#888888"})

# ---------------------------------------------------- 1. Proporcao com IC
fig, ax = plt.subplots(figsize=(7, 4))
nomes = ["B_total", "B1", "B2"]
labels = ["Defeito B (total)", "B1 comportamental", "B2 administrável"]
props = [report["baseline_proporcoes"][n]["proporcao"] for n in nomes]
ci_lo = [report["baseline_proporcoes"][n]["bootstrap_cluster_ic95_34_funcionarios"][0] for n in nomes]
ci_hi = [report["baseline_proporcoes"][n]["bootstrap_cluster_ic95_34_funcionarios"][1] for n in nomes]
err_lo = [p - lo for p, lo in zip(props, ci_lo)]
err_hi = [hi - p for p, hi in zip(props, ci_hi)]
cores = [COR_NEUTRA, COR_B1, COR_B2]

y = np.arange(len(nomes))
ax.barh(y, props, xerr=[err_lo, err_hi], color=cores, capsize=6, height=0.5)
for i, (p, hi) in enumerate(zip(props, ci_hi)):
    ax.text(hi + 0.03, i, f"{p*100:.1f}%", va="center", fontsize=10)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.set_xlabel("Proporção de eventos (IC 95% por bootstrap de 34 funcionários)")
ax.set_xlim(0, 1)
ax.set_title("Baseline — proporção de eventos por categoria de defeito\n(n=733 eventos, IC agrupado por funcionário, não por evento)")
plt.tight_layout()
fig.savefig(OUT_DIR / "baseline_proporcoes.png", dpi=200)
plt.close(fig)

# ---------------------------------------------------- 2. Pareto de taxa
pareto_taxa = report["pareto"]["pareto_taxa_pct_por_codigo"]
labels_reason = {
    "0": "0 - disciplinar", "22": "22 - acompanh.", "23": "23 - consulta méd.",
    "24": "24 - doação sangue", "25": "25 - exame lab.", "26": "26 - injustificada",
    "27": "27 - fisioterapia", "28": "28 - consulta odont.",
}
codigos_ordenados = sorted(pareto_taxa.items(), key=lambda kv: -kv[1])
codigos = [k for k, v in codigos_ordenados]
valores = [v for k, v in codigos_ordenados]
acumulado = np.cumsum(valores)
cores_b = [COR_B1 if int(c) in (0, 26) else COR_B2 for c in codigos]

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar([labels_reason[c] for c in codigos], valores, color=cores_b)
ax1.set_ylabel("% dos eventos do defeito B")
ax1.set_ylim(0, max(valores) * 1.25)
for i, v in enumerate(valores):
    ax1.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(range(len(codigos)), acumulado, color="black", marker="o", linewidth=1.5)
ax2.set_ylabel("% acumulado")
ax2.set_ylim(0, 105)
ax1.set_xticklabels([labels_reason[c] for c in codigos], rotation=30, ha="right")
ax1.set_title("Pareto de TAXA — eventos do defeito B por código de motivo\n(vermelho = B1 comportamental, azul = B2 administrável)")
plt.tight_layout()
fig.savefig(OUT_DIR / "pareto_taxa.png", dpi=200)
plt.close(fig)

# ---------------------------------------------- 3. Pareto de impacto em horas
pareto_horas = report["pareto"]["pareto_impacto_horas_pct_por_codigo_B2_apenas"]
codigos_h_ordenados = sorted(pareto_horas.items(), key=lambda kv: -kv[1])
codigos_h = [k for k, v in codigos_h_ordenados]
valores_h = [v for k, v in codigos_h_ordenados]
acumulado_h = np.cumsum(valores_h)

fig, ax1 = plt.subplots(figsize=(8, 4.5))
ax1.bar([labels_reason[c] for c in codigos_h], valores_h, color=COR_B2)
ax1.set_ylabel("% das horas de ausência do B2")
ax1.set_ylim(0, max(valores_h) * 1.25)
for i, v in enumerate(valores_h):
    ax1.text(i, v + 1, f"{v:.1f}%", ha="center", fontsize=9)
ax2 = ax1.twinx()
ax2.plot(range(len(codigos_h)), acumulado_h, color="black", marker="o", linewidth=1.5)
ax2.set_ylabel("% acumulado")
ax2.set_ylim(0, 105)
ax1.set_xticklabels([labels_reason[c] for c in codigos_h], rotation=30, ha="right")
ax1.set_title(
    "Pareto de IMPACTO EM HORAS — só B2 administrável\n"
    "B1 (códigos 0 e 26) NÃO aparece aqui: 100% dos eventos B1 têm 0h registradas.\n"
    "Para B1, a régua é o Pareto de taxa (contagem de eventos), não horas."
)
plt.tight_layout()
fig.savefig(OUT_DIR / "pareto_impacto_horas.png", dpi=200)
plt.close(fig)

# ------------------------------------ 4. Tabela nao-temporal por mes (grafico)
por_mes = pd.DataFrame(report["tabela_nao_temporal_por_mes"])
fig, ax = plt.subplots(figsize=(8, 4))
ax.bar(por_mes["Month of absence"].astype(str), por_mes["proporcao_B"] * 100, color=COR_NEUTRA)
for i, row in por_mes.iterrows():
    ax.text(i, row["proporcao_B"] * 100 + 1, f'{row["proporcao_B"]*100:.0f}%', ha="center", fontsize=8)
ax.axhline(report["baseline_proporcoes"]["B_total"]["proporcao"] * 100, color=COR_B1, linestyle="--", linewidth=1, label="Baseline agregado (64,3%)")
ax.set_xlabel("Rótulo de 'Month of absence' (0-12)")
ax.set_ylabel("% de eventos do defeito B")
ax.set_ylim(0, 100)
ax.legend(loc="lower right", fontsize=8)
ax.set_title(
    "AVISO: NÃO É UMA SÉRIE TEMPORAL — os 12 rótulos de mês misturam 3 anos\n"
    "calendário sem coluna de ano. Não interpretar como tendência ou sazonalidade real."
)
plt.tight_layout()
fig.savefig(OUT_DIR / "tabela_nao_temporal_por_mes.png", dpi=200)
plt.close(fig)

print("Graficos gerados em", OUT_DIR)
