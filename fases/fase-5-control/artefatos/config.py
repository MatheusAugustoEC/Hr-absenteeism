"""Parametros do pipeline, extraidos do codigo para configuracao (C8).
Cada valor cita a fase em que foi decidido e o arquivo onde a decisao esta
justificada.
"""

# Fase 2A - limiar de plausibilidade do teste de colisao por acaso para
# duplicatas (ver fases/fase-2a-measure-qualidade/relatorio.md, item 2)
LIMIAR_PLAUSIBILIDADE_DUPLICATA = 0.30

# Fases 2B e 3 - semente do bootstrap/permutacao (reprodutibilidade dos
# intervalos de confianca e p-valores)
SEMENTE_BOOTSTRAP = 20260926
N_BOOT = 5000

# Fase 4 - custo de RH assumido no ponto de indiferenca da simulacao de H1.
# PREMISSA DECLARADA, nao medida nesta base - substituir por numero real
# antes de qualquer decisao de negocio (ver fases/fase-4-improve/relatorio.md)
CUSTO_RH_HORAS_POR_MES_PREMISSA = 8.0

# Fase 5 - semente do sorteio do holdout, escolhida e registrada ANTES de
# olhar qualquer numero da confirmacao (ver fases/fase-5-control/relatorio.md)
SEMENTE_HOLDOUT = 20260926
PROPORCAO_EXPLORACAO = 0.75  # ~26 de 34 identidades

# Fase 1 - correcao para multiplos testes (Bonferroni, 4 hipoteses)
ALPHA_BONFERRONI = 0.0125

# Aproximacao de meses do periodo jul/2007-jul/2010, usada em todas as fases
# para traduzir contagens em "eventos/mes" - NAO e uma contagem exata
# (sem coluna de ano na base)
MESES_PERIODO_APROX = 36
