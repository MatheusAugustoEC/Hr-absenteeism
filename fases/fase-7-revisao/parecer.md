# Parecer da banca — Absenteísmo evitável no trabalho

27/09/2026 · rodada 1 · `file:///C:/Users/Augusto/Desktop/Projetos/hr-absenteeism-dmaic/fases/fase-6-entrega/artefatos/index.html` (sem site publicado) · nível 2 (repositório local, pasta `fases/`) · revisão visual: realizada

## Veredito

**APROVADO COM RESSALVAS** — nenhum achado crítico muda o número principal, a recomendação ou a decisão. Há 6 achados importantes (dois deles de legibilidade/robustez que merecem correção antes de qualquer publicação, os demais de completude) e 4 menores.

## A banca

- **Gestor** — Gerente de RH/Operações de uma transportadora de médio porte em Brasília (~35 funcionários, ~17 rotas). Dono das duas ações recomendadas.
- **Especialista do domínio** — Coordenador de Operações/Tráfego de transportadora rodoviária, responsável por escala de rotas e turnos.
- **Cientista de dados sênior** — especializado em inferência causal e desenho experimental com dados agrupados (cluster/ID repetido).
- **Recrutador de dados** — calibrado para vaga de analista de dados júnior e cientista de dados júnior, mercado brasileiro, processo seletivo generalista.

## A voz de cada revisor

**Gestor:** Em menos de um minuto no Dashboard eu entendo o tamanho do problema — 64,3% sem atestado, meta em 33,4% — mas não encontro ali a decisão que eu preciso aprovar; só ao abrir o Relatório ou os Slides vejo as duas ações propostas. A conta da segunda ação (agendamento) é honesta e me dá o número que decide (35,4% de adesão), o que eu valorizo bastante — poucos relatórios internos fazem isso. A primeira ação (travar o código no sistema) não tem estimativa nenhuma de efeito, mesmo sendo apresentada lado a lado com uma ação totalmente quantificada — isso me deixaria perguntando "e essa aqui, resolve quanto?" na reunião. O plano de sustentação com o guardrail do atestado médico é exatamente o que eu pediria — isso eu aprovaria sem hesitar.

**Especialista do domínio:** O tratamento da distância parece tecnicamente cuidadoso, e gostei de ver que testaram se o efeito não era só de poucos funcionários com muitos eventos — isso é o tipo de pergunta que eu faria. Mas ninguém testou a explicação concorrente mais óbvia do meu ponto de vista: quem mora mais longe do trabalho pode também morar mais longe dos serviços de saúde concentrados no Plano Piloto, o que mudaria consultas rápidas em duração e frequência sem que a causa seja a distância ao trabalho em si. A separação entre atestado médico (protegido) e ausência administrável (alvo da ação) está correta e é a linha que eu, no meu lugar, também traçaria. A viabilidade prática de "agendar fora do expediente" depende de algo que a página não discute: se os serviços de saúde que essas pessoas usam (postos, clínicas populares) têm horário fora do expediente — isso eu verificaria antes de aprovar o piloto.

**Cientista de dados sênior:** Os números batem entre Dashboard e Relatório em todas as contas que cruzei — inclusive a decomposição de horas e de participação percentual, o que não é trivial e mostra cuidado. O tratamento do agrupamento por funcionário está correto do início ao fim: bootstrap por cluster, holdout por ID, exclusão do funcionário mais frequente testada. O maior gap metodológico que encontrei é que o Pareto de horas — onde "consulta médica" domina com 31,3% — nunca passou pelo mesmo teste de concentração que a hipótese da distância passou; não dá pra saber se esse ranking também é robusto a poucos funcionários com muitos eventos. Achei também um defeito visual real, não hipotético: os rótulos desse mesmo gráfico se sobrepõem e ficam ilegíveis, nos três temas que testei.

