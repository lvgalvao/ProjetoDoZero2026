# Handoff

Onde a última sessão parou. Atualize ao fechar cada sessão: o agente lê isto na próxima.

## Última sessão: 24/10/2026

- **Feito:** pipeline completa rodando no modo local (extrair → carregar → conferir → relatório), 10 testes verdes, harness montado (`CLAUDE.md`, `.claude/settings.json` com permissões e hooks, subagente `revisor`, comando `/validar`, skill `atualizar-indicadores`, `.mcp.json` somente leitura), workflows `ci.yml` e `diario.yml`.
- **Falta:** criar o projeto no Supabase e preencher o `.env`; cadastrar os secrets no GitHub; rodar o `diario.yml` uma vez à mão (`workflow_dispatch`).
- **Material da aula:** README (guia completo), apresentação de 38 slides, `material/mapa-do-ecossistema.md`, `prd.md` v2 com o harness.
- **Agent Harness:** vídeo baixado e transcrito localmente (`referencias/agent-harness/transcricao-agent-harness.srt` e `.md`); o resumo com minutos está em `resumo-agent-harness.md` e entrou no README e num slide.
- **Atenção:** a Selic meta traz 11 datas futuras a cada extração. É esperado e aparece em `data/rejeitados.json`.
