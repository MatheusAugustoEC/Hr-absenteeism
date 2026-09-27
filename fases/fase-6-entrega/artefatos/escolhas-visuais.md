# Escolhas visuais — Fase 6 · Entrega v2 (Montador de Dashboards)

Data: 27/09/2026 · Refresh de identidade visual sobre a página já aprovada
(v1, tollgate APROVADO). **Nenhum número foi recalculado** — todos continuam
vindo de `artefatos/dados_pagina.json`, gerado pela Fase 6 v1 e não tocado
nesta rodada. Nenhuma decisão de conteúdo foi reaberta.

## Catálogo do Montador (`references/montador.md`) — escolhas

| Camada | Escolha | Nome exato do catálogo |
|---|---|---|
| Template | Clínica médica | `Clínica médica` |
| Estilo | Dark Glass | `Dark Glass` |
| Layout | Painel de controle | `Painel de controle` |
| Peça — Herói (faixa, 12) | Número-herói | `Número-herói` |
| Peça — KPIs (faixa, 12) | Faixa de KPIs | `Faixa de KPIs` |
| Peça — Principal (6) | Pareto | `Pareto` |
| Peça — Secundário (6) | Barras agrupadas | `Barras agrupadas` |
| Peça — Rodapé (12) | Tabela densa | `Tabela densa` |

Nenhum espaço ficou "— vazio —": os cinco têm dado real do pipeline por trás.

## Justificativa de cada escolha

- **Template — Clínica médica.** A recomendação inicial ("Logística e
  entregas") seguiu o setor do empregador (transportadora), não o conteúdo do
  painel — erro apontado pelo usuário e corrigido antes de aplicar no site. O
  conteúdo real é sobre pessoas, ausência e atestado médico, não sobre rota ou
  entrega. "Clínica médica" é o único template do catálogo cujo domínio nativo
  trata "atestado" e "comparecimento" como conceitos centrais, o que casa
  diretamente com o guardrail permanente do projeto (não pressionar
  comparecimento quando há atestado médico).
- **Estilo — Dark Glass.** Grupo "Escuro" da tabela de tons do catálogo:
  leitura de portfólio e RH, mas assunto sóbrio (ausência médica,
  presenteísmo) — descarta claro/editorial (tom de revista) e alto-contraste
  autoral (chama atenção para o estilo, não para o achado). Dentro do grupo
  escuro, Synthwave (neon/retrô) e Terminal (estética hacker) destoam do
  assunto; Dark Glass (superfícies translúcidas em camadas) combina melhor com
  um painel corporativo do que Nocturne (mais atmosférico/autoral), que fica
  como alternativa mais próxima.
- **Layout — Painel de controle.** A regra do catálogo é "o layout segue o
  número de mensagens": este projeto tem uma mensagem principal (X = 64,3%
  dos eventos são evitáveis) e dois apoios (onde concentra; o sinal de
  distância), mais o plano de controle — exatamente o encaixe de "um número
  grande, os guardrails ao lado, dois gráficos e uma tabela". Os outros
  layouts com espaço **Série** (Clássico, Painel denso, Mosaico) foram
  descartados porque este projeto **não pode sustentar uma série temporal**:
  a Fase 2B (M11) já determinou que não existe carta de controle válida aqui
  (máximo 13 rótulos de mês possíveis, sem coluna de ano confiável na base) —
  forçar um espaço Série teria fabricado uma leitura de tendência que os
  dados não sustentam. Três colunas foi descartado por pedir comparações
  paralelas simétricas, que não é a forma desta narrativa. Mapa em destaque
  foi excluído pela regra dura — sem dado geográfico de verdade.
- **Peças.**
  - *Número-herói* (Herói): a proporção evitável com IC, métrica primária
    congelada na Fase 2B (64,26% [57,95%–69,13%]).
  - *Faixa de KPIs* (KPIs): guardrail (atestado médico, 35,7%, com destaque
    verde) + gap vs. meta interna (+30,9 pp) + eventos totais (733) + redução
    potencial (~6,3/mês) — quatro números lado a lado.
  - *Pareto* (Principal): "onde concentra" — taxa por motivo (7 motivos),
    genuíno bar+linha acumulada com eixo único 0–100%, porque a entrada já é
    percentual (soma ~100%), diferente do Pareto de horas (que usa eixo
    duplo) — este último permanece no Dashboard/Relatório, não duplicado
    aqui (regra dura 2, uma mensagem por espaço).
  - *Barras agrupadas* (Secundário): o achado de distância (H1) — proporção
    de cada tipo de ausência dentro de cada grupo de distância (mesma
    normalização por coluna da matriz do Dashboard), com o selo "achado
    promissor, não confirmado" obrigatório no próprio bloco e o texto
    completo (efeito + IC + poder ~3% + resultado do holdout) ao lado.
  - *Tabela densa* (Rodapé): o plano de controle (3 linhas: métrica, limite,
    frequência, responsável, ação).