**Recrutador de dados:** Em 30 segundos entendo o achado principal e fico impressionado com o rigor — Bonferroni, poder estatístico declarado, holdout, tudo isso é acima do que vejo em portfólio júnior. Mas não achei nome, GitHub, LinkedIn ou contato em lugar nenhum da página publicada — nem no README, que só tem "Autor: Augusto" sem link nenhum. Isso é um problema sério de portfólio: o projeto pode ser excelente e eu simplesmente não saberia a quem atribuir. Também não vi o projeto se posicionar explicitamente contra a abordagem padrão desse dataset (regressão para prever horas), que é o ângulo que praticamente todo notebook público usa — quem não conhece o dataset não percebe que isso é incomum, e é exatamente esse o diferencial que eu queria ver destacado.

## Achados críticos

Nenhum.

## Achados importantes

| ID | Achado | Evidência | Correção | Fase de origem |
|---|---|---|---|---|
| I1 | Rótulos sobrepostos no gráfico de Pareto de horas do Relatório, tornando-o ilegível | `sobreposicao.md`: "Consulta O." × "Acompanhamento" e "Acompanhamento" × "Fisioterapia" colidem em desktop, escuro e celular; confirmado visualmente em `graficos/desktop__unico__relatório__00.png` | Rotacionar ou abreviar os rótulos do eixo X, ou aumentar o espaçamento entre categorias | Fase 6 · Entrega |
| I2 | Dominância de "consulta médica" (31,3% das horas de B2, 31,0% dos eventos evitáveis) nunca foi testada quanto à concentração em poucos funcionários — ao contrário do que foi feito para o efeito de distância (H2, seção 8 do Relatório) | `texto/unico__relatório.txt`, seção 3 e 15; nenhuma seção do Relatório ou de `fases/fase-2b-measure-baseline/relatorio.md` reporta esse teste para o Pareto de motivo | Repetir para "consulta médica" o mesmo teste de robustez feito para H2: excluir os funcionários mais frequentes de consulta médica, um de cada vez, e ver se a participação continua dominante | Pós-hoc a partir da Fase 2B/Analyze |
| I3 | Hipótese setorial concorrente não considerada: proximidade a serviços de saúde (não só ao trabalho) pode explicar parte do efeito de distância, distinta da explicação usada | Seção 8 do Relatório testa só a hipótese rival "poucos funcionários" — não testa nem menciona acesso a saúde | Declarar como hipótese a verificar (não testável com esta base — falta endereço/localização de clínica); citar como limitação adicional na seção 14 | Fase 3 · Analyze — declaração, não teste novo |
| I4 | Nenhuma informação de autoria (nome, GitHub, LinkedIn, contato) na página publicada; README tem só "Autor: Augusto" sem links | `texto/unico__dashboard.txt` e `texto/unico__relatório.txt` completos, sem menção de autor; `grep -i "github\|linkedin\|autor\|contato"` em `index.html` não retorna nada; `README.md` linha 6-7 só tem "Autor: Augusto — 26/09/2026" | Adicionar nome completo, GitHub e LinkedIn (ou contato) no rodapé da página e no topo do README | Fase 6 · Entrega |
| I5 | O Dashboard (aba padrão, a primeira que qualquer leitor vê) não apresenta a recomendação nem as ações propostas — só métricas e composição; a decisão só aparece no Relatório (seção 2) ou nos Slides | `texto/unico__dashboard.txt` completo: nenhuma menção às duas ações ("trava no sistema", "piloto de agendamento") | Adicionar um bloco curto no Dashboard com as duas ações recomendadas e seus status (pronta / piloto proposto), com link para a seção correspondente do Relatório | Fase 6 · Entrega |
| I6 | O heatmap "Tipo e distância, cruzados" (Dashboard) não mostra o n de cada célula | `capturas/desktop__unico__dashboard.png`, seção "TIPO E DISTÂNCIA, CRUZADOS"; `numeros.md` só lista os valores percentuais (42,5 / 31,1 / 42,8 / 62,4 / 14,7 / 6,5), sem n por célula | Adicionar o n (contagem de eventos) dentro ou abaixo de cada célula do heatmap | Fase 6 · Entrega |
| I7 | Tabela "Motivo/Distância/Dia/Eventos/Horas" do Dashboard é pouco informativa (repete em drill-down o que o heatmap e os Paretos já mostram) — substituir por gráficos de padrão por dia da semana e por mês, decompostos por categoria. Dia da semana é descritivo seguro (H4 já testada e descartada); mês cruzado com eventos fixos de calendário (Carnaval, Natal) é hipótese nova, pós-hoc, nascida após o holdout aberto | `texto/unico__dashboard.txt`, tabela final; Notas técnicas, seção 15 (H4: 3,95 pp, p=0,5546, descartada); `fases/indice.md`, linha "HOLDOUT ABERTO" (Fase 5 · Control) | Ver apontamento [I7] — sugestão trazida pelo responsável do projeto durante a revisão, 27/09/2026 | Adendo pós-Fase 7, 27/09/2026 |

