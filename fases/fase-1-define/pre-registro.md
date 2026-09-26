# Pré-registro — Fase 1 · Define

**Datado em 26/09/2026. Este arquivo é IMUTÁVEL a partir deste commit.**
Qualquer correção futura é adendo datado ao final do arquivo — nunca edição
silenciosa do que está abaixo. Ele existe para provar que as hipóteses,
o efeito mínimo e o corte de confirmação vieram antes de qualquer teste de
relação entre variáveis (regra 3 do contexto mestre; D8 da `metodo-dmaic`).

## Decisões de escopo que este pré-registro assume (fechadas nesta fase, ver
`relatorio.md` para o raciocínio completo)

- Defeito B = evento com "Reason for absence" fora dos capítulos CID (1–21),
  dividido em **B1 comportamental/disciplinar** (Reason ∈ {0, 26}) e **B2
  administrável na forma** (Reason ∈ {22, 23, 24, 25, 27, 28}).
- Excluídas da população de análise: 3 linhas com Month of absence = 0 e
  Absenteeism time in hours = 0 (IDs 4, 8, 35 — registros administrativos sem
  evento real) e 1 linha do ID 29 (Age=28/Height=169/Weight=69,
  Reason=0/Disciplinary failure=1/0h) — a linha que quebrava a constância dos
  atributos fixos do ID 29 na Fase 0. População final: **736 eventos, 36
  identidades de funcionário**.
- Métrica primária: **proporção de eventos B (B1+B2) sobre o total de eventos**
  — contagem, não soma de horas, porque um único evento de 120h domina a soma
  sem dominar a contagem (Fase 0, seção 5). Horas entram como métrica
  secundária/guardrail, reportada separadamente por subcategoria.
- Granularidade: evento (linha) é a unidade. Toda estatística "por
  funcionário" é obtida por agregação explícita a partir do evento, e todo
  teste usa erro-padrão agrupado por ID ou agregação prévia — nunca trata as
  736 linhas como independentes.

## Holdout — definido agora, aberto uma única vez na fase Control

**Aleatório estratificado por identidade de funcionário, sobre as 36
identidades já corrigidas** (não por linha isolada). Proporção 75/25:
aproximadamente 27 funcionários na janela de exploração, 9 na quarentena de
confirmação, sorteio com semente fixa registrada no manifesto desta fase para
reprodutibilidade. Declarado como **mais fraco que um corte temporal** (D9):
não testa estabilidade ao longo do tempo, só generalização entre funcionários.
Proibido de ser lido, carregado ou inspecionado antes da fase Control (regra
do contexto mestre).

## Correção para múltiplos testes

Quatro hipóteses pré-registradas abaixo, todas decisivas para o projeto
(nenhuma é exploração ampla de muitas variáveis) → **Bonferroni** (D10):
α ajustado = 0,05 / 4 = **0,0125** por teste.

## Hipóteses pré-registradas

### H1 — PRINCIPAL
**Enunciado direcional.** Entre os 402 eventos B2 (administráveis na forma:
consulta médica, exame, doação de sangue, fisioterapia, consulta
odontológica), a proporção de funcionários com "Distance from Residence to
Work" acima da mediana da amostra é maior do que entre os eventos CID (1–21),
em pelo menos 10 pontos percentuais.
**Origem.** [INSPEÇÃO ESTRUTURAL] — nasceu do CTQ da Fase 0 (deslocamento como
fricção de agendamento), não de teoria ou benchmark externo. Vale menos como
evidência causal, e isso fica registrado.
**Teste planejado.** Comparação de duas proporções (funcionários com distância
acima/abaixo da mediana) entre o grupo de eventos B2 e o grupo de eventos CID,
com erro-padrão agrupado por ID de funcionário (a distância é constante por
funcionário — regra de granularidade). Teste de proporções com correção de
cluster ou regressão logística com erro-padrão agrupado (cluster-robust por
ID).
**Efeito mínimo acionável.** 10 pontos percentuais de diferença — abaixo
disso, uma política de agendamento baseada em distância não mudaria decisão
de RH.

