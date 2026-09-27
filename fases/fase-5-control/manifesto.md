# Manifesto — Fase 5 · Control

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| relatorio.md | relatório desta fase (plano de controle, testes, holdout, Kaizen) | escrito nesta fase | Entrega |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| config.py | parâmetros centralizados (limiar de duplicata, sementes, custo de RH, α) | escrito nesta fase | referência para todas as fases; ainda não importado pelos scripts das Fases 2A-4 (pendência registrada) |
| tests/test_qualidade.py | 14 testes automáticos de qualidade (C7) | escrito nesta fase | CI/reprodutibilidade do pipeline |
| README.md (raiz do projeto) | rascunho de README — revisado na Fase 8 | escrito nesta fase | leitura por um estranho que queira rodar o projeto |
| scripts/05a_holdout_sorteio.py | sorteio do holdout — commitado ANTES de qualquer cálculo | escrito nesta fase | fase 5 — prova de abertura única |
| scripts/05b_holdout_confirmacao.py | análise do efeito de H1 no grupo de confirmação | escrito nesta fase | fase 5 |
| artefatos/05a_holdout_sorteio.py, 05b_holdout_confirmacao.py, test_qualidade.py, config.py | cópias congeladas | scripts/, tests/, raiz | prova de reprodutibilidade |
| artefatos/holdout_confirmacao.json | resultado numérico da confirmação | scripts/05b_holdout_confirmacao.py | este relatório |
| artefatos/pytest_saida.txt | saída dos 14 testes automáticos (todos passaram) | pytest | este relatório |

## A quarentena do holdout

| Arquivo | O que é | Hash SHA-256 | Momento |
|---|---|---|---|
| data/holdout/split_ids.json | sorteio das 34 identidades (26 exploração / 8 confirmação), semente 20260926 | e57f11ada4a0c3395567e15374823a728996b094cd6cdb3da9991faa189373f1 | Gerado e **commitado separadamente** (commit anterior a este), antes de qualquer cálculo de confirmação |

Este é o **terceiro artefato de prova imutável** do contexto mestre. O
sorteio em si (`split_ids.json`) não deve ser regravado — se o processo
precisar ser refeito por algum motivo excepcional, isso exige um adendo
datado explicando por quê, nunca uma nova execução silenciosa de
`05a_holdout_sorteio.py`.

## Dados de entrada (não copiados — arquivo já existente, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_qualidade.csv | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

## Ordem dos commits desta fase (prova de que o sorteio veio antes da análise)

1. Commit "sorteio do holdout" — `config.py`, `scripts/05a_holdout_sorteio.py`, `data/holdout/split_ids.json`.
2. Commit deste checkpoint — inclui `scripts/05b_holdout_confirmacao.py`, o relatório e os demais artefatos da fase, gerados **depois** do commit 1.
