# Manifesto — Fase 6 · Entrega (v5, reconstrução do zero)

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| relatorio.md | relatório desta fase (por que recomeçou, plano aprovado, narrativa X-Y-Z, tollgate) | escrito nesta fase | Fase 7 (banca), Fase 8 (Fechamento) |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/06_entrega_dados.py | consolida os JSONs de todas as fases num único `dados_pagina.json` (sobreviveu à limpeza da fase, vive fora de fases/fase-6-entrega/) | já existia, reexecutado nesta fase | fase 6 |
| pagina/index.html | a página de entrega (Dashboard, Relatório, Slides; lateral com navegação e filtros) — publicável no GitHub Pages | scripts/06_entrega_dados.py + construída do zero nesta fase | Fase 7, Fase 8, publicação final |
| pagina/pptxgen.bundle.js | biblioteca irmã necessária para os downloads .pptx/.xlsx | skill entrega-dmaic (assets/pptxgen.bundle.js) | pagina/index.html |
| artefatos/06_entrega_dados.py | cópia congelada do script | scripts/06_entrega_dados.py | prova de reprodutibilidade |
| artefatos/dados_pagina.json | todos os números da página, consolidados | scripts/06_entrega_dados.py | pagina/index.html (embutido) |
| artefatos/index.html, pptxgen.bundle.js | cópia congelada da página entregue | pagina/ | prova de reprodutibilidade |
| artefatos/relatorio-auditoria.md | relatório da auditoria final (1 rodada, 1 achado corrigido) | auditoria com Playwright | este relatório |
| artefatos/auditoria_v5_reconstrucao.py | script Playwright desta auditoria | escrito nesta fase | artefatos/relatorio-auditoria.md |
| artefatos/capturas/*.png | capturas dos três modos (Dashboard claro/escuro/mobile, Relatório escuro, Slides desktop/mobile) | Playwright | artefatos/relatorio-auditoria.md |

## Dados de entrada (não copiados — arquivos já existentes, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_qualidade.csv | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

Os demais números vêm dos JSONs já congelados nos manifestos das Fases 0-5
(`fases/*/artefatos/*.json`), listados individualmente em
`scripts/06_entrega_dados.py`.

## Holdout

Não tocado nesta fase — os números da confirmação (n=8) já estavam
calculados e congelados na Fase 5 (`holdout_confirmacao.json`), só
consumidos aqui.

## Histórico desta fase

As versões v1-v4 (identidade visual, feitas e desfeitas na mesma janela de
trabalho) foram apagadas por decisão do usuário — commit "Fase 6: removida
para recomeçar do zero, a partir do fim da Fase 5" — e continuam no
histórico do git como registro do que foi tentado. Esta é a v5, construída
do zero com um formato diferente (sem Painel, sem registro dual, lateral de
navegação), aprovado pelo usuário antes da construção.
