"""Carga: JSON bruto mais recente → valida → upsert na tabela `indicadores`.

Rodar duas vezes não duplica (chave primária serie + data).
Linhas rejeitadas vão para data/rejeitados.json com o motivo.

Uso:
    uv run python -m scripts.carregar
"""

from __future__ import annotations

import json

from scripts.comum import DATA, RAW, SERIES, Banco, agora, hoje, modo
from scripts.transformar import validar


def pasta_mais_recente():
    pastas = sorted(p for p in RAW.glob("*") if p.is_dir())
    if not pastas:
        raise SystemExit("Nenhum dado bruto. Rode antes: uv run python -m scripts.extrair_bcb")
    return pastas[-1]


def main() -> None:
    pasta = pasta_mais_recente()
    banco = Banco()
    todas_rejeitadas: list[dict] = []
    carimbo = agora()
    print(f"modo {modo()} ({banco.tipo}), dados de {pasta.name}")
    for nome, cfg in SERIES.items():
        registros = json.loads((pasta / f"serie_{nome}.json").read_text())
        validas, rejeitadas = validar(nome, registros, hoje(), cfg["pode_negativo"])
        banco.upsert([(*linha, carimbo) for linha in validas])
        todas_rejeitadas += rejeitadas
        print(f"{nome:6} {len(validas):>4} carregadas, {len(rejeitadas):>2} rejeitadas")
    (DATA / "rejeitados.json").write_text(
        json.dumps(todas_rejeitadas, ensure_ascii=False, indent=1)
    )
    for r in todas_rejeitadas:
        print(f"  rejeitada: {r['serie']} {r.get('data')} {r.get('valor')} ({r['motivo']})")
    banco.fechar()


if __name__ == "__main__":
    main()
