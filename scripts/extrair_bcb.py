"""Extração: API do Banco Central → JSON bruto em data/raw/AAAA-MM-DD/ (camada bronze).

Se SUPABASE_URL e SUPABASE_SERVICE_KEY estiverem no .env, envia o mesmo arquivo
para o Supabase Storage (bucket SUPABASE_BUCKET, padrão "raw").

Uso:
    uv run python -m scripts.extrair_bcb              # últimos 120 dias
    uv run python -m scripts.extrair_bcb --dias 400
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import timedelta

import httpx

from scripts.comum import RAW, SERIES, URL_SGS, hoje


def baixar_serie(codigo: int, dias: int, tentativas: int = 3) -> list[dict]:
    inicio = (hoje() - timedelta(days=dias)).strftime("%d/%m/%Y")
    params = {"formato": "json", "dataInicial": inicio}
    for tentativa in range(1, tentativas + 1):
        try:
            r = httpx.get(URL_SGS.format(codigo=codigo), params=params, timeout=30)
            r.raise_for_status()
            return r.json()
        except (httpx.HTTPError, ValueError) as erro:
            if tentativa == tentativas:
                raise RuntimeError(f"série {codigo}: falhou {tentativas} vezes ({erro})") from erro
            time.sleep(2**tentativa)
    return []


def enviar_storage(caminho_local, caminho_remoto: str) -> bool:
    url = os.getenv("SUPABASE_URL")
    chave = os.getenv("SUPABASE_SERVICE_KEY")
    if not (url and chave):
        return False
    bucket = os.getenv("SUPABASE_BUCKET", "raw")
    r = httpx.post(
        f"{url}/storage/v1/object/{bucket}/{caminho_remoto}",
        headers={
            "Authorization": f"Bearer {chave}",
            "Content-Type": "application/json",
            "x-upsert": "true",
        },
        content=caminho_local.read_bytes(),
        timeout=30,
    )
    r.raise_for_status()
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dias", type=int, default=120)
    args = ap.parse_args()

    pasta = RAW / hoje().isoformat()
    pasta.mkdir(parents=True, exist_ok=True)
    for nome, cfg in SERIES.items():
        dados = baixar_serie(cfg["codigo"], args.dias)
        arquivo = pasta / f"serie_{nome}.json"
        arquivo.write_text(json.dumps(dados, ensure_ascii=False, indent=1))
        nuvem = enviar_storage(arquivo, f"bcb/{pasta.name}/{arquivo.name}")
        destino = "local + Supabase Storage" if nuvem else "local"
        print(f"{nome:6} série {cfg['codigo']:>3}: {len(dados):>4} registros → {destino}")


if __name__ == "__main__":
    main()
