# Fase 1 · Define — Absenteísmo no Trabalho

Data: 26/09/2026 · Janela de dados: base inteira, pré-holdout (736 eventos após exclusões, 34 identidades de funcionário com pelo menos 1 evento) · v1

## Em três linhas

Fechei o defeito B em duas subcategorias (B1 comportamental/disciplinar, B2
administrável na forma), decidi excluir 4 linhas (3 registros administrativos
sem evento real + 1 linha corrompida do ID 29), fixei a métrica primária como
proporção de eventos (não soma de horas) e pré-registrei 4 hipóteses — incluindo
a rival estrutural obrigatória — com holdout aleatório por funcionário definido
e ainda fechado. Tollgate: **APROVADO**.

## O que foi feito

1. Fechamento da fronteira do defeito B em duas subcategorias, a partir da
   contagem de "Reason for absence" já levantada na Fase 0.
2. Decisão sobre as 4 linhas problemáticas identificadas na Fase 0 (ID 29 e as
   3 linhas administrativas), com `scripts/01_define_escopo.py`.
3. Definição da métrica primária e secundária, dos guardrails, da persona, do
   escopo e do holdout.
4. Pré-registro datado das 4 hipóteses em `pre-registro.md` (IMUTÁVEL a partir
   deste commit).

Nenhuma relação entre colunas explicativas distintas foi testada nesta fase
(regra 2 do contexto mestre) — as contagens abaixo reagrupam uma única coluna
("Reason for absence") ou aplicam os critérios de exclusão já decididos, o que
é da mesma natureza das contagens estruturais já feitas na Fase 0.

## Decisões e por quê

### 1 · Persona de decisão (D2, D13, F7)

**Gestor de RH/operações da transportadora** [PREMISSA DECLARADA — stakeholder
simulado; nenhuma pessoa real foi consultada]. Decide sobre: (a) a política de
agendamento de consultas/exames/doação de sangue/fisioterapia (pode empurrá-los
para fora do expediente ou não), (b) a escala de cobertura de turno, e (c) o
enquadramento disciplinar de faltas sem justificativa. Decide com periodicidade
mensal (ciclo de escala), sobre um volume da ordem de 20 eventos/mês na base
observada. Se o resultado sair concentrado em **B2 (administrável)**, a ação é
mudar a política de agendamento (ex.: exigir agendamento fora do expediente
sempre que possível). Se sair concentrado em **B1 (comportamental)**, a ação é
revisar o processo de registro de falta disciplinar (H3) antes de qualquer ação
sobre o funcionário — a explicação mais simples testável primeiro é a de
processo, não de comportamento.

**Frase de honestidade para o README:** o stakeholder deste projeto é simulado;
suas premissas de decisão estão registradas aqui e em `pre-registro.md`, e
nenhuma recomendação da fase Improve deve ser lida como validada por um gestor
real.

### 2 · Problema em uma frase (D1)

"Em **736 eventos de ausência de 34 funcionários com pelo menos um evento no
período** (jul/2007–jul/2010, sem coluna de ano), **a proporção de eventos sem
lastro médico (defeito B)** está em **[a medir com intervalo de confiança na
Fase 2B — contagem bruta preliminar: 64,4% do total, sendo 9,8 p.p. B1
comportamental e 54,6 p.p. B2 administrável; DADO, sem IC. Correção de
26/09/2026, feita ao escrever a Fase 2B: a versão original deste relatório
somava errado (54,4%/44,6%) por erro de digitação — os números de
`artefatos/escopo_define.json` sempre estiveram corretos (B2=54,62%), só a
soma em prosa aqui estava errada]** quando a meta é
**[origem: benchmark externo de taxa não se aplica — não há dias trabalhados
para calcular taxa (Fase 0, seção 7); proponho meta interna — reduzir B2 ao
nível do melhor quartil de funcionário observado, mantendo B1 estável ou em
queda só se H3 mostrar concentração comportamental real, não artefato de
processo]**, representando **[impacto a quantificar na fase Improve, em horas
de cobertura de turno não planejada]** por **[período: mensal, dado o ciclo de
decisão da persona]**."

A contagem preliminar acima (54,4%) é uma contagem bruta de definição de
escopo — **não é o baseline**. O baseline com intervalo de confiança,
verificação de estabilidade (sem carta de controle por falta de coluna de ano,
conforme já registrado na Fase 0) e capabilidade é trabalho da Fase 2B, não
desta fase (regra 2 / F9).