## Achados menores

- **M1** — Rótulo "meta 33%" no gráfico "Por funcionário" do Dashboard arredonda para 33%, enquanto o texto ao lado e o Relatório usam 33,4% — inconsistência de arredondamento. (`capturas/desktop__unico__dashboard.png`, bloco "POR FUNCIONÁRIO")
- **M2** — A ação 1 (trava do código administrativo no sistema) não tem estimativa numérica do efeito esperado, ao lado de uma ação 2 totalmente quantificada. (`texto/unico__relatório.txt`, seção 2)
- **M3** — O diferencial do projeto (agrupamento correto por funcionário, decomposição evitável/não-evitável) não é dito em contraste explícito com a abordagem padrão do dataset (regressão para prever horas), que a maioria dos notebooks públicos usa. (página inteira — nenhuma menção a isso)
- **M4** — `requirements.txt` sem versões fixadas, pendência já registrada na Fase 5 e não resolvida até a Entrega — risco de reprodução divergente em outra máquina. (`fases/indice.md`, linha da Fase 5 · Control)

## Adendo — 27/09/2026

Durante a leitura deste parecer, o responsável trouxe uma sugestão própria (não
gerada pela banca): substituir a tabela "Motivo/Distância/Dia/Eventos/Horas" do
Dashboard por gráficos de padrão por dia da semana e por mês, separados por
categoria (atestado, administrável, sem justificativa), e cruzar o mês com
eventos fixos de calendário (Carnaval, Natal). Avaliada e registrada como
achado **I7** acima — a parte de dia da semana é descritiva e segura de
acrescentar (desde que cite que H4 já foi testada e descartada); a parte de
mês×calendário é uma hipótese nova, pós-hoc (o holdout desta rodada já está
aberto desde a Fase 5 · Control), e precisa entrar rotulada como exploratória,
nunca como achado confirmado.

## O que corrigir, passo a passo

### [I1] · Rótulos sobrepostos no Pareto de horas — prioridade 1
O problema, em linguagem simples: no gráfico "Horas por motivo" do Relatório (a curva vermelha de Pareto), os nomes "Consulta O.", "Acompanhamento" e "Fisioterapia" ficam colados uns nos outros no eixo horizontal, e não dá para ler onde um nome termina e o outro começa.
Por que importa: quem olha rápido pode ler "Consulta OAcompanhamento" como um motivo só, ou simplesmente não confiar no gráfico.
Onde está: modo Relatório, seção "3. O que descobri", gráfico de Pareto (horas por motivo). Confirmado em desktop, tema escuro e celular.
O que fazer:
  1. No componente que desenha esse gráfico, rotacionar os rótulos do eixo X (ex.: -30 a -45 graus) ou abreviar mais os nomes das categorias.
  2. Se a rotação não resolver, aumentar a largura mínima por categoria ou reduzir o tamanho da fonte do rótulo até parar de colidir.
  3. Repetir a checagem nos três temas (claro, escuro) e no celular.
Como saber que ficou certo: rodar de novo a checagem de sobreposição sobre esse gráfico nos três modos e não haver nenhuma ocorrência de "texto sobre texto" nele.
O que pode mudar junto: nada além do layout do próprio gráfico.
Tamanho: pequeno (ajuste de estilo do gráfico).
Fase de origem: Fase 6 · Entrega.

---

