# Fase 6 · Entrega — Absenteísmo no Trabalho

Data: 27/09/2026 · Página única publicável (Painel, Dashboard, Relatório, Slides) construída a partir do molde da skill `entrega-dmaic` · v1

## Em três linhas

Construí a página de entrega a partir do molde testado, com todos os números
lidos de um JSON gerado pelo pipeline (`scripts/06_entrega_dados.py`), sem
nenhum "B1"/"B2"/"CID"/código numérico visível fora do glossário. Rodei a
auditoria final com um navegador real (Playwright): 3 rodadas, 2 com achado
(3 rótulos de gráfico corrigidos), a terceira limpa. Tollgate: **APROVADO**.

## O que foi feito

1. Plano visual apresentado e aprovado antes de construir (nomenclatura,
   blocos por modo, gráficos, filtros, títulos dos slides).
2. Pipeline de consolidação (`scripts/06_entrega_dados.py`) que lê os JSONs
   de todas as fases e escreve um único `dados_pagina.json`, embutido na
   página como `<script type="application/json">`.
3. Página construída a partir de `assets/molde.html` da skill, com a
   mecânica de interação, os tokens de cor e a estrutura de 4 modos/2
   registros reaproveitados; conteúdo, dimensões do cubo e gráficos
   adaptados a este projeto.
4. Auditoria final com navegador real (Playwright + Chromium), não só leitura
   de código — ver `artefatos/relatorio-auditoria.md`.

## Nomenclatura (regra que sobrepôs tudo nesta fase)

| Nome interno (relatórios de fase) | Nome na página |
|---|---|
| B1 (comportamental/disciplinar) | Falta sem justificativa aceita |
| B2 (administrável na forma) | Ausência administrável |
| CID (1–21) | Atestado médico |
| Defeito B = B1+B2 | Parte evitável |
| Códigos de "Reason for absence" | Nome do motivo em português |

Os nomes internos só aparecem no glossário do Relatório (seção 16), como
tradução reversa. Confirmado por busca literal no HTML final — ver seção
"Tollgate" abaixo.

## Narrativa X-Y-Z

- **X** (Painel, abertura do Relatório, slide 1): 64,3% [57,95%–69,13%] dos
  eventos de ausência não têm atestado médico por trás.
- **Y** (Relatório, slides 3-5): a maior parte (54,4 pp) é administrável
  (consulta, exame); uma fatia menor (9,8 pp) é falta sem justificativa,
  concentrada num atalho de registro disperso entre 20 funcionários (H3,
  confirmada); e há um sinal promissor, não confirmado, sobre distância
  (H1, 16,4 pp, reforçado a 9,5 pp numa segunda amostra).
- **Z** (Relatório seção 2, slides 2 e 6): corrigir o registro (poka-yoke,
  pronto) e testar — não implementar — a priorização de agendamento por
  distância (piloto condicional, ponto de indiferença de 35,4%).

## O que é específico deste projeto (conforme instruído)

- **Métrica primária**: proporção de eventos evitáveis, 64,26% [57,95–69,13%],
  n=733/34.
- **Meta**: interna (quartil de melhor desempenho, 33,36%) — sem benchmark
  externo válido, explicado em uma frase no Painel.
- **Controle**: sem carta válida (M11) — tabela descritiva não temporal no
  lugar, com o aviso na própria legenda do gráfico.
- **Guardrail**: proporção de atestado médico, com caixa própria (borda e
  número em verde, `--good`), separada visualmente dos indicadores de
  problema.
