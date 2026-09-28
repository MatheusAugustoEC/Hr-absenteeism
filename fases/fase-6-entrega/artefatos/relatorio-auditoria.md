# Relatório de auditoria — Fase 6 · Entrega (v5, reconstrução do zero)

Data: 27/09/2026 · Ferramenta: Playwright (Chromium real, headless), servindo a página por `python -m http.server` — não como `file://`.

## Contexto

Esta é a reconstrução completa da Fase 6, a partir de uma decisão explícita do usuário: sem alternância Simples/Técnica (um só registro, em linguagem simples, com o rigor técnico reunido numa seção própria — "Notas técnicas"), sem o modo Painel (a função de abertura do X foi incorporada ao topo do Dashboard), navegação e filtros na lateral (filtros só ativos no modo Dashboard), e cada gráfico do Dashboard com uma frase de leitura ("insight"), não só o número cru. Downloads (.xlsx/.pptx/PDF) e a mecânica de interação (`references/interacao.md`) continuam as mesmas da skill. Nenhum número foi inventado — todos vêm de `artefatos/dados_pagina.json`, gerado por `scripts/06_entrega_dados.py` a partir dos artefatos congelados das Fases 0-5.

## Como foi feito

Servida a página localmente, percorridos os três modos (Dashboard, Relatório, Slides), os dois temas (claro/escuro) e duas larguras (desktop 1400px e mobile 390px). Console lido em cada etapa — erro é bloqueante, por regra da skill (`references/auditoria.md`).

## Rodada 1

Script: `auditoria_v5_reconstrucao.py`. Checagens: dropdown abre/marca/permanece aberto, filtro gera etiqueta removível, contador atualiza, seleção de matriz (marca e desmarca), ordenação de coluna da tabela, "Mostrar todas", download `.xlsx` (> 1 KB), "Limpar filtros" zera a seleção, bloco de filtros da lateral escondido fora do Dashboard, navegação de slides até 9/9, download `.pptx` (> 1 KB), manchete idêntica entre Dashboard e Slide 1, busca literal de B1/B2/CID (nenhuma ocorrência — o glossário desta versão nem cita os códigos internos, só os nomes descritivos), zero erros de console.

**Achado (não bloqueante para as checagens automáticas, mas visual, confirmado por captura): no modo Slides, em largura de celular, o selo "1 / 9" (posicionado de forma absoluta no canto do quadro) sobrepunha a última linha do parágrafo em quadros com texto mais longo (quadros 1 e 9 testados) — a `aspect-ratio:16/9` do cartão do slide, numa tela estreita, deixava pouca altura para o texto, e o selo ficava por cima da última linha.**

Corrigido: em telas até 900px, o cartão do slide deixa de ter proporção fixa (`aspect-ratio:auto; min-height:300px`) e o selo de página vira parte do fluxo normal do texto (`position:static`), em vez de sobreposto — a mesma solução já usada na versão impressa/PDF. Conferido de novo nos quadros 1 e 9 (os de texto mais longo): sem sobreposição.

**Resultado: 1 rodada, 1 achado (rótulo sobre texto no Slides/mobile), corrigido, reverificado sem novo achado.**

## Capturas

`capturas/dashboard-escuro.png`, `dashboard-claro.png`, `dashboard-mobile.png`, `relatorio-escuro.png`, `slide1.png`, `slide1-mobile.png` — nenhum rótulo sobre dado em nenhuma, filtros da lateral corretamente ausentes fora do Dashboard, guardrail (atestado médico) sempre em destaque verde, separado dos indicadores de problema.

## Lista de conferência (references/auditoria.md)

- Unidade presente em todo número (%, pp, h, eventos) — conferido.
- pp nunca chamado de porcentagem — conferido (seções 7, 8, 13, notas técnicas).
- Formatação pt-BR (vírgula decimal, ponto de milhar) — conferido nos números e no `nf()`.
- Mesmo número, mesmas casas decimais, em Dashboard/Relatório/Slides — checado para a manchete (64,3%); os demais números (35,7%, 733, +30,9 pp, 16,4 pp, 35,4%) são reaproveitados nos três modos a partir do mesmo objeto `DADOS`, nunca redigitados.
- Todo número diz a sua janela — a base é toda jul/2007–jul/2010, declarada no rodapé do Dashboard e na seção 1 do Relatório; a confirmação (holdout, n=8) é rotulada como segunda amostra em todo lugar que aparece (seção 13, Notas técnicas).
- Gráfico de mês não-temporal mantém o aviso "SEM ORDEM CRONOLÓGICA CONFIÁVEL" no próprio título.
- Rampa sequencial (matriz e barras) com contraste ≥2:1 nos dois temas — tokens reaproveitados e já testados nas rodadas anteriores desta fase (ver commits anteriores, mesma paleta Dark Glass/claro).
- Nenhum termo técnico sem explicação no corpo principal — todo termo (IC, poder estatístico, cluster, holdout) só aparece com número já contextualizado em português corrido; a explicação formal de cada termo está no Glossário e nas Notas técnicas.
- Nenhum resto de exemplo do molde — busca por textos de exemplo (título "MODELO", nomes de placeholder) não encontrou ocorrência.
- Ordem problema → solução → prova: Relatório abre com o tamanho do problema (seção 1) e a recomendação (seção 2) antes de qualquer prova; Slides têm X no quadro 1 e a recomendação no quadro 2.
- Nenhum controle que não reage, nenhum erro de console.

