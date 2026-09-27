# Fase 2B · Measure — Baseline, estabilidade e capabilidade — Absenteísmo no Trabalho

Data: 26/09/2026 · Janela de dados: `data/processed/eventos_qualidade.csv` (733 eventos, 34 identidades — janela de exploração, holdout fechado) · v1

## Em três linhas

O baseline da proporção de eventos do defeito B é **64,3%** [57,95%–69,13%],
com o intervalo calculado por bootstrap agrupado por funcionário — bem mais
largo que o Wilson ingênuo, porque só há 34 clusters, não 733 observações
independentes. Omiti a carta de controle por regra (M11: no máximo 12 pontos
possíveis, abaixo do mínimo de 20-25), construí capabilidade contra meta
interna (quartil de melhor desempenho) e dois Paretos na mesma dimensão — com
uma régua alternativa obrigatória para B1, cujo impacto em horas é sempre
zero. O poder disponível para H1 e H4, calculado sobre 34 clusters, é **muito
baixo (≈3%)** — achado central desta fase para o Analyze. Tollgate:
**APROVADO**.

## O que foi feito

1. Baseline da métrica primária e secundárias, com IC por bootstrap de
   cluster (`scripts/02b_measure_baseline.py`).
2. Tabela descritiva não temporal por rótulo de mês, no lugar da carta de
   controle (justificado por regra, não por falta de coluna de ano apenas).
3. Capabilidade contra meta interna (quartil de melhor desempenho por
   funcionário).
4. Dois Paretos na mesma dimensão (Reason for absence detalhado), com régua
   alternativa para B1.
5. Cálculo de poder sobre o n efetivo de clusters (34 funcionários), não
   sobre 733 eventos.
6. Congelamento do baseline em `baseline-congelado.md` (IMUTÁVEL a partir
   deste commit).

**Correção declarada sobre a Fase 1**: ao calcular este baseline, percebi que
o `relatorio.md` do Define somava errado a proporção preliminar de B1+B2
("54,4%... 44,6% B2" — na verdade B2 era 54,62%, dando 64,4%, não 54,4%). O
`artefatos/escopo_define.json` sempre esteve correto; era um erro de digitação
na prosa do relatório. Corrigi diretamente o texto do `relatorio.md` da Fase 1
(não é artefato imutável — só o pré-registro e o baseline são) e registro
aqui, por transparência, que o número real sempre foi próximo de 64%, batendo
com o baseline formal desta fase (64,26%).

## Decisões e por quê

### 1 · Baseline (M6, M7)

Reportei a proporção com **dois** intervalos de confiança, deliberadamente:

- **Wilson ingênuo** (M7), tratando as 733 linhas como independentes:
  [60,72%; 67,64%] — **não usar para decisão**, porque ignora a granularidade.
- **Bootstrap agrupado por cluster**: reamostrei os **34 funcionários**
  inteiros (não eventos) 5.000 vezes, recalculando a proporção a cada
  reamostragem — [57,95%; 69,13%]. Este é o IC que orienta decisão, e é bem
  mais largo, confirmando que ignorar a granularidade (regra do contexto
  mestre) subestimaria a incerteza real.

DPMO e nível sigma: 642.565 DPMO, nível sigma -0,365 sem deslocamento (1,135
com o deslocamento convencional de 1,5σ, M16, reportado nos dois formatos).
Um nível sigma negativo ou próximo de zero é esperado aqui: o defeito B é
maioria do processo (64%), não uma exceção rara — o arcabouço DPMO/sigma foi
desenhado para defeitos raros e apresenta números pouco intuitivos quando o
"defeito" é a maioria. Isso não invalida a métrica de proporção (que continua
o número que importa para decisão), só mostra que DPMO/sigma é um
complemento formal aqui, não a métrica central do projeto.

Métricas secundárias — B1 em 9,82% [5,52%; 16,19%] e B2 em 54,43%
[44,68%; 61,75%] (M6, M17 — recalculadas a partir das contagens desta fase,
não copiadas do Define).

Horas por subcategoria (M6 — distribuição inteira, não só média): B1 tem
mediana **0h** (72% dos eventos B1 têm 0 horas — o achado da Fase 1/2A de que
reason=0/26 zeram a duração se reflete diretamente aqui). B2 tem mediana 2h,
cauda até 24h. CID tem a distribuição mais dispersa (desvio 20,48h, máximo
120h) — o outlier que a Fase 0 já havia identificado.

### 2 · Estabilidade — carta de controle omitida por regra (M8, M9, M11)

Não construí carta de controle. A justificativa não é só "não há coluna de
ano" — é uma regra quantitativa: mesmo ignorando a mistura de 3 anos
calendário no mesmo rótulo de "Month of absence", o máximo de pontos possíveis
seria **13** (rótulos 0 a 12), abaixo do mínimo de 20-25 subgrupos que M11
exige para limites estáveis. Forçar uma carta aqui produziria limites
instáveis demais para sustentar qualquer classificação de causa comum vs.
especial (M8).