### 3 · Definição operacional do defeito B e da métrica primária (D3)

**Fronteira fechada, sem zona cinzenta remanescente:**

| Subcategoria | Reason for absence | O que é | n (pós-exclusão) |
|---|---|---|---|
| B1 — comportamental/disciplinar | 0 (com Disciplinary failure=1) e 26 ("unjustified absence") | Ausência sem justificativa aceita | 72 |
| B2 — administrável na forma | 22, 23, 24, 25, 27, 28 (acompanhamento, consulta médica, doação de sangue, exame laboratorial, fisioterapia, consulta odontológica) | Evitável só na forma — pode, em princípio, ser agendado fora do expediente; não no mérito | 402 |
| CID (não-defeito) | 1–21 | Doença atestada por capítulo CID | 262 |

As duas subcategorias somadas formam o defeito B (474 eventos, 64,4% da
população limpa) e recebem **Paretos separados** na Fase 2B — não um único
Pareto agregado — porque a ação de RH sobre cada uma é diferente (D2): B1 é
questão de processo/comportamento, B2 é questão de agenda.

**Critérios de exclusão (D3), decididos e aplicados nesta fase:**

1. **3 linhas administrativas** (IDs 4, 8, 35): Month of absence = 0,
   Absenteeism time in hours = 0, Disciplinary failure = 0. Não têm mês, não
   têm duração, não têm enquadramento — nenhum indício de evento real de
   ausência. Excluídas da população de análise. **Efeito colateral
   registrado**: os IDs 4 e 35 tinham só essa linha na base inteira — ao
   excluí-la, essas 2 identidades de funcionário desaparecem da população de
   evento (por isso 34, não 36, identidades na Ficha desta fase). O ID 8 tinha
   uma segunda linha e permanece. Isso não é problema para a análise por
   evento (a unidade é o evento, e esses funcionários não contribuem nenhum),
   mas é uma ambiguidade a registrar: não sabemos se essas 3 linhas eram
   "funcionário sem ausência no período" (o que faria sentido excluir do
   numerador mas manter no denominador de uma taxa por funcionário) ou erro de
   digitação puro. Como este projeto não calcula taxa por funcionário (Fase 0,
   seção 7), a ambiguidade não afeta a métrica primária, mas fica registrada
   para quem for reusar esta base para outro fim.
2. **1 linha do ID 29** (Age=28, Height=169cm, Weight=69kg, Reason=0,
   Disciplinary failure=1, 0h): é simultaneamente a linha que quebrava a
   constância dos atributos fixos do ID 29 (Fase 0, 3.1) **e** um dos casos
   "reason=0/disciplinary=1/0h" (Fase 0, 3.3) — as duas armadilhas coincidem
   na mesma linha. Excluída, e não dividida em 29a/29b: dividir criaria uma
   identidade de funcionário com 1 único evento, degenerada para qualquer
   estratificação por ID; excluir é a solução mais simples que resolve as duas
   armadilhas ao mesmo tempo (regra 8 do contexto mestre) com perda de só 1
   evento em 740. As 4 linhas restantes do ID 29 (perfil Age=41/Height=182/
   Weight=94) permanecem como uma identidade única e agora consistente.

**Correção declarada sobre a Fase 0**: o relatório da Fase 0 (seção 3.3) dizia
que as "outras 3" linhas com reason=0 tinham 0 horas, implicando que as 40
linhas com Disciplinary failure=1 tinham horas variadas. Ao aprofundar para
esta fase, verifiquei que **todas as 43 linhas com reason=0 têm 0 horas**, não
só as 3 administrativas — incluindo as 40 ligadas a falta disciplinar. Isso é
consistente com "Disciplinary failure" sendo um enquadramento sem duração
associada, e reforça (não contradiz) a leitura de que reason=0 é um código
usado de forma diferente do resto da tabela. Não reabro o relatório da Fase 0
(tollgate já aprovado) — registro o refinamento aqui, com a evidência em
`artefatos/escopo_define.json`.

