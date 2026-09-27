# Comentários — Fase 1 · Define

**26/09/2026** — Decisões substantivas aceitas: fronteira B1/B2/CID, exclusão
das 4 linhas (3 administrativas + 1 do ID 29), métrica primária como proporção
de eventos, as 4 hipóteses pré-registradas (incluindo a rival estrutural H2 e
a hipótese de artefato de registro H3), e o registro honesto do quase-garimpo
em H3. Tudo isso fica como está.

**Bloqueante encontrado, não corrigir por conta própria:** `relatorio.md`
afirma "34, não 36, identidades" na população de evento pós-exclusão (IDs 4 e
35 perdem sua única linha e desaparecem da população de evento). Mas
`pre-registro.md` — arquivo IMUTÁVEL — usa "36 identidades" em dois lugares:
na lista de decisões de escopo e, mais grave, na definição operacional do
holdout ("sorteio... sobre as 36 identidades já corrigidas"). O relatório e o
pré-registro divergem sobre o denominador do próprio sorteio que vai reger a
fase Control. Isso precisa de um adendo datado ao final de `pre-registro.md`
(nunca edição silenciosa, regra do contexto mestre) fixando o número correto
(34) e a razão — antes que a Control tente executar um sorteio 75/25 sobre um
N que não bate com a população de evento real.
