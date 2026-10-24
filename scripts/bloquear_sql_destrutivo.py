"""Hook PreToolUse: bloqueia SQL destrutivo antes de uma ferramenta MCP executar.

O Claude Code manda a chamada da ferramenta em JSON pela entrada padrão.
Se algum texto da chamada tiver DELETE FROM, DROP TABLE/SCHEMA/DATABASE ou
TRUNCATE, o hook sai com código 2 e a chamada não acontece.

É a segunda camada. A primeira é o banco: o usuário da carga não tem DELETE
nem DROP (material/supabase-usuarios.sql).

Uso (em .claude/settings.json): uv run python -m scripts.bloquear_sql_destrutivo
"""

import json
import re
import sys

PADRAO = re.compile(
    r"\b(DELETE\s+FROM|DROP\s+(TABLE|SCHEMA|DATABASE|VIEW)|TRUNCATE)\b",
    re.IGNORECASE,
)


def textos(valor) -> list[str]:
    """Todos os textos dentro da entrada da ferramenta, em qualquer nível."""
    if isinstance(valor, str):
        return [valor]
    if isinstance(valor, dict):
        return [t for v in valor.values() for t in textos(v)]
    if isinstance(valor, list):
        return [t for v in valor for t in textos(v)]
    return []


def motivo_bloqueio(entrada_ferramenta: dict) -> str | None:
    """Devolve o comando destrutivo encontrado, ou None se a chamada é segura."""
    for texto in textos(entrada_ferramenta):
        achado = PADRAO.search(texto)
        if achado:
            return achado.group(0).upper()
    return None


def main() -> int:
    evento = json.load(sys.stdin)
    motivo = motivo_bloqueio(evento.get("tool_input", {}))
    if motivo:
        print(
            f"Bloqueado pelo hook: {motivo} não é permitido no banco. "
            "A carga é upsert (insere e atualiza). Para apagar dado, peça ao Luciano.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
