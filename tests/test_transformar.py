"""Testes das regras do dado. Não chamam a API: usam registros no formato real dela."""

from datetime import date

from scripts.transformar import converter_data, converter_valor, validar

HOJE = date(2026, 10, 24)


def test_valor_vem_como_texto_com_ponto():
    assert converter_valor("5.0377") == 5.0377


def test_valor_com_virgula_tambem_converte():
    assert converter_valor("5,0377") == 5.0377


def test_data_no_formato_brasileiro():
    assert converter_data("23/10/2026") == date(2026, 10, 23)


def test_ipca_negativo_e_aceito():
    validas, rejeitadas = validar("ipca", [{"data": "01/08/2026", "valor": "-0.32"}], HOJE, True)
    assert validas == [("ipca", date(2026, 8, 1), -0.32)]
    assert rejeitadas == []


def test_dolar_negativo_e_rejeitado():
    validas, rejeitadas = validar("dolar", [{"data": "23/10/2026", "valor": "-5"}], HOJE, False)
    assert validas == []
    assert rejeitadas[0]["motivo"] == "valor negativo"


def test_selic_com_data_no_futuro_e_rejeitada():
    registros = [
        {"data": "24/10/2026", "valor": "13.75"},
        {"data": "02/11/2026", "valor": "13.75"},
    ]
    validas, rejeitadas = validar("selic", registros, HOJE, False)
    assert [linha[1] for linha in validas] == [date(2026, 10, 24)]
    assert rejeitadas[0]["motivo"] == "data no futuro"


def test_data_repetida_e_rejeitada():
    registros = [{"data": "23/10/2026", "valor": "5.03"}, {"data": "23/10/2026", "valor": "5.04"}]
    validas, rejeitadas = validar("dolar", registros, HOJE, False)
    assert len(validas) == 1
    assert rejeitadas[0]["motivo"] == "data repetida"


def test_valor_que_nao_e_numero_e_rejeitado():
    validas, rejeitadas = validar("dolar", [{"data": "23/10/2026", "valor": "n/d"}], HOJE, False)
    assert validas == []
    assert rejeitadas[0]["motivo"].startswith("não converte")
