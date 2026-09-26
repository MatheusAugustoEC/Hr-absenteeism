# Manifesto — Fase 1 · Define

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| pre-registro.md | pré-registro datado das hipóteses, holdout e critério de sucesso — **IMUTÁVEL a partir do commit desta fase**; correção futura é adendo datado ao final, nunca edição | escrito nesta fase | Analyze (teste das hipóteses), Control (abertura do holdout) |
| pre-registro.pdf | PDF do pré-registro | scripts/md_to_pdf.py | leitura e arquivo |
| relatorio.md | relatório desta fase (charter, definição operacional, guardrails, escopo) | escrito nesta fase | Measure 2A, Measure 2B |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/01_define_escopo.py | script que aplica os critérios de exclusão e reagrupa Reason for absence em B1/B2/CID | escrito nesta fase | fase 1 (este relatório) |
| artefatos/01_define_escopo.py | cópia congelada do script | scripts/01_define_escopo.py | prova de reprodutibilidade |
| artefatos/escopo_define.json | contagens de exclusão, categoria de defeito e distribuição de eventos por funcionário | scripts/01_define_escopo.py | este relatório, Measure 2B |
| data/processed/eventos_limpos.csv | base pós-exclusões (736 linhas), sem nenhuma relação entre variáveis aplicada — **não é o holdout** | scripts/01_define_escopo.py | Measure 2A, Measure 2B, Analyze (janela de exploração) |

## Dado bruto usado (não copiado — arquivo original, mesmo hash da Fase 0)

| Arquivo | Hash SHA-256 |
|---|---|
| data/raw/Absenteeism_at_work.csv | 41930631aa5b14f91fde29ae595cefad2beac464ddf837bf8150487e40038320 |

## Hash do pré-registro no momento em que se tornou imutável

| Arquivo | Hash SHA-256 (26/09/2026) |
|---|---|
| fases/fase-1-define/pre-registro.md | e5a3a86dd132ea7a162060f19f906e5c29ed31231f758a2c905ca1548cacb149 |

## Holdout

A quarentena do holdout (recorte aleatório por identidade de funcionário,
definido em `pre-registro.md`) ainda não foi materializada em arquivo — o
sorteio efetivo só é executado e congelado quando a fase Control abrir o
recorte pela primeira vez. Até lá, nenhum script deste projeto deve gerar,
salvar ou ler esse recorte.