### H2 — RIVAL ESTRUTURAL (obrigatória, testada antes de H1)
**Enunciado direcional.** A diferença observada em H1, se existir, é
composição de mix: concentrada nos poucos funcionários com maior número total
de eventos (a distribuição de eventos por funcionário tem média 20,5 e desvio
23,7 — Fase 0), não um efeito causal da distância em si sobre o tipo de
evento.
**Origem.** [INSPEÇÃO ESTRUTURAL] — da própria forma da distribuição de
linhas por ID observada no perfilamento da Fase 0.
**Teste planejado.** Como "Distance from Residence to Work" é constante por
funcionário (não varia dentro do mesmo ID), o teste de composição de mix não
pode ser feito por decomposição dentro-de-funcionário. Em vez disso: (a)
recalcular o resultado de H1 excluindo, um de cada vez, os 3 funcionários com
mais eventos totais, e verificar se o efeito se sustenta; (b) comparar o
efeito bruto (todos os funcionários) com o efeito ponderado por funcionário
(cada ID conta uma vez, não uma vez por evento) — se divergirem, reportar a
versão ponderada por funcionário como a que orienta decisão (regra do
Paradoxo de Simpson, `armadilhas.md` item 4).
**Efeito mínimo acionável.** Se o efeito de H1 cair abaixo de 10 p.p. ao
excluir qualquer um dos 3 funcionários mais frequentes, ou se inverter entre a
versão bruta e a ponderada por funcionário, H1 é considerada não sustentada
pela evidência — é composição de mix, não fator causal.

### H3 — Artefato de registro (reason = 0)
**Enunciado direcional.** Os 39 eventos com "Reason for absence" = 0 e
"Disciplinary failure" = 1 (após excluir a linha do ID 29) estão dispersos por
muitos funcionários diferentes (mais de 5 IDs distintos respondendo por menos
de 50% dos casos cada), consistente com um código de registro administrativo
usado pontualmente, e não com um pequeno grupo de funcionários reincidentes.
**Origem.** [INSPEÇÃO ESTRUTURAL] — da Fase 0, seção 3.3.
**Teste planejado.** Distribuição de frequência dos 39 eventos por ID;
calcular a proporção do total concentrada nos 5 IDs mais frequentes nesta
categoria.
**Efeito mínimo acionável.** Se ≤ 5 funcionários responderem por mais de 50%
dos 39 casos, a hipótese é refutada (é comportamento concentrado, não
artefato disperso do processo) — o que muda o guardrail: passaria a exigir
acompanhamento individual, não só revisão do processo de registro.

### H4 — Padrão por dia da semana
**Enunciado direcional.** Os eventos do defeito B (B1+B2) concentram-se em
segunda-feira (Day of the week = 2) e sexta-feira (Day of the week = 6) mais
do que os eventos CID, com diferença de pelo menos 8 pontos percentuais na
distribuição por dia.
**Origem.** [TEORIA DE DOMÍNIO, não verificada localmente] — o padrão de
"emenda de fim de semana" é citado na literatura geral de gestão de pessoas,
mas não tenho experiência de domínio em RH/logística para confirmar que se
aplica aqui (contexto mestre, ficha) nem benchmark que o sustente para este
setor; a hipótese é levantada por prática comum do campo, não por inspeção
dos dados desta base.
**Teste planejado.** Comparação da distribuição por dia da semana entre
eventos B e eventos CID (qui-quadrado ou teste de proporções por dia), com
agregação prévia por funcionário-dia para não inflar n por funcionários com
muitos eventos.
**Efeito mínimo acionável.** 8 pontos percentuais de diferença na proporção
concentrada em segunda+sexta entre B e CID.

## Critério de sucesso do projeto (D12)

O projeto vale mesmo que todas as quatro hipóteses acima sejam refutadas: a
decomposição evitável/não-evitável do defeito B, feita com o rigor de
granularidade que a Fase 0 expôs (evento como unidade, erro-padrão agrupado
por funcionário, ID 29 corrigido, Work load/Hit target tratadas como nível de
período), já é o achado metodológico central — é o que a maioria dos
notebooks públicos deste dataset não faz (Fase 0, seção 10, Saturação). Um
resultado nulo em H1/H4, documentado com o mesmo rigor, vale mais para o
portfólio do que uma confirmação conveniente.
