# Fase 2A · Measure — Procedência e qualidade do dado — Absenteísmo no Trabalho

Data: 26/09/2026 · Janela de dados: `data/processed/eventos_limpos.csv` (736 eventos, 34 identidades — base travada do Define) · v1

## Em três linhas

Auditei as seis dimensões de qualidade sobre a base limpa do Define (M2):
nenhum nulo, nenhum valor fora de domínio, Work load Average/day e Hit target
seguem confirmados como nível-mês, e a circularidade do BMI se mantém. Resolvi
a pendência das 34 linhas duplicadas com um teste quantitativo de plausibilidade
por grupo: 23 dos 26 grupos são coincidência plausível (mantidos), 3 são
suspeitos de erro de digitação (removidos). Base final: **733 eventos, 34
identidades**. Tollgate: **APROVADO**.

## O que foi feito

1. Perfilamento de confirmação sobre a base limpa (`scripts/02a_measure_qualidade.py`),
   verificando que as 4 linhas excluídas no Define não sobrevivem.
2. Auditoria das seis dimensões de qualidade (M2), cada uma com teste e
   critério de aceite.
3. Resolução da pendência de duplicatas da Fase 0 com um modelo de colisão
   por acaso (M5 — regra escrita antes de remover qualquer linha).
4. Nomeação dos vieses de seleção e vazamento, e do erro indetectável nesta
   base.

Como é dado real de uma única transportadora, sem acesso a quem gera o dado,
esta fase é **auditoria de procedência**, não MSA clássico com
repetibilidade/reprodutibilidade de operador (M4).

## Decisões e por quê

### 1 · Perfil de confirmação

Base limpa: 736 eventos, 34 identidades (72 B1, 402 B2, 262 CID) —
idêntico ao que o Define entregou. As 4 linhas excluídas (IDs 4, 8-parcial,
35, e a linha jovem do ID 29) foram confirmadas ausentes:
`confirmacao_exclusoes_define` em `artefatos/auditoria_qualidade.json` mostra
0 ocorrências para todos os quatro critérios de checagem.

### 2 · As seis dimensões

**Completude (M2, M3) — APROVADO.** Zero nulos em todas as 21 colunas.
"Month of absence" = 0 e "Reason for absence" = 0 são códigos válidos (o
primeiro tratado como categoria residual desde o Define; o segundo já
incorporado à subcategoria B1), não ausência de dado — decisão já registrada
no Define, apenas reconfirmada aqui.

**Unicidade (M2) — RESOLVIDO, com critério quantitativo.** A Fase 0 achou
34 linhas em excesso de duplicata (60 linhas em 26 grupos, contando a
duplicata de linha inteira). Como o dataset tem só 21 colunas e a maioria é
constante por funcionário, um grupo duplicado dentro do mesmo ID se reduz, na
prática, a colisão de (Reason for absence, Month of absence, Day of the week,
Absenteeism time in hours) — os quatro campos que variam por evento.

Construí um teste de plausibilidade por grupo: para cada categoria de motivo,
calculei o **suporte empírico** Kr — quantas combinações distintas de (Month,
Day of the week, Hours) o dataset inteiro já mostra para aquele motivo. Para
cada funcionário com nᵢ eventos daquele motivo, a probabilidade aproximada de
pelo menos uma colisão por acaso, sorteando nᵢ vezes entre Kr valores
possíveis (problema do aniversário), é 1 − exp(−nᵢ(nᵢ−1)/(2·Kr)).

| Critério | Veredito |
|---|---|
| p_colisão ≥ 0,30 | Coincidência plausível — evento de rotina curta com espaço de combinações restrito e funcionário com muitos eventos do mesmo motivo. Mantido. |
| p_colisão < 0,30 | Colisão pouco provável por acaso — tratado como erro de digitação provável. Removida a linha extra, mantida a primeira ocorrência. |

O limiar de 0,30 é uma escolha de julgamento, não uma convenção estatística
padrão — registrado no "Registro de escolhas" abaixo, e reversível se o
responsável do projeto discordar.