No lugar, produzi uma **tabela descritiva não temporal** (proporção de B por
rótulo de mês), com o aviso de que não é série temporal escrito **na própria
legenda do gráfico** (`artefatos/tabela_nao_temporal_por_mes.png`), não só no
texto. A proporção varia de 53% (mês 5) a 81% (mês 9) — variação real, mas sem
significado cronológico atribuível, porque cada rótulo mistura até 3 anos.
Nenhum mês é tratado como sinal de causa especial.

### 3 · Capabilidade contra meta interna (M16)

Como não há benchmark externo de taxa (Fase 0, seção 7), a meta é a proposta
interna já registrada no Define: o quartil de funcionários com melhor
desempenho (8 dos 34, os 25% com menor proporção de eventos B) tem proporção
média de **33,36%** — bem abaixo do baseline agregado de 64,26%.

**Tradução em negócio**: ao ritmo observado (~13,1 eventos B por mês, numa
aproximação de 36 meses corridos para o período jul/2007–jul/2010 — o
denominador de meses é estimado, não contado, porque não há coluna de ano
exata), atingir o nível do quartil superior reduziria para ~6,8 eventos B por
mês — uma queda aproximada de **6,3 eventos evitáveis por mês**. Este número é
sobre o baseline agregado; não é o ganho líquido (isso é trabalho da fase
Improve, com ponto de indiferença, dado que não há contrafactual nesta base).

### 4 · Estratificação e Pareto (M17, M18)

Dimensão: **Reason for absence detalhado** dentro do defeito B (8 códigos: 0,
22, 23, 24, 25, 26, 27, 28) — não só B1/B2 agregado, para não perder onde
exatamente a ação de agenda deve mirar.

**Pareto de taxa** (`artefatos/pareto_taxa.png`): "consulta médica" (23, 31,0%)
e "consulta odontológica" (28, 23,8%) somam 54,8% dos eventos B sozinhas;
"fisioterapia" (27, 14,7%) leva a 69,5% acumulado. Os três primeiros códigos
(todos B2) já respondem por quase 70% do volume.

**Pareto de impacto em horas** (`artefatos/pareto_impacto_horas.png`) —
**armadilha declarada**: como 100% dos eventos B1 (reason 0 e 26) têm
Absenteeism time in hours = 0 (achado da Fase 1, reconfirmado na Fase 2A),
**B1 não pode aparecer neste Pareto** — apareceria com impacto zero, o que
esconderia o problema comportamental/disciplinar em vez de revelá-lo. O
Pareto de impacto foi construído **só com os 6 códigos de B2**: "consulta
médica" (31,3%), "consulta odontológica" (25,1%) e "acompanhamento" (22,0%)
somam 78,4% das horas de B2.

**Qual orienta a decisão**: para B2, os dois Paretos concordam nos dois
primeiros lugares (23 e 28 lideram taxa e impacto) — a recomendação da fase
Improve pode mirar esses dois com confiança dupla. Para B1, **a única régua
disponível é o Pareto de taxa** (contagem de eventos) — horas não existe como
métrica para esta subcategoria, e isso precisa ser dito toda vez que B1 for
discutido daqui em diante, para não ser lido como "B1 não tem custo".

### 5 · Tamanho de amostra e poder (M19)

Este é o achado mais importante desta fase para o que vem depois. O n efetivo
para os testes de H1 e H4 não é 733 (eventos) — é **34** (funcionários,
porque "Distance from Residence to Work" é constante por funcionário, e H4
precisa de agregação prévia por funcionário-dia para não inflar n). Com uma
divisão aproximada de 17 funcionários por grupo (mediana de distância) e a
correção de Bonferroni (α=0,0125):

| Hipótese | Efeito mínimo pré-registrado | Poder aproximado com n=17/grupo |
|---|---|---|
| H1 (distância × B2) | 10 p.p. | **≈2,9%** |
| H4 (dia da semana × B) | 8 p.p. | **≈2,7%** |

Poder de ~3% é dramaticamente abaixo do convencional (80%). **Isso não invalida
o pré-registro** — o efeito mínimo e o teste já estavam decididos antes de eu
calcular isso (regra 3, anti-garimpo) — mas significa que um resultado "não
significativo" em H1 ou H4 no Analyze **não pode ser lido como "não há
efeito"**: com este poder, a ausência de significância é quase garantida
mesmo que o efeito exista. O Analyze precisa reportar o efeito observado com
seu IC, não só o p-valor, e tratar qualquer "não significativo" como
inconclusivo, não como refutação (D6, M19).