## O que saiu do Painel (e por quê)

A grade de 5 espaços do "Painel de controle" é mais enxuta que os 6 blocos da
v1 (regra dura 3: "o Painel continua sendo lido em dez segundos"). Dois
blocos da v1 não tinham espaço na nova grade e foram simplificados para fora
do Painel — continuam intactos no Dashboard e no Relatório, sem perda de
conteúdo na página como um todo:

- A tabela/gráfico não-temporal por mês (aviso M11) — resumida numa frase
  dentro do card do Número-herói; o gráfico completo está no Relatório
  (seção 6) e no Dashboard.
- O Pareto de impacto em horas (6 motivos administráveis) — permanece no
  Dashboard e no Relatório (seção 6), sem duplicar a mensagem do Pareto de
  taxa que agora ocupa o espaço Principal do Painel.

## Importação e contraste (`assets/importar_estilo.py`)

Rodado sobre o HTML baixado do Montador (`montador-clinica-aurora-operacao.html`).
31 variáveis `:root` encontradas. O script aponta 4 alertas, todos falsos
positivos verificados manualmente (o script testa toda variável contra
`--bg`, mas `--on-acc`/`--on-cat`/`--on-good` são cores de texto para ficar
**sobre** os chips coloridos, não sobre o fundo — testado contra o fundo
real de cada chip, todos ficam entre 4,66:1 e 11,81:1, acima do mínimo de
4,5:1; `--bg` contra si mesmo não é um defeito real).

**Nenhuma cor importada precisou de ajuste de tom** — mas o token `--accent`
do projeto (usado como texto, não só como chip de UI) foi **derivado**, não
copiado 1:1 do `--acc` do site (`#8B5CF6`), porque o roxo original só dava
4,31:1 contra a superfície dos cards e 3,72:1 contra o próprio fundo do selo
"achado promissor, não confirmado" — abaixo do mínimo de 4,5:1 para texto.
Clareei o mesmo matiz (mesmo hue, luminosidade maior) até `#A681F8`,
verificado em 6,18:1 (superfície) e 5,06:1 (selo). O `--accent-soft` (fundo
translúcido do roxo original) não mudou, porque é só um fundo, não texto.

A rampa sequencial `--s1..--s5` (usada nas barras e na matriz) **não existe
pronta no kit** — o Dark Glass define 5 cores categóricas (`c1..c5`, tons
diferentes), não uma rampa de intensidade de um único matiz. Derivei uma
rampa roxa de 5 passos a partir do mesmo `--accent`, com cada degrau
verificado contra a superfície (2,13:1 a 9,80:1, todos acima do mínimo de
2:1 para uso como marca).

Como o Estilo escolhido é escuro (sem contraparte clara no kit do site), o
tema claro do projeto foi mantido pela estrutura já testada na v1
(neutros inalterados), com o acento e a rampa recalculados na mesma família
roxa para manter a identidade entre os dois temas — `--accent` claro
`#4B0CD9` (7,58–8,92:1) e `--crit`/`--warn`/`--good` escurecidos para
4,65–5,75:1 contra branco (as versões do kit, pensadas só para fundo escuro,
ficavam abaixo de 3:1 em fundo claro).

## Correção de um defeito de contraste descoberto ao testar (não do import)

Ao redesenhar os tokens, `--surface` passou de sólido (branco/cinza-escuro
na v1) para **translúcido** (`rgba(255,255,255,.055)` no escuro), pelo efeito
"glass" do Dark Glass. Três regras de CSS e uma função JS (`textOn`, usada
pela matriz tipo×distância do Dashboard) reaproveitavam `--surface` como "cor
sólida de contraste" para texto sobre botões cheios de `--accent` (aba ativa
do menu, marca de seleção do checkbox, botões de download) — com o valor
translúcido, esse texto ficava quase invisível (contraste ~1:1). Corrigido
trocando essas quatro referências para um novo uso de `--paper` (sempre
sólido nos dois temas: `#07070E` escuro, `#E9EDF0` claro), que dá 6,81:1
(escuro) e 7,58:1 (claro) contra o `--accent` — verificado com Playwright
antes e depois da correção.

## Tipografia

Trocada por completo pela do kit: `Fraunces` (títulos serifados) e
`IBM Plex Mono` → `Inter` (títulos e corpo) e `JetBrains Mono` (dados,
rótulos, código) — inclusive dentro dos textos SVG dos gráficos (que leem a
variável CSS ao vivo via `getComputedStyle`, então a troca de token já
recolore todos os gráficos sem precisar tocar na lógica de desenho).
`Public Sans` (corpo) também virou `Inter`.

## Auditoria final desta rodada

Ver `artefatos/relatorio-auditoria.md`, seção "Rodada 3 (v2 — identidade
visual)". Resumo: 1 rodada com Playwright/Chromium, zero erros de console,
10/10 checagens funcionais (dropdown, filtro cruzado, seleção da matriz,
ordenação de tabela, download .xlsx, navegação de slides até 9/9, download
.pptx), número-âncora (64,3%) idêntico entre Painel e Slides, checagem de
B1/B2/CID confirmando as duas únicas ocorrências dentro do glossário (mesmo
estado da v1), capturas em tema claro/escuro/mobile sem rótulo sobre dado.

