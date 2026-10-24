---
description: Gate do projeto — lint, testes e conferência dos números. Rode antes de cada commit.
---

# /validar

Rode, nesta ordem, e conserte até tudo passar:

```bash
uv run ruff check --fix scripts tests
uv run pytest -q
uv run python -m scripts.conferir
```

- Se o **ruff** acusar: deixe o autofix resolver e corrija o resto.
- Se o **pytest** falhar: conserte o código, não o teste (a não ser que o teste esteja errado, e aí diga por quê).
- Se a **conferência** falhar: não "ajuste" o número. Descubra de onde veio a diferença e mostre.

Só diga que terminou com tudo verde. Depois, sugira passar o subagente `revisor`.
