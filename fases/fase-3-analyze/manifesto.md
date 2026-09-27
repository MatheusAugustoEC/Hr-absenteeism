# Manifesto — Fase 3 · Analyze

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| relatorio.md | relatório desta fase (Ishikawa, H2, H1, H3, H4, quantificação) | escrito nesta fase | Improve |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/03_analyze.py | script que testa H2, H1, H3 e H4 | escrito nesta fase | fase 3 |
| scripts/03b_ishikawa.py | script que desenha o diagrama causal | escrito nesta fase | fase 3 (seção 1 do relatório) |
| scripts/03c_graficos_analyze.py | script que gera os gráficos de robustez de H1 e efeito de H4 | escrito nesta fase | fase 3 |
| artefatos/03_analyze.py, 03b_ishikawa.py, 03c_graficos_analyze.py | cópias congeladas dos scripts | scripts/ | prova de reprodutibilidade |
| artefatos/analyze.json | todos os números dos testes de H1-H4 | scripts/03_analyze.py | este relatório |
| artefatos/diagrama-causal.svg / .png | Ishikawa adaptado, com testabilidade marcada no desenho | scripts/03b_ishikawa.py | seção 1 do relatório |
| artefatos/h1_efeito_ic.png | efeito de H1 com IC | scripts/03c_graficos_analyze.py | seção 3 do relatório |
| artefatos/h2_robustez_h1.png | robustez do efeito de H1 (exclusões e ponderação) | scripts/03c_graficos_analyze.py | seção 2 do relatório |
| artefatos/h4_efeito_ic.png | efeito de H4 com IC | scripts/03c_graficos_analyze.py | seção 5 do relatório |

## Dados de entrada (não copiados — arquivo já existente, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_qualidade.csv | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

## Holdout

Não tocado nesta fase (A17) — todos os testes rodaram sobre a janela de
exploração inteira (733 eventos, 34 identidades). Continua fechado até a fase
Control.