## Arquivos desta pasta

- `montador-clinica-aurora-operacao.html` — HTML baixado do Montador, como
  está, sem edição (prova de reprodutibilidade da identidade visual).
- `index.html` — cópia congelada da página final v3.
- `capturas/painel-claro.png`, `capturas/painel-escuro.png`,
  `capturas/dashboard-tecnica.png`, `capturas/relatorio-escuro.png`,
  `capturas/slide1.png`, `capturas/dashboard-mobile.png` — atualizadas na v3.

---

## Adendo v3 — reconstrução estrutural (27/09/2026)

A v2 tratou o HTML do Montador só como fonte de tokens de cor, aplicados por
cima do esqueleto antigo (`assets/molde.html` da skill) em Dashboard,
Relatório e Slides — só o Painel ganhou a grade nova. Resultado apontado
pelo usuário: os três outros modos continuavam "lendo" como o molde antigo,
só recolorido. Corrigido tratando
`montador-clinica-aurora-operacao.html` como o **molde estrutural real**
desta entrega — não só a fonte de `:root` — e propagando sua linguagem de
componente (card de vidro com brilho no topo, grade de 12 colunas, chips
arredondados com sombra) para os quatro modos, não só o Painel. **Nenhum
número foi recalculado nesta rodada também** — só marcação, CSS e disposição
dos mesmos blocos.

### O que mudou estruturalmente em cada modo

- **Painel** — já usava a grade "Painel de controle" desde a v2; nesta
  rodada a Faixa de KPIs deixou de ser uma tira com divisórias internas e
  virou uma **grade de cartões individuais** (o padrão exato dos chips
  "Ticket médio / Conversão / Pedidos / Devoluções" do exemplo do Montador),
  cada um com borda, raio e sombra próprios.
- **Dashboard** — deixou de ser uma coluna de cards soltos com espaçamento
  ad hoc (`.two`, margens manuais) e passou a usar a **mesma grade de 12
  colunas do Painel** (`#dash-body` como `.grade12`, com `g12`/`g6`
  explícitos por bloco): composição por tipo em faixa cheia, taxa e horas
  por motivo lado a lado, matriz/funcionário/tabela em faixa cheia — e a
  Faixa de KPIs do topo ganhou o mesmo tratamento de cartões individuais do
  Painel. Antes, a primeira diferença visual entre v1 e v2 aqui era "só a
  cor"; agora é a grade e os cartões de vidro.
- **Relatório** — ganhou uma **Faixa de KPIs no topo** (logo após a
  resposta em uma frase, antes do sumário), repetindo em cartões os mesmos
  quatro números que abrem o Painel — nenhum número novo, só uma segunda
  leitura em formato de painel antes da prosa. A tabela de FMEA (seção 11)
  trocou o texto colorido "Alta"/"Média" por **badges arredondados**
  (mesmo padrão visual dos indicadores de status do exemplo "Convênios" do
  Montador). Antes, a única mudança aqui era cor de fundo e tipografia;
  agora o relatório abre com um componente que não existia na v1/v2.
  A prosa em si permanece prosa — converter parágrafos inteiros em cards
  quebraria a leitura, que é o ponto forte deste modo.
- **Slides** — cada quadro com número-destaque (`.fstat`) ganhou um
  **chip de contexto** abaixo do número (mesmo padrão do "▲ 5,4% vs. mês
  anterior" do exemplo do Montador), com o IC ou a premissa citada na
  própria frase do slide — não um número novo. O indicador de posição
  ("1 / 9") deixou de ser texto solto e virou um badge arredondado. O
  cartão do slide (`.deck`) ganhou a mesma linha de brilho no topo dos
  cards do Painel/Dashboard. O `.pptx` gerado não inclui os chips (a função
  `visText()` só lê `<p>`; os chips são `<div>`) — o conteúdo do arquivo
  exportado não mudou, é uma camada só da versão web.

### Resposta à pergunta de validação do prompt

*"Qual é a primeira diferença que salta aos olhos em cada um dos quatro
modos, comparando v1 com esta versão?"*

- Painel: a Faixa de KPIs virou 4 cartões separados, não uma tira única.
- Dashboard: os blocos agora estão numa grade de 12 colunas com cartões de
  vidro (a mesma do Painel), não empilhados com espaçamento manual.
- Relatório: uma faixa de 4 cartões de KPI logo no topo, antes do sumário —
  elemento que não existia antes.
- Slides: cada número grande vem com um chip de contexto arredondado
  embaixo, e o contador de página é um badge, não texto solto.

Nenhuma resposta é "só a cor" — as quatro têm um componente ou uma grade que
não existia na v1/v2.
