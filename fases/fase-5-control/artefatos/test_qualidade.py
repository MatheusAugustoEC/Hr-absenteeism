"""Testes automaticos que convertem a auditoria de qualidade da Fase 2A em
verificacoes que falham se o dado de entrada mudar de forma, dominio ou
volume (C7). Rode com: pytest tests/test_qualidade.py -v

Nao repete a decisao de exclusao/duplicata (isso e decisao de projeto,
travada nos relatorios das Fases 1 e 2A) - so verifica se o ARQUIVO FINAL
continua com a forma esperada.
"""
from pathlib import Path

import pandas as pd
import pytest

BASE = Path(__file__).resolve().parents[1]
QUALIDADE = BASE / "data" / "processed" / "eventos_qualidade.csv"

COLUNAS_ESPERADAS = [
    "ID", "Reason for absence", "Month of absence", "Day of the week", "Seasons",
    "Transportation expense", "Distance from Residence to Work", "Service time",
    "Age", "Work load Average/day", "Hit target", "Disciplinary failure",
    "Education", "Son", "Social drinker", "Social smoker", "Pet", "Weight",
    "Height", "Body mass index", "Absenteeism time in hours",
]


@pytest.fixture(scope="module")
def df():
    return pd.read_csv(QUALIDADE)


def test_colunas_esperadas_presentes(df):
    for c in COLUNAS_ESPERADAS:
        assert c in df.columns, f"coluna esperada ausente: {c}"


def test_sem_nulos(df):
    nulos = df[COLUNAS_ESPERADAS].isna().sum()
    assert nulos.sum() == 0, f"nulos encontrados:\n{nulos[nulos > 0]}"


def test_dominio_day_of_week(df):
    assert df["Day of the week"].isin([2, 3, 4, 5, 6]).all()


def test_dominio_seasons(df):
    assert df["Seasons"].isin([1, 2, 3, 4]).all()


def test_dominio_education(df):
    assert df["Education"].isin([1, 2, 3, 4]).all()


def test_dominio_reason_for_absence(df):
    assert df["Reason for absence"].between(0, 28).all()


@pytest.mark.parametrize("coluna", ["Disciplinary failure", "Social drinker", "Social smoker"])
def test_dominio_binarias(df, coluna):
    assert df[coluna].isin([0, 1]).all()


def test_circularidade_bmi(df):
    """M2/F1 - BMI = Weight / (Height/100)^2, com residuo pequeno na maioria
    das linhas. Alerta se o residuo piorar (ex.: unidade de Weight/Height
    mudou, ou uma nova fonte de dado nao segue a mesma convencao)."""
    bmi_calc = df["Weight"] / ((df["Height"] / 100) ** 2)
    residuo = (bmi_calc - df["Body mass index"]).abs()
    pct_menor_que_1 = (residuo < 1).mean()
    assert pct_menor_que_1 >= 0.95, (
        f"circularidade BMI degradou: só {pct_menor_que_1:.1%} das linhas com "
        "resíduo < 1 (esperado >= 95%, Fase 2A registrou 98,64%)"
    )


def test_volume_eventos(df):
    """Fase 2A travou 733 eventos apos as exclusoes do Define e a resolucao
    de duplicatas. Mudanca de volume sem uma nova exclusao registrada em
    relatorio e um alerta, nao um erro silencioso."""
    assert len(df) == 733, (
        f"volume mudou: {len(df)} linhas, esperado 733 (Fase 2A). Se uma nova "
        "exclusao foi decidida e registrada em relatorio, atualize este teste "
        "citando o relatorio; senao, investigue a mudanca."
    )


def test_volume_identidades(df):
    assert df["ID"].nunique() == 34, (
        f"numero de identidades mudou: {df['ID'].nunique()}, esperado 34 (Fase 2A)"
    )


def test_ids_excluidos_no_define_nao_reaparecem(df):
    """IDs 4 e 35 so tinham a linha administrativa excluida no Define -
    nao deveriam reaparecer na base final."""
    assert not df["ID"].isin([4, 35]).any()


def test_linha_jovem_id29_nao_reaparece(df):
    """A linha do ID 29 com Age=28/Height=169/Weight=69 foi excluida no
    Define (Fase 1) por corromper a granularidade por funcionario."""
    linha = df[(df["ID"] == 29) & (df["Age"] == 28)]
    assert linha.empty
