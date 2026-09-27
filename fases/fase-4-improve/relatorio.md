# Fase 4 · Improve — Recomendação que não vou implementar — Absenteísmo no Trabalho

Data: 26/09/2026 · Janela de dados: `data/processed/eventos_qualidade.csv` (733 eventos, 34 identidades — janela de exploração, holdout fechado) · v1

## Em três linhas

Separei duas recomendações com tom de confiança diferente: para H3
(confirmada) uma correção de sistema firme — eliminar o código 0 como opção
de motivo de ausência. Para H1 (promissora, não confirmada) uma política de
agendamento explicitamente **condicional e piloto**, com ponto de indiferença
de **35,4%** de adesão (dado um custo de RH assumido de 8h/mês — premissa
declarada) e um experimento desenhado que exigiria **~550 rotas por grupo**
para 80% de poder — **32 vezes mais que as 17 disponíveis na operação atual**.
O experimento é desenhável, não é viável nesta empresa. Tollgate: **APROVADO**.

## O que foi feito

1. Contramedidas separadas por causa (H3 firme, H1 condicional/piloto),
   classificadas em elimina/reduz/protege/detecta.
2. Dois entregáveis concretos: regra de sistema (H3) e tabela de priorização
   de agendamento marcada como piloto (H1).
3. Simulação de ganho de H1 com contrafactual, conta visível, três cenários e
   ponto de indiferença (`scripts/04_improve.py`).
4. Desenho do experimento de confirmação, com cálculo de n e comparação com o
   tamanho real da operação.
5. FMEA das duas recomendações, incluindo o modo de falha de pressão sobre
   atestado médico.
6. O contra, escrito e respondido.

Holdout não tocado (a simulação usa só a janela de exploração).

## Decisões e por quê

### 1 · Contramedidas (I1)

**Para H3 (firme — achado confirmado no Analyze):**

| Contramedida | Classificação | Por quê esta ordem |
|---|---|---|
| Eliminar o código 0 da lista de motivos no sistema de registro; restringir seu uso (se necessário para outro fim administrativo) a um fluxo separado, nunca como "motivo de ausência" | **Poka-yoke** (protege contra o efeito) | Remove a opção errada da interface, em vez de confiar que quem registra vai lembrar da regra sob pressão de tempo — trava vence meta (I1) |
| Relatório mensal de eventos com código fora da lista oficial UCI (1–28) | Detecta | Pega reincidência do atalho antes que se acumule, caso o poka-yoke não seja implementado de imediato ou falhe |

**Para H1 (condicional — piloto, não confirmada):**

| Contramedida | Classificação | Por quê esta ordem |
|---|---|---|
| Política de agendamento: priorizar consultas/exames/fisioterapia (B2) fora do expediente para funcionários com distância acima da mediana (25,5km) | Reduz a variação | Ataca a fricção de agendamento identificada em H1 — mas só reduz, não elimina, porque a causa não está confirmada |

**Esta contramedida de H1 não deve ser implementada antes da confirmação da
fase Control.** É o entregável que a Improve prepara para ser testado, não
uma ação já justificada pelos dados — a diferença de tom entre as duas
tabelas acima é deliberada e reflete o estágio de confiança de cada causa
(Fase 3).

### 2 · Entregáveis concretos

**H3 — regra de sistema (especificação, pronta para uso):**

> "O código 0 não é uma opção válida de motivo de ausência. Falta sem
> justificativa aceita usa o código 26 ('unjustified absence'). O código 0,
> se necessário para outro fim administrativo, fica fora da lista de
> motivos de ausência disponível para registro."

**H1 — tabela de priorização de agendamento (PILOTO PROPOSTO, NÃO REGRA ATIVA
— condicionada à confirmação da fase Control):**

| Faixa de distância | Prioridade de agendamento fora do expediente | Status |
|---|---|---|
| > 25,5 km (mediana) | Alta | Piloto proposto — aguarda confirmação |
| ≤ 25,5 km (mediana) | Padrão (sem mudança) | — |

### 3 · Simulação do ganho (I2, I3, I4) — só para H1

