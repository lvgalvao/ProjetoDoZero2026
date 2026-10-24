# CLAUDE.md · Painel de indicadores

Índice do projeto, lido em toda sessão. O detalhe está no `README.md` e no `prd.md`.

## O que é

Painel de dólar (SGS 1), Selic meta (SGS 432) e IPCA (SGS 433) do Banco Central, operado por agente. Também é o projeto da live "Projeto de Dados do Zero 2026" da Jornada de Dados (Luciano Vasconcelos).

## Comandos

- instalar: `uv sync`
- pipeline completa: `uv run python -m scripts.rodar_tudo`
- etapas: `uv run python -m scripts.extrair_bcb` · `scripts.carregar` · `scripts.conferir` · `scripts.relatorio_diario`
- gate: `uv run ruff check scripts tests && uv run pytest -q` (ou `/validar`)
- revisar antes do commit: subagente `revisor`

## Nunca quebrar

- **Segredos:** chave só no `.env`. Nunca ler, imprimir ou commitar o `.env`. Nunca escrever chave no código.
- **Carga é upsert** por `(serie, data)`. Rodar duas vezes não pode duplicar.
- **Regras do dado:** data no futuro não entra; negativo só no IPCA; valor vem como texto e é convertido em `scripts/transformar.py`.
- **Nunca inventar número.** Todo número do relatório vem do banco e cita a série do SGS.
- **Todo script fica em `scripts/`** e roda com `uv run python -m scripts.<nome>`. Nada só em pasta temporária.
- **Teste não chama a API real nem o banco de produção.** Nunca apagar ou pular teste para passar.
- **Dependência só com `uv add`.**
- Commit e push só quando o Luciano pedir.

## Onde fica cada coisa

- código: `scripts/` · testes: `tests/` · relatórios: `relatorios/` · dado local: `data/` (fora do git)
- harness: `.claude/settings.json` (permissões e hooks), `.claude/agents/revisor.md`, `.claude/commands/validar.md`, `.claude/skills/atualizar-indicadores/`, `.mcp.json` (Postgres somente leitura)
- rotina: `.github/workflows/diario.yml` (9h) · CI: `.github/workflows/ci.yml`
- decisões: `decisoes.md` · onde a última sessão parou: `HANDOFF.md`
- material da live: `prd.md`, `apresentacao/index.html`, `material/`, `referencias/`

## Convenções

Português curto e direto. Código em inglês ou português de domínio (`serie`, `valor`). Datas `YYYY-MM-DD` no banco, `DD/MM/AAAA` na tela. Identidade visual da Jornada: azul `#0059DB`, ciano `#22C2F4`, preto `#14141A`, Poppins.