**Métrica primária:** proporção de eventos B (B1+B2) sobre o total de eventos
(736, pós-exclusão) — contagem, não soma de horas (Fase 0, seção 5: um único
evento de 120h domina a soma sem dominar a contagem). **Métrica
secundária/complementar:** horas por subcategoria, reportadas separadamente,
nunca somadas à contagem de eventos na mesma métrica.

**Granularidade:** evento é a unidade. Estatística "por funcionário" (ex.:
frequência de eventos B por pessoa) é sempre agregação explícita a partir do
evento, nunca lida direto da linha — e todo teste usa erro-padrão agrupado por
ID (regra de granularidade do contexto mestre).

### 4 · Métricas secundárias e guardrails (D5)

**Armadilha de otimização local nomeada:** uma recomendação que reduza a
proporção de eventos B pressionando comparecimento com atestado médico real
(categorias CID 1–21) é uma **falha de guardrail**, não um sucesso — mesmo que
a métrica primária melhore. É exatamente o guardrail permanente do contexto
mestre (presenteísmo custa mais que ausência).

**Guardrail de aceitação, não aspiração:** nenhuma recomendação da fase
Improve pode ser aceita se, na simulação de ganho, a proporção de eventos CID
sobre o total cair junto com a proporção de eventos B — isso sinalizaria
supressão de ausência legítima (funcionário deixando de tirar atestado por
pressão), não redução do evitável. Essa checagem é obrigatória em toda
recomendação que toque B1 ou B2.

### 5 · Hipóteses pré-registradas

Ver `pre-registro.md` (arquivo imutável, datado). Resumo: H1 (principal —
distância e eventos B2), H2 (rival estrutural obrigatória — composição de mix
por funcionário, testada antes de H1), H3 (artefato de registro do reason=0)
e H4 (padrão por dia da semana, origem teoria de domínio não verificada
localmente).

**Nota de processo (regra 9 — honestidade de portfólio):** ao escrever
`scripts/01_define_escopo.py` para calcular as exclusões desta fase, cheguei a
incluir, num primeiro rascunho, o cálculo de concentração por ID dos casos
"reason=0" — que é exatamente o teste planejado para H3. Percebi antes de
rodar o pré-registro que isso seria testar a hipótese antes dela estar escrita
e datada (regra 3), removi o cálculo do script (ver comentário no código) e
não usei o número para calibrar o efeito mínimo de H3. Registro isso
explicitamente porque é o tipo de deslize que a regra 3 existe para pegar, e
prefiro documentá-lo a escondê-lo.

### 6 · Anti-garimpo (D8, D9, D10)

Holdout aleatório estratificado por identidade de funcionário (34 identidades
pós-exclusão), proporção 75/25, semente fixa — ver `pre-registro.md` para o
texto completo e imutável. Correção Bonferroni para as 4 hipóteses: α = 0,0125
por teste.

### 7 · Escopo (D11)

**DENTRO:** decomposição evitável/não-evitável (B1 vs. B2 vs. CID); teste da
hipótese principal (H1) e da rival estrutural (H2) antes dela; teste do
artefato de registro (H3); teste do padrão por dia da semana (H4);
granularidade corrigida com erro-padrão agrupado por funcionário.

**FORA:** taxa de absenteísmo (sem denominador de dias trabalhados);
sazonalidade como conclusão fechada (sem coluna de ano); qualquer afirmação
causal sobre a crise financeira 2008–2009; previsão de "Absenteeism time in
hours" por regressão (saturado, Fase 0 seção 10); scoring de risco por
funcionário (n=34, insuficiente); tratamento das 34 linhas duplicadas exatas
da Fase 0 (decisão adiada para o Measure 2A); uso de Work load Average/day ou
Hit target como atributo por linha de funcionário sem tratamento de efeito de
período compartilhado.

**A DECIDIR → decidido nesta fase:** a ambiguidade que a Fase 0 deixou em
aberto (métrica de contagem vs. horas) foi fechada no item 3 acima: contagem é
primária, horas é secundária/guardrail.

### 8 · Critério de sucesso (D12)

Ver `pre-registro.md`, seção final — resumo: a decomposição evitável/
não-evitável feita com este rigor de granularidade é o achado central, e vale
mesmo que H1 e H4 sejam refutadas.

