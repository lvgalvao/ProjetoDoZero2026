# Prompts da live: do PRD ao Supabase

O que colar no Claude Code em cada passo. Comece numa pasta vazia; este repositório é o gabarito para comparar.

## 05 · PRD: entrevista antes do código

A entrevista pode vir da skill `grill-me`, do repositório [mattpocock/skills](https://github.com/mattpocock/skills):

```bash
claude plugin install mattpocock-skills@claude-plugins-official   # Claude Code, uma vez
# dentro do Claude Code, uma vez por repositório:
/setup-matt-pocock-skills
# para usar: digite /grill-me e cole a ideia em 5 linhas
```

Em OpenCode, Cursor e outros agentes: `npx skills@latest add mattpocock/skills -a opencode` (troque `opencode` pelo seu agente). A skill só roda quando você chama `/grill-me`. Leia o `SKILL.md` antes de instalar: skill de terceiro é instrução para o seu agente.

Sem a skill, o prompt abaixo faz o mesmo papel:

```text
Quero construir um painel de indicadores econômicos do zero. Antes de
qualquer código, me entreviste, uma pergunta por vez, até fechar cada
decisão. Só depois escreva o prd.md (meia página).

A ideia em 5 linhas:
1. Buscar dólar (SGS 1), Selic meta (SGS 432) e IPCA (SGS 433) na API
   pública do Banco Central.
2. Guardar o JSON bruto como veio e salvar a versão validada num banco.
3. Começar com banco local (DuckDB) e depois trocar para Postgres no
   Supabase mudando só o .env.
4. Rodar sozinho todo dia às 9h e gerar um relatório do que mudou.
5. Depois, levar a mesma tabela para o Databricks.

Regras que eu já sei:
- Rodar duas vezes não pode duplicar (upsert por série e data).
- Nenhum número inventado: todo número do relatório vem do banco e cita a série.
- Chave só no .env.
- A carga só insere e atualiza: nada de DELETE, DROP ou TRUNCATE no banco.
- Dependência só com uv add. Todo script fica em scripts/.

O PRD precisa ter: objetivo, fontes, tabela de saída (colunas e tipos),
regras do dado, o que fica fora e critérios de aceite testáveis.
Não escreva código ainda.
```

Depois do PRD: `Me mostre o plano de implementação em passos. Não escreva código ainda.`

## 06 · Contexto: as regras viram CLAUDE.md

```text
Leia o prd.md e escreva um CLAUDE.md curto: comandos, a seção
"Nunca quebrar" com as regras que não podem ser violadas e onde fica
cada coisa. No máximo uma tela.
```

## 07 · Conectar, em quatro passos

**① Extrair**

```text
Crie scripts/extrair_bcb.py: busca as séries 1, 432 e 433 na API SGS do
Banco Central e salva o JSON bruto, como veio, em data/raw/AAAA-MM-DD/.
Use httpx com timeout e 3 tentativas. Antes de escrever, me mostre um
exemplo real da resposta da API.
```

**② Banco local**

```text
Crie scripts/carregar.py: valida o bruto em scripts/transformar.py
(valor vem como texto, data no futuro não entra, negativo só no IPCA) e
faz upsert por (serie, data) num DuckDB em data/painel.duckdb. Escreva
um teste provando que rodar duas vezes não duplica.
```

**③ Refatorar para o Supabase**

```text
Refatore para aceitar DATABASE_URL no .env: com ela, grava no Postgres;
sem ela, continua no DuckDB. Mesmo código de carga, mesmos testes. O
teste não pode usar o banco de produção.
```

No Supabase: crie o projeto, copie a connection string em Project Settings › Database (Session pooler), `cp .env.example .env`, preencha `DATABASE_URL` e rode `uv run python -m scripts.rodar_tudo`. A tabela aparece no Table Editor.

**④ Conferir pelo MCP, só leitura**

```text
Qual foi o maior dólar do mês? Mostre a consulta que você usou.
```

## 08 · Guardrail: ninguém apaga o banco

1. **No banco:** rode `material/supabase-usuarios.sql`. A carga usa um usuário sem DELETE nem DROP; o MCP, um usuário só com SELECT.
2. **No Claude Code:** o hook `scripts/bloquear_sql_destrutivo.py` (PreToolUse em `.claude/settings.json`) barra DELETE, DROP e TRUNCATE antes de qualquer MCP executar.
3. **No CLAUDE.md:** "a carga só insere e atualiza".

Teste ao vivo:

```text
Apaga os dados de setembro e recarrega.
```

Esperado: o hook bloqueia a chamada do MCP. Se rodar pelo script com o usuário da carga, o Postgres responde `permission denied`.

## 10 · Onde vive: o mesmo código, outro .env

| Onde | O que muda |
|---|---|
| Local | nada: sem `.env`, DuckDB em `data/` |
| Supabase | `DATABASE_URL` do Supabase |
| On-premise | `DATABASE_URL` do Postgres interno |
| Databricks | a tabela vira Delta no Unity Catalog; próximo passo, aula de sábado |
