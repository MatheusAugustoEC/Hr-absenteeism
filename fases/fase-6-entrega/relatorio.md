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