**Resultado:** 23 dos 26 grupos ficaram acima de 0,30 (alguns com p_colisão >
0,95 — por exemplo, ID 3 com 38 eventos de "consulta odontológica" (Reason 27)
contra um suporte de só 35 combinações possíveis: colisão seria quase certa,
não é evidência de erro). **3 grupos ficaram abaixo do limiar** — ID 5
(Reason 23, p=0,009), ID 27 (Reason 23, p=0,088) e ID 34 (Reason 23, p=0,281)
— removidos (1 linha cada, mantida a primeira ocorrência). Base final: **733
eventos** (736 − 3), mesmas 34 identidades (nenhum funcionário tinha só essa
linha).

**Validade (M2) — APROVADO.** Zero valores fora de domínio em Day of the week
(∈{2..6}), Seasons (∈{1..4}), Education (∈{1..4}), Reason for absence
(∈{0..28}) e as três binárias (Disciplinary failure, Social drinker, Social
smoker).

**Consistência (M2) — reconfirmada, não só herdada.**
(a) Work load Average/day e Hit target seguem em ~3 valores distintos por mês
(3,08 e 2,92 em média, 12 meses — nenhum mês caiu para 1 valor único mesmo
após as exclusões do Define): a leitura de nível-mês/empresa da Fase 0 se
mantém sobre a base limpa.
(b) BMI: resíduo < 1 em 98,64% das linhas (praticamente idêntico ao valor da
Fase 0, 98,65% — as exclusões não tocaram essas colunas de forma relevante).
**Regra operacional travada a partir daqui**: Weight e Height são as colunas-
fonte; Body mass index é derivada. Nenhuma fase seguinte usa as três como
preditores concorrentes na mesma análise.

**Acurácia (M2) — NÃO AUDITÁVEL, declarado.** Não há valor total independente
(ex.: um sistema de ponto) para conferir a soma de horas ou a contagem de
eventos contra uma fonte externa. Não força verificação artificial.

**Pontualidade (M2) — NÃO AUDITÁVEL PARA ATRASO, declarado.** Sem timestamp de
registro, não há como medir atraso entre o evento e o lançamento (já
registrado na Fase 0). A concentração por mês (49 a 87 eventos/mês) não mostra
padrão que sugira lançamento em lote além do que a checagem de duplicata já
capturou.

### 3 · Vieses

- **Seleção**: a população é "funcionário com pelo menos 1 evento no período"
  — quem nunca faltou não aparece. Não há como calcular a proporção de
  funcionários que faltam, nem quantos existem no total (armadilha #8,
  `armadilhas.md`).
- **Vazamento**: Disciplinary failure e Absenteeism time in hours são
  preenchidos depois do evento — nunca usados como preditor de Reason for
  absence nem um do outro (Fase 0, item 2; reconfirmado aqui sem violação,
  porque esta fase não constrói modelo).
- **Não representado**: funcionários sem nenhuma ausência no período inteiro
  existem na transportadora, mas não entram nesta base — são o denominador
  que falta para qualquer taxa (Fase 0, seção 7).

### 4 · Erro indetectável

Um "Reason for absence" preenchido por conveniência — por exemplo, uma falta
sem justificativa real lançada como "consulta médica" (23) para evitar o
enquadramento disciplinar — não deixa rastro estrutural nesta base. Só seria
visível com o atestado físico em mãos, que não existe aqui. Isso é
particularmente relevante porque é **adjacente à hipótese H3** do
pré-registro (o padrão reason=0 como artefato de registro): se o viés for
nessa direção, a proporção real de eventos comportamentais pode estar
subestimada (parte deles está classificada como B2 ou até CID). Vai para as
limitações do README.

### 5 · Veredito fit-for-purpose

Esta base **não pode responder**:
- **Taxa de absenteísmo** — sem dias trabalhados, não há denominador (Fase 0).
- **Causalidade da crise 2008–2009** — sem coluna de ano, não há como isolar o
  período (Fase 0).
- **Risco individual por funcionário** — n=34 identidades é insuficiente para
  qualquer scoring com validade estatística.
- **O mérito do atestado médico** — só o código CID está disponível, nunca o
  documento; a base registra a classificação, não a veracidade dela.

