# Manifesto — Fase 2B · Measure — Baseline, estabilidade e capabilidade

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| baseline-congelado.md | baseline versionado — **IMUTÁVEL a partir do commit desta fase**; correção futura é adendo datado ao final | escrito nesta fase | Analyze, Improve, Control (verificação de ganho) |
| baseline-congelado.pdf | PDF do baseline congelado | scripts/md_to_pdf.py | leitura e arquivo |
| relatorio.md | relatório desta fase (baseline, estabilidade, capabilidade, Paretos, poder) | escrito nesta fase | Analyze |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/02b_measure_baseline.py | script que calcula baseline, IC por bootstrap de cluster, DPMO/sigma, capabilidade, Paretos e poder | escrito nesta fase | fase 2B |
| scripts/02b_graficos.py | script que gera as figuras do baseline | escrito nesta fase | fase 2B |
| artefatos/02b_measure_baseline.py | cópia congelada do script de cálculo | scripts/02b_measure_baseline.py | prova de reprodutibilidade |
| artefatos/02b_graficos.py | cópia congelada do script de gráficos | scripts/02b_graficos.py | prova de reprodutibilidade |
| artefatos/baseline.json | todos os números desta fase | scripts/02b_measure_baseline.py | este relatório, baseline-congelado.md |
| artefatos/baseline_proporcoes.png | gráfico de proporção com IC | scripts/02b_graficos.py | este relatório |
| artefatos/pareto_taxa.png | Pareto de taxa por código de motivo | scripts/02b_graficos.py | este relatório |
| artefatos/pareto_impacto_horas.png | Pareto de impacto em horas (só B2) | scripts/02b_graficos.py | este relatório |
| artefatos/tabela_nao_temporal_por_mes.png | tabela descritiva por mês, com aviso de não-temporalidade na legenda | scripts/02b_graficos.py | este relatório |

## Dados de entrada (não copiados — arquivo já existente, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_qualidade.csv | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

## Hash do baseline congelado no momento em que se tornou imutável

| Arquivo | Hash SHA-256 (26/09/2026) |
|---|---|
| fases/fase-2b-measure-baseline/baseline-congelado.md | 1e84638fa4b03357b44bc13511105bf1ef640826bc76faae60e17d02face5659 |

## Correção registrada nesta fase (não é adendo a artefato imutável)

`fases/fase-1-define/relatorio.md` (arquivo comum, não imutável) tinha um erro
de digitação na soma da proporção preliminar de B1+B2 ("54,4%" em vez de
"64,4%"). Corrigido diretamente no texto, com nota de correção datada dentro
do próprio parágrafo — não é o pré-registro nem o baseline, então não exige o
protocolo de adendo dos artefatos de prova.

## Holdout

Não tocado nesta fase. Continua fechado até a fase Control.
