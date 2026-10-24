"""Relatório do dia: relatorios/AAAA-MM-DD.md com o último valor de cada série,
a variação contra a observação anterior e a fonte de cada número.

Uso:
    uv run python -m scripts.relatorio_diario
"""

from __future__ import annotations

from scripts.comum import RELATORIOS, SERIES, URL_SGS, Banco, agora, hoje, modo


def formatar(valor: float, casas: int) -> str:
    return f"{valor:,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def montar(banco: Banco) -> str:
    linhas = [
        f"# Indicadores · {hoje().strftime('%d/%m/%Y')}",
        "",
        f"Gerado em {agora().strftime('%d/%m/%Y %H:%M')} (horário de Brasília), modo {modo()}.",
        "",
        "| Indicador | Último | Data | Anterior | Variação | Fonte |",
        "|---|---|---|---|---|---|",
    ]
    for nome, cfg in SERIES.items():
        sql = "SELECT data, valor FROM indicadores WHERE serie = {p} ORDER BY data DESC LIMIT 2"
        obs = banco.consultar(sql, (nome,))
        if not obs:
            linhas.append(f"| {cfg['nome']} | sem dado | | | | |")
            continue
        casas = 4 if nome == "dolar" else 2
        (d1, v1), anterior = obs[0], obs[1] if len(obs) > 1 else None
        fonte = f"[SGS {cfg['codigo']}]({URL_SGS.format(codigo=cfg['codigo'])}?formato=json)"
        if anterior:
            d0, v0 = anterior
            if nome == "dolar":
                var = f"{formatar((v1 / v0 - 1) * 100, 2)}%"
            else:
                var = f"{formatar(v1 - v0, 2)} p.p."
            ant = f"{formatar(v0, casas)} ({d0.strftime('%d/%m')})"
        else:
            var, ant = "", ""
        linhas.append(
            f"| {cfg['nome']} | {formatar(v1, casas)} | {d1.strftime('%d/%m/%Y')} "
            f"| {ant} | {var} | {fonte} |"
        )
    linhas += [
        "",
        "Fonte: API SGS do Banco Central. Datas no futuro e valores fora do contrato não entram "
        "(ver `data/rejeitados.json`).",
    ]
    return "\n".join(linhas) + "\n"


def main() -> None:
    banco = Banco()
    texto = montar(banco)
    banco.fechar()
    RELATORIOS.mkdir(exist_ok=True)
    arquivo = RELATORIOS / f"{hoje().isoformat()}.md"
    arquivo.write_text(texto)
    print(texto)
    print(f"→ {arquivo.relative_to(RELATORIOS.parent)}")


if __name__ == "__main__":
    main()
