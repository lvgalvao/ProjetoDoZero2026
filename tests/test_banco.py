"""Testes da carga num DuckDB temporário (nada de banco de verdade em teste)."""

from datetime import date, datetime

from scripts.comum import Banco

CARIMBO = datetime(2026, 10, 24, 9, 0)


def test_rodar_duas_vezes_nao_duplica(tmp_path):
    banco = Banco(caminho_duckdb=tmp_path / "teste.duckdb")
    linhas = [("dolar", date(2026, 10, 23), 5.0377, CARIMBO)]
    banco.upsert(linhas)
    banco.upsert(linhas)
    assert banco.consultar("SELECT count(*) FROM indicadores")[0][0] == 1


def test_upsert_atualiza_valor_corrigido(tmp_path):
    banco = Banco(caminho_duckdb=tmp_path / "teste.duckdb")
    banco.upsert([("dolar", date(2026, 10, 23), 5.0, CARIMBO)])
    banco.upsert([("dolar", date(2026, 10, 23), 5.0377, CARIMBO)])
    assert banco.consultar("SELECT valor FROM indicadores")[0][0] == 5.0377
