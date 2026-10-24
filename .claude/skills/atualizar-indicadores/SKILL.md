---
name: atualizar-indicadores
description: >-
  Atualiza o painel de indicadores (dólar, Selic, IPCA do Banco Central) e conta o que mudou.
  Usar quando pedirem "atualiza os indicadores", "como está o dólar hoje", "roda o painel",
  "o que mudou desde ontem" ou "gera o relatório do dia".
---

# Atualizar indicadores

## Passos

1. Rode a pipeline completa:
   ```bash
   uv run python -m scripts.rodar_tudo
   ```
   Ela extrai, carrega, confere e escreve `relatorios/AAAA-MM-DD.md`. Se parar, diga em qual etapa e por quê. Não pule a conferência.
2. Leia o relatório do dia e o `data/rejeitados.json`.
3. Responda em até 6 linhas:
   - o último valor de cada indicador, com a data e a fonte (SGS 1, 432, 433);
   - o que mudou contra a observação anterior;
   - quantas linhas foram rejeitadas e por quê (ex.: "11 datas futuras da Selic").

## Regras

- Nunca invente ou arredonde número por conta própria: use o que está no relatório.
- Data no futuro não é erro da pipeline, é a meta da Selic já anunciada. Conte, não esconda.
- Se a conferência falhar, pare e mostre a diferença. Não rode de novo até "passar".
