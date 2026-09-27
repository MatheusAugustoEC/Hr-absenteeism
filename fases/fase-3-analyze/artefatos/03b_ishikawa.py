"""Fase 3 - diagrama de Ishikawa adaptado (espinha de peixe), com testabilidade
marcada no proprio desenho: linha solida = testavel com esta base; linha
tracejada + rotulo "NAO TESTAVEL" = nao testavel.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

OUT_DIR = Path(__file__).resolve().parents[1] / "fases" / "fase-3-analyze" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COR_TESTAVEL = "#2b6cb0"
COR_NAO_TESTAVEL = "#a0a0a0"
COR_TEXTO = "#1a1a1a"

categorias = [
    {
        "nome": "AGENDAMENTO / ADMINISTRAÇÃO (gera B2)",
        "x_base": 2.5, "y_cat": 6.3, "lado": "cima",
        "causas": [
            ("Distância residência-trabalho\n(H1 - testada)", True),
            ("Falta de agendamento\nfora do expediente", False),
        ],
    },
    {
        "nome": "PROCESSO DE REGISTRO DISCIPLINAR (gera B1)",
        "x_base": 8.0, "y_cat": 6.3, "lado": "cima",
        "causas": [
            ("Código reservado (reason=0)\ncomo atalho administrativo\n(H3 - testada)", True),
            ("Quem cobriu o turno /\ncusto da cobertura", False),
        ],
    },
    {
        "nome": "CARGA DE PERÍODO COMPARTILHADA",
        "x_base": 2.5, "y_cat": -6.3, "lado": "baixo",
        "causas": [
            ("Work load Average/day,\nHit target (nível-mês,\nnão é causa individual)", False),
        ],
    },
    {
        "nome": "CARACTERÍSTICAS FIXAS DO FUNCIONÁRIO",
        "x_base": 8.0, "y_cat": -6.3, "lado": "baixo",
        "causas": [
            ("Dia da semana\n(H4 - testada)", True),
            ("Weight/Height/BMI como\nperfil de risco -\nPROIBIDO pelo guardrail", False),
        ],
    },
]

fig, ax = plt.subplots(figsize=(15, 11))
ax.set_xlim(0, 16)
ax.set_ylim(-8, 8)
ax.axis("off")

# espinha principal
ax.annotate("", xy=(14.5, 0), xytext=(1, 0),
            arrowprops=dict(arrowstyle="-|>", linewidth=2.5, color="#222222"))
ax.text(14.9, 0, "Defeito B\n(evento sem\nlastro médico)", fontsize=12, fontweight="bold",
        va="center", ha="left", color=COR_TEXTO)

for cat in categorias:
    x_base = cat["x_base"]
    y_cat = cat["y_cat"]
    sinal = 1 if cat["lado"] == "cima" else -1
    y_ponta = 0.15 * sinal
    x_ponta = x_base + 3.3
    # tronco da categoria (linha grossa ate a espinha)
    ax.plot([x_base, x_ponta], [y_cat * 0.55, y_ponta], color="#444444", linewidth=2.2)
    ax.text(x_base, y_cat, cat["nome"], fontsize=11.5, fontweight="bold",
            ha="center", va="center", color=COR_TEXTO,
            bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="none"))
    # causas: pequenas setas que chegam no tronco, com texto afastado do tronco
    n = len(cat["causas"])
    for i, (texto, testavel) in enumerate(cat["causas"]):
        frac = 0.25 + 0.5 * (i / max(n - 1, 1)) if n > 1 else 0.5
        xc = x_base + frac * (x_ponta - x_base)
        yc = (y_cat * 0.55) + frac * (y_ponta - y_cat * 0.55)
        cor = COR_TESTAVEL if testavel else COR_NAO_TESTAVEL
        estilo = "-" if testavel else (0, (3, 3))
        dx, dy = -1.3, 1.35 * sinal
        line = ax.plot([xc, xc + dx], [yc, yc + dy], color=cor, linewidth=1.6)[0]
        line.set_linestyle(estilo)
        rotulo = texto + ("" if testavel else "\n[NÃO TESTÁVEL]")
        ax.text(xc + dx, yc + dy * 1.25, rotulo, fontsize=8.8, ha="center",
                va="center", color=cor, fontweight=("bold" if testavel else "normal"))

ax.text(8, 7.6, "Ishikawa adaptado — causas candidatas da ausência sem lastro médico (Fase 3)",
        ha="center", fontsize=14.5, fontweight="bold", color=COR_TEXTO)

legend_elements = [
    Line2D([0], [0], color=COR_TESTAVEL, lw=2, label="Testável com esta base (testada nesta fase)"),
    Line2D([0], [0], color=COR_NAO_TESTAVEL, lw=2, linestyle=(0, (3, 3)), label="Não testável com esta base"),
]
ax.legend(handles=legend_elements, loc="lower center", bbox_to_anchor=(0.5, -0.02), ncol=2, fontsize=10, frameon=False)

plt.tight_layout()
fig.savefig(OUT_DIR / "diagrama-causal.svg", format="svg", bbox_inches="tight")
fig.savefig(OUT_DIR / "diagrama-causal.png", format="png", dpi=200, bbox_inches="tight")
print("Gerado diagrama-causal.svg e .png em", OUT_DIR)
