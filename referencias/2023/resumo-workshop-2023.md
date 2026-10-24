# Resumo do workshop de 2023

**Workshop: Como estruturar o seu projeto de dados do zero**, ao vivo em 08/10/2023, 4h25min. YouTube `9-k6pRlU3kc` (privado). A transcrição completa está em `transcricao-workshop-2023.md`, tirada da legenda automática.

**Caso usado:** uma ETL em pandas que lê 50 arquivos Excel com o mesmo esquema, junta tudo e salva um arquivo só (`data/input` → `data/output`). A abertura comparava dois repositórios com a mesma ETL: um só com o código e outro com README, testes e documentação.

**Mensagem central:** "o objetivo é que outra pessoa consiga rodar o seu projeto na máquina dela" e "o problema não é desenvolver, é sustentar o que você desenvolveu".

## Os blocos, na ordem da live

| # | Tempo | Bloco | Ferramentas em 2023 |
|---|---|---|---|
| 1 | 0:15 | Versão do Python (usar a mais nova que as bibliotecas suportam) | pyenv, `.python-version` |
| 2 | 0:21 | Ambiente virtual e dependências ("na minha máquina funciona") | Poetry, `pyproject.toml`, `poetry.lock`, site-packages |
| 3 | 0:42 | Git e GitHub (commit pequeno, branch, `.gitignore`, voltar no tempo no histórico do pandas) | git, GitHub, gitignore do Toptal |
| 4 | 1:10 | Estrutura de pastas | `app/`, `tests/`, `docs/`, `data/` |
| 5 | 1:11 | IA ao lado ("escrevo a docstring antes, a IA escreve o código") | ChatGPT, Copilot |
| 6 | 1:13 | Código modular: extract → transform → load, docstring, tipagem, `if __name__ == "__main__"`, `__init__.py` | pandas, openpyxl, typing |
| 7 | 1:47 | Testes unitários (arrange/act/assert, testar sem depender do Excel, testar request) | pytest |
| 8 | 2:41 | Padrão de código (PEP 8, acabar com a discussão de estilo no time) | Blue/Black, isort, Flake8, pydocstyle, pip-audit |
| 9 | 2:59 | Atalhos de comando (`task format`, `task test`, `task run`, `task docs`) | taskipy |
| 10 | 3:09 | Documentação gerada do código (no lugar do Confluence) | MkDocs Material, Mermaid, mkdocstrings, `mkdocs gh-deploy` |
| 11 | 3:34 | Hooks antes do commit | pre-commit |
| 12 | 3:46 | CI no Pull Request (testes rodam antes do merge; "todo bug vira um teste") | GitHub Actions |
| fim | 4:13 | README: objetivo, link da documentação, como rodar, contato | — |

## O que deu errado ao vivo (lição para 2026)

- Conflito de versão do Python com o interpretador escolhido no VS Code (0:27).
- Caminho relativo errado na pasta `app/` travou a extração por vários minutos (1:40).
- Black e Flake8 brigaram; Blue e Flake8 também (2:44).
- O pre-commit bloqueou o commit e acabou sendo removido do projeto (3:43).
- O CI quebrou no projeto da live e só funcionou num repositório antigo (3:57 a 4:07).
- Deploy ficou para "um próximo workshop".

Para 2026: ensaiar, ter uma branch ou tag de gabarito por bloco e deixar o CI testado antes da live.
