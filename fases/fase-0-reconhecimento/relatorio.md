# Fase 0 · Reconhecimento — Absenteísmo no Trabalho

Data: 26/09/2026 · Janela de dados: base inteira (jul/2007–jul/2010, 740 linhas) · v1

## Em três linhas

Reconstruí o processo que gera cada linha, confirmei que a granularidade é mista
(evento de ausência dentro de funcionário) e mais irregular do que o previsto — um
ID (29) mistura dois funcionários fisicamente diferentes — e que "Work load
Average/day" e "Hit target" são mesmo variáveis de nível-mês/empresa, não de
funcionário, evidenciado pela contagem de valores distintos por mês (≈3, batendo
com os 3 anos que a base cobre sem coluna de ano). Encontrei ainda 34 linhas
duplicadas e 43 linhas com "Reason for absence" = 0, quase todas ligadas a
falta disciplinar. Tollgate: **APROVADO com ressalvas** — nenhuma delas impede
seguir para o Define, mas todas mudam decisões concretas lá.

## O que foi feito

1. Perfilamento estrutural do CSV bruto com `scripts/00_reconhecimento.py`
   (forma, tipos, nulos, duplicatas, constância de atributos por ID, contagem de
   valores distintos de Work load/Hit target por mês, resíduo da fórmula de BMI,
   distribuições de categóricas). Saída completa em
   `artefatos/perfil_estrutural.json`.
2. Leitura de `data/raw/Attribute Information.docx` para confirmar a definição
   oficial de cada coluna (categorias do "Reason for absence", codificação de
   "Day of the week", "Education").
3. Busca de fontes oficiais (Banco Central e IBGE) para a linha do tempo de
   eventos externos.

Nenhuma correlação, cruzamento ou teste de relação entre colunas foi feito nesta
fase (F9) — só estrutura, procedência e granularidade.

## 1 · SIPOC reverso

| Etapa | Descrição | Evidência |
|---|---|---|
| Fornecedor | O funcionário (gera o evento de ausência) e a área médica/administrativa da transportadora (registra e classifica) | [INFERÊNCIA] |
| Entrada | Comparecimento esperado ao trabalho num turno programado | [INFERÊNCIA — não há coluna de escala ou turno] |
| Processo | Evento de ausência ocorre → é classificado por motivo (CID ou administrativo) → é registrado com data (mês/dia/estação), duração em horas e se houve falta disciplinar | [EVIDENTE NO DADO] as colunas Reason for absence, Month of absence, Day of the week, Disciplinary failure, Absenteeism time in hours |
| Saída | Um registro de ausência com motivo, duração e enquadramento disciplinar | [EVIDENTE NO DADO] |
| Cliente | A gestão de RH/operações da transportadora, que precisa cobrir o turno e decidir se há penalidade | [INFERÊNCIA] |

Etapas que o dado **não registra** (F1): quem substituiu o funcionário ausente,
se houve atestado médico anexado (só o código CID), a escala/turno original, o
custo da ausência para a operação, e — crucial para Seis Sigma clássico — os
dias efetivamente trabalhados (não há denominador para taxa).

## 2 · Linha do tempo de uma unidade (F2 — vazamento)

Narrativa de uma linha: o funcionário já existe com seus atributos fixos
(Transportation expense, Distance, Service time, Age, Education, Son, Social
drinker/smoker, Pet, Weight, Height, BMI) → ocorre a ausência → ela é
classificada por motivo → é registrada com mês, dia da semana e estação → é
somada em horas → se for falta sem justificativa aceita, "Disciplinary failure"
é marcado.

Duas perguntas específicas:

- **Alguma medida já está líquida de outra?** Sim — "Body mass index" é
  calculado de "Weight" e "Height" (IMC = peso / (altura/100)²). Recalculei e o
  resíduo é menor que 1 unidade em 98,6% das linhas (artefatos/perfil_estrutural.json,
  `circularidade_bmi`) — a diferença residual é só arredondamento. **As três
  colunas contam como uma evidência só**, nunca três preditores concorrentes
  (regra do contexto mestre).
- **Que colunas só existem após o desfecho?** "Disciplinary failure" e
  "Absenteeism time in hours" só podem ser preenchidas depois que a ausência
  aconteceu e foi avaliada — nenhuma das duas é utilizável como preditor de si
  mesma nem de "Reason for absence" (que é concomitante). Isso não é vazamento
  neste projeto porque não há modelo preditivo de curto prazo sendo construído,
  mas fica registrado para a fase de Modelagem, se houver.

