# Fase 3 · Analyze — relatório v2 (adendo pós-hoc)

Data: 27/09/2026 · `relatorio.md` original permanece intocado — este arquivo
só acrescenta o que a revisão por banca da Fase 7 pediu (achado I2). Não é
uma reabertura da Fase 3: as quatro hipóteses pré-registradas (H1-H4) e seus
veredictos continuam exatamente como estavam.

## [I2] Concentração de "consulta médica" no Pareto administrável — pós-hoc

**Origem:** parecer da banca (Fase 7 · Revisão), 27/09/2026, sobre a página
publicada da Fase 6. Não estava no pré-registro da Fase 1 — é uma pergunta
nova, motivada por uma observação sobre a Entrega: "consulta médica" lidera
os dois rankings do Pareto administrável (31,3% das horas, 31,0% dos eventos
evitáveis) sem que ninguém tivesse testado se essa liderança vem de muitos
funcionários ou de poucos com muitas consultas — o mesmo tipo de pergunta que
H2 já fazia para a hipótese da distância, só que nunca aplicada a este
Pareto.

**Por que pós-hoc, e por que isso é uma limitação, não um defeito:** o
holdout já foi aberto na Fase 5 (Control), então este teste roda inteiro
sobre a amostra de exploração (34 identidades) — não há mais uma segunda
amostra livre para confirmar o resultado. O teste vale como evidência
descritiva sobre a base já vista, não como confirmação independente.

**Desenho:** idêntico ao de H2 (Fase 3, item já concluído) — excluir, um de
cada vez, os 3 funcionários com mais eventos do motivo em questão (aqui,
consulta médica; em H2, eventos totais) e observar se a métrica se sustenta.
Script: `scripts/03b_pareto_concentracao_posthoc.py`. Artefato:
`artefatos/pareto_concentracao_posthoc.json`. Base: a mesma
`data/processed/eventos_qualidade.csv` (733 eventos, 34 identidades) usada
em toda a Fase 3.

**Resultado:**

| | Baseline | Excluindo ID (1º) | Excluindo ID (2º) | Excluindo ID (3º) | Faixa |
|---|---|---|---|---|---|
| % das horas administráveis (B2) | 31,26% | 28,38% | 33,80% | 29,92% | 28,38–33,80% |
| % dos eventos evitáveis (B1+B2) | 31,00% | 27,16% | 33,07% | 30,41% | 27,16–33,07% |

Os três funcionários excluídos são os que mais têm eventos de consulta
médica na base (identidades internas, não expostas na página pública).

**Leitura:** em nenhuma das três exclusões a participação de consulta médica
se aproxima da média das outras categorias do Pareto (~15%) — a liderança é
distribuída entre muitos funcionários, não puxada por poucos. O texto da
página ("consulta médica e odontológica continuam liderando o tempo
perdido") permanece correto e agora tem essa verificação por trás, no mesmo
padrão da caixa "O efeito não depende de poucos funcionários" da seção 8 do
Relatório (robustez de H1).

**Não muda:** nenhuma decisão da Fase 3 original, nenhuma hipótese
pré-registrada, nenhuma recomendação da Improve. Nenhuma das duas
quantidades citadas na página (31,3%, 31,0%) foi alterada — este teste só
verifica se elas resistem à exclusão dos maiores contribuintes, e resistem.

**Onde entrou na página:** Relatório, seção 3 (caixa de destaque) e seção
15 (Notas técnicas); Dashboard, nota de leitura do bloco "Onde está o tempo
perdido". Ver `fases/fase-6-entrega/artefatos/relatorio-auditoria.md`
para a rodada de auditoria que cobriu esta mudança.

## [I3] Distância ao trabalho como possível proxy de distância a serviços de saúde — declaração de limite

**Origem:** parecer da banca (Fase 7 · Revisão), 27/09/2026. Não é um teste
novo — é uma limitação que deveria ter sido declarada desde a Fase 3, quando
H1 (distância) foi formulada e testada, e não foi.

**O problema:** a página testou se o efeito da distância sobre a ausência
administrável era um artefato de composição (H2, poucos funcionários com
muitos eventos — seção 8 do Relatório), mas nunca considerou por escrito uma
explicação concorrente diferente: morar mais longe *do trabalho* costuma
também significar morar mais longe *de clínicas e postos de saúde*. Se for
essa a causa real, o piloto de agendamento (recomendação da seção 2, ainda
condicional) mira a variável errada — a distância ao trabalho seria só uma
proxy, não o mecanismo.

**Por que não dá para testar:** confirmado nesta rodada — a base
(`data/processed/eventos_qualidade.csv`) só tem a coluna `Distance from
Residence to Work`; não existe nenhuma outra coluna de localização (bairro,
zona, distância a unidade de saúde). As duas explicações (distância ao
trabalho vs. distância a serviços de saúde) são indistinguíveis com este
dado — a única correção possível é declarar o limite, não testá-lo.

**O que mudou:** um item novo na seção 14 do Relatório ("O que eu não sei")
e uma frase curta na seção 2 (a recomendação), apontando para a seção 14.
Nenhum número muda — H1 continua com o mesmo efeito (16,4 pp de exploração,
9,5 pp de holdout) e o mesmo status (candidata não confirmada). O que muda é
que o Relatório agora nomeia explicitamente por que o piloto pode estar
mirando a variável errada, mesmo se H1 for confirmada no futuro.