### [I2] · Testar concentração no Pareto de "consulta médica" — prioridade 2
O problema, em linguagem simples: o gráfico de horas por motivo mostra "consulta médica" como o motivo que mais consome tempo (31,3% das horas administráveis). Não foi verificado se isso vem de muitos funcionários diferentes ou de poucos funcionários com muitas consultas cada.
Por que importa: se for concentrado em poucos funcionários, "consulta médica" deixa de ser o alvo certo de uma ação geral de agendamento — a ação teria de mirar esses funcionários específicos, não o motivo em si.
Onde está: Relatório, seção "3. O que descobri" (tabela de participação e horas por motivo); Dashboard, bloco "ONDE ESTÁ O TEMPO PERDIDO".
O que fazer:
  1. Calcular a participação de "consulta médica" nas horas administráveis excluindo, um de cada vez, os 3 funcionários com mais eventos de consulta médica — no mesmo molde do teste já feito para H2 (seção 8 do Relatório).
  2. Se a participação continuar acima de ~25-30% mesmo excluindo os 3 principais, registrar como robusto; se cair para próximo da média das outras categorias, declarar a concentração explicitamente no texto.
  3. Adicionar o resultado como uma frase curta perto do gráfico "Horas por motivo", no mesmo padrão da caixa "O efeito não depende de poucos funcionários" da seção 8.
Pronto quando: existir uma frase no Relatório citando o resultado desse teste, com o intervalo de participação (ex.: "X%–Y% mesmo excluindo os 3 funcionários mais frequentes").
Muda junto: nenhum número principal muda — só a seção 3 do Relatório ganha uma checagem a mais.
Tamanho: médio (novo cálculo sobre a base já processada, sem reabrir o holdout).
Fase de origem: pós-hoc a partir da Fase 2B/Analyze — registrar como tal.

---

### [I3] · Declarar a hipótese de acesso a saúde como limitação — prioridade 3
O problema, em linguagem simples: a página testou se o efeito da distância era só um artefato de poucos funcionários, mas não considerou (nem descartou por escrito) que morar mais longe do trabalho pode também significar morar mais longe de clínicas e postos de saúde — o que mudaria a duração/frequência das consultas por um motivo diferente da distância ao trabalho em si.
Por que importa: se essa explicação concorrente for verdadeira, o piloto de agendamento (que mira "quem mora longe do trabalho") pode estar mirando a proxy errada.
Onde está: Relatório, seção "8. A explicação que quase me enganou" (só cobre a hipótese de concentração em poucos funcionários) e seção "14. O que eu não sei".
O que fazer:
  1. Verificar se a base tem alguma variável de localização além de "Distance from Residence to Work" que permita aproximar acesso a saúde (não deve ter — é uma limitação a declarar, não um teste a rodar).
  2. Adicionar um item na seção "14. O que eu não sei": distância ao trabalho pode ser proxy de distância a serviços de saúde, e a base não permite separar as duas explicações.
Pronto quando: a lista de "O que eu não sei" tiver esse item, com uma frase explicando por que não é testável com esta base.
Muda junto: nada além do texto da seção 14; nenhum número muda.
Tamanho: pequeno (texto).
Fase de origem: Fase 3 · Analyze — declaração de limite, não teste novo.

---

### [I4] · Adicionar autoria à página e ao README — prioridade 4
O problema, em linguagem simples: quem chega na página publicada não encontra nome, GitHub, LinkedIn ou qualquer contato do autor.
Por que importa: numa peça de portfólio, isso impede o leitor (um recrutador, por exemplo) de saber a quem atribuir o trabalho ou como entrar em contato — o esforço todo do projeto perde alcance.
Onde está: rodapé (ou cabeçalho) da página, em todos os modos; topo do README.
O que fazer:
  1. Adicionar um rodapé fixo na página (visível em Dashboard, Relatório e Slides) com nome completo, link do GitHub e link do LinkedIn (ou outro contato à escolha do autor).
  2. Atualizar a linha "Autor: Augusto — 26/09/2026" do README para incluir os mesmos links.
Se os dados reais não estiverem disponíveis nesta conversa, usar `<preencha: nome completo · URL do GitHub · URL do LinkedIn>` nesse passo e avisar que precisa ser completado antes de publicar.
Pronto quando: o rodapé aparece nas quatro capturas (`capturas/*.png`) e o README mostra os mesmos links.
Muda junto: nada além de rodapé e README.
Tamanho: pequeno.
Fase de origem: Fase 6 · Entrega.

---