## O que ficou de fora (não bloqueante)

- A checagem de sobreposição automatizada (`assets/sobreposicao.js` da skill `banca-dmaic`) não foi rodada nesta rodada; a inspeção visual por captura, nos dois temas e larguras, não encontrou outra ocorrência além da já corrigida.

## Rodada 2 (ajustes de leiaute pedidos pelo usuário)

Data: 27/09/2026. O usuário pediu: aproveitar melhor a largura da página
(muito espaço vazio nas laterais), mover os filtros da lateral para o corpo
da página (a navegação entre modos continua na lateral), o botão "Limpar
filtros" ao lado dos filtros, remover o texto explicativo embaixo do
número nas caixas de KPI (só título e valor), títulos de KPI mais claros
por si só (sem depender do texto removido), e nenhuma "observação"
embutida no título/rótulo de um gráfico — observação vai no texto abaixo.

Mudanças: `.pane`/`.wrap` de 1080px para 1480px de largura máxima (o
Relatório manteve a coluna de leitura estreita, 74ch, centralizada dentro
do espaço maior); lateral reduzida a marca + navegação (200px); filtros
viraram um cartão no corpo do Dashboard, com os 5 menus numa linha e
"Limpar filtros" alinhado à direita da mesma barra dos filtros ativos;
caixas de KPI perderam a linha de texto embaixo, e três títulos foram
reescritos para não depender dela ("Distância da meta interna" →
"Distância da meta de ausência evitável", "Eventos no período" → "Eventos
de ausência", "Redução potencial" → "Redução potencial de eventos"); o
cabeçalho da matriz tipo × distância voltou a mostrar só "Mais perto" /
"Mais longe" (sem o "(até a mediana)"), e a explicação da mediana (25,5 km)
foi para o parágrafo de leitura abaixo do gráfico, junto do resto da
ressalva sobre poder estatístico.

**Achado (bloqueante) descoberto ao testar os filtros já movidos para o
corpo da página:** com os filtros dentro da grade de 12 colunas, o menu
suspenso de cada filtro (posicionado de forma absoluta) passou a ser
pintado **atrás** do cartão de gráfico seguinte na grade — clique numa
opção do meio ou do fim da lista acertava o cartão por trás, não a opção.
Causa: itens de grade CSS (`grid-column`) pintam na ordem do documento
quando não têm `z-index` próprio, então o cartão seguinte da grade cobria
o menu aberto do cartão de filtros, mesmo o menu tendo `z-index` alto —
o `z-index` só vale dentro do mesmo contexto de empilhamento, e o item de
grade em si não tinha um. Corrigido dando `z-index` ao item de grade que
contém o cartão de filtros (`position:relative; z-index:10` no `div.g12`
que envolve `.card.filters`), o que eleva todo o cartão — e o menu dentro
dele — acima dos vizinhos. Testado depois: as cinco opções de cada um dos
cinco menus, incluindo os itens no meio/fim da lista, aplicam o filtro
corretamente.

Reexecutado `auditoria_v5_reconstrucao.py` por completo depois da correção:
19 checagens automáticas aprovadas (a 20ª é uma expectativa errada do
próprio script de teste — contava 16 `h2` no Relatório, mas são 15 `h2`
mais o Glossário em `details`, que nunca foi um `h2` — não é um defeito da
página).

**Resultado: 1 rodada, 1 achado bloqueante (menu de filtro clicável no
cartão errado), corrigido, reverificado sem novo achado.**

## Rodada 7 (v6 — correções da banca, Fase 7)

Data: 27/09/2026. Escopo: os 7 achados importantes (I1-I7) e os 4 de
acabamento (M1-M4) do parecer da banca (`fases/fase-7-revisao/parecer.md`,
prompt executado em `fases/fase-7-revisao/prompt-correcao.md`). Detalhe
item a item em `fases/fase-7-revisao/correcoes.md`.

Script desta rodada: `auditoria_v6_correcoes_banca.py`. Checagens:

- I1: rótulos do Pareto de horas do Relatório sem sobreposição (rotação
  -38°, testado nos 3 temas).
- I5: bloco de recomendação presente no Dashboard, link troca de modo e
  rola até a seção 2 do Relatório.
- I6: as 6 células da matriz mostram percentual e n juntos.
- I7: os dois selos (âmbar "já testado", vermelho "exploratório") e os
  dois gráficos novos (dia da semana, mês) renderizam no Dashboard E no
  Relatório; a tabela bruta está dentro de um `<details>` recolhível, sem
  deixar de alimentar o `.xlsx`.
- I4: o rodapé de autoria aparece nos três modos (Dashboard, Relatório,
  Slides).
- Regressão completa da mecânica que já existia: filtro cruzado, seleção
  de matriz (marca/desmarca), ordenação de coluna, "Limpar filtros",
  download `.xlsx` e `.pptx` (>1 KB cada), navegação de slides até 9/9.
- Busca literal de B1/B2/CID: zero ocorrências (nem no glossário desta
  versão, que já descreve os termos sem citar os códigos internos).
- Manchete (64,3%) idêntica em todos os pontos onde aparece.
- Zero erros de console.
- Capturas em tema claro, escuro e mobile — nenhum rótulo sobre dado nos
  dois gráficos novos nem no rodapé de autoria.

**Resultado: 1 rodada, 23/23 checagens aprovadas, 0 achados novos.** Nenhum
defeito foi encontrado testando as correções da banca — diferente das
rodadas 1-2 desta fase, que cada uma achou e corrigiu 1 problema.

## Conclusão

Reconstrução completa da Fase 6 (v5): 1 rodada de auditoria, 1 achado visual (rótulo sobre texto no Slides/mobile), corrigido e reverificado sem novo achado. A mecânica herdada da skill (filtros, matriz, downloads) foi retestada do zero, já que a casca da página mudou por completo (lateral no lugar da barra superior, três modos no lugar de quatro, um só registro de linguagem).

Rodada 2, sobre os ajustes de leiaute pedidos em seguida: 1 achado
bloqueante (menu de filtro sobreposto por um cartão de grade), corrigido e
reverificado.

Rodada 7, sobre as correções da banca (Fase 7): 23/23 checagens aprovadas,
0 achados.

## Rodada 8 (v6, rodada 2 da banca — I1 reaberto)

Data: 28/09/2026. A banca conferiu a Rodada 7 numa segunda passada e
mediu — não só olhou — o gráfico de Pareto de horas do Relatório: a
correção de I1 na Rodada 7 tinha trocado rótulos abreviados por nomes
completos sem testar se cabiam rotacionados, e o número de colisões **subiu**
de 2 para 4. Corrigido com abreviação (função nova `abreviaMotivo()`,
que abrevia pela última palavra do nome, não a segunda — evita o "Doação
D." sem sentido que uma regra ingênua daria) + rotação maior (-38° → -60°)
+ gráfico mais largo (460px → 500px). Medido de novo com um script dedicado
(`checagem_sobreposicao_i1.py`, `getBoundingClientRect()` de cada rótulo +
teste de interseção de retângulo, não inspeção visual): **0 colisões** nos
três cenários (desktop escuro, desktop claro, celular).

M5 (sugestão do responsável, aceita pela banca) também entrou nesta
rodada: bloco "Por funcionário" movido para depois dos gráficos de dia/mês,
antes da tabela detalhada — confirmado lendo a ordem real do DOM.

`auditoria_v6_correcoes_banca.py` reexecutado por completo: 23/23,
zero regressão. Detalhe completo, com a tabela de colisões antes/depois,
em `fases/fase-7-revisao/correcoes.md`, seção "Rodada 2".

**Resultado: 1 rodada, 2 achados (I1 reaberto, M5), ambos corrigidos e
verificados por medição, 0 achados novos.**

## Conclusão (atualizada)

Oito rodadas de auditoria ao longo da Fase 6 e das duas rodadas de revisão
por banca: seis encontraram e corrigiram pelo menos 1 achado cada
(rótulos de gráfico, contraste, sobreposição de painel, menu de filtro,
correções de conteúdo da banca), duas terminaram limpas (0 achados). A
lição que atravessa o projeto: sobreposição de rótulo rotacionado não se
confirma "de olho" — as Rodadas 1, 2 e 8 encontraram exatamente esse tipo
de defeito depois de uma inspeção visual que tinha parecido suficiente; só
a medição de retângulo (`getBoundingClientRect()` + teste de interseção)
pegou o problema de forma confiável.
