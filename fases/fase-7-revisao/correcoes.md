# Correções da banca — execução

Data: 27/09/2026 · Prompt de correção: `fases/fase-7-revisao/prompt-correcao.md`
(parecer completo em `parecer.md`). Todos os itens abaixo foram executados,
na ordem do prompt. Nenhum bloco foi apagado do prompt original — todos os
7 achados importantes (I1-I7) e os 4 de acabamento (M1-M4) foram corrigidos.

## Regras seguidas

- Nenhum número sólido (conta de ganho da ação 2, ponto de equilíbrio de
  35,4%, separação atestado/administrável, bootstrap por cluster, holdout
  por ID, linguagem causal proporcional à evidência) foi tocado.
- Fase de origem refeita com `relatorio-v2.md` (sem apagar o original):
  `fases/fase-3-analyze/relatorio-v2.md` (I2 e I3, ambos pós-hoc, sem
  reabrir a Fase 3 original).
- O holdout (Fase 5 · Control) não foi tocado nem reaberto — I2 e I7
  (H5) rodam só sobre a amostra de exploração, e dizem isso explicitamente
  na página.
- Todo número que mudou foi conferido nos três modos (Dashboard, Relatório,
  Slides) e no PDF gerado do Relatório.
- Todo conteúdo novo do Dashboard (I5, I6, I7) entrou também no Relatório,
  nos mesmos termos e com a mesma ressalva.

## I1 — Rótulos sobrepostos no Pareto de horas do Relatório

**Antes:** rótulos do eixo X abreviados ("Consulta O.") e sem rotação —
"Consulta O." colidia com "Acompanhamento", que colidia com "Fisioterapia".
**Depois:** rótulos na íntegra, rotacionados -38°, margem inferior do
gráfico aumentada (52px → 68px, altura total 256 → 272). Conferido nos
três temas (claro, escuro) e em largura de celular — nenhuma sobreposição.
**Número:** nenhum mudou — só o leiaute do gráfico `paretoAcum` (usado em
`#rep-pareto`).

## I2 — Concentração de "consulta médica" testada (⚑ novo número)

