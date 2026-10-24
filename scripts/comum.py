"""Configuração compartilhada: caminhos, séries e conexão com o banco.

O banco é escolhido pelo `.env`:
- sem `DATABASE_URL`: DuckDB local em `data/painel.duckdb` (modo local, roda offline);
- com `DATABASE_URL`: Postgres na nuvem (Supabase).
"""

from __future__ import annotations

import os
from datetime import date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"
RELATORIOS = ROOT / "relatorios"
FUSO = ZoneInfo("America/Sao_Paulo")

load_dotenv(ROOT / ".env")

# Séries do SGS (Sistema Gerenciador de Séries Temporais) do Banco Central.
SERIES: dict[str, dict] = {
    "dolar": {"codigo": 1, "nome": "Dólar comercial (venda), R$", "pode_negativo": False},
    "selic": {"codigo": 432, "nome": "Selic meta, % a.a.", "pode_negativo": False},
    "ipca": {"codigo": 433, "nome": "IPCA, variação mensal %", "pode_negativo": True},
}

URL_SGS = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados"

DDL = """
CREATE TABLE IF NOT EXISTS indicadores (
    serie TEXT NOT NULL,
    data DATE NOT NULL,
    valor DOUBLE PRECISION NOT NULL,
    carregado_em TIMESTAMP NOT NULL,
    PRIMARY KEY (serie, data)
)
"""

UPSERT = """
INSERT INTO indicadores (serie, data, valor, carregado_em) VALUES ({p}, {p}, {p}, {p})
ON CONFLICT (serie, data) DO UPDATE SET valor = excluded.valor, carregado_em = excluded.carregado_em
"""


def hoje() -> date:
    return datetime.now(FUSO).date()


def agora() -> datetime:
    return datetime.now(FUSO).replace(tzinfo=None, microsecond=0)


def modo() -> str:
    """'nuvem' quando há DATABASE_URL no .env; senão 'local'."""
    return "nuvem" if os.getenv("DATABASE_URL") else "local"


class Banco:
    """Conexão mínima que funciona igual no DuckDB (local) e no Postgres (nuvem)."""

    def __init__(self, caminho_duckdb: Path | None = None) -> None:
        url = os.getenv("DATABASE_URL")
        if url and caminho_duckdb is None:
            import psycopg

            self.con = psycopg.connect(url, autocommit=True)
            self.p = "%s"
            self.tipo = "postgres"
        else:
            import duckdb

            caminho = caminho_duckdb or DATA / "painel.duckdb"
            caminho.parent.mkdir(parents=True, exist_ok=True)
            self.con = duckdb.connect(str(caminho))
            self.p = "?"
            self.tipo = "duckdb"
        self.executar(DDL)

    def executar(self, sql: str, params: tuple | None = None) -> None:
        cur = self.con.cursor()
        cur.execute(sql, params or ())

    def consultar(self, sql: str, params: tuple | None = None) -> list[tuple]:
        cur = self.con.cursor()
        cur.execute(sql.replace("{p}", self.p), params or ())
        return cur.fetchall()

    def upsert(self, linhas: list[tuple]) -> int:
        sql = UPSERT.format(p=self.p)
        for linha in linhas:
            self.executar(sql, linha)
        return len(linhas)

    def fechar(self) -> None:
        self.con.close()
