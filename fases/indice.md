# Absenteísmo no Trabalho — o que alonga a ausência evitável

| Fase | Status | Tollgate | Relatório | Data |
|---|---|---|---|---|
| 0 · Reconhecimento | concluída | APROVADO com ressalvas | [relatório](fase-0-reconhecimento/relatorio.pdf) | 26/09/2026 |
| 1 · Define | concluída | APROVADO | [relatório](fase-1-define/relatorio.pdf) · [pré-registro](fase-1-define/pre-registro.pdf) | 26/09/2026 |
| 2A · Measure — qualidade | concluída | APROVADO | [relatório](fase-2a-measure-qualidade/relatorio.pdf) | 26/09/2026 |
| 2B · Measure — baseline | concluída | APROVADO | [relatório](fase-2b-measure-baseline/relatorio.pdf) · [baseline congelado](fase-2b-measure-baseline/baseline-congelado.pdf) | 26/09/2026 |
| 3 · Analyze | concluída | APROVADO | [relatório](fase-3-analyze/relatorio.pdf) | 26/09/2026 |
| 4 · Improve | concluída | APROVADO | [relatório](fase-4-improve/relatorio.pdf) | 26/09/2026 |
| 5 · Control | concluída | APROVADO com ressalva | [relatório](fase-5-control/relatorio.pdf) | 26/09/2026 |
| 6 · Entrega | não iniciada | — | — | — |
| 7 · Revisão por banca | não iniciada | — | — | — |
| 8 · Fechamento | não iniciada | — | — | — |

## Fluxo

```mermaid
flowchart LR
    F0[0 · Reconhecimento] --> F1[1 · Define]
    F1 --> F2A[2A · Measure qualidade]
    F2A --> F2B[2B · Measure baseline]
    F2B --> F3[3 · Analyze]
    F3 --> F4[4 · Improve]
    F4 --> F5[5 · Control]
    F5 --> F6[6 · Entrega]
    F6 --> F7[7 · Revisão por banca]
    F7 --> F8[8 · Fechamento]
```

## Decisões que atravessam o projeto