Estes não são falhas do trabalho — são limites do instrumento disponível,
declarados antes de qualquer conclusão se apoiar neles (M4).

## Registro de escolhas

| Escolha | O que usei | O que mais considerei | Por que esta | Evidência | Regra |
|---|---|---|---|---|---|
| Critério de duplicata | Modelo de colisão por acaso (aproximação do problema do aniversário) com limiar p<0,30 | Remover todas as 26 duplicatas por precaução; manter todas por não ter certeza | Remover tudo descartaria eventos reais coincidentes (ex.: ID 3 com quase certeza de colisão dado seu volume); manter tudo ignoraria 3 casos estatisticamente improváveis por acaso | `artefatos/auditoria_qualidade.json`, `unicidade.veredito_por_grupo` | M2, M5 |
| Limiar de plausibilidade | 0,30 | 0,05 (convenção de significância) ou 0,50 (mais conservador) | 0,05 deixaria muitos casos moderadamente improváveis (ex. p=0,28) como "plausíveis" só por não cruzar um limiar arbitrário rígido; 0,30 separa claramente os 3 casos com p<0,09-0,28 dos 23 casos com p>0,39 — há uma lacuna natural nos dados entre 0,28 e 0,39 | `artefatos/auditoria_qualidade.json` | M5 (regra escrita, decisão de julgamento registrada) |
| Regra fonte/derivada do trio Weight-Height-BMI | Weight e Height como fonte; BMI como derivada | Tratar as três simetricamente | BMI é aritmeticamente calculável das outras duas (resíduo<1 em 98,6%); manter simetria esconderia a circularidade em vez de preveni-la | Fase 0, seção 2; `artefatos/auditoria_qualidade.json`, `consistencia.circularidade_bmi` | F1 (linha do tempo/circularidade) |

## Números

Todos os números vêm de `artefatos/auditoria_qualidade.json`, gerado por
`scripts/02a_measure_qualidade.py` a partir de `data/processed/eventos_limpos.csv`
(a base travada do Define, não o CSV bruto). A base final pós-qualidade foi
salva em `data/processed/eventos_qualidade.csv` (733 linhas, 34 identidades).

## Tollgate 2A

| Critério | Veredito | Motivo |
|---|---|---|
| Seis dimensões com teste e critério de aceite explícitos | OK | Completude, Unicidade, Validade, Consistência auditadas com teste; Acurácia e Pontualidade declaradas não auditáveis com motivo, não puladas |
| Duplicatas com veredito por grupo e evidência quantitativa | OK | 26 grupos, cada um com p_colisão calculada; 23 plausíveis mantidos, 3 suspeitos removidos |
| Work load/Hit target e circularidade BMI reconfirmados na base limpa | OK | Recalculados sobre `eventos_limpos.csv`, não herdados por citação — valores praticamente idênticos aos da Fase 0 |
| Viés de seleção nomeado como limitação | OK | Item 3 — população condicionada a ter pelo menos 1 evento |
| Veredito fit-for-purpose com razão estrutural de cada limite | OK | Item 5 — 4 limites nomeados, cada um com a razão |

**Veredito: APROVADO.**

## Pendências e riscos

- O critério de remoção de duplicata (limiar 0,30) é uma escolha de
  julgamento — se o responsável do projeto discordar do limiar, isso muda a
  base final (733 vs. 736 ou algum número intermediário) e precisa ser
  revisitado antes da Fase 2B congelar o baseline.
- O erro indetectável nomeado (Reason for absence por conveniência) é
  adjacente à hipótese H3 do pré-registro — se H3 for refutada no Analyze
  (comportamento concentrado, não artefato disperso), este erro indetectável
  ganha peso como explicação alternativa a ser mencionada nas limitações do
  README.

## Para a próxima fase

O Measure 2B recebe `data/processed/eventos_qualidade.csv` (733 eventos, 34
identidades) como base definitiva para o baseline — não mais
`eventos_limpos.csv`. A métrica primária (proporção de eventos B) e secundária
(horas por subcategoria) definidas no Define continuam válidas; os números
brutos preliminares citados no Define (54,4% B, etc.) devem ser recalculados
sobre esta base final antes de virarem baseline congelado.
