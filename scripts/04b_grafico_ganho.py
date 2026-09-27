"""Fase 4 - grafico dos tres cenarios de adesao e o ponto de indiferenca."""
import json
from pathlib import Path

import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
OUT_DIR = BASE / "fases" / "fase-4-improve" / "artefatos"

with open(OUT_DIR / "improve.json", encoding="utf-8") as f:
    r = json.load(f)

COR_CENARIO = "#2b6cb0"
COR_INDIFERENCA = "#c0392b"

fracao_indif = r["ponto_de_indiferenca"]["fracao_de_adesao_para_empatar"]
custo_mes = r["ponto_de_indiferenca"]["custo_rh_assumido_horas_por_mes_PREMISSA"]

fig, ax = plt.subplots(figsize=(8, 4.5))
adesoes = [0.20, 0.50, 0.80]
labels = [f"{int(a*100)}% adesão" for a in adesoes]
horas = [r["cenarios_ganho"][f"adesao_{int(a*100)}pct"]["horas_evitadas_por_mes"] for a in adesoes]
cores = [COR_CENARIO if h_ >= custo_mes else "#a0a0a0" for h_ in horas]

ax.bar(labels, horas, color=cores)
for i, h_ in enumerate(horas):
    ax.text(i, h_ + 0.3, f"{h_:.1f}h/mês", ha="center", fontsize=9.5)
ax.axhline(custo_mes, color=COR_INDIFERENCA, linestyle="--", linewidth=1.8,
           label=f"Custo de RH assumido (premissa): {custo_mes:.0f}h/mês")
ax.set_ylabel("Horas de ausência B2 evitadas por mês\n(funcionários com distância acima da mediana)")
ax.set_title(
    f"Simulação de ganho — política de agendamento (H1, piloto proposto)\n"
    f"Ponto de indiferença: {fracao_indif*100:.1f}% de adesão para empatar com o custo assumido de RH"
)
ax.legend(fontsize=8.5, loc="upper left")
plt.tight_layout()
fig.savefig(OUT_DIR / "simulacao_ganho.png", dpi=200)
plt.close(fig)
print("Gerado simulacao_ganho.png em", OUT_DIR)