Não há coluna com timestamp de registro (data de digitação) versus data do
evento — não dá para medir atraso de registro.

## 3 · Teste de armadilha prioritária — granularidade e circularidade

Esta é a armadilha mais grave detectada e muda decisões de Define e Measure.

**3.1 A granularidade é mais irregular do que o contexto mestre assumia.**
Testei se cada "atributo fixo do funcionário" é de fato constante dentro do
mesmo ID. Onze de doze colunas são constantes para 35 dos 36 IDs. O **ID 29**
quebra a regra em todas elas ao mesmo tempo: 1 linha tem Age=28, Height=169cm,
Weight=69kg, Education=1 (ensino médio), Son=1; as outras 4 linhas do mesmo ID
têm Age=41, Height=182cm, Weight=94kg, Education=4 (mestrado/doutorado), Son=2.
Uma pessoa não cresce 13cm nem envelhece 13 anos em uma janela de 3 anos — isso
não é deriva natural de atributo (o que seria esperado para Age ou Service time
crescendo 1–3 no período), **é o mesmo número de ID reaproveitado para duas
pessoas fisicamente diferentes** [DADO, alta confiança — 3 colunas
antropométricas incompatíveis simultaneamente]. Efeito prático: os "36
funcionários" da ficha são na verdade 37 pessoas; o holdout aleatório
estratificado por ID (regra do contexto mestre) vai colocar as 5 linhas do ID 29
inteiras de um lado do corte, misturando duas pessoas — **decisão a levar ao
Define**: dividir ID 29 em 29a/29b pela combinação de Age/Height/Weight, ou
excluir a linha minoritária (a única com o perfil "jovem") e documentar a perda
de 1 registro.

**3.2 Work load Average/day e Hit target são de nível-mês (provavelmente
empresa), não de funcionário — confirmado, não só suspeitado.** Dentro do mês
mais frequente (87 linhas), "Work load Average/day" assume só 3 valores
distintos e "Hit target" também só 3 — para dezenas de funcionários diferentes
no mesmo "Month of absence". Isso é exatamente o padrão esperado se a coluna é
uma métrica da operação inteira, medida uma vez por mês-calendário, e a base
cobre **3 anos sem coluna de ano**: "Month of absence" = 7 mistura julho/2007,
julho/2008 e julho/2009, cada um com seu próprio valor de carga de trabalho —
daí os ~3 valores por rótulo de mês (média de 2,92 valores distintos por mês em
13 categorias de mês, incluindo o mês "0"). **Consequência para o Define**:
estas duas colunas não podem entrar como preditor por linha de um modelo de
funcionário sem, no mínimo, ser tratadas como efeito de período partilhado —
usá-las lado a lado com atributos de funcionário como se fossem da mesma
natureza é outra camada da armadilha de granularidade misturada, exatamente como
o contexto mestre já antecipava, e este teste a confirma.

**3.3 Qualidade adicional que emergiu da checagem estrutural (não corrigida
aqui — registrada para o Measure 2A):**
- 34 linhas são duplicatas exatas nas 21 colunas; olhando o grupo completo
  (contando também a primeira ocorrência), 60 linhas pertencem a algum grupo
  duplicado, concentradas em só 9 IDs. Ex.: ID 3 repete a combinação
  (Reason=27 "consulta odontológica", mesmo mês, mesmo dia da semana, mesma
  duração) várias vezes. Pode ser (a) coincidência plausível — poucos valores
  possíveis por evento de rotina curto — ou (b) duplicação de digitação. Não
  decido isso aqui: é tarefa da auditoria de qualidade (Measure 2A, dimensão
  Unicidade).
- "Reason for absence" = 0 aparece em 43 linhas. O valor 0 **não existe** na
  lista oficial do UCI (que vai de 1/I a 28); ele coincide com "Disciplinary
  failure" = 1 em 40 dessas 43 linhas (as outras 3 têm também "Month of
  absence" = 0 e 0 horas de ausência — parecem registros administrativos
  incompletos, não eventos de ausência de fato). Ou seja: **falta disciplinar
  não usa código CID nem o código 26 ("unjustified absence")** — usa um valor
  reservado (0). Isso é central para a definição de defeito no item 5.

## 4 · Atores e incentivos (F3)

