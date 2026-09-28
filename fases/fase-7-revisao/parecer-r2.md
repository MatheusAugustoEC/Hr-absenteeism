# Parecer da banca — Absenteísmo evitável no trabalho (rodada 2)

28/09/2026 · rodada 2 · `file:///C:/Users/Augusto/Desktop/Projetos/hr-absenteeism-dmaic/fases/fase-6-entrega/artefatos/index.html` (sem site publicado) · nível 2 (repositório local, pasta `fases/`, incluindo `fase-7-revisao/correcoes.md`) · revisão visual: realizada

Esta rodada não repete os roteiros inteiros: olha só os achados da rodada 1
(`parecer.md`) que foram marcados como corrigidos em `correcoes.md`, confere
se a correção realmente resolveu cada um, e verifica se alguma correção
quebrou algo que estava sólido. Uma sugestão nova do responsável também entrou
nesta rodada (ver M5).

## Veredito

**APROVADO COM RESSALVAS** — nenhum crítico. 6 dos 7 achados importantes da
rodada 1 foram confirmadamente resolvidos; **I1 continua aberto — a correção
aplicada não resolveu o problema, e a sobreposição piorou** (2 colisões antes,
4 agora). Achado novo M5 (menor, sugestão do responsável, aceita).

## Conferência achado a achado

| ID | O que `correcoes.md` afirma | O que a banca confirmou nesta rodada | Status |
|---|---|---|---|
| I1 | "Rótulos na íntegra, rotacionados -38°... nenhuma sobreposição" nos três temas | **Não confere.** `sobreposicao.md` desta rodada mostra 4 colisões de texto sobre texto no gráfico de Pareto do Relatório (antes eram 2) — os nomes completos ("Consulta médica", "Consulta odontológica") são mais longos que as versões abreviadas usadas antes e continuam colidindo mesmo rotacionados. Confirmado visualmente em `graficos/desktop__unico__relatório__00.png`. | **Reaberto — piorou** |
| I2 | Testada concentração de "consulta médica", faixa 28,4–33,8% das horas / 27,2–33,1% dos eventos, não concentrado | Confere. Presente no Relatório (seção 3, caixa "A LIDERANÇA NÃO DEPENDE DE POUCOS FUNCIONÁRIOS") e no Dashboard (nota no bloco "Onde está o tempo perdido"), com os mesmos números; Notas técnicas (seção 15) documenta o método e a data (pós-hoc, 27/09/2026), holdout não tocado | **Resolvido** |
| I3 | Limitação de proxy de saúde declarada na seção 14 | Confere. Item presente na seção 14 do Relatório, com a frase de conexão na seção 2 ("Ela também assume que a causa é a distância até o trabalho, não até serviços de saúde") | **Resolvido** |
| I4 | Rodapé com autoria, placeholder porque dados reais não disponíveis | Confere quanto ao mecanismo — rodapé presente nos três modos e no README, com o placeholder `<preencha: nome completo · URL do GitHub · URL do LinkedIn>`. Pendência humana, não é um novo achado da banca | **Pendente (esperado)** |
| I5 | Bloco de recomendação abaixo do número-herói no Dashboard, com link para o Relatório | Confere. Bloco presente ("Trava no sistema — pronta..." / "Piloto de agendamento — proposto...") com link "Ver a conta completa no Relatório →" | **Resolvido** |
| I6 | n em cada célula do heatmap de distância | Confere. As 6 células mostram percentual e n (ex.: "62,4% / n=271"); percentuais não mudaram | **Resolvido** |
| I7 | Tabela bruta movida para `<details>`; dois gráficos novos (dia da semana, mês) com selos distintos; Carnaval verificado por cálculo da Páscoa; espelhado no Relatório | Confere, e mais completo do que o pedido: o cálculo das datas de Carnaval (5/fev/2008, 24/fev/2009, 16/fev/2010) está registrado e datado, os dois selos usam cores visualmente distintas entre si e do selo do heatmap de distância, e a tabela bruta virou seção recolhível sem sumir (ainda alimenta o .xlsx) | **Resolvido** |
| M1 | Rótulo "meta 33%" → "meta 33,4%" | Confere — `capturas/desktop__unico__dashboard.png`, bloco "Por funcionário" | **Resolvido** |
| M2 | Nota de efeito da ação 1 no Relatório | Confere — "Afeta até 39 eventos — 5,3% do total registrado (seção 7, H3)" na seção 2 | **Resolvido** |
| M3 | Seção de contraste de ângulo no README | Não verificável pela banca nesta rodada (README não faz parte da captura da página) — aceito com base no que `correcoes.md` descreve; confira no README diretamente | **Não verificado pela banca (fora do escopo de captura)** |
| M4 | `requirements.txt` com versões fixas | Não verificável pela banca (arquivo fora da página) — aceito com base em `correcoes.md` | **Não verificado pela banca (fora do escopo de captura)** |

## O que a correção não quebrou

Conferido explicitamente porque é o segundo objetivo desta rodada:
- O número principal (64,3% [57,9%;69,1%]) e todos os números já sólidos da
  rodada 1 continuam idênticos em `numeros.md` desta rodada.
