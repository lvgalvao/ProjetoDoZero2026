"""Conferência: o que está no banco bate com o que veio da API?

Para cada série compara, entre o JSON bruto mais recente e o banco:
- o último valor válido;
- a quantidade de datas válidas (o banco pode ter mais, de cargas antigas, nunca menos);
- se há data duplicada.

Sai com código 1 se algo não bater (o hook e o GitHub Actions param aí).

Uso:
    uv run python -m scripts.conferir
"""

from __future__ import annotations

import json
import sys

from scripts.carregar import pasta_mais_recente
from scripts.comum import SERIES, Banco, hoje
from scripts.transformar import validar


def conferir(banco: Banco, pasta) -> list[str]:
    problemas: list[str] = []
    for nome, cfg in SERIES.items():
        registros = json.loads((pasta / f"serie_{nome}.json").read_text())
        validas, _ = validar(nome, registros, hoje(), cfg["pode_negativo"])
        if not validas:
            problemas.append(f"{nome}: a API não trouxe nenhuma linha válida")
            continue
        ultima_api = max(validas, key=lambda linha: linha[1])
        sql_ultima = (
            "SELECT data, valor FROM indicadores WHERE serie = {p} ORDER BY data DESC LIMIT 1"
        )
        linha = banco.consultar(sql_ultima, (nome,))
        if not linha:
            problemas.append(f"{nome}: nada no banco")
            continue
        data_banco, valor_banco = linha[0]
        if str(data_banco) != str(ultima_api[1]) or abs(valor_banco - ultima_api[2]) > 1e-9:
            api = f"{ultima_api[1]} = {ultima_api[2]}"
            problemas.append(f"{nome}: API {api} x banco {data_banco} = {valor_banco}")
        sql_qtd = "SELECT count(*), count(DISTINCT data) FROM indicadores WHERE serie = {p}"
        total, distintas = banco.consultar(sql_qtd, (nome,))[0]
        if total != distintas:
            problemas.append(f"{nome}: {total - distintas} datas duplicadas no banco")
        if total < len(validas):
            problemas.append(f"{nome}: banco tem {total} linhas, API trouxe {len(validas)}")
    return problemas


def main() -> None:
    banco = Banco()
    problemas = conferir(banco, pasta_mais_recente())
    banco.fechar()
    if problemas:
        print("CONFERÊNCIA FALHOU")
        for p in problemas:
            print(f"  - {p}")
        sys.exit(1)
    print("Conferência ok: último valor e quantidade batem com a API, sem duplicadas.")


if __name__ == "__main__":
    main()
