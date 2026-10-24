"""Regras de conversão e validação do dado do Banco Central.

O que a API devolve de verdade (conferido em 24/10/2026):
- valor como TEXTO com ponto: {"data": "23/10/2026", "valor": "5.0377"};
- data como texto DD/MM/AAAA;
- IPCA pode ser negativo (deflação): "-0.32" em 08/2026;
- Selic meta já vem com datas no futuro (a meta vale até a próxima reunião).
"""

from __future__ import annotations

from datetime import date, datetime


def converter_valor(texto: str) -> float:
    """Converte o valor da API em número. Aceita ponto e, por segurança, vírgula."""
    return float(str(texto).strip().replace(",", "."))


def converter_data(texto: str) -> date:
    """Converte DD/MM/AAAA em date."""
    return datetime.strptime(texto.strip(), "%d/%m/%Y").date()


def validar(
    serie: str, registros: list[dict], hoje: date, pode_negativo: bool
) -> tuple[list[tuple[str, date, float]], list[dict]]:
    """Separa linhas válidas e rejeitadas (com o motivo).

    Regras (o contrato do dado):
    - data e valor precisam converter;
    - data não pode estar no futuro;
    - valor negativo só onde a série permite (IPCA);
    - nada de data repetida dentro da mesma série.
    """
    validas: list[tuple[str, date, float]] = []
    rejeitadas: list[dict] = []
    vistas: set[date] = set()
    for reg in registros:
        try:
            d = converter_data(reg["data"])
            v = converter_valor(reg["valor"])
        except (KeyError, ValueError) as erro:
            rejeitadas.append({**reg, "serie": serie, "motivo": f"não converte: {erro}"})
            continue
        if d > hoje:
            rejeitadas.append({**reg, "serie": serie, "motivo": "data no futuro"})
        elif v < 0 and not pode_negativo:
            rejeitadas.append({**reg, "serie": serie, "motivo": "valor negativo"})
        elif d in vistas:
            rejeitadas.append({**reg, "serie": serie, "motivo": "data repetida"})
        else:
            vistas.add(d)
            validas.append((serie, d, v))
    return validas, rejeitadas