- **O funcionário** decide se falta e escolhe (ou recebe) o motivo declarado.
  Incentivo: motivos médicos (CID) não geram punição; "unjustified absence"
  (26) e o valor reservado 0 (ligado a "Disciplinary failure") geram. Isso cria
  incentivo para que uma ausência ambígua seja registrada com CID sempre que
  possível — um viés de registro que nenhum teste estatístico revela sozinho
  (F3), e que a instituição não teria como policiar sem exame médico
  presencial.
- **Quem classifica e digita o motivo** (RH ou área médica, [INFERÊNCIA] — não
  há coluna que identifique o registrador) tem interesse em manter a
  consistência do CID informado, mas não necessariamente em auditar a
  veracidade do atestado.
- **A gestão direta** decide sobre "Disciplinary failure": aplica a falta
  disciplinar quando julga a ausência não justificada. Esse julgamento é a
  fonte mais provável do padrão descrito em 3.3 (reason=0 quase sempre junto de
  disciplinary=1).

## 5 · Defeito — candidatos e recomendação (F6)

| Candidato | Definição operacional | Vantagem | Problema |
|---|---|---|---|
| A — Falta disciplinar | Disciplinary failure = 1 | Já existe no dado, sem premissa inventada; liga a governança | Muito raro (40/740 = 5,4%) e é consequência de um julgamento humano prévio (circular com o próprio ato de punir), não uma medida direta do processo de ausência |
| B — Ausência sem lastro médico (evitável em potencial) | Reason for absence ∈ {0, 22, 23, 24, 25, 26, 27, 28} (falta disciplinar + as 7 categorias sem CID) vs. Reason ∈ {1..21} (capítulos CID) | Já existe no dado; separa o que é, em princípio, agendável/administrável (consulta, exame, falta injustificada) do que é doença atestada; acionável — RH pode agir sobre agendamento, não sobre doença | A fronteira tem zona cinzenta: "unjustified absence" (26, n=33) e reason=0 (n=43, ligado à falta disciplinar) não são a mesma coisa que "consulta médica" (23, n=149) ou "consulta odontológica" (28, n=112) — juntar as duas debaixo de "evitável" precisa de definição explícita de borda, feita no Define |
| C — Duração fora do padrão (limite de especificação) | Absenteeism time in hours acima de um limiar (ex.: 8h = 1 dia) | Casa com Cp/Cpk clássico | O limite não está no dado — precisaria ser declarado como premissa (ex.: "mais de 1 dia" ou "mais de 3 dias" segundo alguma norma trabalhista), e eu não tenho essa norma confirmada ainda |

**Recomendo o candidato B**, com a fronteira fina que falta ser resolvida no
Define: dentro de "sem lastro médico", separar "unjustified absence + falta
disciplinar" (claramente evitável, comportamental) de "consulta/exame/doação de
sangue/fisioterapia" (evitável só na forma — pode ser agendado fora do
expediente — não no mérito). Essa é a decomposição evitável/não-evitável que o
contexto mestre já define como o ângulo livre do projeto (ver item 9,
Saturação). O candidato A fica como sub-métrica dentro de B, não como defeito
principal, porque é raro demais para sustentar um Pareto sozinho (regra F6 e
critério 7 da triagem).

**Decisão de unidade (granularidade):** o defeito é definido no nível do
**evento de ausência** (a linha), não do funcionário. Um funcionário com uma
ausência evitável e nove legítimas tem 1 evento não conforme em 10, não uma
"pessoa não conforme" — evita a armadilha de tratar o funcionário inteiro como
unidade quando o que varia é o evento. Consequência: toda estatística de
posição sobre o funcionário (ex.: "funcionário X falta mais") precisa declarar
se é sobre contagem de eventos ou sobre horas somadas, porque um único evento
de 120h (o máximo observado) domina a soma sem dominar a contagem.

## 6 · CTQ (características críticas para o cliente do processo)

O "cliente" aqui é a operação da transportadora, que precisa de cobertura de
turno previsível. Tensão central: **reduzir a ausência evitável x não
desincentivar a ausência por doença real**. Um CTQ que otimizasse só "menos
horas de ausência" empurraria contra atestados médicos legítimos — exatamente o
guardrail permanente do contexto mestre. CTQs candidatos: (1) proporção de
eventos evitáveis sobre o total de eventos; (2) previsibilidade do dia da
semana em que a ausência evitável concentra (afeta escala); (3) tempo entre
eventos evitáveis por funcionário (frequência), separado da duração.

