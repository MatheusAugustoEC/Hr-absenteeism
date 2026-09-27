# Absenteísmo no Trabalho — o que alonga a ausência evitável

| Fase | Status | Tollgate | Relatório | Data |
|---|---|---|---|---|
| 0 · Reconhecimento | concluída | APROVADO com ressalvas | [relatório](fase-0-reconhecimento/relatorio.pdf) | 26/09/2026 |
| 1 · Define | concluída | APROVADO | [relatório](fase-1-define/relatorio.pdf) · [pré-registro](fase-1-define/pre-registro.pdf) | 26/09/2026 |
| 2A · Measure — qualidade | não iniciada | — | — | — |
| 2B · Measure — baseline | não iniciada | — | — | — |
| 3 · Analyze | não iniciada | — | — | — |
| 4 · Improve | não iniciada | — | — | — |
| 5 · Control | não iniciada | — | — | — |
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