| Decisão | Fase de origem | O que muda nas fases seguintes |
|---|---|---|
| Granularidade mista confirmada: linha = evento de ausência, não funcionário | Fase 0 | Qualquer estatística por funcionário precisa de erro-padrão agrupado por ID, efeitos mistos, ou agregação prévia |
| ID 29 mistura duas pessoas fisicamente diferentes (Age, Height, Weight incompatíveis) | Fase 0 | Define precisa decidir: dividir em 29a/29b, ou excluir a linha minoritária. Holdout aleatório por ID depende dessa decisão |
| Work load Average/day e Hit target são de nível-mês/empresa, não de funcionário | Fase 0 | Não usar como atributo por linha sem tratar como efeito de período compartilhado |
| BMI é aritmeticamente derivado de Weight e Height (resíduo < 1 em 98,6% das linhas) | Fase 0 | As três colunas contam como uma evidência só — nunca preditores concorrentes |
| Defeito candidato recomendado: B — ausência sem lastro médico (Reason for absence fora dos capítulos CID 1–21) | Fase 0 | Define precisa fechar a fronteira entre "comportamental" (26, disciplinar) e "administrável" (consultas/exames) dentro do candidato B |
| 34 linhas duplicadas exatas, concentradas em 9 IDs | Fase 0 | Measure 2A decide se são coincidência plausível ou erro de digitação, e o tratamento de cada caso |
| Crise financeira 2008–2009 (Selic 13,75%→8,75%; PIB -3,6% no 4º tri/2008) não é testável nesta base por falta de coluna de ano | Fase 0 | Só entra como explicação rival qualitativa no Analyze, nunca como achado |
| Holdout: aleatório estratificado por ID de funcionário (mais fraco que corte temporal) | Contexto mestre | Proibido antes da fase Control |
| Defeito B fechado em duas subcategorias — B1 comportamental/disciplinar (Reason 0,26) e B2 administrável na forma (Reason 22,23,24,25,27,28) — cada uma com Pareto separado | Fase 1 · Define | Measure 2B mede as duas separadamente; Improve recomenda ações diferentes para cada uma |
| Excluídas 4 linhas: 3 administrativas sem evento real (IDs 4, 8, 35) + 1 linha corrompida do ID 29 (resolve a armadilha de granularidade E o padrão reason=0/0h ao mesmo tempo) | Fase 1 · Define | População de evento passa de 740 para 736; identidades de funcionário de 36 para 34 (IDs 4 e 35 tinham só essa linha) |
| Métrica primária: proporção de eventos (contagem). Horas: métrica secundária/guardrail, nunca somada à contagem | Fase 1 · Define | Baseline da Fase 2B mede proporção com IC; horas reportadas separadamente por subcategoria |
| 4 hipóteses pré-registradas e imutáveis em fase-1-define/pre-registro.md (H1 principal, H2 rival estrutural, H3 artefato de registro, H4 dia da semana) — correção Bonferroni, α=0,0125 | Fase 1 · Define | Analyze testa exatamente estas 4, nesta ordem (H2 antes de H1), nenhuma nova hipótese pode ser adicionada depois |
| Holdout: aleatório por identidade de funcionário (34 identidades pós-exclusão), 75/25, semente fixa — ainda não materializado em arquivo | Fase 1 · Define | Control sorteia e congela; nenhum script antes disso pode gerar esse recorte |
| **Correção (adendo datado):** pre-registro.md original citava "36 identidades" por engano; corrigido para 34, com o split do holdout ajustado para ~26/8 (não 27/9) | Fase 1 · Define — adendo de 26/09/2026 | Sorteio do holdout na Control deve usar 34 identidades e a proporção ~26/8, conforme o adendo em pre-registro.md |
| Duplicatas resolvidas com modelo de colisão por acaso (limiar p<0,30): 23/26 grupos mantidos (coincidência plausível), 3 removidos (erro de digitação provável) | Fase 2A · Measure | Base final = `data/processed/eventos_qualidade.csv` (733 eventos, 34 identidades) — usar esta base a partir da Fase 2B, não mais `eventos_limpos.csv` |
| Regra travada: Weight e Height são as colunas-fonte; Body mass index é derivada — nunca as três como preditores concorrentes | Fase 2A · Measure | Vale para Analyze e qualquer modelagem futura |
| Erro indetectável nomeado: Reason for absence por conveniência (ex. falta disciplinar lançada como consulta médica) não deixa rastro estrutural — adjacente à hipótese H3 | Fase 2A · Measure | Se H3 for refutada no Analyze, este erro indetectável vira explicação alternativa a mencionar no README |
| Baseline congelado: proporção de eventos B = 64,26% [57,95%;69,13%] IC por bootstrap de 34 clusters (não Wilson ingênuo sobre 733 eventos) | Fase 2B · Measure — imutável | Improve e Control medem ganho contra este número; nenhuma fase pode recalcular o baseline |
| Sem carta de controle por regra (M11: máximo 13 pontos possíveis) — tabela descritiva não temporal no lugar | Fase 2B · Measure | Nenhuma leitura de "mês" pode virar conclusão de tendência ou sazonalidade |
| Pareto de impacto em horas só cobre B2 (6 códigos) — B1 tem 100% dos eventos com 0h e usa o Pareto de taxa como régua | Fase 2B · Measure | Toda menção a B1 daqui em diante precisa citar contagem de eventos, nunca horas, como medida de impacto |
| Poder estatístico muito baixo para H1 e H4 (~3%, n efetivo=34 funcionários) | Fase 2B · Measure | Analyze deve reportar efeito+IC, nunca só p-valor; "não significativo" é inconclusivo, não refutação |
| Correção: relatorio.md da Fase 1 tinha erro de digitação na soma B1+B2 (54,4%→64,4%) — corrigido diretamente (não é artefato imutável) | Fase 2B · Measure | Nenhuma decisão do Define mudou; só a prosa do número preliminar |
| H2 (rival estrutural) não refuta H1: efeito de 16,4 p.p. sobrevive à exclusão dos 3 funcionários mais frequentes e à ponderação por funcionário | Fase 3 · Analyze | H1 segue candidata para Improve/Control — não descartada como composição de mix |
| H1: efeito grande (16,4 p.p., > mínimo de 10 p.p.) mas não significativo no α=0,0125 (p=0,0178) — dado o poder ~3%, é INCONCLUSIVO, não refutação | Fase 3 · Analyze | Nenhuma recomendação da Improve pode tratar H1 como confirmada; precisa de confirmação formal no holdout (Control) |
| H3 não refutada: 39 eventos reason=0 vêm de 20 funcionários, top-5 concentram 48,72% (<50%) — consistente com atalho administrativo disperso, não comportamento concentrado | Fase 3 · Analyze | B1 deve ser tratado como correção de processo (usar código 26, não 0, para falta disciplinar), não como ação sobre funcionários específicos |
| H4 descartada: efeito de 3,95 p.p., abaixo do mínimo de 8 p.p., p=0,555 | Fase 3 · Analyze | Dia da semana não entra como fator na Improve |
| Causalidade reversa para H1 (rota alocada por gestão antes do histórico de ausência) não pode ser descartada com esta base | Fase 3 · Analyze | Toda menção a H1 no README/Entrega precisa citar este limite |
| H3: recomendação firme (poka-yoke) — eliminar código 0 da lista de motivos, forçar uso do código 26 para falta disciplinar | Fase 4 · Improve | Entra no plano de controle da Control como regra de sistema pronta |
| H1: recomendação condicional/piloto — política de agendamento priorizando distância > 25,5km, NÃO ativa até confirmação | Fase 4 · Improve | Control decide se confirma via holdout; Entrega deve marcar como piloto, nunca como decisão tomada |
| Ponto de indiferença de H1: 35,4% de adesão para empatar com custo de RH assumido (8h/mês, premissa ilustrativa) | Fase 4 · Improve | Número principal da recomendação — não o ganho bruto; substituir premissa por dado real antes de decisão de negócio |
| Experimento formal de H1 (rota como unidade) exigiria ~550 unidades/grupo para 80% de poder — 32x mais que as 17 disponíveis | Fase 4 · Improve | Experimento controlado inviável nesta operação; via realista é o holdout observacional (mais fraco) da Control |
| Guardrail do experimento: nenhuma queda em B2 pode vir com queda em CID (sinalizaria supressão de atestado médico) | Fase 4 · Improve | Critério de aceite obrigatório em qualquer avaliação de H1 na Control |
| **HOLDOUT ABERTO** (semente 20260926, 26 exploração/8 confirmação): efeito de H1 na confirmação = 9,48 p.p. [IC 95% 0,0-32,2], mesma direção que a exploração (16,4 p.p.), IC muito largo | Fase 5 · Control | Reforço qualitativo, NÃO confirmação estatística — piloto de H1 continua condicional, sem mudança de status |
| Decisão final sobre H1: não implementar como regra ativa; continuar coletando dados ou aceitar piloto informal com monitoramento cuidadoso do guardrail CID | Fase 5 · Control | Entrega/README devem apresentar H1 como candidato não confirmado, nunca como achado decidido |
| 14 testes automáticos de qualidade (tests/test_qualidade.py) travam forma, domínio e volume (733 eventos, 34 identidades) da base final | Fase 5 · Control | Qualquer mudança futura no dado de entrada que quebre esses testes exige investigação antes de reusar os resultados |
| Pendência de reprodutibilidade: requirements.txt sem versões pinadas; scripts das Fases 2A-4 não importam config.py (constantes duplicadas) | Fase 5 · Control | Resolver antes de reexecutar o pipeline em outra máquina/ambiente |
