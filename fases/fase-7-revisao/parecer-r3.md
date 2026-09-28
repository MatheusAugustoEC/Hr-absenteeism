# Parecer da banca — Absenteísmo evitável no trabalho (rodada 3, checagem final)

28/09/2026 · rodada 3 · `file:///C:/Users/Augusto/Desktop/Projetos/hr-absenteeism-dmaic/fases/fase-6-entrega/artefatos/index.html` (sem site publicado) · nível 1 (só a página; nível 2 não necessário nesta rodada) · revisão visual: realizada

Rodada focada só nos dois pontos abertos pela rodada 2 (`parecer-r2.md`): I1
(sobreposição no Pareto de horas, reaberto) e M5 (ordem do bloco "por
funcionário"). Não repete os roteiros inteiros.

## Veredito

**APROVADO** — os dois pontos abertos foram confirmados resolvidos, e nada
que estava sólido quebrou. Não há achados novos nesta rodada.

## Conferência

| ID | O que se esperava | O que a banca confirmou | Status |
|---|---|---|---|
| I1 | Nenhuma sobreposição no Pareto de horas, nos três temas e no celular | `sobreposicao.md` desta rodada: "Nenhuma sobreposição detectada" nos 7 conjuntos testados (desktop/celular/escuro × Dashboard/Relatório, + Slides celular). Confirmado visualmente em `graficos/desktop__unico__relatório__00.png` — rótulos voltaram à forma abreviada ("Consulta M.", "Consulta O." etc.), rotação mantida, sem colisão | **Resolvido** |
| M5 | Ordem dos blocos do Dashboard: motivo → tempo perdido → distância → dia → mês → por funcionário → tabela | `texto/unico__dashboard.txt` desta rodada confirma exatamente essa sequência — "por funcionário" agora vem depois do bloco de mês (H5) e antes de "Ver a tabela detalhada" | **Resolvido** |

## O que a correção não quebrou

- Zero erros de console; zero ocorrências em `sobreposicao.md` em qualquer
  modo, tema ou largura testada — inclusive os gráficos que já estavam OK
  antes (heatmap, composição, dia da semana, mês) continuam sem sobreposição.
- O número principal e todos os textos de ressalva (badges de H4 e H5, nota
  de I2, item de I3, bloco de recomendação de I5, n do heatmap de I6)
  continuam presentes e idênticos aos da rodada 2.
- A reordenação do bloco "por funcionário" não alterou nenhum número, filtro
  ou interação — confirmado por leitura do texto completo do Dashboard.

## Achados

Nenhum.

## Cobertura desta rodada

Os dois itens abertos da rodada 2 (I1, M5) foram conferidos e confirmados.
Não é necessário nível 2 nesta rodada — os dois pontos eram inteiramente
verificáveis pela página.

## Limites desta revisão

Mesmas limitações já registradas nas rodadas anteriores (download não
clicado; README e requirements.txt fora do escopo de captura da página) —
nenhuma delas foi reaberta ou reavaliada nesta rodada, por não fazer parte do
escopo de I1/M5.