## 7 · Gemba documental — benchmarks a buscar

Não há taxa de absenteísmo calculável aqui (sem denominador de dias
trabalhados) — então benchmark de "taxa setorial de absenteísmo" **não é
comparável** a este dado, ainda que exista publicado. O que vale buscar:

- Termos: `"absenteísmo" "transporte de cargas" Brasil pesquisa CNT`,
  `FGV IBRE absenteísmo indicadores RH Brasil`, `"unjustified absence" logistics
  benchmark`, para meta **interna** (melhor quartil de funcionário/mês
  observado neste próprio dado), já que benchmark externo de taxa não se aplica.
- Tipo de fonte: pesquisas setoriais de RH (ex.: Fundação Instituto de
  Pesquisas Contábeis, Atuariais e Financeiras — FIPECAFI/USP; CNT — 
  Confederação Nacional do Transporte) e não boletins internacionais de "taxa
  de absenteísmo", que usam denominador diferente e país diferente.

## 8 · O que o dado não registra (e o efeito de cada ausência)

| Ausência | Efeito sobre o que se pode concluir |
|---|---|
| Dias efetivamente trabalhados / escala | Nenhuma taxa de absenteísmo é calculável; toda métrica é condicional a "dado que uma ausência ocorreu" |
| Ano da ocorrência | Sazonalidade mistura 3 anos; qualquer leitura de padrão por mês é hipótese, não conclusão fechada |
| Contrafactual (o que aconteceria sem a ausência) | Nenhum ganho de uma recomendação pode ser apresentado como líquido — a fase Improve precisa usar ponto de indiferença, não ganho bruto |
| Identificação de quem cobriu o turno / custo da cobertura | Não dá para monetizar o impacto operacional direto, só o tempo perdido |
| Registro médico além do capítulo CID (gravidade, recorrência da doença) | Não dá distinguir, dentro de um capítulo CID, doença aguda de crônica |

## 9 · Linha do tempo de eventos externos (F10)

O período (jul/2007–jul/2010) atravessa a crise financeira global de
2008–2009. Fontes oficiais:

| Data | Evento | Fonte |
|---|---|---|
| Set–dez/2008 | Selic mantida no pico de 13,75% a.a. (resposta inicial de cautela) | Banco Central do Brasil, Boletim/Relatório Anual 2009 |
| 4º tri/2008 | PIB brasileiro recua 3,6% (início da recessão técnica) | IBGE, Contas Nacionais Trimestrais |
| 1º tri/2009 | PIB recua mais 0,8% | IBGE, Contas Nacionais Trimestrais |
| Ao longo de 2009 | Selic cai de 13,75% para 8,75% a.a., em resposta à crise | Banco Central do Brasil |
| Ano de 2009 (fechado) | PIB do ano cai 0,2% ante 2008 (pior resultado desde 1992) | IBGE |
| 4º tri/2009 | Recuperação: PIB cresce 4,3% ante mesmo trimestre de 2008 | IBGE |

**[HIPÓTESE A VERIFICAR, não fato]:** se a recessão de out/2008–meados/2009
coincidiu com mudança na frequência ou no tipo de ausência (ex.: mais faltas
disciplinares por insegurança no emprego, ou menos ausência por medo de
demissão — os dois sentidos são plausíveis na literatura de risco moral e
incentivo, Varian/Pindyck-Rubinfeld), isso teria que aparecer nos meses que
caem dentro dessa janela. **O problema estrutural**: como "Month of absence"
não tem ano, não dá para saber se uma linha com mês=10 é outubro/2007,
outubro/2008 (auge da crise) ou outubro/2009. Ou seja, **a base não permite
testar esta hipótese com rigor** — só permite registrá-la como limitação e como
possível explicação rival qualitativa se algum padrão anômalo aparecer no
Analyze. Fica marcada aqui para não ser esquecida, e para não ser atribuída
depois a um "efeito de mês" sem esta ressalva.

## 10 · Tipo de projeto

**Diagnóstico** — entender onde e por que o processo de ausência varia, e
separar o evitável do não-evitável — não previsão. Confirma a leitura do
contexto mestre sobre saturação: o ângulo de regressão para prever
"Absenteeism time in hours" já foi exaustivamente explorado publicamente; este
projeto não constrói esse modelo. Não há modelo supervisionado central neste
projeto; `references/modelagem.md` não se aplica além de, eventualmente, um
modelo de efeitos mistos na fase Analyze para separar variação
entre-funcionário de variação dentro-funcionário — não para prever, para
decompor variância.

