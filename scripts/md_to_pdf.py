"""Converte um relatorio.md em relatorio.pdf, preservando UTF-8, tabelas e
codigo. Uso: python scripts/md_to_pdf.py <entrada.md> [<saida.pdf>]
"""
import sys
from pathlib import Path

import markdown
from xhtml2pdf import pisa

_FONT_DIR = Path(__file__).resolve().parent / "fonts"
_REGULAR = (_FONT_DIR / "DejaVuSans.ttf").as_posix()
_BOLD = (_FONT_DIR / "DejaVuSans-Bold.ttf").as_posix()
_ITALIC = (_FONT_DIR / "DejaVuSans-Oblique.ttf").as_posix()
_MONO = (_FONT_DIR / "DejaVuSansMono.ttf").as_posix()

CSS = f"""
@font-face {{ font-family: "DejaVu"; src: url("{_REGULAR}"); }}
@font-face {{ font-family: "DejaVu"; font-weight: bold; src: url("{_BOLD}"); }}
@font-face {{ font-family: "DejaVu"; font-style: italic; src: url("{_ITALIC}"); }}
@font-face {{ font-family: "DejaVuMono"; src: url("{_MONO}"); }}
@page {{ size: A4; margin: 2cm; }}
body {{ font-family: "DejaVu"; font-size: 10.5pt; line-height: 1.4; color: #1a1a1a; }}
h1 {{ font-size: 18pt; border-bottom: 2px solid #333; padding-bottom: 4px; }}
h2 {{ font-size: 14pt; margin-top: 18px; color: #222; }}
h3 {{ font-size: 12pt; margin-top: 14px; color: #333; }}
table {{ width: 100%; margin: 8px 0; font-size: 9pt; }}
th, td {{ border: 1px solid #999; padding: 4px 6px; text-align: left; }}
th {{ background-color: #e8e8e8; }}
code {{ background-color: #f0f0f0; padding: 1px 3px; font-family: "DejaVuMono"; }}
pre {{ background-color: #f0f0f0; padding: 6px; font-family: "DejaVuMono"; font-size: 8.5pt; }}
"""


def convert(md_path: Path, pdf_path: Path) -> None:
    text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(text, extensions=["tables", "fenced_code"])
    html = f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{html_body}</body></html>"
    with open(pdf_path, "wb") as f:
        result = pisa.CreatePDF(src=html, dest=f, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"Falha ao gerar PDF: {result.err}")


if __name__ == "__main__":
    md_path = Path(sys.argv[1])
    pdf_path = Path(sys.argv[2]) if len(sys.argv) > 2 else md_path.with_suffix(".pdf")
    convert(md_path, pdf_path)
    print(f"PDF gerado em {pdf_path}")
