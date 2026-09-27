# Absenteísmo no Trabalho — o que alonga a ausência evitável

**[RASCUNHO — Fase 5 · Control. Será revisado na Fase 8, depois da revisão por banca.]**

Projeto de portfólio conduzido por DMAIC (Lean Seis Sigma) sobre o dataset
público *Absenteeism at Work* (UCI Machine Learning Repository). Autor:
Augusto — 26/09/2026.

## Que pergunta este projeto responde

Onde e por que a ausência sem lastro médico (evitável em potencial) se
concentra no processo de ausência de uma transportadora de Brasília, e que
mudança de agendamento ou processo administrativo reduziria essa parte sem
afetar a ausência com lastro médico.

## A resposta em uma frase

**64,26%** dos 733 eventos de ausência analisados (IC 95% [57,95%–69,13%])
não têm lastro médico — divididos em **9,82%** comportamental/disciplinar
(**H3, confirmado**: é um atalho de registro administrativo disperso entre 20
funcionários, não comportamento concentrado) e **54,43%** administrável na
forma (consultas, exames, fisioterapia). Uma causa candidata para a parte
administrável — distância acima da mediana entre residência e trabalho — teve
efeito grande (16,4 pontos percentuais) mas **não confirmado com significância
estatística** na fase de análise, e a confirmação no holdout mostrou a mesma
direção, com magnitude menor (9,5 p.p.) e intervalo de confiança muito largo —
reforço qualitativo, não confirmação estatística formal.

## Como rodar do zero

```bash
python -m venv .venv
.venv\Scripts\activate    # Windows
pip install -r requirements.txt

# reproduz o pipeline fase a fase (ordem importa)
python scripts/00_reconhecimento.py
python scripts/00b_sipoc_diagrama.py
python scripts/01_define_escopo.py
python scripts/02a_measure_qualidade.py
python scripts/02b_measure_baseline.py
python scripts/02b_graficos.py
python scripts/03_analyze.py
python scripts/03b_ishikawa.py
python scripts/03c_graficos_analyze.py
python scripts/04_improve.py
python scripts/04b_grafico_ganho.py

# testes automaticos de qualidade do dado
pytest tests/test_qualidade.py -v

# ATENCAO: os dois scripts abaixo abrem/leem o holdout. Ja foram executados
# uma unica vez nesta Fase 5 (semente fixa em config.py) - nao rode de novo
# esperando um resultado diferente; rodar de novo so reproduz o mesmo sorteio.
python scripts/05a_holdout_sorteio.py
python scripts/05b_holdout_confirmacao.py

# gera os PDFs de cada relatorio de fase
python scripts/md_to_pdf.py fases/fase-0-reconhecimento/relatorio.md
# (repita para as demais fases, ou veja fases/indice.md para a lista completa)
```

Parâmetros centralizados em `config.py` (limiar de duplicata, sementes de
bootstrap/permutação/holdout, custo de RH assumido na simulação de ganho).

## Origem e natureza dos dados — o que isso proíbe concluir