- O holdout continua não tocado — nenhuma menção nova a reabertura, I2 e H5
  seguem descritos como rodando só sobre a amostra de exploração.
- A separação atestado médico/administrável e a linguagem causal proporcional
  à evidência continuam consistentes nos dois gráficos novos (badges corretos,
  nenhuma linguagem de causa em H5).
- Os filtros, o heatmap e a tabela por funcionário continuam funcionando nos
  três temas e no celular, sem novo erro de console.

## Achado reaberto

### [I1] · Sobreposição no Pareto de horas — a correção piorou o problema
Onde: modo Relatório, seção "3. O que descobri", gráfico de Pareto de horas
por motivo. Confirmado em desktop, tema escuro e celular.
O que aconteceu: a correção trocou os rótulos abreviados ("Consulta M.",
"Consulta O.") pelos nomes completos ("Consulta médica", "Consulta
odontológica") e aplicou rotação de -38°, mas não testou se os nomes mais
longos, mesmo rotacionados, caberiam sem colidir. Resultado: agora são 4
pares de rótulos sobrepostos (Consulta médica × Consulta odontológica;
Consulta odontológica × Acompanhamento; Fisioterapia × Exame laboratorial;
Exame laboratorial × Doação de sangue), contra 2 antes da correção.
Evidência: `sobreposicao.md` desta rodada; `graficos/desktop__unico__relatório__00.png`.
O que fazer:
  1. Voltar aos nomes abreviados ("Consulta M.", "Consulta O.", "Acomp.",
     "Fisiot.", "Exame L.", "Doação S.") OU manter os nomes completos mas
     aumentar a rotação para -60/-90 graus (vertical), que ocupa menos
     largura por rótulo.
  2. Se nenhuma das duas resolver sozinha, aumentar a largura mínima por
     categoria (menos categorias visíveis por vez não é opção aqui — são só
     6) ou reduzir a fonte do rótulo.
  3. Depois de qualquer ajuste, rodar a checagem de sobreposição de novo — não
     apenas visualmente "parecer bom" — nos três temas e no celular, e só
     marcar como resolvido quando `sobreposicao.md` não acusar nenhuma
     ocorrência nesse gráfico.
Pronto quando: `sobreposicao.md` de uma nova captura não lista nenhuma
ocorrência para `rep-pareto` em nenhum dos três temas.
Fase de origem: Fase 6 · Entrega — reaberto na Fase 7, rodada 2.

## Achado novo — sugestão do responsável

### [M5] · Mover o gráfico "Por funcionário" para o fim do Dashboard
O responsável sugeriu, ao ver o Dashboard corrigido, mover o bloco "Por
funcionário (anonimizado) — quem está mais perto ou mais longe da meta" para
depois dos dois gráficos novos (dia da semana e mês), ficando por último,
logo antes da tabela detalhada recolhível.
A banca concorda: a ordem atual vai de agregado por motivo → cruzamento
tipo×distância → indivíduo anonimizado → padrão por dia → padrão por mês, o
que quebra a progressão "do mais agregado ao mais granular" no meio (o
gráfico por funcionário, o mais granular de todos depois da tabela, aparece
antes dos padrões temporais, que são tão agregados quanto os primeiros
blocos). Mover para o fim cria uma ordem mais limpa: motivo → distância →
tempo (dia, mês) → indivíduo → tabela bruta — cada bloco mais granular que o
anterior, terminando exatamente onde a tabela recolhível (o mais granular de
todos) já está.
Onde: Dashboard, ordem dos blocos principais.
O que fazer:
  1. Mover o bloco "POR FUNCIONÁRIO (ANONIMIZADO)" para depois do bloco
     "PADRÃO POR MÊS DO CALENDÁRIO" e antes de "Ver a tabela detalhada".
  2. Replicar a mesma ordem no Relatório, se ele também apresentar esses
     blocos em sequência (confirmar a ordem atual da seção 3 antes de mover).
Pronto quando: a ordem dos blocos no Dashboard (e no Relatório, se aplicável)
segue motivo → distância → dia → mês → funcionário → tabela.
Muda junto: nada além da ordem visual — nenhum número ou gráfico muda de
conteúdo.
Tamanho: pequeno (reordenação de layout).
Fase de origem: adendo pós-Fase 7, rodada 2, 28/09/2026 — sugestão do
responsável, registrada pela banca.

## Cobertura desta rodada

Todos os 7 achados importantes e os 4 menores da rodada 1 foram conferidos
(2 menores — M3, M4 — não são verificáveis pela captura da página e foram
aceitos com base no registro de `correcoes.md`, não testados diretamente pela
banca). 1 achado novo (M5) surgiu da conversa com o responsável.

## Limites desta revisão

- M3 e M4 tocam arquivos fora da página (README, requirements.txt) — a banca
  não os recaptura nem confere; o registro em `correcoes.md` foi aceito como
  está.
- A mesma limitação da rodada 1 continua: não foi possível clicar nos botões
  de download para verificar os arquivos gerados.
- O modo Slides não foi alterado por nenhuma correção e não foi
  recapturado em detalhe nesta rodada — sem indício de que tenha sido
  tocado.
