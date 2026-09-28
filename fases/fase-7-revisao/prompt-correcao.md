# CORREÇÕES DA BANCA — Absenteísmo evitável no trabalho

Uma banca de revisores independentes revisou a página local do projeto
(`fases/fase-6-entrega/artefatos/index.html`, sem site publicado, 27/09/2026).
Abaixo estão as correções, na ordem em que devem ser feitas: as primeiras mudam
números de que as outras dependem. Execute todas de uma vez, uma por vez, na
ordem.

As correções marcadas com ⚑ mudam números. Depois de cada uma delas, confira o
"Pronto quando" antes de seguir:
- passou: escreva em uma linha o número antigo e o novo, e siga para a próxima;
- não passou, ou o número novo parece estranho (mudou de ordem de grandeza,
  inverteu uma conclusão): pare e me mostre o que aconteceu. Não construa as
  correções seguintes sobre um número que não passou.

Se eu tiver apagado algum bloco, é porque decidi não corrigir aquele ponto — não
o reintroduza.

## Regras
- Não mexa no que a banca considerou sólido: a conta de ganho da ação 2 (piloto
  de agendamento) e seu ponto de equilíbrio de 35,4%; a separação entre atestado
  médico (protegido) e ausência administrável (alvo); o tratamento do
  agrupamento por funcionário (bootstrap por cluster, holdout por ID); a
  linguagem causal proporcional à evidência em todo o texto.
- Refaça cada fase de origem gravando `relatorio-v2.md` (sem apagar o
  `relatorio.md` original) na respectiva pasta de `fases/`, e atualize
  `fases/indice.md` com a mudança.
- O holdout já foi aberto (Fase 5 · Control): toda correção que mude a análise
  (I2, I3) é pós-hoc — registre isso explicitamente no relatório e na página, e
  não "reconfirme" no holdout, que continua congelado.
- Um número mudou? Atualize todos os lugares da página em que ele aparece — nos
  quatro modos (Dashboard, Relatório, Slides, e o PDF gerado do Relatório).
- Conteúdo novo adicionado ao Dashboard (gráfico, bloco, selo) entra também no
  Relatório, nos mesmos termos e com a mesma ressalva — o Dashboard nunca é o
  único lugar onde uma leitura nova aparece.
- Ao terminar todas as correções: refaça a Entrega (rode de novo o script de
  geração de dados da Entrega, se algum número mudou), rode de novo a auditoria
  final da página (a mesma rotina de captura com navegador real já usada nas
  rodadas anteriores da Fase 6), grave o que foi feito em
  `fases/fase-7-revisao/correcoes.md` — um item por ID, com o antes e o depois —
  e faça commit. Me diga, em uma linha por ID, o que mudou.

---

