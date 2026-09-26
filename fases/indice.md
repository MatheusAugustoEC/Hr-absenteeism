# Absenteísmo no Trabalho — o que alonga a ausência evitável

| Fase | Status | Tollgate | Relatório | Data |
|---|---|---|---|---|
| 0 · Reconhecimento | concluída | APROVADO com ressalvas | [relatório](fase-0-reconhecimento/relatorio.pdf) | 26/09/2026 |
| 1 · Define | não iniciada | — | — | — |
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