## 11 · Comparabilidade entre países

Não se aplica — um só país, uma só unidade (transportadora em Brasília).

## Registro de escolhas

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Defeito candidato recomendado | B — ausência sem lastro médico (CID vs. não-CID) | A — falta disciplinar isolada; C — limite de horas | A é raro demais para Pareto (5,4%); C exige premissa de limite que não tenho como sustentar ainda | `reason_for_absence_contagem` em artefatos/perfil_estrutural.json | F6 |
| Unidade de análise do defeito | Evento de ausência (linha) | Funcionário (linha agregada) | O que varia é o evento; agregar por funcionário already é decisão da fase de baseline, não do Define do defeito | Seção 3.1 e 5 deste relatório | F1, F6 |
| Tratamento do ID 29 | Registrar como achado a decidir no Define (dividir ou excluir) | Corrigir silenciosamente agora | Corrigir sem registrar violaria a regra de honestidade de portfólio — a decisão pertence a quem conduz o projeto | `constancia_atributos_por_id` em artefatos/perfil_estrutural.json | F5, regra 9 do contexto mestre |

## Números

Todos os números citados acima vêm de `artefatos/perfil_estrutural.json`,
gerado por `scripts/00_reconhecimento.py` a partir de
`data/raw/Absenteeism_at_work.csv` (740 linhas, 21 colunas, hash abaixo no
manifesto).

## Tollgate 0

| Critério | Veredito | Motivo |
|---|---|---|
| Processo reconstruível (triagem 1) | OK | SIPOC reverso montado, com etapas ausentes explicitadas |
| Unidade de análise (triagem 2) | RESSALVA | Granularidade mista confirmada e mais irregular que o previsto (ID 29); decisão final vai para o Define |
| Defeito definível (triagem 3) | OK | Candidato B recomendado, com fronteira a fechar no Define |
| Eixo temporal (triagem 4) | RESSALVA FORTE | Sem coluna de ano; carta de controle e holdout temporal ficam inviabilizados, conforme já previsto no contexto mestre |
| Dimensões de estratificação (triagem 5) | OK | Reason for absence, Day of the week, Seasons, Education, Disciplinary failure — ≥3 categóricas utilizáveis |
| Procedência (triagem 6) | OK, com ressalva pontual | Dado real e documentado (UCI); encontrado 1 ID corrompido (29) e 34 duplicatas exatas a resolver no Measure 2A |
| Volume x efeito (triagem 7) | A CALCULAR NO DEFINE | Depende do efeito mínimo acionável, ainda não definido |
| Teste do cheque (triagem 8) | OK | Gestor de RH/operações da transportadora pagaria para saber onde a ausência evitável concentra e agiria sobre agendamento/escala |
| Saturação (triagem 9) | OK | Ângulo de regressão preditiva descartado por saturação; ângulo de variação/capabilidade e decomposição evitável/não-evitável mantido como livre |

**Veredito: APROVADO com ressalvas.** As ressalvas (ID 29, granularidade de
Work load/Hit target, ausência de ano, 34 duplicatas, fronteira do defeito B)
não impedem o Define — mas cada uma vira uma decisão explícita lá, não um
detalhe a resolver depois.

## Pendências e riscos

- Decidir no Define: o que fazer com ID 29 (dividir em duas identidades ou
  excluir a linha minoritária).
- Decidir no Measure 2A: se as 34 linhas duplicadas são coincidência plausível
  ou erro de digitação — e o que fazer com cada caso.
- A fronteira exata do defeito B (o que entra em "evitável" além de 26 e do
  reason=0) precisa ser fechada e travada antes de qualquer contagem de defeito.
- A hipótese da crise de 2008–2009 não é testável com rigor nesta base (sem
  ano) — mantê-la só como explicação rival qualitativa, nunca como achado.

## Para a próxima fase

O Define recebe: o defeito candidato B com sua fronteira em aberto, a decisão
pendente sobre ID 29, a confirmação de que Work load Average/day e Hit target
são de nível-mês/empresa (não usar como atributo de funcionário sem tratamento
de efeito de período), e a lista de duplicatas a resolver no Measure — não
antes, porque resolver duplicata já é decisão de qualidade, não de escopo.
