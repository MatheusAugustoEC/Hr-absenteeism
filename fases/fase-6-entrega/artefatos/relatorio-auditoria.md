# Relatório de auditoria — Fase 6 · Entrega

Data: 27/09/2026 · Ferramenta: Playwright (Chromium real, headless), servindo a página por `python -m http.server` — não como `file://`.

## Como foi feito

Diferente de uma auditoria só de leitura de código, esta rodou a página de
verdade num navegador: os quatro modos, os dois registros de linguagem, os
dois temas, e duas larguras (desktop 1280px e mobile 390px). As rodadas 1-3
(v1) usaram scripts equivalentes a `auditoria_v2_visual.py`/
`auditoria_v2_funcional.py`, mas as cópias originais não foram salvas em
`artefatos/` nessa época — inconsistência do relatório da v1, registrada aqui
e corrigida a partir da rodada da v2 (scripts desta rodada estão salvos em
`artefatos/`, reprodutíveis).

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

## Rodada 4 (v2 — identidade visual, Montador de Dashboards)

Data: 27/09/2026. Escopo: só o refresh visual (Template Clínica médica,
Estilo Dark Glass, Layout Painel de controle) — ver `escolhas-visuais.md`
para as escolhas e justificativas. Nenhum número foi recalculado.

**Achado durante a checagem de contraste (não bloqueante para a auditoria
funcional, mas corrigido antes de fechar a rodada):** ao trocar `--surface`
de sólido para translúcido (efeito "glass"), quatro pontos que reaproveitavam
essa variável como cor de texto sobre fundo cheio de `--accent` (aba ativa do
menu de modo/registro, marca do checkbox nos dropdowns, botões de download
`.xlsx`/`.pptx`/PDF, e a função `textOn()` usada pela matriz tipo×distância
do Dashboard) ficaram com texto quase invisível (contraste ~1:1, verificado
via `getComputedStyle` no Playwright). Corrigido trocando as quatro
referências para um token sempre sólido (`--paper`), verificado em 6,81:1
(escuro) e 7,58:1 (claro) contra `--accent`.

Checagens rodadas (`auditoria_v2_visual.py` + `auditoria_v2_funcional.py`):

- Zero erros de console/página nos 4 modos.
- Selo "achado promissor, não confirmado" e KPI de guardrail presentes no
  Painel.
- Gráficos novos (Pareto do Principal, Barras agrupadas do Secundário)
  renderizam com a contagem certa de elementos (7 barras do Pareto = 7
  motivos; 6 barras agrupadas = 3 tipos × 2 grupos de distância) e legenda
  de cores do achado de distância presente.
- Dropdown do Dashboard abre, filtra, gera chip removível, atualiza contador.
- Seleção por clique na matriz tipo×distância aplica e remove o contorno de
  seleção.
- Ordenação de coluna da tabela aplica `aria-sort`.
- Download `.xlsx` gerado (> 1 KB) e `.pptx` gerado (> 1 KB).
- Navegação de slides chega a 9/9 e para (botão desabilitado no último).
- Manchete (64,3%) idêntica entre Painel e Slides.
- Busca literal de B1/B2/CID: só as duas ocorrências do glossário (mesmo
  estado da v1) — confirmado.
- Capturas em tema claro, escuro e largura mobile (390px): nenhum rótulo
  sobre dado, cards com contraste de texto ≥4,5:1 verificado nos tons
  extremos da rampa (ver `escolhas-visuais.md`).

**Resultado: 1 rodada, 1 achado de contraste (corrigido), 10/10 checagens
funcionais aprovadas na repetição após a correção.**

## Rodada 5 (v3 — reconstrução estrutural sobre o molde do Montador)

Data: 27/09/2026. Escopo: a v2 só recolori Dashboard/Relatório/Slides sobre
o esqueleto antigo (`assets/molde.html`) — o usuário apontou que isso não
cumpria o pedido de adotar o Montador como base visual. Nesta rodada, a
grade de 12 colunas, os cartões de vidro (`--radius`/`--shadow`/brilho no
topo) e o padrão de chip arredondado do HTML baixado do Montador foram
propagados para os quatro modos. Detalhe de cada mudança em
`escolhas-visuais.md`, adendo v3. Nenhum número recalculado.

Checagens rodadas (`auditoria_v3_reconstrucao.py`):

- Zero erros de console/página nos 4 modos, após a reconstrução.
- `#dash-body` confirmado usando a classe `grade12` (mesma grade do Painel).
- Faixa de KPIs do Relatório presente (`#pane-relatorio .kpis`) e badges de
  severidade do FMEA presentes (`.sevpill`).
- Slide 1 confirmado com o chip de contexto (`.fpill`) sob o número-destaque.
- Filtro cruzado do Dashboard (dropdown → chip → remoção), seleção por
  clique na matriz tipo×distância, e ordenação de coluna da tabela — todos
  retestados depois da reestruturação em grade, sem regressão.
- Download `.xlsx` e `.pptx` gerados (> 1 KB cada) depois da reconstrução.
- Navegação de slides chega a 9/9.
- Busca literal de B1/B2/CID no DOM renderizado: 1+1+2 ocorrências, todas
  dentro do glossário — mesma contagem da v1/v2, nenhuma vazou para a nova
  marcação.
- Manchete (64,3%) idêntica entre Painel e Slides.
- Capturas novas dos quatro modos (claro, escuro e mobile) — nenhum rótulo
  sobre dado, grade de 12 colunas colapsando para 1 coluna em telas
  estreitas nos quatro modos.

**Resultado: 1 rodada, 0 achados bloqueantes, 9/9 checagens aprovadas.**

## Conclusão

V1: após 3 rodadas (2 com achado, 1 limpa), a página ficou pronta para
entrega, com os quatro modos funcionais, os números idênticos nos dois
registros, e nenhum resto de conteúdo do molde.

V2 (identidade visual, só Painel): 1 rodada com 1 achado de contraste,
corrigido e reverificado. Escopo insuficiente — só o Painel usou a grade do
Montador; Dashboard/Relatório/Slides ficaram com o esqueleto antigo
recolorido.

V3 (reconstrução estrutural, quatro modos): 1 rodada, 0 achados. A grade e
os componentes do Montador agora estruturam Painel, Dashboard, Relatório e
Slides. Nenhum número mudou em relação à v1; toda a mecânica de interação
(filtros, matriz, ordenação, downloads, zoom, registros de linguagem) foi
retestada e continua igual.
