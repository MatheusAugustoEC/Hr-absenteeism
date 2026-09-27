# Relatório de auditoria — Fase 6 · Entrega (v5, reconstrução do zero)

Data: 27/09/2026 · Ferramenta: Playwright (Chromium real, headless), servindo a página por `python -m http.server` — não como `file://`.

## Contexto

Esta é a reconstrução completa da Fase 6, a partir de uma decisão explícita do usuário: sem alternância Simples/Técnica (um só registro, em linguagem simples, com o rigor técnico reunido numa seção própria — "Notas técnicas"), sem o modo Painel (a função de abertura do X foi incorporada ao topo do Dashboard), navegação e filtros na lateral (filtros só ativos no modo Dashboard), e cada gráfico do Dashboard com uma frase de leitura ("insight"), não só o número cru. Downloads (.xlsx/.pptx/PDF) e a mecânica de interação (`references/interacao.md`) continuam as mesmas da skill. Nenhum número foi inventado — todos vêm de `artefatos/dados_pagina.json`, gerado por `scripts/06_entrega_dados.py` a partir dos artefatos congelados das Fases 0-5.

## Como foi feito

Servida a página localmente, percorridos os três modos (Dashboard, Relatório, Slides), os dois temas (claro/escuro) e duas larguras (desktop 1400px e mobile 390px). Console lido em cada etapa — erro é bloqueante, por regra da skill (`references/auditoria.md`).

## Rodada 1

Script: `auditoria_v5_reconstrucao.py`. Checagens: dropdown abre/marca/permanece aberto, filtro gera etiqueta removível, contador atualiza, seleção de matriz (marca e desmarca), ordenação de coluna da tabela, "Mostrar todas", download `.xlsx` (> 1 KB), "Limpar filtros" zera a seleção, bloco de filtros da lateral escondido fora do Dashboard, navegação de slides até 9/9, download `.pptx` (> 1 KB), manchete idêntica entre Dashboard e Slide 1, busca literal de B1/B2/CID (nenhuma ocorrência — o glossário desta versão nem cita os códigos internos, só os nomes descritivos), zero erros de console.

**Achado (não bloqueante para as checagens automáticas, mas visual, confirmado por captura): no modo Slides, em largura de celular, o selo "1 / 9" (posicionado de forma absoluta no canto do quadro) sobrepunha a última linha do parágrafo em quadros com texto mais longo (quadros 1 e 9 testados) — a `aspect-ratio:16/9` do cartão do slide, numa tela estreita, deixava pouca altura para o texto, e o selo ficava por cima da última linha.**

Corrigido: em telas até 900px, o cartão do slide deixa de ter proporção fixa (`aspect-ratio:auto; min-height:300px`) e o selo de página vira parte do fluxo normal do texto (`position:static`), em vez de sobreposto — a mesma solução já usada na versão impressa/PDF. Conferido de novo nos quadros 1 e 9 (os de texto mais longo): sem sobreposição.

**Resultado: 1 rodada, 1 achado (rótulo sobre texto no Slides/mobile), corrigido, reverificado sem novo achado.**

## Capturas

`capturas/dashboard-escuro.png`, `dashboard-claro.png`, `dashboard-mobile.png`, `relatorio-escuro.png`, `slide1.png`, `slide1-mobile.png` — nenhum rótulo sobre dado em nenhuma, filtros da lateral corretamente ausentes fora do Dashboard, guardrail (atestado médico) sempre em destaque verde, separado dos indicadores de problema.

## Lista de conferência (references/auditoria.md)

- Unidade presente em todo número (%, pp, h, eventos) — conferido.
- pp nunca chamado de porcentagem — conferido (seções 7, 8, 13, notas técnicas).
- Formatação pt-BR (vírgula decimal, ponto de milhar) — conferido nos números e no `nf()`.
- Mesmo número, mesmas casas decimais, em Dashboard/Relatório/Slides — checado para a manchete (64,3%); os demais números (35,7%, 733, +30,9 pp, 16,4 pp, 35,4%) são reaproveitados nos três modos a partir do mesmo objeto `DADOS`, nunca redigitados.
- Todo número diz a sua janela — a base é toda jul/2007–jul/2010, declarada no rodapé do Dashboard e na seção 1 do Relatório; a confirmação (holdout, n=8) é rotulada como segunda amostra em todo lugar que aparece (seção 13, Notas técnicas).
- Gráfico de mês não-temporal mantém o aviso "SEM ORDEM CRONOLÓGICA CONFIÁVEL" no próprio título.
- Rampa sequencial (matriz e barras) com contraste ≥2:1 nos dois temas — tokens reaproveitados e já testados nas rodadas anteriores desta fase (ver commits anteriores, mesma paleta Dark Glass/claro).
- Nenhum termo técnico sem explicação no corpo principal — todo termo (IC, poder estatístico, cluster, holdout) só aparece com número já contextualizado em português corrido; a explicação formal de cada termo está no Glossário e nas Notas técnicas.
- Nenhum resto de exemplo do molde — busca por textos de exemplo (título "MODELO", nomes de placeholder) não encontrou ocorrência.
- Ordem problema → solução → prova: Relatório abre com o tamanho do problema (seção 1) e a recomendação (seção 2) antes de qualquer prova; Slides têm X no quadro 1 e a recomendação no quadro 2.
- Nenhum controle que não reage, nenhum erro de console.

## O que ficou de fora (não bloqueante)

- A checagem de sobreposição automatizada (`assets/sobreposicao.js` da skill `banca-dmaic`) não foi rodada nesta rodada; a inspeção visual por captura, nos dois temas e larguras, não encontrou outra ocorrência além da já corrigida.

## Conclusão

Reconstrução completa da Fase 6 (v5): 1 rodada de auditoria, 1 achado visual (rótulo sobre texto no Slides/mobile), corrigido e reverificado sem novo achado. A mecânica herdada da skill (filtros, matriz, downloads) foi retestada do zero, já que a casca da página mudou por completo (lateral no lugar da barra superior, três modos no lugar de quatro, um só registro de linguagem).