- **Dois Paretos**: taxa (8 motivos) e impacto em horas (6 motivos
  administráveis, com aviso embutido no próprio card sobre por que "falta sem
  justificativa" não aparece nele).
- **Filtros do Dashboard**: tipo de ausência, motivo, grupo de distância, dia
  da semana, estação — cinco menus suspensos, todos no padrão
  selecionar-todos/limpar/seleção múltipla do molde.
- **Matriz tipo × distância**: com o selo "achado promissor, não confirmado"
  ao lado do título, e a mesma frase completa (efeito + IC + poder + holdout)
  sempre que o texto menciona distância.
- **Barra por funcionário**: anonimizada ("Funcionário 1"..."34"), nunca o ID
  do CSV, com a meta interna marcada.

## Janelas de tempo

- Série completa / janela pós-qualidade (733 eventos, 34 identidades): usada
  em todos os KPIs, Paretos e na tabela não temporal.
- Segunda amostra de confirmação (holdout, n=8): usada só na seção 13 do
  Relatório e no slide 8, sempre rotulada como tal e nunca misturada com a
  amostra principal no mesmo bloco.

## Auditoria final

Ver `artefatos/relatorio-auditoria.md` — 3 rodadas com um navegador real
(Playwright/Chromium), 3 achados bloqueantes na rodada 2 (rótulos de gráfico:
um cortado, um ambíguo, um sobreposto a um dado), todos corrigidos, rodada 3
limpa.

## Tollgate ENTREGA

| Critério | Veredito | Motivo |
|---|---|---|
| Nenhuma ocorrência de B1/B2/CID/código numérico em texto visível | OK | Busca literal confirma: só aparecem dentro de `<details id="s16">` (glossário) |
| Narrativa X-Y-Z explícita no Painel, Relatório e Slides, mesma ordem e números | OK | Painel abre com X; Relatório abre com X (resposta em 1 frase) e resolve com Z na seção 2; Slides 1-2 são X e Z |
| Guardrail com destaque visual próprio | OK | `.guardrail-box`, borda e número em `--good`, distinto dos indicadores de problema |
| Filtro de tipo de ausência com as três categorias sempre visíveis | OK | Dropdown "Tipo de ausência" nunca esconde "Atestado médico" |
| Pareto de impacto avisa por que "sem justificativa" não aparece | OK | Nota no próprio card, nos dois registros |
| Todo número sobre distância traz poder baixo + resultado da 2ª amostra juntos | OK | Matriz (Dashboard), seção 7 e seção 13 do Relatório, slide 5 e 8 |
| Página partiu do molde, 4 modos existem, números vêm do pipeline | OK | `dados_pagina.json` embutido, gerado por `scripts/06_entrega_dados.py` |
| Auditoria final rodou, quantas rodadas, terminou sem bloqueante | OK | 3 rodadas (ver `artefatos/relatorio-auditoria.md`) |

**Veredito: APROVADO.**

## Pendências e riscos

- `requirements.txt` sem versões pinadas (dívida técnica já registrada na
  Fase 5, não específica desta página).
- Rótulos abreviados do gráfico de impacto em horas ficam apertados em telas
  estreitas — legível, não bloqueante.

## Para a próxima fase

A Fase 7 (revisão por banca) recebe o link da página publicada — numa
conversa nova, sem os bastidores deste projeto. A Fase 8 (Fechamento) recebe
esta página como fonte dos números finais do README.

## Adendo — v2, identidade visual (27/09/2026)

A skill `entrega-dmaic` ganhou o fluxo do Montador de Dashboards
(`references/montador.md`). Nesta rodada, só a identidade visual da página
mudou — Template **Clínica médica**, Estilo **Dark Glass**, Layout **Painel
de controle**, com as Peças Número-herói/Faixa de KPIs/Pareto/Barras
agrupadas/Tabela densa. Justificativa completa de cada escolha, a correção de
contraste encontrada ao importar os tokens (texto quase invisível sobre botões
de acento, corrigido trocando `--surface` translúcido por `--paper` sólido em
quatro pontos de CSS/JS) e a repetição da auditoria estão em
`artefatos/escolhas-visuais.md` e na Rodada 4 de
`artefatos/relatorio-auditoria.md`. **Nenhum número mudou** em relação à v1;
nenhuma decisão de conteúdo foi reaberta. Tollgate desta rodada: ver seção
abaixo, adendo ao veredito original.

### Tollgate ENTREGA (visual) — v2

| Critério | Veredito | Motivo |
|---|---|---|
| Recomendação mostrada e fase parada antes do HTML devolvido | OK | Template/Estilo/Layout/Peças recomendados e discutidos com o usuário antes de qualquer construção |
| HTML baixado e folha de escolhas salvos intactos em artefatos/ | OK | `montador-clinica-aurora-operacao.html` (sem edição) + `escolhas-visuais.md` |
| Toda cor importada passa no contraste mínimo (2:1 rampa, 4,5:1 texto) | OK | `escolhas-visuais.md` — 1 ajuste de acento derivado (mesmo matiz, luminosidade maior) e 1 defeito de reaproveitamento de variável corrigido, ambos documentados com antes/depois |
| Painel usa a grade e os blocos escolhidos, todos alimentados pelo pipeline | OK | `dados_pagina.json` inalterado; grade `Painel de controle` com as 5 peças recomendadas |
| Nenhuma ocorrência de B1/B2/CID fora do glossário | OK | Busca literal confirma: mesmo estado da v1 |
| Nenhum número mudou em relação à versão anterior da página | OK | `06_entrega_dados.py` e `dados_pagina.json` não tocados nesta rodada |
| Auditoria final rodou de novo, terminou sem bloqueante | OK | Rodada 4: 1 achado de contraste, corrigido, 10/10 checagens funcionais na repetição |

**Veredito: APROVADO.**

## Adendo — v3, reconstrução estrutural (27/09/2026)

A v2 só recolori Dashboard, Relatório e Slides sobre o esqueleto antigo
(`assets/molde.html` da skill) — o Montador entrou como fonte de variáveis
de cor, não como molde estrutural. O usuário apontou que isso não cumpria o
pedido: "a primeira diferença" entre a v1 e a v2 em três dos quatro modos
era só a cor. Corrigido tratando
`artefatos/montador-clinica-aurora-operacao.html` como o molde estrutural
real desta entrega — a grade de 12 colunas, o cartão de vidro (borda, raio,
sombra, brilho no topo) e o chip arredondado do Montador agora estruturam
os quatro modos, não só o Painel. Detalhe completo, por modo, no adendo v3
de `artefatos/escolhas-visuais.md`. **Nenhum número mudou** nesta rodada
também — o pipeline (`dados_pagina.json`) segue intocado desde a v1.

### Tollgate ENTREGA (visual) — v3

| Critério | Veredito | Motivo |
|---|---|---|
| Dashboard, Relatório e Slides usam a linguagem visual do Montador na estrutura dos componentes, não só nas variáveis de cor | OK | Dashboard: grade de 12 colunas (`grade12`) igual ao Painel, KPIs em cartões individuais. Relatório: faixa de KPIs nova no topo, badges de severidade no FMEA. Slides: chip de contexto sob cada número-destaque, contador de página em badge, brilho no topo do card |
| A resposta à pergunta "qual é a primeira diferença visual" está registrada para os quatro modos | OK | `escolhas-visuais.md`, seção "Resposta à pergunta de validação do prompt" — nenhuma resposta é "só a cor" |
| Nenhum número, filtro, download ou regra de interação quebrou na reconstrução | OK | Filtro cruzado, seleção da matriz, ordenação de tabela, download .xlsx/.pptx e navegação de slides retestados após a reestruturação — 9/9 checagens aprovadas |
| A auditoria final rodou de novo, completa, com quantas rodadas precisou | OK | Rodada 5 (v3): 1 rodada, 0 achados bloqueantes |

**Veredito: APROVADO.**

## Adendo — v4, o Painel vira o enxerto real do arquivo (27/09/2026)

A skill `entrega-dmaic` corrigiu `references/montador.md`: o Painel não
pode ser recriado com os componentes desta skill usando as cores extraídas
do arquivo — tem que ser a **marcação real** do HTML baixado do Montador,
populada com os dados do projeto. A v3 ainda recriava os cinco blocos do
Painel com `.card`/`.kpis`/gráficos SVG desta skill; nesta rodada o
`<body>` inteiro de `artefatos/montador-clinica-aurora-operacao.html` foi
transplantado para dentro do Painel — a mesma grade de 12 colunas, os
mesmos cinco `<section>`, com os números e textos de exemplo trocados
pelos do pipeline e `.sim`/`.tec` acrescentados a cada texto estático. Os
dois gráficos (Pareto, Barras agrupadas) passaram a ser desenhados pelo
motor original do arquivo (ECharts), não mais pelas funções SVG desta
skill. Dashboard, Relatório e Slides não foram tocados. **Nenhum número
mudou.** Detalhe completo, incluindo os 3 defeitos visuais achados e
corrigidos testando ao vivo (rótulos do Pareto, "80%" duplicado, fundo
claro vazando no cabeçalho da tabela), em `artefatos/escolhas-visuais.md`
(adendo v4) e na Rodada 6 de `artefatos/relatorio-auditoria.md`.

### Tollgate ENTREGA (visual) — v4

| Critério | Veredito | Motivo |
|---|---|---|
| O Painel é a marcação real do arquivo baixado, não uma recriação com os componentes desta skill | OK | `<body>` de `montador-clinica-aurora-operacao.html` transplantado como está; só o `:root` virou `#painel-enxerto` (escopo, ver adendo) |
| Nenhum resto de exemplo do gerador original; nenhum número digitado à mão | OK | Todos os 5 blocos lêem `paretoTaxa`/`TIPO`/`DIST`/`cubo` (as mesmas variáveis do Dashboard) |
| Nenhum bloco vazio sem justificativa | OK | Os 5 espaços têm dado real — nenhum precisou de "— vazio —" |
| Os dois registros de linguagem funcionam dentro do enxerto | OK | `.sim`/`.tec` em todo texto estático, controlados pelo `data-reg` já existente |
| Dashboard, Relatório e Slides mantidos exatamente como estavam, só com os tokens | OK | Nenhuma edição fora do Painel nesta rodada |
| Contraste conferido de novo, claro e escuro | OK | `importar_estilo.py` rerodado; Painel é sempre escuro por design (kit sem contraparte clara), documentado |
| Auditoria final rodou de novo | OK | Rodada 6: 3 achados corrigidos na própria rodada, 8/8 checagens na repetição |

**Veredito: APROVADO.**