**Recortes sem n suficiente** (menos de 15 eventos): "doação de sangue"
(Reason 24, n=3) — já antecipado como provavelmente raro desde a Fase 0.
Nenhum outro código de Reason ficou abaixo desse limiar.

### 6 · Código e gráficos

Gerados em `scripts/02b_measure_baseline.py` (números) e
`scripts/02b_graficos.py` (figuras): proporção com IC (`baseline_proporcoes.png`),
os dois Paretos (`pareto_taxa.png`, `pareto_impacto_horas.png`) e a tabela
não temporal (`tabela_nao_temporal_por_mes.png`, com o aviso na própria
legenda do título).

### 7 · Congelamento

Ver `baseline-congelado.md` — **IMUTÁVEL a partir deste commit**.

## Registro de escolhas

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Método de IC para a proporção | Bootstrap por cluster (34 funcionários) | Wilson padrão (M7) sobre 733 eventos | Wilson é a convenção (M7), mas ignora a granularidade — reportei os dois, e uso o bootstrap para decisão, seguindo a regra de granularidade que prevalece sobre a convenção quando conflitam | `artefatos/baseline.json`, `baseline_proporcoes` | M7, granularidade do contexto mestre |
| Ausência de carta de controle | Tabela descritiva não temporal | Carta I-MR ou p mensal forçada | Máximo de 13 pontos possíveis, abaixo do mínimo de 20-25 (M11) — mesmo ignorando a mistura de anos | Fase 0, seção 4; `artefatos/baseline.json` | M8, M9, M11 |
| Régua de impacto para B1 | Contagem de eventos (Pareto de taxa) | Forçar horas com valor 0 no Pareto de impacto | Reportar B1 com impacto-em-horas=0 esconderia o problema em vez de revelá-lo | `artefatos/baseline.json`, `pareto.nota_B1` | M18 |
| Denominador de meses para a tradução de capabilidade em negócio | 36 meses (aproximação) | Contar meses exatos do período | Sem coluna de ano não há como contar meses exatos — declarado como aproximação, não apresentado como contagem | `artefatos/baseline.json`, `capabilidade.nota_meses_periodo` | regra 5 do contexto mestre (nunca inventar número — aproximação declarada como tal) |

## Números

Todos os números vêm de `artefatos/baseline.json`, gerado por
`scripts/02b_measure_baseline.py` a partir de
`data/processed/eventos_qualidade.csv`. Gráficos em `artefatos/*.png`,
gerados por `scripts/02b_graficos.py`.

## Tollgate 2B

| Critério | Veredito | Motivo |
|---|---|---|
| Baseline com número, unidade e IC agrupado por funcionário | OK | 64,26% [57,95%;69,13%] por bootstrap de 34 clusters — não trata 733 eventos como independentes |
| Ausência de carta de controle justificada por regra | OK | M11: máximo 13 pontos possíveis, abaixo do mínimo de 20-25 |
| Capabilidade contra meta interna, com tradução em negócio | OK | Quartil superior = 33,36%; tradução ≈6,3 eventos evitáveis/mês a menos |
| Dois Paretos na mesma dimensão, com limitação de B1 declarada e régua alternativa | OK | Pareto de taxa (8 códigos) e de impacto em horas (6 códigos de B2); B1 fica só no Pareto de taxa, com a razão explícita |
| Poder calculado sobre n efetivo de clusters (34), recortes sem n listados | OK | Poder ≈3% para H1 e H4 com n=17/grupo; Reason=24 (n=3) sinalizado |
| Baseline congelado como artefato imutável, com data e filtros | OK | `baseline-congelado.md`, datado, com janela e filtros declarados |

**Veredito: APROVADO.**

## Pendências e riscos

- O poder muito baixo para H1 e H4 (~3%) é uma limitação estrutural do
  projeto (n=34 funcionários), não corrigível nesta base — o Analyze precisa
  reportar efeito e IC, nunca só significância, e isso precisa aparecer nas
  limitações do README.
- A tradução de capabilidade em "eventos por mês" usa uma aproximação de 36
  meses no período — se o responsável do projeto tiver uma contagem mais
  precisa (ex.: a partir da documentação original do UCI), isso deveria
  substituir a aproximação antes da Entrega.
- O erro de digitação corrigido no relatório do Define (item acima) não altera
  nenhuma decisão tomada — só a prosa que descrevia o número preliminar.

## Para a próxima fase

O Analyze recebe: o baseline congelado (64,26% de eventos B, com IC), os dois
Paretos com a régua diferenciada para B1, e — mais importante — o aviso de
poder baixo para H1 e H4, que muda como um resultado "não significativo"
deve ser interpretado. A ordem pré-registrada continua valendo: H2 (rival
estrutural) antes de H1, depois H3 e H4, com correção de Bonferroni
(α=0,0125). O holdout continua fechado.