## Registro de escolhas

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Tratamento do ID 29 | Excluir a linha minoritária (1 evento) | Dividir em 29a/29b | Divisão criaria identidade de funcionário com n=1, degenerada para holdout estratificado por ID; exclusão resolve as duas armadilhas (granularidade + reason=0/0h) que coincidem nessa linha | `artefatos/escopo_define.json`, `excluidos.id29_linha_minoritaria` | regra 8 do contexto mestre |
| Tratamento das 3 linhas administrativas | Excluir da população de evento | Manter como eventos de 0 horas | Não têm mês nem enquadramento — nenhum indício de evento real; manter inflaria a contagem de "eventos" sem um evento de fato ter ocorrido | `artefatos/escopo_define.json`, `excluidos.administrativos_month0_hours0` | D3 |
| Métrica primária | Proporção de eventos (contagem) | Soma de horas; as duas em métrica composta | Um evento de 120h domina a soma sem dominar a contagem (Fase 0); contagem é mais robusta a outlier de duração | Fase 0, seção 5; `artefatos/escopo_define.json`, `horas_describe_por_categoria` | D3 |
| Estrutura do defeito B | Duas subcategorias com Pareto separado (B1, B2) | Um único Pareto agregado | A ação de RH é diferente para cada uma (processo de registro vs. agenda); agregar esconderia essa diferença | Fase 0, seção 5; este relatório, item 3 | F6, D3 |
| Correção para múltiplos testes | Bonferroni (α=0,0125, 4 testes) | Benjamini-Hochberg | Poucas hipóteses (4), todas decisivas para a recomendação final, nenhuma é exploração ampla | `pre-registro.md` | D10 |

## Números

Todos os números desta fase vêm de `artefatos/escopo_define.json`, gerado por
`scripts/01_define_escopo.py` a partir de `data/raw/Absenteeism_at_work.csv`
(o mesmo arquivo hash-verificado na Fase 0). A base limpa pós-exclusão (sem
nenhuma relação entre variáveis aplicada) foi salva em
`data/processed/eventos_limpos.csv` para uso nas fases seguintes.

## Tollgate DEFINE

| Critério | Veredito | Motivo |
|---|---|---|
| Fronteira comportamental/administrável fechada, sem zona cinzenta | OK | B1={0,26}, B2={22,23,24,25,27,28}, sem sobreposição, com Pareto separado por subcategoria |
| ID 29 com decisão registrada, datada, tratada como pré-registro | OK | Exclusão da linha minoritária, registrada em `pre-registro.md` e neste relatório |
| Métrica primária declarada com razão | OK | Contagem de eventos, horas como secundária — razão registrada no item 3 |
| 3 a 5 hipóteses pré-registradas, direcionais, com origem, teste e efeito mínimo | OK | 4 hipóteses em `pre-registro.md`, incluindo rival estrutural (H2) e hipótese sobre reason=0 (H3) |
| Guardrail contra supressão de ausência médica como regra de aceitação | OK | Item 4 — regra explícita, não aspiracional |
| Holdout descrito de forma operacional | OK | Aleatório por 34 identidades, 75/25, semente fixa, em `pre-registro.md` |

**Veredito: APROVADO.** Nenhum critério do tollgate ficou em ressalva. A única
observação de processo (o quase-garimpo de H3, corrigido antes do
pré-registro) está documentada acima e não compromete o pré-registro
resultante.

## Pendências e riscos

- Os IDs 4 e 35 desaparecem da população de evento após a exclusão das linhas
  administrativas — se uma fase futura precisar de uma métrica "por
  funcionário" que inclua funcionários sem nenhum evento evitável, essa
  ausência precisa ser revisitada (não é o caso deste projeto, mas fica
  registrado).
- O baseline real da proporção de eventos B (com intervalo de confiança) só
  sai na Fase 2B — o número preliminar citado no item 2 é contagem bruta, não
  conclusão.
- As 34 linhas duplicadas exatas da Fase 0 continuam sem decisão — Measure 2A.

## Para a próxima fase

O Measure 2A recebe: a base limpa (`data/processed/eventos_limpos.csv`, 736
eventos, 34 identidades), a fronteira B1/B2/CID travada, e a lista de
duplicatas da Fase 0 para decidir. O Measure 2B recebe a métrica primária
(proporção de eventos B) e secundária (horas por subcategoria) já definidas,
prontas para baseline com intervalo de confiança — sem carta de controle, pela
ausência de coluna de ano já registrada na Fase 0.
