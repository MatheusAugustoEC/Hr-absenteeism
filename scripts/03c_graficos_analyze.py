"""Fase 3 - graficos de apoio: robustez de H1 (H2) e efeito de H4 com IC."""
import json
from pathlib import Path

import matplotlib.pyplot as plt

BASE = Path(__file__).resolve().parents[1]
OUT_DIR = BASE / "fases" / "fase-3-analyze" / "artefatos"

with open(OUT_DIR / "analyze.json", encoding="utf-8") as f:
    r = json.load(f)

COR_OK = "#2b6cb0"
COR_LIMIAR = "#c0392b"

# ---------------------------------------------- H2: robustez do efeito de H1
fig, ax = plt.subplots(figsize=(8, 4.5))
labels = ["Bruto\n(todos os eventos)", "Ponderado por\nfuncionário"] + [
    f"Excluindo ID {k}\n(ponderado)" for k in r["H2a_exclusao_top3"]
]
valores = [r["H2b_bruto_vs_ponderado"]["efeito_bruto_pp"], r["H2b_bruto_vs_ponderado"]["efeito_ponderado_por_funcionario_pp"]]
valores += [v["efeito_ponderado_pp"] for v in r["H2a_exclusao_top3"].values()]
cores = [COR_OK] * len(valores)
ax.bar(labels, valores, color=cores)
ax.axhline(10, color=COR_LIMIAR, linestyle="--", linewidth=1.5, label="Efeito mínimo pré-registrado (10 p.p.)")
for i, v in enumerate(valores):
    ax.text(i, v + 0.5, f"{v:.1f}", ha="center", fontsize=9)
ax.set_ylabel("Efeito de H1 (p.p.)")
ax.set_title("H2 — robustez do efeito de H1 à composição de mix\n(nenhuma versão cai abaixo do efeito mínimo pré-registrado)")
ax.legend(fontsize=8.5)
plt.xticks(rotation=15, ha="right", fontsize=8.5)
plt.tight_layout()
fig.savefig(OUT_DIR / "h2_robustez_h1.png", dpi=200)
plt.close(fig)

# ---------------------------------------------- H1: efeito com IC
fig, ax = plt.subplots(figsize=(6.5, 3.5))
efeito = r["H1_teste"]["efeito_observado_pp"]
ci_lo, ci_hi = r["H1_teste"]["ic_98_75_bootstrap_cluster"]
ax.errorbar([0], [efeito], yerr=[[efeito - ci_lo], [ci_hi - efeito]], fmt="o", color=COR_OK,
            capsize=8, markersize=10, linewidth=2)
ax.axhline(10, color=COR_LIMIAR, linestyle="--", linewidth=1.5, label="Efeito mínimo pré-registrado (10 p.p.)")
ax.axhline(0, color="#888888", linewidth=1)
ax.set_xlim(-1, 1)
ax.set_xticks([])
ax.set_ylabel("Efeito de H1 (p.p.)")
ax.set_title(
    f"H1 — efeito observado {efeito:.1f} p.p., IC 98,75% [{ci_lo:.1f}; {ci_hi:.1f}]\n"
    f"p={r['H1_teste']['p_valor_permutacao_por_funcionario']:.4f} (α={r['H1_teste']['alpha']}) — "
    "NÃO significativo no α, mas efeito grande: inconclusivo, não nulo"
)
ax.legend(fontsize=8)
plt.tight_layout()
fig.savefig(OUT_DIR / "h1_efeito_ic.png", dpi=200)
plt.close(fig)

# ---------------------------------------------- H4: efeito com IC
fig, ax = plt.subplots(figsize=(6.5, 3.5))
efeito4 = r["H4_teste"]["efeito_medio_pp_por_funcionario"]
ci4_lo, ci4_hi = r["H4_teste"]["ic_98_75_bootstrap"]
ax.errorbar([0], [efeito4], yerr=[[efeito4 - ci4_lo], [ci4_hi - efeito4]], fmt="o", color="#888888",
            capsize=8, markersize=10, linewidth=2)
ax.axhline(8, color=COR_LIMIAR, linestyle="--", linewidth=1.5, label="Efeito mínimo pré-registrado (8 p.p.)")
ax.axhline(0, color="#888888", linewidth=1)
ax.set_xlim(-1, 1)
ax.set_xticks([])
ax.set_ylabel("Efeito de H4 (p.p.)")
ax.set_title(
    f"H4 — efeito observado {efeito4:.1f} p.p., IC 98,75% [{ci4_lo:.1f}; {ci4_hi:.1f}]\n"
    f"p={r['H4_teste']['p_valor_permutacao_sinal']:.4f} — efeito pequeno, CI cruza zero"
)
ax.legend(fontsize=8)
plt.tight_layout()
fig.savefig(OUT_DIR / "h4_efeito_ic.png", dpi=200)
plt.close(fig)

print("Graficos do Analyze gerados em", OUT_DIR)
