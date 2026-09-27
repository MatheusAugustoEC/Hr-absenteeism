# Relatório de auditoria — Fase 6 · Entrega

Data: 27/09/2026 · Ferramenta: Playwright (Chromium real, headless), servindo a página por `python -m http.server` — não como `file://`.

## Como foi feito

Diferente de uma auditoria só de leitura de código, esta rodou a página de
verdade num navegador: os quatro modos, os dois registros de linguagem, os
dois temas, e duas larguras (desktop 1280px e mobile 390px). Os scripts de
auditoria estão em `artefatos/` desta fase (`auditoria_playwright.py`,
`auditoria2.py`) para reprodução.

## Rodada 1 — funcional (18 checagens)

Console ao carregar, os 4 modos × 2 registros sem erro, menu de filtro que
continua aberto ao marcar uma opção, KPIs recalculando ao filtrar, etiqueta de
filtro ativo aparecendo e removendo, clique duplo na matriz selecionando e
desmarcando, ordenação de tabela, "Mostrar todas", download da planilha
`.xlsx` (31.061 bytes, gerado e validado sem salvar no disco do usuário),
navegação completa dos 9 quadros de slide, download da apresentação `.pptx`
(117.590 bytes), contagem de seções do relatório (15 h2 + 1 glossário = 16,
batendo com o índice), tema escuro e largura mobile sem erro de console.

**Resultado: 0 bloqueantes de 18 checagens.**

## Rodada 2 — consistência numérica e inspeção visual (4 checagens + capturas)

Conferiu que a manchete do Painel (64,3%) é idêntica nos dois registros, que a
seção 1 do Relatório cita o mesmo número, e que o primeiro slide bate com o
Painel. Capturou telas do Painel (claro e escuro), Dashboard, slide 1 e
Relatório para inspeção visual.

**Três achados bloqueantes encontrados nas capturas, e corrigidos antes de
fechar a rodada:**

1. **Rótulo cortado**: "Falta sem justificativa aceita" não cabia na margem
   esquerda do gráfico de barras (`barrasH`). Corrigido aumentando a margem de
   138 para 168px.
2. **Rótulo ambíguo no eixo**: o gráfico de horas por motivo mostrava
   "Consulta" duas vezes (consulta médica e consulta odontológica, cortadas
   pela mesma regra de primeira palavra). Corrigido para primeira palavra +
   inicial da segunda ("Consulta M.", "Consulta O.").
3. **Rótulo sobre dado**: no gráfico não-temporal por mês, o aviso "NÃO
   TEMPORAL" no topo colidia com o rótulo da linha de referência "média
   geral", que por sua vez caía em cima da barra do mês 12. Corrigido dando
   mais espaço ao título (margem superior) e movendo o rótulo da média para
   fora da área de barras, na margem direita do gráfico.

## Rodada 3 — repetição completa após as correções

Rodada 1 e rodada 2 repetidas do zero. **0 bloqueantes em ambas.** A rodada
terminou inteira sem achado — não precisou de uma quarta rodada.

## Melhorias não bloqueantes que ficaram de fora

- Os rótulos abreviados no eixo do gráfico de impacto em horas ("Consulta M.",
  "Acompanhamento", "Fisioterapia") ficam com pouco espaço entre si em telas
  estreitas — legível, mas apertado. Não bloqueante porque nenhum texto
  sobrepõe outro texto ou marca.
- `requirements.txt` do projeto (Python) sem versões pinadas — já registrado
  como dívida técnica na Fase 5, não específico desta página.

## Conclusão

Após 3 rodadas (2 com achado, 1 limpa), a página está pronta para entrega,
com os quatro modos funcionais, os números idênticos nos dois registros, e
nenhum resto de conteúdo do molde.
