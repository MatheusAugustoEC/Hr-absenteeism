# Fase 6 · Entrega — Absenteísmo no Trabalho

Data: 27/09/2026 · Página única publicável (Dashboard, Relatório, Slides), reconstruída do zero a partir de uma decisão explícita do usuário sobre formato · v5

## Em três linhas

A Fase 6 foi apagada e recomeçada do zero (commit anterior "Fase 6: removida
para recomeçar do zero"), depois de três rodadas de identidade visual (v2-v4)
que não chegaram a um formato satisfatório. O usuário pediu um formato
diferente do padrão de quatro modos/dois registros da skill `entrega-dmaic`:
sem Simples/Técnica (um só registro, em linguagem simples), sem o modo
Painel, navegação e filtros numa lateral fixa, e cada gráfico do Dashboard
com uma frase de leitura, não só o número cru. Construí a página assim,
mantendo a mecânica de interação e os downloads da skill intactos. Auditoria
com navegador real: 1 rodada, 1 achado (rótulo sobreposto no modo Slides em
celular), corrigido. Tollgate: **APROVADO**.

## Por que a reconstrução

Registrado em `fases/indice.md` e no histórico de commits: as versões v1-v4
desta fase tentaram, em sequência, (1) uma página completa no molde padrão
da skill, (2) recolorir com tokens do Montador de Dashboards só no Painel,
(3) propagar a grade do Montador para os quatro modos, e (4) enxertar a
marcação real do arquivo baixado do Montador no Painel. O usuário pediu
então para apagar tudo e recomeçar com um formato deliberadamente diferente — não
uma correção incremental das versões anteriores, mas uma decisão de escopo
nova, confirmada com perguntas de esclarecimento antes de qualquer construção
(ver "Plano aprovado" abaixo).

## Plano aprovado antes de construir

Perguntado e confirmado com o usuário, nesta ordem:

1. **Registro único**: só linguagem simples, sem termo técnico solto no
   corpo — números como IC 95%, poder estatístico e correção de Bonferroni
   ficam reunidos numa seção própria ("Notas técnicas"), não espalhados.
2. **Lateral fixa, filtros só no Dashboard**: a navegação entre os três
   modos fica sempre visível numa coluna lateral; o bloco de filtros
   (tipo/motivo/distância/dia/estação) só aparece ativo quando o modo é
   Dashboard — Relatório e Slides são leitura corrida, não exploração.
3. **Downloads e auditoria continuam iguais**: `.xlsx`, `.pptx`, PDF do
   relatório, e a auditoria de navegador real com até três rodadas.
4. Reforçado pelo usuário: **o Relatório continua no modelo X-Y-Z** —
   abre com o tamanho do problema (X), resolve com a recomendação (Z) na
   seção 2, e prova com as descobertas e o holdout (Y) no meio e no fim.

## O que foi feito

1. Pipeline reexecutado (`scripts/06_entrega_dados.py`, que sobreviveu à
   limpeza porque vive em `scripts/`, não em `fases/fase-6-entrega/`) —
   gerou `artefatos/dados_pagina.json` de novo, a partir dos mesmos
   artefatos congelados das Fases 0-5. Nenhum número mudou em relação às
   versões anteriores desta fase.
2. Página construída do zero: casca com lateral (marca, navegação de 3
   modos, filtros condicionais) + área de conteúdo; Dashboard abre com o
   número-herói e o guardrail (função que era do Painel, incorporada ao
   topo do Dashboard); cada bloco do Dashboard tem uma frase de leitura
   ("insight"), não só o gráfico.
3. Relatório com as 15 seções no modelo X-Y-Z + seção 15 "Notas técnicas"
   (todo IC, p-valor, poder estatístico e detalhe de método que estava nos
   registros Técnico das versões anteriores) + Glossário.
4. Slides: os mesmos 9 quadros de sempre, reescritos em linguagem simples,
   sem registro técnico paralelo.
5. Mecânica de interação (`references/interacao.md`) retestada do zero:
   filtros cruzados, seleção de matriz, ordenação de tabela, downloads.
6. Auditoria final com navegador real (Playwright) — ver
   `artefatos/relatorio-auditoria.md`.

## Nomenclatura (regra que sobrepôs tudo, mantida desde a v1)

| Nome interno (relatórios de fase) | Nome na página |
|---|---|
| B1 (comportamental/disciplinar) | Falta sem justificativa aceita |
| B2 (administrável na forma) | Ausência administrável |
| CID (1–21) | Atestado médico |
| Defeito B = B1+B2 | Parte evitável |

Confirmado por busca literal no HTML final: nenhuma ocorrência de B1, B2 ou
CID em texto visível — nem sequer no glossário desta versão, que descreve os
termos sem citar os códigos internos (mudança em relação às versões
anteriores, consistente com o objetivo de um texto só, para leigo).

## Narrativa X-Y-Z

- **X** (Dashboard, abertura do Relatório, slide 1): 64,3% [57,9%–69,1%] dos
  eventos de ausência não têm atestado médico por trás.
- **Z** (Relatório seção 2, slide 2): corrigir o registro (poka-yoke,
  pronto) e testar — não implementar — a priorização de agendamento por
  distância (piloto condicional, ponto de indiferença de 35,4%).
- **Y** (Relatório seções 3-13, slides 3-8): a maior parte é administrável
  (consulta, exame); uma fatia menor é falta sem justificativa, concentrada
  num atalho de registro disperso entre 20 funcionários (H3, confirmada); e
  há um sinal promissor, não confirmado, sobre distância (H1, 16,4 pp,
  reforçado a 9,5 pp numa segunda amostra).

## O que é específico deste projeto (mantido das versões anteriores)

- **Métrica primária**: proporção de eventos evitáveis, 64,26% [57,95–69,13%].
- **Meta**: interna (quartil de melhor desempenho, 33,36%) — sem benchmark
  externo válido.
- **Controle**: sem carta válida (M11) — tabela descritiva não temporal no
  Relatório, com o aviso na própria legenda do gráfico.
- **Guardrail**: proporção de atestado médico, com destaque verde próprio no
  Dashboard e no Relatório, separado dos indicadores de problema.
- **Matriz tipo × distância**: com o selo "achado promissor, não
  confirmado" e a frase completa de poder baixo + holdout sempre junto.
- **Barra por funcionário**: anonimizada ("Funcionário 1"..."34").

## Auditoria final

Ver `artefatos/relatorio-auditoria.md` — 1 rodada, 1 achado (rótulo do
contador de slide sobreposto ao texto em celular), corrigido, reverificado
sem novo achado.

## Tollgate ENTREGA

| Critério | Veredito | Motivo |
|---|---|---|
| Nenhuma ocorrência de B1/B2/CID em texto visível | OK | Busca literal confirma: zero ocorrências, inclusive no glossário |
| Narrativa X-Y-Z explícita no Dashboard, Relatório e Slides, mesma ordem e números | OK | Dashboard abre com X; Relatório abre com X e resolve com Z na seção 2; Slides 1-2 são X e Z |
| Guardrail com destaque visual próprio | OK | Cor verde (`--good`), separado dos indicadores de problema, no Dashboard e no Relatório |
| Filtros só ativos no Dashboard, lateral fixa nos 3 modos | OK | `#side-filtros` escondido fora do Dashboard, testado |
| Um só registro de linguagem, sem termo técnico solto no corpo | OK | Notas técnicas (seção 15) reúnem IC, poder, Bonferroni; corpo principal em português simples |
| Cada bloco do Dashboard tem uma frase de leitura, não só o número | OK | `.insight` presente em todos os 6 gráficos do Dashboard |
| Página com números vindos do pipeline, nenhum digitado à mão | OK | `dados_pagina.json` embutido, gerado por `scripts/06_entrega_dados.py` |
| Downloads e mecânica de interação intactos | OK | `.xlsx`/`.pptx` gerados e validados (>1KB), filtro cruzado, matriz, ordenação — retestados do zero |
| Auditoria final rodou, terminou sem bloqueante | OK | 1 rodada, 1 achado corrigido (ver relatorio-auditoria.md) |

**Veredito: APROVADO.**

## Pendências e riscos

- `requirements.txt` sem versões pinadas (dívida técnica já registrada na
  Fase 5, não específica desta página).
- A checagem automatizada de sobreposição (`assets/sobreposicao.js` da
  skill `banca-dmaic`) não foi rodada nesta rodada — a inspeção visual por
  captura, nos dois temas e larguras, não encontrou outra ocorrência além
  da já corrigida no Slides/mobile.

## Adendo — ajustes de leiaute (27/09/2026)

Depois da entrega, o usuário pediu quatro ajustes de leiaute, sem tocar em
nenhum número: (1) aproveitar melhor a largura da tela — a página estava
com muito espaço vazio nas laterais; (2) mover os filtros da lateral para
o corpo da página, mantendo só a navegação entre modos na lateral; (3)
"Limpar filtros" ao lado dos filtros; (4) tirar o texto explicativo de
baixo das caixas de KPI (só título e valor) e tornar os títulos claros o
bastante para dispensar esse texto; (5) nenhuma observação dentro do
título/rótulo de um gráfico — explicação vai no texto abaixo dele, nunca
dentro do desenho.

Aplicado: largura máxima do conteúdo subiu de 1080px para 1480px (o
Relatório manteve a coluna de leitura estreita, centralizada); a lateral
ficou só com marca e navegação; os filtros viraram um cartão no Dashboard,
com os 5 menus numa linha e "Limpar filtros" alinhado à direita da mesma
barra; as caixas de KPI perderam a legenda embaixo e três títulos
ficaram mais explícitos; o cabeçalho da matriz tipo × distância voltou a
mostrar só "Mais perto"/"Mais longe", com a explicação da mediana (25,5 km)
movida para o parágrafo de leitura abaixo do gráfico.

Testando os filtros já no novo lugar, apareceu um defeito real: o menu
suspenso de cada filtro, dentro da grade de 12 colunas, era pintado atrás
do cartão de gráfico seguinte — cliques no meio/fim da lista de opções
acertavam o cartão errado, não a opção do menu. Causa: itens de grade CSS
sem `z-index` próprio pintam na ordem do documento, então o `z-index` alto
do menu não bastava — precisava de um `z-index` no item de grade que
contém o cartão de filtros. Corrigido, reverificado nas cinco opções dos
cinco menus. Detalhe completo na Rodada 2 de
`artefatos/relatorio-auditoria.md`.

**Nenhum número mudou nesta rodada.**

## Adendo — correções da banca, Fase 7 (27/09/2026)

A banca (Fase 7 · Revisão) devolveu 7 achados importantes (I1-I7) e 4 de
acabamento (M1-M4) sobre esta página. Todos foram corrigidos, na ordem do
prompt de correção. Detalhe item a item, com antes/depois, em
`fases/fase-7-revisao/correcoes.md`. Resumo:

- **I1** rótulos sobrepostos no Pareto de horas do Relatório — corrigido
  (rotação, sem mudar número).
- **I2** (pós-hoc, ⚑) concentração de "consulta médica" testada com o
  mesmo desenho de H2 — não concentrada em poucos funcionários; baseline
  (31,3%/31,0%) não mudou, faixa de robustez nova acrescentada.
- **I3** limitação declarada: distância ao trabalho pode ser proxy de
  distância a serviços de saúde — sem número novo.
- **I4** rodapé de autoria nos três modos e no README — com placeholder,
  porque os dados reais do autor não estavam disponíveis nesta conversa;
  **pendência que precisa de ação humana antes de publicar**.
- **I5** recomendação (as duas ações) agora também no Dashboard.
- **I6** (⚑) n adicionado às 6 células da matriz de distância — percentuais
  não mudaram.
- **I7** tabela bruta do Dashboard virou `<details>` recolhível; dois
  gráficos novos (dia da semana × tipo, mês × tipo) com selos de status
  distintos ("já testado, sem efeito confirmado" / "exploratório, hipótese
  nova"), espelhados no Relatório. H5 (calendário) registrada como
  hipótese pós-hoc, não confirmada, não vira recomendação.
- **M1-M4**: rótulo de meta com uma casa decimal, nota de efeito da ação 1,
  contraste de ângulo no README, `requirements.txt` com versões fixas.

O holdout não foi tocado. `scripts/06_entrega_dados.py` ganhou um agregado
novo (mês × tipo) e foi reexecutado — nenhum agregado existente mudou.
Auditoria reexecutada: 23/23 checagens aprovadas, 0 achados novos (Rodada 7
de `artefatos/relatorio-auditoria.md`).

## Adendo — correções da banca, rodada 2 (28/09/2026)

A banca conferiu a rodada 1 numa segunda passada e **mediu**, em vez de só
olhar, o gráfico de Pareto de horas do Relatório: a correção de I1 tinha
piorado a sobreposição de rótulos (2 → 4 colisões), porque trocou rótulos
abreviados por nomes completos sem testar se cabiam rotacionados a -38°.
Corrigido com abreviação + rotação maior (-60°) + gráfico mais largo, e
**verificado com um script que mede `getBoundingClientRect()` de cada
rótulo e testa interseção de retângulo** (`checagem_sobreposicao_i1.py`) —
0 colisões nos três cenários (desktop claro/escuro, celular), não mais
"parece bom" numa captura. M5 (sugestão aceita pela banca) também entrou:
o bloco "Por funcionário" foi movido para o fim do Dashboard, depois dos
gráficos de dia/mês. Detalhe com a tabela de colisões antes/depois em
`fases/fase-7-revisao/correcoes.md`, seção "Rodada 2". Nenhum número
mudou. Auditoria: Rodada 8, 2 achados corrigidos, 0 achados novos.

## Para a próxima fase

A Fase 7 (revisão por banca) recebe o link da página publicada — numa
conversa nova, sem os bastidores deste projeto. A Fase 8 (Fechamento) recebe
esta página como fonte dos números finais do README.
