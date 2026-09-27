# Manifesto — Fase 2A · Measure — Procedência e qualidade

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| relatorio.md | relatório desta fase (auditoria das seis dimensões, resolução de duplicatas) | escrito nesta fase | Measure 2B |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/02a_measure_qualidade.py | script de auditoria e resolução de duplicatas | escrito nesta fase | fase 2A (este relatório) |
| artefatos/02a_measure_qualidade.py | cópia congelada do script | scripts/02a_measure_qualidade.py | prova de reprodutibilidade |
| artefatos/auditoria_qualidade.json | resultado completo da auditoria das seis dimensões e veredito por grupo duplicado | scripts/02a_measure_qualidade.py | este relatório |
| data/processed/eventos_qualidade.csv | base final pós-qualidade (733 linhas, 34 identidades) — usada a partir daqui | scripts/02a_measure_qualidade.py | Measure 2B, Analyze (janela de exploração) |

## Dados de entrada (não copiados — arquivos já existentes, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_limpos.csv (entrada desta fase, saída do Define) | 1db18345ba89ac3375919011f796cb4a4dd3f99617ff9eb5d07cc474656462c8 |
| data/processed/eventos_qualidade.csv (saída desta fase) | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

## Holdout

Não tocado nesta fase. Continua fechado até a fase Control.