- **Dataset real**, de uma transportadora em Brasília, jul/2007–jul/2010
  (UCI Machine Learning Repository — [Absenteeism at Work](https://archive.ics.uci.edu/dataset/445/absenteeism+at+work)).
- **Sem coluna de ano**: qualquer leitura de sazonalidade ou tendência mensal
  é hipótese, nunca conclusão fechada — os 12 rótulos de mês misturam 3 anos
  calendário.
- **Sem dias trabalhados**: não existe "taxa de absenteísmo" calculável aqui
  — toda métrica é condicional a "dado que uma ausência ocorreu".
- **Sem contrafactual**: não há registro do que deixou de acontecer (ex.:
  funcionário que teria faltado e não faltou por já ter agendado fora do
  expediente). Toda simulação de ganho usa ponto de indiferença, não ganho
  bruto, por essa razão.
- **n = 34 funcionários** (identidades com pelo menos um evento, após
  exclusões de qualidade): insuficiente para scoring de risco individual, e
  o poder estatístico disponível para testar as hipóteses de fricção de
  agendamento é de **apenas ~3%** — um resultado "não significativo" nesta
  base nunca deve ser lido como "não há efeito".

## Decisões metodológicas e por quê

- **Defeito definido em duas subcategorias**: B1 comportamental/disciplinar
  (Reason for absence = 0 ou 26) e B2 administrável na forma (Reason = 22,
  23, 24, 25, 27, 28) — porque a ação de RH sobre cada uma é diferente
  (processo de registro vs. agenda), e agregá-las esconderia essa diferença.
- **4 linhas excluídas no Define**: 3 registros administrativos sem evento
  real (Month of absence = 0 e 0 horas) e 1 linha do ID 29 que misturava dois
  funcionários fisicamente diferentes (Age 28 vs. 41, Height 169 vs. 182cm) —
  a mesma exclusão resolveu as duas armadilhas ao mesmo tempo.
- **Limiar de 0,30 para duplicata** (Measure 2A): das 34 linhas duplicadas
  encontradas na Fase 0, um teste de colisão por acaso (problema do
  aniversário, dado o pequeno espaço de combinações de motivo/mês/dia/duração
  observado) mostrou que 23 dos 26 grupos são coincidência plausível de
  eventos de rotina curta; 3 foram removidos como erro de digitação provável.
- **Erro-padrão agrupado por funcionário em todos os testes**: as 733/733
  linhas não são observações independentes — são ~34 funcionários com
  múltiplos eventos cada. Ignorar isso (como a maioria dos notebooks públicos
  deste dataset faz ao tratar a base como 740 linhas independentes) infla
  artificialmente a significância.

## Premissas do stakeholder simulado

Este projeto não teve cliente real. O stakeholder assumido — um gestor de
RH/operações da transportadora, que decide sobre agendamento, escala e
enquadramento disciplinar — é **simulado**. Suas premissas de decisão estão
registradas em `fases/fase-1-define/relatorio.md`. Nenhuma recomendação deste
projeto foi validada por uma pessoa real da operação.

## Veredito da armadilha prioritária

A granularidade mista (evento de ausência dentro de funcionário) era a
armadilha mais grave suspeitada na Fase 0 — e se confirmou mais séria do que
o esperado: um ID (29) misturava duas pessoas fisicamente diferentes, e o
código "Reason for absence = 0" (fora da lista oficial do UCI) se revelou um
atalho administrativo para falta disciplinar, usado por 20 funcionários
diferentes de forma dispersa — não um padrão de comportamento de poucos
indivíduos (hipótese H3, confirmada no Analyze).

## O que eu faria com acesso a dados reais

1. **Coluna de ano** — para separar os 3 anos calendário misturados nos
   rótulos de mês e permitir carta de controle real (mínimo 20-25 pontos).
2. **Dias trabalhados/escala** — para calcular uma taxa de absenteísmo de
   verdade, em vez de proporções condicionais a "dado que uma ausência
   ocorreu".
3. **Rota ou turno explícito** — para desenhar o experimento de confirmação
   de H1 com a unidade de aleatorização correta, em vez do proxy por
   funcionário usado aqui (que mostrou precisar de ~550 unidades para 80% de
   poder — 32 vezes mais que as ~17 disponíveis nesta base).

## Estrutura do projeto

- `fases/` — checkpoint de cada fase do DMAIC (relatório, manifesto,
  artefatos), com `fases/indice.md` como mapa do projeto.
- `data/raw/` — dataset original, intocado.
- `data/processed/` — bases intermediárias geradas pelo pipeline
  (`eventos_limpos.csv`, `eventos_qualidade.csv`).
- `data/holdout/` — sorteio do holdout (Fase 5), aberto uma única vez.
- `scripts/` — pipeline reprodutível, numerado por fase.
- `tests/` — testes automáticos de qualidade do dado (C7).
- `config.py` — parâmetros extraídos do código.

## Revisão independente

Pendente — a Fase 7 (revisão por banca) ainda não ocorreu nesta versão do
projeto.

## Uso de assistente de IA

Este projeto foi conduzido em parceria com um assistente de IA (Claude),
seguindo o método DMAIC descrito acima, com decisões de escopo, interpretação
e aceite de tollgate feitas pelo responsável do projeto a cada fase.