**Contrafactual explícito (I2)**: "se os eventos B2 dos 16 funcionários com
distância acima da mediana passassem a ser resolvidos fora do expediente na
mesma proporção da premissa de adesão, a mesma fração de horas de ausência B2
desse grupo deixaria de ocorrer." O grupo é comparável a ele mesmo (não há
grupo de controle nesta simulação — é uma projeção sobre o próprio grupo
"longe", não uma comparação com o grupo "perto", porque H1 propõe que o
grupo "longe" tem a fricção, não que o grupo "perto" seria o padrão a
alcançar). **Sem como confirmar isso com esta base** (sem contrafactual real
— Fase 0, armadilha #6): a projeção assume que a ausência realmente deixaria
de ocorrer, quando na verdade poderia só mudar de categoria de registro ou
não mudar nada (ver "o que a simulação não captura", abaixo).

**Conta visível, passo a passo:**

| Passo | Valor | Fonte |
|---|---|---|
| Funcionários com distância acima da mediana (25,5km) | 16 (dos 17 "longe") tiveram ≥1 evento B2 | `artefatos/improve.json` |
| Eventos B2 desses funcionários, na janela (733 eventos, ~36 meses) | 271 | idem |
| Eventos B2 desses funcionários, por mês (aproximação) | 7,53 | 271 ÷ 36 |
| Horas medianas por evento B2 **neste subgrupo específico** | 3h | `artefatos/improve.json` — mais alto que a mediana geral de B2 (2h, Fase 2B); a diferença fica registrada, não escondida |

**Três cenários de adesão** (`artefatos/simulacao_ganho.png`):

| Adesão | Eventos evitados/mês | Horas evitadas/mês |
|---|---|---|
| 20% (pessimista) | 1,51 | 4,52h |
| 50% (provável) | 3,76 | 11,29h |
| 80% (otimista) | 6,02 | 18,07h |

**PONTO DE INDIFERENÇA (o número principal desta recomendação, não o ganho
bruto)**: assumi, como **[PREMISSA DECLARADA, não medida nesta base]**, um
custo de coordenação de RH de **8 horas/mês** para negociar agendamento com os
16 funcionários elegíveis (aproximadamente 30 minutos/funcionário/mês). Sob
essa premissa, a política só se paga se **pelo menos 35,4% dos eventos B2
elegíveis** migrarem para fora do expediente — abaixo disso (cenário
pessimista de 20% fica abaixo do ponto de indiferença), o tempo de RH gasto
supera a economia de horas de ausência. **O valor de 8h/mês é ilustrativo**
— quem conduz o projeto na operação real deveria substituí-lo por um número
medido antes de decidir.

**O que a simulação não captura:**
- Funcionários que já agendam fora do expediente por conta própria e não
  aparecem como "resolvidos" nesta base (não há coluna que distinga isso).
- A causalidade reversa não descartada no Analyze (item 6 do relatório da
  Fase 3): se a distância for consequência de uma alocação de rota anterior
  ao histórico de ausência, e não causa do evento, a política de agendamento
  não mudaria nada — o ganho simulado aqui pressupõe a direção causal
  pré-registrada, que **não foi confirmada**.
- Qualquer custo de oportunidade do tempo de RH além da coordenação direta
  (ex.: renegociação de contrato com convênio médico).

### 4 · Desenho do experimento (I8, I9, I10)

**Unidade de aleatorização**: **rota ou turno**, não o funcionário individual
— a distância é fixa por funcionário e não pode ser manipulada; o que se
testa é a política de agendamento aplicada a grupos de rota. Esta base não
tem uma coluna de rota/turno explícita (só ID e Distance); a proposta usa o
agrupamento por funcionário com distância acima da mediana como proxy do que
seria, na operação real, um agrupamento por rota.

**Elegibilidade**: funcionários com distância acima da mediana observada
(25,5km) — os mesmos 17 do teste de H1.

**Duração**: pelo menos um ciclo de escala completo (mensal); não há como
estender por um "ciclo sazonal" com confiança, porque a Fase 2B já declarou
que a base não sustenta leitura de sazonalidade real (M13 não se aplica por
falta de eixo temporal confiável).

**Tamanho de amostra**: para poder de 80% (padrão convencional, mais exigente
que o poder de ~3% já demonstrado com n=34), detectando o efeito mínimo
pré-registrado de 10 p.p. com α=0,0125, o cálculo indica **~550 unidades por
grupo** (rotas ou turnos). A operação real dispõe de **17** rotas longas
identificáveis nesta base — **32 vezes menos** que o necessário
(`artefatos/improve.json`, `experimento`).

**Conclusão de viabilidade, dita sem rodeio**: este experimento é
**desenhável, mas não viável na escala desta operação**. Um efeito de 10 p.p.
com apenas ~17 unidades elegíveis não vai ser confirmável por experimento
controlado dentro desta empresa — a via realista de confirmação é o holdout
observacional da fase Control (mais fraco, mas o único que o tamanho da
operação permite), ou acumular dados de múltiplos períodos/unidades da mesma
transportadora ao longo do tempo antes de tentar um experimento formal.

**Guardrail obrigatório** (Define, regra de aceitação, não aspiração):
nenhum critério de decisão deste experimento — nem do holdout observacional —
pode aceitar queda na proporção de eventos B2 acompanhada de queda na
proporção de eventos CID. Isso sinalizaria supressão de ausência médica
legítima, não redução do evitável, e invalidaria qualquer leitura de sucesso.

**Ameaças à validade específicas desta base (I9):**
- **Contaminação entre rotas que compartilham supervisor**: se o mesmo
  supervisor administra rotas longas e curtas, a política pode vazar
  informalmente para o grupo de controle.
- **Efeito Hawthorne**: funcionários cientes de estarem sendo observados
  podem mudar o padrão de registro de ausência independentemente da política
  em si — particularmente relevante dado o achado de H3 (o código já é usado
  de forma administrativa, não estritamente ligada ao comportamento real).

### 5 · FMEA da recomendação (I11, I12)

| Recomendação | Modo de falha | Severidade | Ocorrência | Detecção | Mitigação |
|---|---|---|---|---|---|
| H3 — eliminar código 0 | Quem registra usa outro código indevido como novo atalho (ex.: código 22 "acompanhamento" para disfarçar falta disciplinar) | Média | Média — a meta pode ser contornada (I11) se o sistema só bloquear o código 0 sem revisar o processo por trás | Relatório mensal de código fora do padrão (já proposto) pode não pegar um atalho que use um código válido | Auditoria periódica cruzando Disciplinary failure=1 com o código usado, não só a ausência do código 0 |
| H1 — política de agendamento | **Comunicação da política é lida como pressão para não tirar atestado médico** (violação direta do guardrail permanente do contexto mestre) | **Alta** | Plausível se a comunicação não distinguir explicitamente B2 (agendável) de CID (atestado médico) | A mesma checagem de proporção CID do guardrail (Define) — queda em CID junto com queda em B2 | Comunicar a política citando só as categorias B2 nominalmente (consulta, exame, fisioterapia, doação de sangue), nunca "reduzir ausência" de forma genérica; treinar quem comunica antes do piloto |
| H1 — política de agendamento | Funcionários "longe" percebem a priorização como discriminação (ex.: "por que só eu preciso agendar fora do horário?") | Média | Média | Pesquisa de clima ou feedback direto no piloto | Comunicar a razão operacional (fricção de deslocamento), não o resultado do teste estatístico |

### 6 · O contra (I14)

**O parágrafo mais forte que um cético escreveria**: "H1 tem p-valor
(0,0178) acima do limiar de significância ajustado (0,0125), foi extraída de
uma base com apenas 34 funcionários e poder de detecção de aproximadamente
3%, é uma entre quatro hipóteses testadas nesta fase, e a causalidade reversa
— rotas longas alocadas antes de qualquer histórico de ausência do
funcionário — não foi descartada. Implementar qualquer política de
agendamento com base nisso, antes da confirmação da Control, arrisca mudar o
processo de trabalho de 17 funcionários que moram longe sem nenhuma garantia
de que a distância seja a causa real do padrão observado — e ainda corre o
risco, se mal comunicada, de pressionar contra atestados médicos legítimos."

**Resposta**: é exatamente por isso que a recomendação desta fase é
**explicitamente condicional e marcada como piloto proposto, não regra
ativa** (item 2) — o holdout da fase Control existe precisamente para decidir
essa questão, não para confirmar o que já se quer crer. Se a Control não
confirmar o efeito, a recomendação de H1 é descartada sem custo, porque nada
foi implementado. A única recomendação que **não** carrega essa ressalva é a
de H3, porque essa causa já foi confirmada com o critério pré-registrado no
Analyze — a diferença de tom entre as duas recomendações desta fase é a
própria resposta ao cético.

## Registro de escolhas

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Métrica de horas por evento B2 na simulação | Mediana do subgrupo "longe" (3h) | Mediana geral de B2 da Fase 2B (2h) | A simulação é sobre o subgrupo específico elegível pela política — usar a mediana geral subestimaria o impacto real desse grupo | `artefatos/improve.json` | I3 |
| Custo de RH no ponto de indiferença | 8h/mês, premissa declarada | Não calcular ponto de indiferença; usar 0 (sem custo) | Sem premissa de custo não há ponto de indiferença calculável (I4 exige a premissa desconhecida); custo zero seria fingir que a política não consome tempo de ninguém | `artefatos/improve.json`, `ponto_de_indiferenca` | I4 |
| Unidade de aleatorização do experimento | Rota/turno (proxy: funcionário "longe") | Funcionário individual | Distance é fixa por funcionário — não há como aleatorizar a exposição dentro da mesma pessoa; a intervenção (agendamento) é aplicada a nível de grupo/rota | Item 4 deste relatório | I8 |

## Números

Todos os números vêm de `artefatos/improve.json`, gerado por
`scripts/04_improve.py` a partir de `data/processed/eventos_qualidade.csv`.
Gráfico em `artefatos/simulacao_ganho.png`, gerado por
`scripts/04b_grafico_ganho.py`.

## Tollgate IMPROVE

| Critério | Veredito | Motivo |
|---|---|---|
| Contramedidas de H3 e H1 separadas, com tom de confiança diferente e classificação elimina/reduz/protege/detecta | OK | Item 1 — H3 poka-yoke+detecta (firme); H1 reduz a variação (condicional) |
| Entregável de H3 é regra de sistema pronta; entregável de H1 marcado como piloto, não regra ativa | OK | Item 2 |
| Simulação com contrafactual, conta visível, três cenários, ponto de indiferença como número principal | OK | Item 3 — 35,4% de adesão, não o ganho bruto |
| Experimento usa rota/turno como unidade, e diz se o n é viável dado o tamanho real | OK | Item 4 — 550 necessário vs. 17 disponível, declarado inviável |
| Guardrail contra supressão de ausência médica como critério de decisão do experimento | OK | Item 4 |
| FMEA nomeia o modo de falha de pressão sobre atestado médico | OK | Item 5 — severidade alta, mitigação proposta |
| "O contra" específico desta base (poder, n, causalidade reversa) | OK | Item 6 |

**Veredito: APROVADO.**

## Pendências e riscos

- O custo de RH de 8h/mês no ponto de indiferença é uma premissa ilustrativa
  — precisa ser substituído por um número real antes de qualquer decisão de
  negócio.
- O experimento formal de H1 não é viável no tamanho atual da operação; a via
  realista é o holdout observacional da Control, que é mais fraco.
- Nenhuma das duas recomendações deve ser apresentada na Entrega como "já
  decidida" — H3 é firme quanto à causa, mas a implementação em si não foi
  testada; H1 é explicitamente condicional.

## Para a próxima fase

O Control recebe: a regra de sistema de H3 pronta para o plano de controle; a
tabela de priorização de H1 marcada como piloto condicional; o guardrail
contra supressão de CID como critério de aceite; e a instrução de abrir o
holdout uma única vez para testar H1 formalmente — sabendo que mesmo essa
confirmação observacional é mais fraca que o experimento (inviável) desenhado
aqui.
