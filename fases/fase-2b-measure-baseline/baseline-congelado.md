# Baseline congelado — Fase 2B · Measure

**Datado em 26/09/2026. Este arquivo é IMUTÁVEL a partir deste commit** — o
segundo dos três artefatos de prova do contexto mestre (junto com o
pré-registro e a quarentena do holdout). Qualquer correção futura é adendo
datado ao final, nunca edição do valor congelado.

## Janela e filtros

- Base: `data/processed/eventos_qualidade.csv` (saída da Fase 2A).
- N = **733 eventos**, **34 identidades** de funcionário.
- Filtros aplicados até aqui: exclusão das 4 linhas do Define (3
  administrativas + 1 do ID 29) e das 3 duplicatas suspeitas do Measure 2A.
  Nenhuma relação entre variáveis foi usada para chegar a este número — só
  estrutura e reagrupamento de uma coluna (Reason for absence).
- Holdout: fechado. Este baseline é sobre a janela de exploração inteira
  (nenhum recorte de confirmação foi aberto).

## Métrica primária

**Proporção de eventos do defeito B (B1+B2) sobre o total de eventos.**

| | Valor |
|---|---|
| n eventos B | 471 |
| N total | 733 |
| Proporção | **64,26%** |
| IC 95% (bootstrap por cluster de 34 funcionários) | **[57,95% ; 69,13%]** |
| IC 95% Wilson ingênuo (733 eventos independentes — não usar para decisão) | [60,72% ; 67,64%] |
| DPMO | 642.565 |
| Nível sigma sem deslocamento de 1,5σ | -0,365 |
| Nível sigma com deslocamento de 1,5σ | 1,135 |

O IC correto para decisão é o de **bootstrap por cluster** — mais largo que o
Wilson ingênuo porque respeita que os 733 eventos vêm de só 34 funcionários,
não de 733 unidades independentes (regra de granularidade do contexto mestre).

## Métricas secundárias

| Subcategoria | n eventos | Proporção do total | IC 95% (bootstrap por cluster) |
|---|---|---|---|
| B1 comportamental/disciplinar | 72 | 9,82% | [5,52% ; 16,19%] |
| B2 administrável na forma | 399 | 54,43% | [44,68% ; 61,75%] |

Horas por subcategoria (distribuição inteira, não só média):

| Categoria | n | Média | Mediana | Desvio padrão | P25 | P75 | Máximo |
|---|---|---|---|---|---|---|---|
| B1 comportamental | 72 | 3,33h | 0,0h | 3,97h | 0,0h | 8,0h | 16h |
| B2 administrável | 399 | 3,34h | 2,0h | 2,74h | 2,0h | 4,0h | 24h |
| CID (não-defeito) | 262 | 13,52h | 8,0h | 20,48h | 3,0h | 8,0h | 120h |

## Capabilidade (meta interna)

- Meta interna: média de proporção B do quartil de funcionários com melhor
  desempenho (25% com menor proporção de eventos B) = **33,36%**.
- Baseline agregado atual: **64,26%**.
- Tradução em negócio: ao ritmo observado (~20,4 eventos/mês na operação,
  aproximação sobre ~36 meses do período), a operação registra
  aproximadamente **13,1 eventos B por mês**; no nível do quartil superior,
  seriam **~6,8 eventos B por mês** — uma redução aproximada de **6,3 eventos
  evitáveis por mês**, se todo funcionário operasse como o quartil de melhor
  desempenho.

## Data e versão

Congelado em 26/09/2026, gerado por `scripts/02b_measure_baseline.py` a
partir de `data/processed/eventos_qualidade.csv`. Ver `manifesto.md` para o
hash de ambos os arquivos.