## [I1] Rótulos sobrepostos no Pareto de horas do Relatório — prioridade 1
Crítica: no gráfico "Horas por motivo" do modo Relatório (seção "3. O que
descobri", o gráfico de Pareto com a curva vermelha acumulada), os rótulos do
eixo X colidem: "Consulta O." se sobrepõe a "Acompanhamento", e
"Acompanhamento" se sobrepõe a "Fisioterapia" — ficam ilegíveis, como se fosse
um nome só.
Onde: modo Relatório, seção 3, gráfico de Pareto de horas por motivo.
Confirmado em desktop, tema escuro e celular (os três temas testados).
O que fazer:
  1. No componente que desenha esse gráfico, rotacionar os rótulos do eixo X
     (por exemplo -30 a -45 graus) ou abreviar mais os nomes das categorias
     até parar de colidir.
  2. Se a rotação não resolver sozinha, aumentar a largura mínima por
     categoria ou reduzir o tamanho da fonte do rótulo.
  3. Conferir visualmente o resultado nos três temas (claro, escuro) e na
     largura de celular.
Pronto quando: inspecionando o gráfico nos três temas, nenhum rótulo do eixo X
encosta ou se sobrepõe a outro.
Muda junto: nada além do layout deste gráfico — nenhum número muda.
Fase de origem: Fase 6 · Entrega.

---

## [I2] ⚑ Testar concentração no Pareto de "consulta médica" — prioridade 2
Crítica: o motivo "consulta médica" domina o ranking de horas administráveis
(31,3% das horas, 31,0% dos eventos evitáveis), mas, ao contrário do que foi
feito para a hipótese da distância (H2, onde se testou excluir os 3
funcionários mais frequentes um de cada vez), ninguém testou se essa
dominância vem de muitos funcionários diferentes ou de poucos funcionários com
muitas consultas cada.
Onde: Relatório, seção "3. O que descobri" (tabela de participação/horas por
motivo); Dashboard, bloco "ONDE ESTÁ O TEMPO PERDIDO". Nível 2: o cálculo deve
partir da mesma base processada usada na Fase 2B
(`data/processed/eventos_qualidade.csv`, 733 eventos, 34 identidades).
O que fazer:
  1. Calcular a participação de "consulta médica" nas horas administráveis
     (B2) excluindo, um de cada vez, os 3 funcionários com mais eventos de
     consulta médica — no mesmo desenho do teste da seção 8 do Relatório
     (H2, rival estrutural).
  2. Registrar os valores resultantes (participação com cada exclusão) e
     comparar com o valor bruto de 31,3%/31,0%.
  3. Se a participação permanecer acima de ~25% mesmo excluindo os 3
     principais, escrever no Relatório uma frase no mesmo estilo da caixa "O
     EFEITO NÃO DEPENDE DE POUCOS FUNCIONÁRIOS" da seção 8, mas para este
     Pareto. Se cair para perto da média das outras categorias, declarar a
     concentração explicitamente e ajustar a leitura da seção 3 (o
     texto atual, "consulta médica e odontológica continuam liderando o
     tempo perdido", precisaria de ressalva).
Pronto quando: existe, na seção 3 do Relatório, uma frase citando o
intervalo de participação de "consulta médica" com cada uma das 3 exclusões
testadas, no mesmo padrão da seção 8.
Muda junto: se a concentração for confirmada, a recomendação da seção 2 pode
precisar de nota adicional (mirar funcionários específicos, não só o motivo).
Se não for confirmada, nenhuma outra mudança.
Fase de origem: pós-hoc a partir da Fase 2B/Analyze — registre como pós-hoc,
já que o holdout está aberto.

---

## [I3] Declarar a hipótese de acesso a saúde como limitação — prioridade 3
Crítica: a página testou se o efeito da distância era um artefato de poucos
funcionários (seção 8), mas não considerou nem descartou por escrito uma
explicação concorrente: morar mais longe do trabalho pode também significar
morar mais longe de clínicas e postos de saúde, o que mudaria a duração ou
frequência das consultas por um motivo diferente da distância ao trabalho em
si. Se essa explicação for verdadeira, o piloto de agendamento mira a proxy
errada.
Onde: Relatório, seção "14. O que eu não sei" (lista de limitações).
O que fazer:
  1. Confirmar que a base não tem nenhuma coluna de localização além de
     "Distance from Residence to Work" (não deve ter — isso é o que torna a
     hipótese não testável, e é o ponto a declarar).
  2. Adicionar um item à lista da seção 14: "Distância ao trabalho pode ser
     proxy de distância a serviços de saúde — a base não tem como separar as
     duas explicações, e o piloto de agendamento assume que a causa é a
     primeira."
Pronto quando: o item aparece na seção 14 do Relatório, em todos os modos e
registros de linguagem da página.
Muda junto: nenhum número muda — só o texto da seção 14 e, se fizer sentido,
uma nota curta na seção 2 (a recomendação) mencionando essa limitação.
Fase de origem: Fase 3 · Analyze — declaração de limite, não teste novo
(pode ser adicionada como adendo datado ao relatório da Fase 3, já concluída).

---

## [I4] Adicionar autoria à página e ao README — prioridade 4
Crítica: a página publicada não tem nome, GitHub, LinkedIn ou qualquer contato
do autor em lugar nenhum; o README só tem "Autor: Augusto — 26/09/2026", sem
nenhum link. Numa peça de portfólio, isso impede o leitor de saber a quem
atribuir o trabalho ou como entrar em contato.
Onde: rodapé (ou cabeçalho) de `fases/fase-6-entrega/artefatos/index.html`, em
todos os modos (Dashboard, Relatório, Slides); linha 6-7 de `README.md`.
O que fazer:
  1. Adicionar um rodapé fixo na página, visível nos três modos, com nome
     completo, link do GitHub e link do LinkedIn (ou outro contato à escolha
     do autor). Se esses dados não estiverem disponíveis nesta conversa, usar
     `<preencha: nome completo · URL do GitHub · URL do LinkedIn>` neste passo
     e avisar no fim da execução que esse campo precisa ser completado antes
     de publicar a página.
  2. Atualizar a linha "Autor: Augusto — 26/09/2026" do README para incluir os
     mesmos links.
Pronto quando: o rodapé aparece em todos os modos da página e o README mostra
os mesmos links (ou o placeholder, se os dados não estiverem disponíveis).
Muda junto: nada além de rodapé e README.
Fase de origem: Fase 6 · Entrega.

---

## [I5] Mostrar a recomendação também no Dashboard — prioridade 5
Crítica: o Dashboard (a aba padrão, a primeira que qualquer leitor vê) só
mostra métricas e composição — as duas ações recomendadas ("trava no
sistema", "piloto de agendamento") só aparecem no Relatório (seção 2) ou nos
Slides. Quem não rola até o Relatório sai sem saber qual é a decisão proposta.
Onde: modo Dashboard — atualmente ausente em qualquer ponto da aba.
O que fazer:
  1. Adicionar um bloco curto (2 linhas) no Dashboard, logo abaixo do
     número-herói (64,3%), com as duas ações e seus status: "Trava no
     sistema — pronta, sem custo real de implementação" e "Piloto de
     agendamento — proposto, não confirmado".
  2. Linkar esse bloco à seção 2 do Relatório ("A recomendação"), para quem
     quiser a conta completa.
Pronto quando: o bloco aparece no Dashboard sem precisar trocar de aba, nos
três temas.
Muda junto: nada além do layout do Dashboard; nenhum número muda.
Fase de origem: Fase 6 · Entrega.

---

## [I6] ⚑ Adicionar n às células do heatmap de distância — prioridade 6
Crítica: o quadro "Tipo e distância, cruzados" do Dashboard mostra percentuais
(ex.: 62,4% de ausência administrável entre quem mora mais longe), mas não
mostra quantos eventos sustentam cada percentual — o leitor não consegue
avaliar sozinho se algum percentual vem de poucos eventos.
Onde: Dashboard, bloco "TIPO E DISTÂNCIA, CRUZADOS".
O que fazer:
  1. Calcular o n (contagem de eventos) de cada uma das 6 células (3 tipos ×
     2 faixas de distância) a partir da mesma base usada para os percentuais
     já exibidos.
  2. Exibir o n entre parênteses abaixo do percentual em cada célula (ex.:
     "62,4% (n=228)").
Pronto quando: as 6 células mostram percentual e n juntos, nos três temas.
Muda junto: nada — os percentuais não mudam, só ganham o n ao lado.
Fase de origem: Fase 6 · Entrega.

---

## [I7] Trocar a tabela bruta do Dashboard por padrão de dia da semana e mês — prioridade 6b
Crítica: a tabela final do Dashboard ("Motivo / Distância / Dia / Eventos /
Horas") é densa e repete, em drill-down, o que o heatmap e os Paretos acima já
mostram, sem contar nada novo. Um gráfico de padrão por dia da semana e por
mês, separado por categoria (atestado médico, ausência administrável, sem
justificativa), comunicaria melhor com menos esforço de leitura — é uma
dúvida natural de quem olha o Dashboard ("qual dia/mês tem mais ausência?").
Os dois gráficos têm status epistêmico DIFERENTE um do outro, e cada um leva
um selo diferente, no mesmo padrão visual que a página já usa para o selo
"ACHADO PROMISSOR, NÃO CONFIRMADO" acima do heatmap de distância — ou seja,
**acima do gráfico, antes do leitor ver os números**, não como legenda embaixo.
Onde: Dashboard, bloco final, tabela atual "MOTIVO / DISTÂNCIA / DIA / EVENTOS / HORAS".
O que fazer:
  1. Dia da semana — já foi testado, não é exploratório: construir um gráfico
     de barras com a contagem ou proporção de eventos por dia da semana,
     decomposto em três séries — atestado médico, ausência administrável, sem
     justificativa. Acima do gráfico, em destaque visual (cor diferente do
     selo do heatmap de distância), o selo: "JÁ TESTADO — SEM EFEITO
     CONFIRMADO (H4)", com a frase: "Testado formalmente como hipótese
     pré-registrada; efeito de 3,95 p.p., abaixo do mínimo de 8 p.p. para
     agir, p=0,555 — o gráfico é só descritivo." Não usar "exploratório" aqui:
     seria mais fraco que a realidade, que é "testado e não confirmado".
  2. Mês × calendário — este sim é exploratório: escrever e datar, no
     Relatório ou num arquivo de registro de hipóteses, a hipótese nova: "H5,
     hipótese pós-hoc, nascida em 27/09/2026 ao revisar a Entrega: meses com
     eventos fixos de calendário (Carnaval, Natal) concentram mais ausência
     administrável ou mais falta sem justificativa." Registrar que não foi
     pré-registrada no Define e que, por isso, vale menos como evidência
     causal (regra 3 do contexto mestre).
  3. Antes de qualquer gráfico, levantar as datas reais de Carnaval em 2008,
     2009 e 2010 (a data varia ano a ano, segue a Páscoa) e checar em que mês
     cada uma caiu — não assumir que Carnaval é sempre fevereiro.
  4. Construir o gráfico de mês por categoria com, acima dele, um selo em cor
     própria (diferente da do item 1 e da do heatmap de distância): "EXPLORATÓRIO
     — HIPÓTESE NOVA, NÃO TESTADA", com a frase: "Nasceu ao olhar este
     Dashboard, não estava no pré-registro. Sem ordem cronológica confiável
     (mistura 3 anos) e sem amostra de confirmação restante (o holdout desta
     rodada já foi aberto na Fase 5 · Control) — leitura só sugestiva." Nunca
     usar linguagem de causa ou confirmação para esse cruzamento.
  5. Remover a tabela bruta atual do Dashboard, ou movê-la para uma seção
     opcional/expansível — os dois gráficos novos cobrem melhor o mesmo
     território de forma mais legível.
  6. Atualizar o Relatório para refletir os dois gráficos novos: adicionar uma
     subseção (pode ser dentro da seção "3. O que descobri" ou uma nova
     seção) descrevendo os dois padrões, com os mesmos dois selos e as mesmas
     ressalvas do Dashboard — nunca só no Dashboard. Qualquer conteúdo novo
     que entrar no Dashboard por esta correção entra também no Relatório, nos
     mesmos termos, nos três temas e no PDF gerado do Relatório.
Pronto quando: os dois gráficos novos existem no Dashboard E no Relatório,
cada um com o selo certo acima dele (não embaixo), em cor visualmente distinta
um do outro e do selo já existente do heatmap de distância, nos três temas
(claro, escuro, celular); a tabela bruta não é mais o conteúdo principal do
bloco final.
Muda junto: nenhum número principal do projeto muda — é conteúdo novo, não
recálculo de achado existente. Se a hipótese de calendário (H5) mostrar algo
interessante, isso NÃO pode subir de status para "confirmado" nem virar nova
recomendação de negócio sem uma rodada de confirmação própria, que esta base
não tem mais como fornecer (holdout já consumido).
Fase de origem: adendo pós-Fase 7, 27/09/2026 — pós-hoc.

---

## Acabamento (menores) — prioridade 7, todos juntos

- **M1**: no gráfico "Por funcionário" do Dashboard, trocar o rótulo "meta
  33%" por "meta 33,4%" para bater com o texto ao lado e com o Relatório.
- **M2**: na tabela de ações da seção 2 do Relatório, adicionar uma nota curta
  com o efeito esperado da ação 1 — ex.: "afeta até 39 eventos, 5,3% do
  total" (o n de 39 já está reportado na seção 7, hipótese H3) — mesmo que não
  seja uma conta de horas.
- **M3**: no início do Relatório ou do README, adicionar uma frase
  contrastando o ângulo do projeto (agrupamento correto por funcionário,
  decomposição evitável/não-evitável por categoria) com a abordagem padrão
  do dataset (regressão para prever "Absenteeism time in hours"), citando que
  é essa a abordagem que a maioria dos notebooks públicos usa com este
  dataset.
- **M4**: fixar as versões no `requirements.txt` rodando `pip freeze` a partir
  do ambiente que executou o pipeline com sucesso, e commitar o arquivo
  atualizado.

Pronto quando (para os quatro juntos): cada um dos quatro pontos acima está
refletido na página ou nos arquivos citados.
Fase de origem: Fase 6 · Entrega (M1-M3); Fase 5 · Control (M4).