### [I5] · Mostrar a recomendação também no Dashboard — prioridade 5
O problema, em linguagem simples: quem abre a página cai no Dashboard, mas o Dashboard só mostra números — as duas ações recomendadas (travar o código, piloto de agendamento) só aparecem no Relatório ou nos Slides.
Por que importa: um leitor que decide não rolar até o Relatório sai sem saber qual é a decisão proposta, que é o objetivo final do projeto.
Onde está: modo Dashboard, em qualquer ponto — atualmente ausente.
O que fazer:
  1. Adicionar um bloco curto (2 linhas) no Dashboard, logo abaixo do número-herói (64,3%), com as duas ações e seus status: "Trava no sistema — pronta" e "Piloto de agendamento — proposto, não confirmado".
  2. Linkar esse bloco à seção 2 do Relatório ("A recomendação"), para quem quiser os detalhes e a conta.
Pronto quando: o bloco aparece em `capturas/desktop__unico__dashboard.png` (ou na nova captura, após a correção) sem precisar trocar de aba.
Muda junto: nada além do layout do Dashboard; nenhum número muda.
Tamanho: pequeno/médio (novo bloco de UI, sem novo cálculo).
Fase de origem: Fase 6 · Entrega.

---

### [I6] · Adicionar n às células do heatmap de distância — prioridade 6
O problema, em linguagem simples: o quadro "Tipo e distância, cruzados" mostra percentuais (ex.: 62,4% para ausência administrável entre quem mora mais longe), mas não mostra quantos eventos sustentam cada percentual.
Por que importa: sem o n, o leitor não consegue avaliar sozinho se algum percentual vem de poucos eventos e é menos confiável que os outros.
Onde está: Dashboard, bloco "TIPO E DISTÂNCIA, CRUZADOS".
O que fazer:
  1. Calcular o n (contagem de eventos) de cada uma das 6 células (3 tipos × 2 faixas de distância) a partir da base já processada.
  2. Exibir o n entre parênteses abaixo do percentual em cada célula do heatmap (ex.: "62,4% (n=228)").
Pronto quando: as 6 células do heatmap mostram percentual e n juntos.
Muda junto: nada além da exibição; os percentuais não mudam.
Tamanho: pequeno.
Fase de origem: Fase 6 · Entrega.

---