**Antes:** 31,3% das horas administráveis / 31,0% dos eventos evitáveis
vinham de "consulta médica", sem checagem de concentração por funcionário.
**Depois:** mesmo desenho de H2 — excluídos, um de cada vez, os 3
funcionários com mais eventos de consulta médica. Resultado: 28,4%-33,8%
das horas, 27,2%-33,1% dos eventos, em nenhuma exclusão a participação cai
perto da média das outras categorias (~15%) — **não concentrado em poucos
funcionários**. Script `scripts/03b_pareto_concentracao_posthoc.py`,
artefato `fases/fase-3-analyze/artefatos/pareto_concentracao_posthoc.json`,
adendo em `fases/fase-3-analyze/relatorio-v2.md`.
**Número:** 31,3%/31,0% (baseline, não mudou) → nova faixa de robustez
28,4-33,8% / 27,2-33,1% acrescentada. Entrou no Relatório (seção 3, caixa
de destaque, e seção 15) e no Dashboard (nota do bloco "Onde está o tempo
perdido"). Pós-hoc, holdout não tocado.

## I3 — Distância a serviços de saúde como limitação declarada

**Antes:** a seção 14 (limitações) não mencionava que distância ao
trabalho pode ser proxy de distância a serviços de saúde.
**Depois:** confirmado que a base só tem `Distance from Residence to Work`
(nenhuma outra coluna de localização) — a explicação concorrente não pode
ser testada, só declarada. Item novo na seção 14 do Relatório, e uma frase
curta na seção 2 apontando para ele. Adendo em
`fases/fase-3-analyze/relatorio-v2.md`.
**Número:** nenhum mudou — só texto novo.

## I4 — Autoria na página e no README

**Depois:** rodapé fixo na lateral (visível nos três modos: Dashboard,
Relatório, Slides) e linha do README atualizados com
`<preencha: nome completo · URL do GitHub · URL do LinkedIn>`, porque nome
completo, GitHub e LinkedIn reais não estavam disponíveis nesta conversa.
**Pendência que fica registrada aqui, como o prompt pediu:** este campo
precisa ser completado à mão (`.autor` em `pagina/index.html`, linha do
README) antes de publicar a página.

## I5 — Recomendação também no Dashboard

**Depois:** bloco de 2 linhas logo abaixo do número-herói, com as duas
ações e status ("Trava no sistema — pronta" / "Piloto de agendamento —
proposto, ainda não confirmado") e um link que troca para o modo Relatório
e rola até a seção 2. Testado: o link funciona, chega à seção certa.
**Número:** nenhum novo — só reaproveita o que já estava na seção 2.

## I6 — n nas células do heatmap de distância (⚑ sem mudar percentual)

**Depois:** cada uma das 6 células da matriz tipo × distância mostra o
percentual (já existente) e o n (contagem de eventos) numa segunda linha —
ex. "62,4% / n=271". Os percentuais em si não mudaram, só ganharam o n ao
lado. Testado nos três temas.

## I7 — Tabela bruta trocada por padrão de dia da semana e mês

**Antes:** o bloco final do Dashboard era uma tabela densa
(motivo/distância/dia/eventos/horas), repetindo o que a matriz e os
Paretos já mostravam.
**Depois:**
- Tabela bruta movida para dentro de um `<details>` recolhível ("Ver a
  tabela detalhada") — continua existindo e alimentando o download .xlsx,
  só não é mais o conteúdo principal do bloco.
- Gráfico novo de dia da semana × tipo (atestado médico / administrável /
  sem justificativa), com o selo **"JÁ TESTADO — SEM EFEITO CONFIRMADO
  (H4)"** (âmbar) acima do gráfico, citando o efeito de 3,95 p.p. (abaixo
  do mínimo de 8 p.p.) já testado na Fase 3.
- Gráfico novo de mês do calendário × tipo, com o selo **"EXPLORATÓRIO —
  HIPÓTESE NOVA, NÃO TESTADA"** (vermelho) acima do gráfico. Hipótese H5,
  datada de 27/09/2026, registrada como pós-hoc — não estava no
  pré-registro da Fase 1. Verificado por cálculo da data da Páscoa que o
  Carnaval caiu em fevereiro nos três anos cobertos por este recorte
  (5/fev/2008, 24/fev/2009, 16/fev/2010) — não assumido, calculado.
- Os dois gráficos e os dois selos entraram também no Relatório (seção 3,
  duas subseções novas), com o mesmo texto de ressalva.
- Pipeline: `scripts/06_entrega_dados.py` ganhou o agregado
  `mes_por_tipo` (mês × tipo, a partir da mesma base
  `eventos_qualidade.csv`) — nenhum agregado existente foi alterado.
**Número:** os dois gráficos são conteúdo novo (contagens/percentuais por
dia e por mês, nunca antes exibidos) — não substituem nem contradizem
nenhum número já publicado. H5 não confirma nem vira recomendação de
negócio.

## M1 — Rótulo "meta 33%" → "meta 33,4%"

Corrigido no gráfico "Por funcionário" do Dashboard (`funcBar`) — o rótulo
agora usa uma casa decimal, batendo com o resto da página.

## M2 — Nota de efeito na ação 1 (seção 2 do Relatório)

Acrescentado: "Afeta até 39 eventos — 5,3% do total registrado (seção 7,
H3)" na linha da ação "Trava no sistema".

## M3 — Contraste de ângulo (README)

Nova seção "Por que este ângulo, e não o de sempre" no README, citando a
regressão de "Absenteeism time in hours" como a abordagem padrão da maioria
dos notebooks públicos com este dataset, e o ângulo deste projeto
(variação/estabilidade, decomposição evitável/não-evitável, agrupamento
correto por funcionário) como o contraste.

## M4 — `requirements.txt` com versões fixas

Gerado com `pip freeze` a partir do ambiente que rodou o pipeline com
sucesso durante toda esta sessão: pandas 2.3.3, numpy 2.3.3, scipy 1.16.2,
statsmodels 0.14.6, matplotlib 3.10.6, seaborn 0.13.2, python-docx 1.2.0,
markdown 3.11, xhtml2pdf 0.2.20, pytest 9.1.1.

## Depois das correções

- `scripts/06_entrega_dados.py` reexecutado (novo agregado `mes_por_tipo`)
  — `fases/fase-6-entrega/artefatos/dados_pagina.json` atualizado e
  reembutido na página.
- Auditoria final reexecutada com navegador real (Playwright):
  `fases/fase-6-entrega/artefatos/auditoria_v6_correcoes_banca.py` — 23/23
  checagens automáticas aprovadas (mecânica existente retestada sem
  regressão: filtro cruzado, seleção de matriz, ordenação, downloads
  .xlsx/.pptx, navegação de slides; mais os itens novos: bloco de
  recomendação, badges, gráficos novos espelhados no Relatório, autoria
  visível nos três modos); zero erros de console; busca literal confirma
  zero ocorrências de B1/B2/CID fora do glossário. Capturas em tema claro,
  escuro e mobile sem rótulo sobre dado. Detalhe completo na Rodada 7 de
  `fases/fase-6-entrega/artefatos/relatorio-auditoria.md`.
- `fases/indice.md` atualizado.

## Pendência que precisa de ação humana antes de publicar

**I4 não tem os dados reais do autor.** O placeholder
`<preencha: nome completo · URL do GitHub · URL do LinkedIn>` está na
página (lateral, visível nos 3 modos) e no README — substituir pelos dados
reais antes de publicar.
