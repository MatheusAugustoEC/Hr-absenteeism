# Manifesto — Fase 6 · Entrega

| Arquivo | O que é | Gerado por | Usado em |
|---|---|---|---|
| relatorio.md | relatório desta fase (plano, nomenclatura, narrativa X-Y-Z, tollgate) | escrito nesta fase | Fase 7 (banca), Fase 8 (Fechamento) |
| relatorio.pdf | PDF do relatório | scripts/md_to_pdf.py | leitura pelo responsável do projeto |
| scripts/06_entrega_dados.py | consolida os JSONs de todas as fases num único `dados_pagina.json` | escrito nesta fase | fase 6 |
| pagina/index.html | a página de entrega (Painel, Dashboard, Relatório, Slides) — publicável no GitHub Pages | scripts/06_entrega_dados.py + molde da skill entrega-dmaic | Fase 7, Fase 8, publicação final |
| pagina/pptxgen.bundle.js | biblioteca irmã necessária para os downloads .pptx/.xlsx | skill entrega-dmaic (assets/pptxgen.bundle.js) | pagina/index.html |
| artefatos/06_entrega_dados.py | cópia congelada do script | scripts/06_entrega_dados.py | prova de reprodutibilidade |
| artefatos/dados_pagina.json | todos os números da página, consolidados | scripts/06_entrega_dados.py | pagina/index.html (embutido) |
| artefatos/index.html, pptxgen.bundle.js | cópia congelada da página entregue | pagina/ | prova de reprodutibilidade |
| artefatos/relatorio-auditoria.md | relatório da auditoria final (v1: 3 rodadas; v2: +1 rodada de cor; v3: +1 rodada de reconstrução estrutural) | auditoria com Playwright | este relatório |
| artefatos/capturas/*.png | capturas dos quatro modos (Painel claro/escuro, Dashboard técnica/mobile, Relatório, slide 1), atualizadas na v3 | Playwright | artefatos/relatorio-auditoria.md |
| artefatos/auditoria_v2_visual.py, auditoria_v2_funcional.py | scripts Playwright da auditoria v2 (visual + funcional) | escritos na v2 | artefatos/relatorio-auditoria.md |
| artefatos/auditoria_v3_reconstrucao.py | script Playwright da auditoria v3 (reconstrução estrutural nos 4 modos) | escrito nesta rodada | artefatos/relatorio-auditoria.md |
| artefatos/montador-clinica-aurora-operacao.html | HTML baixado do Montador de Dashboards, como está, sem edição | dashbuilder.asimov.academy | artefatos/escolhas-visuais.md |
| artefatos/escolhas-visuais.md | Template/Estilo/Layout/Peças escolhidos, justificativas, ajustes de contraste | escrito nesta rodada | fases/indice.md |

## Dados de entrada (não copiados — arquivos já existentes, com hash)

| Arquivo | Hash SHA-256 |
|---|---|
| data/processed/eventos_qualidade.csv | ba78283944d6c64f1a126677de3f10bc5fb344453c25a47bfd294f4e9658ff47 |

Os demais números vêm dos JSONs já congelados nos manifestos das Fases 0-5
(`fases/*/artefatos/*.json`), listados individualmente em
`scripts/06_entrega_dados.py`.

## Holdout

Não tocado nesta fase — os números da confirmação (n=8) já estavam calculados
e congelados na Fase 5 (`holdout_confirmacao.json`), só consumidos aqui.