### [I7] · Trocar a tabela bruta por padrão de dia da semana e mês — prioridade 6b
O problema, em linguagem simples: a tabela final do Dashboard lista eventos
individuais cruzando motivo, distância, dia e horas — é densa e repete o que
os gráficos acima já mostram, sem contar uma história nova. É uma dúvida
natural de quem olha o Dashboard ("qual dia/mês tem mais ausência?"), então
vale responder — mas os dois gráficos propostos têm status epistêmico
diferente, e cada um precisa do selo certo, **acima do gráfico**, no mesmo
padrão do selo "ACHADO PROMISSOR, NÃO CONFIRMADO" que a página já usa sobre o
heatmap de distância — não como legenda embaixo.
Por que importa: quem chega até o fim do Dashboard não ganha nada de novo com
essa tabela; e se os dois gráficos novos não vierem rotulados de forma
diferente um do outro, o leitor pode achar que "dia da semana" tem o mesmo
status de incerteza que "mês × calendário" — quando na verdade um já foi
testado e descartado, e o outro nunca foi testado.
Onde está: Dashboard, bloco final, tabela "MOTIVO / DISTÂNCIA / DIA / EVENTOS / HORAS".
O que fazer:
  1. Dia da semana — já foi testado, não é exploratório: construir um gráfico
     de barras com a contagem (ou proporção) de eventos por dia da semana,
     decomposto em três séries — atestado médico, ausência administrável, sem
     justificativa. Acima do gráfico, em cor de destaque própria, o selo:
     "JÁ TESTADO — SEM EFEITO CONFIRMADO (H4)", com a frase: "Testado
     formalmente como hipótese pré-registrada; efeito de 3,95 p.p., abaixo do
     mínimo de 8 p.p. para agir, p=0,555 — o gráfico é só descritivo." Não
     chamar isso de "exploratório": seria mais fraco que a realidade, que é
     "testado e não confirmado".
  2. Mês × calendário — este sim é exploratório: escrever e datar a hipótese
     nova (ex.: "H5, hipótese pós-hoc, nascida em 27/09/2026 ao revisar a
     Entrega: meses com eventos fixos de calendário [Carnaval, Natal]
     concentram mais ausência administrável ou mais falta sem justificativa"),
     registrando a origem — não pré-registrada no Define, vale menos como
     evidência causal (regra 3 do contexto mestre).
  3. Levantar as datas reais de Carnaval em 2008, 2009 e 2010 (variam por
     seguir a Páscoa) e verificar em que mês cada uma caiu, antes de associar
     qualquer mês do dataset ao evento.
  4. Construir o gráfico de mês por categoria com, acima dele, um selo em cor
     própria (diferente da do item 1 e da do heatmap de distância):
     "EXPLORATÓRIO — HIPÓTESE NOVA, NÃO TESTADA", com a frase: "Nasceu ao
     olhar este Dashboard, não estava no pré-registro. Sem ordem cronológica
     confiável (mistura 3 anos) e sem amostra de confirmação restante (holdout
     já aberto na Fase 5 · Control) — leitura só sugestiva." Nunca usar
     linguagem de causa ou confirmação ("aumenta", "causa", "prova").
  5. Remover a tabela bruta atual do Dashboard, ou movê-la para uma seção
     opcional/expansível, já que os novos gráficos cobrem melhor o mesmo
     território.
  6. Atualizar o Relatório para refletir os dois gráficos novos: adicionar uma
     subseção (dentro da seção "3. O que descobri" ou uma seção nova)
     descrevendo os dois padrões, com os mesmos dois selos e as mesmas
     ressalvas do Dashboard. Nenhum conteúdo novo fica só no Dashboard.
Como saber que ficou certo: os dois gráficos novos existem no Dashboard E no
Relatório, cada um com o selo certo acima dele, em cor visualmente distinta
um do outro e do selo já existente do heatmap de distância; a tabela bruta
não aparece mais como conteúdo principal do bloco final.
O que pode mudar junto: nenhum número principal do projeto muda; é conteúdo
novo, não recálculo de achado existente. Se H5 mostrar algo interessante, não
pode virar "confirmado" nem nova recomendação de negócio sem uma rodada de
confirmação própria, que esta base não tem mais como fornecer.
Tamanho: médio (novos gráficos e cálculos descritivos, os dois selos, mais a
seção correspondente no Relatório) a grande, se a hipótese de calendário for
aprofundada além do descritivo.
Fase de origem: adendo pós-Fase 7, 27/09/2026 — pós-hoc.

---

### Acabamento (menores)
- **M1**: no gráfico "Por funcionário" do Dashboard, trocar o rótulo "meta 33%" por "meta 33,4%" para bater com o texto e o Relatório.
- **M2**: na tabela de ações da seção 2 do Relatório, adicionar uma coluna ou nota curta explicando o efeito esperado da ação 1 (ex.: "afeta até 39 eventos, 5,3% do total" — o n já reportado na seção 7), mesmo que não seja uma conta de horas.
- **M3**: no início do Relatório ou do README, adicionar uma frase contrastando o ângulo do projeto (agrupamento por funcionário, evitável/não-evitável) com a abordagem padrão do dataset (regressão para prever horas), citando que a maioria dos notebooks públicos usa esta última.
- **M4**: fixar as versões no `requirements.txt` (`pip freeze > requirements.txt` a partir do ambiente que rodou o pipeline com sucesso).

## O que está sólido

**Gestor:** a conta de ganho da ação 2 é completa e contestável linha a linha, com ponto de equilíbrio declarado (35,4%); o plano de sustentação tem o guardrail de atestado médico explícito; a meta interna tem origem declarada (quartil superior) e não é comparada a benchmark de mercado inexistente.

**Especialista do domínio:** a separação entre atestado médico (protegido) e ausência administrável (alvo) é exatamente a que o setor faria; a ação 1 (poka-yoke no sistema) atua na etapa certa, onde o erro de registro nasce; os riscos de má comunicação do piloto (pressão para não tirar atestado, percepção de discriminação) foram antecipados com mitigação.

**Cientista de dados sênior:** o agrupamento por funcionário é tratado corretamente do início ao fim — bootstrap por cluster, holdout por ID, exclusão de funcionários frequentes testada, poder estatístico baixo declarado em vez de escondido; a linguagem causal é proporcional à evidência em todos os textos lidos; os números batem entre Dashboard e Relatório em toda conferência cruzada feita.

**Recrutador de dados:** o achado principal e a margem de erro são entendidos em menos de 30 segundos; o rigor (Bonferroni, poder, holdout, hipótese pré-registrada) está muito acima do padrão júnior; a seção "A explicação que quase me enganou" é o tipo de conteúdo que demonstra pensamento crítico melhor que qualquer lista de habilidades.

## Cobertura dos roteiros

| Revisor | Itens | OK | Achado | Não se aplica |
|---|---|---|---|---|
| Gestor | 8 (G1–G8) | 6 | 2 (I5, M2) | 0 |
| Especialista do domínio | 8 (E1–E8) | 6 | 2 (I3, e nota de viabilidade dentro da voz do revisor) | 0 |
| Cientista de dados sênior | 12 (T1–T12) | 9 | 3 (I1, I2, I6) | 0 |
| Cientista de dados sênior — modelo | 8 (T13–T20) | 0 | 0 | 8 (projeto de diagnóstico, sem modelo preditivo) |
| Recrutador de dados | 8 (R1–R8) | 5 | 3 (I4, M1 não — M3, e nota de R6 dentro da voz) | 0 |

Todos os itens de todos os roteiros foram respondidos; nenhum ficou sem resposta.

## Matriz de achados

| ID | Gravidade | Revisor | Fase de origem | Pós-hoc | Status |
|---|---|---|---|---|---|
| I1 | Importante | Cientista de dados sênior | Fase 6 · Entrega | Não | aguardando decisão |
| I2 | Importante | Cientista de dados sênior | Fase 2B/Analyze | Sim | aguardando decisão |
| I3 | Importante | Especialista do domínio | Fase 3 · Analyze | Sim (declaração) | aguardando decisão |
| I4 | Importante | Recrutador de dados | Fase 6 · Entrega | Não | aguardando decisão |
| I5 | Importante | Gestor | Fase 6 · Entrega | Não | aguardando decisão |
| I6 | Importante | Cientista de dados sênior | Fase 6 · Entrega | Não | aguardando decisão |
| I7 | Importante | Sugestão do responsável (registrada pela banca) | Adendo pós-Fase 7 | Sim | aguardando decisão |
| M1 | Menor | Cientista de dados sênior | Fase 6 · Entrega | Não | aguardando decisão |
| M2 | Menor | Gestor | Fase 6 · Entrega | Não | aguardando decisão |
| M3 | Menor | Recrutador de dados | Fase 6 · Entrega | Não | aguardando decisão |
| M4 | Menor | Cientista de dados sênior | Fase 5 · Control | Não | aguardando decisão |

## Limites desta revisão

- A revisão foi feita sobre o arquivo local (`file:///…/index.html`), não há site publicado ainda — nível 1 foi feito sobre esse arquivo local, tratado como a "página" para todos os efeitos.
- Não foi possível verificar se os botões de download (.xlsx, .pptx, PDF) de fato geram arquivos corretos — a captura lê a página renderizada, não clica em botões de download nem abre os arquivos gerados.
- O modo "Slides" só foi capturado em largura de celular; a captura em desktop e tema escuro não encontrou esse modo isoladamente (o script de captura detectou só "Dashboard" e "Relatório" como modos distintos nesses casos, mas o conteúdo de Slides foi conferido via a captura de celular, que o mostrou corretamente com 9 slides e sem sobreposição).
- O nível 2 usado foi a pasta `fases/` local do repositório (não um repositório público no GitHub), já que não há link publicado; os números citados nos achados foram cruzados com `fases/indice.md` e `fases/fase-2b-measure-baseline/relatorio.md`.
- A viabilidade prática de "agendamento fora do expediente" (se os serviços de saúde usados pelos funcionários têm esse horário) é uma hipótese de setor da banca, não verificada nem verificável com o dado disponível — fica como pergunta para a próxima etapa, não como achado formal.
