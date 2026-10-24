"""Pipeline completa, na ordem: extrair → carregar → conferir → relatório.

É o que o GitHub Actions roda todo dia às 9h. Para no primeiro erro.

Uso:
    uv run python -m scripts.rodar_tudo
"""

from __future__ import annotations

import subprocess
import sys

ETAPAS = ["extrair_bcb", "carregar", "conferir", "relatorio_diario"]


def main() -> None:
    for etapa in ETAPAS:
        print(f"\n=== {etapa} ===", flush=True)
        r = subprocess.run([sys.executable, "-m", f"scripts.{etapa}"])
        if r.returncode != 0:
            sys.exit(f"Parou em {etapa} (código {r.returncode}).")
    print("\nPipeline completa.")


if __name__ == "__main__":
    main()
