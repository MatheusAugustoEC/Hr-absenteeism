"""Gera o diagrama do SIPOC reverso (Fase 0, secao 1 do relatorio) como
sipoc.svg e sipoc.png. As etapas EVIDENTE NO DADO e INFERENCIA sao
visualmente distintas no proprio desenho (cor de preenchimento e borda),
nao so na legenda da tabela.
"""
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

OUT_DIR = Path(__file__).resolve().parents[1] / "fases" / "fase-0-reconhecimento" / "artefatos"
OUT_DIR.mkdir(parents=True, exist_ok=True)

COR_EVIDENTE = "#2b6cb0"   # azul - evidente no dado
COR_INFERENCIA = "#a0a0a0"  # cinza - inferencia
COR_TEXTO = "#1a1a1a"

etapas = [
    {
        "titulo": "FORNECEDOR",
        "texto": "Funcionário (gera o\nevento de ausência) e\nárea médica/admin.\nda transportadora",
        "evidencia": "INFERÊNCIA",
    },
    {
        "titulo": "ENTRADA",
        "texto": "Comparecimento\nesperado ao trabalho\nnum turno programado",
        "evidencia": "INFERÊNCIA",
    },
    {
        "titulo": "PROCESSO",
        "texto": "Ausência ocorre →\nclassificada por motivo\n(CID/administrativo) →\nregistrada (mês, dia,\nestação, horas,\nfalta disciplinar)",
        "evidencia": "EVIDENTE NO DADO",
    },
    {
        "titulo": "SAÍDA",
        "texto": "Registro de ausência\ncom motivo, duração e\nenquadramento\ndisciplinar",
        "evidencia": "EVIDENTE NO DADO",
    },
    {
        "titulo": "CLIENTE",
        "texto": "Gestão de RH/operações\nda transportadora\n(cobre o turno, decide\npenalidade)",
        "evidencia": "INFERÊNCIA",
    },
]

fig, ax = plt.subplots(figsize=(14, 5.2))
ax.set_xlim(0, 14)
ax.set_ylim(0, 5.2)
ax.axis("off")

box_w, box_h = 2.3, 2.6
y0 = 1.6
xs = [0.4 + i * 2.75 for i in range(5)]

for etapa, x in zip(etapas, xs):
    cor = COR_EVIDENTE if etapa["evidencia"] == "EVIDENTE NO DADO" else COR_INFERENCIA
    estilo_borda = "-" if etapa["evidencia"] == "EVIDENTE NO DADO" else (0, (4, 3))
    box = FancyBboxPatch(
        (x, y0), box_w, box_h,
        boxstyle="round,pad=0.08,rounding_size=0.12",
        linewidth=2.4,
        edgecolor=cor,
        facecolor=(cor if etapa["evidencia"] == "EVIDENTE NO DADO" else "white"),
        alpha=1.0 if etapa["evidencia"] == "EVIDENTE NO DADO" else 1.0,
    )
    box.set_linestyle(estilo_borda)
    if etapa["evidencia"] == "EVIDENTE NO DADO":
        box.set_facecolor(cor)
        box.set_alpha(0.18)
    ax.add_patch(box)

    ax.text(x + box_w / 2, y0 + box_h - 0.32, etapa["titulo"],
            ha="center", va="top", fontsize=12, fontweight="bold", color=COR_TEXTO)
    ax.text(x + box_w / 2, y0 + box_h / 2 - 0.15, etapa["texto"],
            ha="center", va="center", fontsize=8.8, color=COR_TEXTO)
    ax.text(x + box_w / 2, y0 - 0.22, etapa["evidencia"],
            ha="center", va="top", fontsize=8, fontweight="bold",
            color=cor if etapa["evidencia"] == "EVIDENTE NO DADO" else "#555555")

for x in xs[:-1]:
    arrow = FancyArrowPatch(
        (x + box_w + 0.05, y0 + box_h / 2), (x + 2.75 - 0.05, y0 + box_h / 2),
        arrowstyle="-|>", mutation_scale=18, linewidth=2, color="#333333",
    )
    ax.add_patch(arrow)

ax.text(7, 4.85, "SIPOC reverso — Absenteísmo no Trabalho (Fase 0)",
        ha="center", va="top", fontsize=13.5, fontweight="bold", color=COR_TEXTO)

# legenda
leg_y = 0.75
ax.add_patch(FancyBboxPatch((0.4, leg_y), 0.35, 0.28, boxstyle="round,pad=0.02",
                             facecolor=COR_EVIDENTE, alpha=0.18, edgecolor=COR_EVIDENTE, linewidth=2))
ax.text(0.85, leg_y + 0.14, "Evidente no dado", fontsize=9, va="center", color=COR_TEXTO)
leg2 = FancyBboxPatch((3.6, leg_y), 0.35, 0.28, boxstyle="round,pad=0.02",
                       facecolor="white", edgecolor=COR_INFERENCIA, linewidth=2)
leg2.set_linestyle((0, (4, 3)))
ax.add_patch(leg2)
ax.text(4.05, leg_y + 0.14, "Inferência (não registrada explicitamente)", fontsize=9, va="center", color=COR_TEXTO)

plt.tight_layout()
fig.savefig(OUT_DIR / "sipoc.svg", format="svg", bbox_inches="tight")
fig.savefig(OUT_DIR / "sipoc.png", format="png", dpi=200, bbox_inches="tight")
print(f"Gerado: {OUT_DIR / 'sipoc.svg'}")
print(f"Gerado: {OUT_DIR / 'sipoc.png'}")
