# Manifesto — Fase 0 · Reconhecimento

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| scripts/00_reconhecimento.py | script de perfilamento estrutural (granularidade, circularidade, contagens) | escrito nesta fase | fase 0 (este relatório) |
| artefatos/00_reconhecimento.py | cópia congelada do script no estado em que gerou este checkpoint | scripts/00_reconhecimento.py | prova de reprodutibilidade |
| artefatos/perfil_estrutural.json | saída completa do perfilamento (shape, dtypes, nulos, constância por ID, circularidade BMI, contagens de categóricas) | scripts/00_reconhecimento.py | fase 0, insumo de referência para Define e Measure 2A |
| fases/fase-0-reconhecimento/relatorio.md | relatório desta fase | escrito nesta fase | Define, Entrega |
| fases/fase-0-reconhecimento/relatorio.pdf | PDF do relatório, para leitura | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/md_to_pdf.py | conversor reutilizável de relatorio.md para PDF (fontes DejaVu embutidas em scripts/fonts/) | escrito nesta fase | todas as fases seguintes |

## Dado bruto usado (não copiado para artefatos/ — arquivo original)

| Arquivo | Hash SHA-256 |
|---|---|
| data/raw/Absenteeism_at_work.csv | 41930631aa5b14f91fde29ae595cefad2beac464ddf837bf8150487e40038320 |

## Documentação de referência consultada

| Arquivo | Uso |
|---|---|
| data/raw/Attribute Information.docx | confirmação das categorias oficiais de Reason for absence, Day of the week e Education |
