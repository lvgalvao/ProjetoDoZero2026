import pytest

from scripts.bloquear_sql_destrutivo import motivo_bloqueio


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM indicadores WHERE data >= '2026-09-01'",
        "delete from indicadores",
        "DROP TABLE indicadores",
        "drop schema public cascade",
        "TRUNCATE indicadores",
    ],
)
def test_bloqueia_sql_destrutivo(sql):
    assert motivo_bloqueio({"sql": sql}) is not None


@pytest.mark.parametrize(
    "sql",
    [
        "SELECT max(valor) FROM indicadores WHERE serie = '1'",
        "INSERT INTO indicadores VALUES ('1', '2026-10-23', 5.0377, now()) "
        "ON CONFLICT (serie, data) DO UPDATE SET valor = excluded.valor",
        "SELECT * FROM deleted_items",
    ],
)
def test_deixa_passar_leitura_e_upsert(sql):
    assert motivo_bloqueio({"sql": sql}) is None


def test_procura_em_campos_aninhados():
    assert motivo_bloqueio({"args": {"query": ["select 1", "DROP TABLE x"]}}) == "DROP TABLE"
