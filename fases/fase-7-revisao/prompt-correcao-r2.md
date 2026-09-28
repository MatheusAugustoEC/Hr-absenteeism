# CORREÇÕES DA BANCA — Absenteísmo evitável no trabalho (rodada 2)

Uma banca de revisores independentes conferiu, numa segunda rodada, as
correções aplicadas a partir do parecer da rodada 1
(`fases/fase-6-entrega/artefatos/index.html`, sem site publicado, 28/09/2026).
Da rodada anterior, 6 dos 7 achados importantes e os achados menores testáveis
pela página foram confirmados como resolvidos. Restam dois pontos abaixo.
Execute os dois, na ordem, um de cada vez.

A correção marcada com ⚑ pode envolver ajuste visual sem mudar número. Depois
dela, confira o "Pronto quando" antes de seguir. Se eu tiver apagado algum
bloco, é porque decidi não corrigir aquele ponto — não o reintroduza.

## Regras
- Não mexa no que já está confirmado sólido: I2 (28,4–33,8% / 27,2–33,1%,
  concentração de "consulta médica"), I3 (limitação de acesso à saúde), I5
  (bloco de recomendação), I6 (n nas células do heatmap), I7 (os dois gráficos
  novos e seus selos, incluindo o cálculo das datas de Carnaval). Nenhum
  desses precisa ser tocado de novo.
- O holdout continua não tocado (Fase 5 · Control) — nada nestas duas
  correções pode reabri-lo ou usá-lo.
- Depois de aplicar a correção de I1, rode de novo a checagem de sobreposição
  (o mesmo script/rotina já usado nas auditorias anteriores da Fase 6) nos
  três temas (claro, escuro) e no celular, sobre o gráfico de Pareto do
  Relatório especificamente — não confie em inspeção visual "parece bom": o
  teste automático já mostrou 2 vezes que o olho sozinho não bastou aqui.
- Ao terminar: atualize `fases/fase-7-revisao/correcoes.md` com uma nova
  seção "Rodada 2" (não sobrescreva a seção da rodada 1) — para I1, registre
  o que foi tentado antes (rótulos completos + rotação -38°, que piorou de 2
  para 4 colisões) e o que resolveu desta vez, com a evidência (contagem de
  colisões antes/depois). Atualize `fases/indice.md`. Faça commit. Me diga em
  uma linha por ID o que mudou.

---

## [I1] ⚑ Sobreposição no Pareto de horas do Relatório — a correção anterior piorou o problema — prioridade 1
Crítica: a correção da rodada 1 trocou os rótulos abreviados ("Consulta M.",
"Consulta O.") pelos nomes completos ("Consulta médica", "Consulta
odontológica", "Acompanhamento", "Fisioterapia", "Exame laboratorial",
"Doação de sangue") e rotacionou -38°, mas não testou se os nomes mais longos
caberiam sem colidir mesmo rotacionados. Resultado medido nesta rodada: agora
são 4 pares de rótulos sobrepostos (Consulta médica × Consulta odontológica;
Consulta odontológica × Acompanhamento; Fisioterapia × Exame laboratorial;
Exame laboratorial × Doação de sangue) — contra 2 pares antes da correção da
rodada 1. A correção piorou o problema que deveria resolver.
Onde: modo Relatório, seção "3. O que descobri", gráfico de Pareto de horas
por motivo (mesmo gráfico de I1 na rodada 1). Confirmado em desktop, tema
escuro e celular.
O que fazer:
  1. Escolher uma destas duas abordagens (ou combinar as duas se uma sozinha
     não bastar):
     a) Voltar aos nomes abreviados ("Consulta M.", "Consulta O.", "Acomp.",
        "Fisiot.", "Exame L.", "Doação S.") mantendo a rotação de -38°; ou
     b) Manter os nomes completos, mas aumentar a rotação para -60° ou -90°
        (vertical), que ocupa muito menos largura horizontal por rótulo.
  2. Se, mesmo assim, ainda houver colisão, aumentar a largura mínima
     reservada por categoria no eixo X (só são 6 categorias, há espaço de
     sobra) ou reduzir o tamanho da fonte do rótulo.
  3. Depois do ajuste, rodar de novo a checagem automática de sobreposição
     (não validar só visualmente) sobre este gráfico especificamente, nos
     três temas e na largura de celular.
Pronto quando: a checagem de sobreposição não acusa nenhuma ocorrência de
"texto sobre texto" no gráfico de Pareto do Relatório, em nenhum dos três
temas nem no celular.
Muda junto: nada além do layout deste gráfico — nenhum número muda.
Fase de origem: Fase 6 · Entrega — reaberto na Fase 7, rodada 2, 28/09/2026.

---

## [M5] Mover o gráfico "Por funcionário" para o fim do Dashboard — prioridade 2
Crítica: no Dashboard atual, a ordem dos blocos é: composição por motivo →
tempo perdido por motivo → cruzamento tipo×distância → **por funcionário
(anonimizado)** → padrão por dia da semana → padrão por mês → tabela
detalhada. O bloco "por funcionário" é o mais granular de todos depois da
tabela bruta, mas aparece no meio, antes dos padrões temporais — que são tão
agregados quanto os primeiros blocos da página. Isso quebra a progressão
natural de "mais agregado" para "mais granular".
Onde: Dashboard, ordem dos blocos principais (e Relatório, seção 3, se a
mesma sequência de conteúdo se aplicar lá).
O que fazer:
  1. Mover o bloco "POR FUNCIONÁRIO (ANONIMIZADO) — Quem está mais perto ou
     mais longe da meta" para depois do bloco "PADRÃO POR MÊS DO CALENDÁRIO"
     e antes de "Ver a tabela detalhada".
  2. Conferir a seção 3 do Relatório: se ela replica a mesma sequência de
     blocos do Dashboard (motivo → distância → funcionário → dia → mês),
     aplicar a mesma reordenação lá, mantendo Dashboard e Relatório
     consistentes entre si.
Pronto quando: a ordem dos blocos no Dashboard é motivo → tempo perdido →
distância → dia da semana → mês → por funcionário → tabela detalhada (e o
Relatório segue a mesma ordem, se aplicável).
Muda junto: nada além da ordem visual — nenhum gráfico, número ou texto muda
de conteúdo, só de posição.
Tamanho: pequeno (reordenação de layout, sem novo cálculo).
Fase de origem: adendo pós-Fase 7, rodada 2, 28/09/2026 — sugestão do
responsável, aceita pela banca.
