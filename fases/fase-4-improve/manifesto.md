# Manifesto — Fase 4 · Improve

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| relatorio.md | relatório desta fase (contramedidas, simulação, experimento, FMEA, o contra) | escrito nesta fase | Control |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/04_improve.py | script que calcula a simulação de ganho, ponto de indiferença e n do experimento | escrito nesta fase | fase 4 |
| scripts/04b_grafico_ganho.py | script que gera o gráfico dos três cenários e ponto de indiferença | escrito nesta fase | fase 4 |
| artefatos/04_improve.py, 04b_grafico_ganho.py | cópias congeladas dos scripts | scripts/ | prova de reprodutibilidade |
| artefatos/improve.json | todos os números da simulação e do cálculo de amostra | scripts/04_improve.py | este relatório |
| artefatos/simulacao_ganho.png | gráfico dos três cenários de adesão e o ponto de indiferença | scripts/04b_grafico_ganho.py | seção 3 do relatório |

## Dados de entrada (não copiados — arquivo já existente, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_qualidade.csv | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

## Holdout

Não tocado nesta fase — a simulação de ganho e o cálculo de n usam só a janela
de exploração. Continua fechado até a fase Control.
