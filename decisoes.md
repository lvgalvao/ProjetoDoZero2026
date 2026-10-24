# Decisões

Toda decisão confirmada, em ordem: data, decisão, por quê.

| Data | Decisão | Por quê |
|---|---|---|
| 24/10/2026 | Caso prático: dólar (SGS 1), Selic meta (432) e IPCA (433) do Banco Central. | API pública, sem chave, brasileira, muda todo dia. |
| 24/10/2026 | Data no futuro não entra no banco. | A API da Selic meta traz datas futuras (a meta vale até a próxima reunião). O painel mostra o que já aconteceu. |
| 24/10/2026 | Negativo só é aceito no IPCA. | Deflação existe (IPCA de 08/2026 = -0,32%). Dólar e Selic negativos são erro. |
| 24/10/2026 | Dois modos de banco: DuckDB local sem `DATABASE_URL`, Postgres (Supabase) com ela. | O aluno roda tudo sem conta nenhuma e sobe para a nuvem trocando uma linha do `.env`. |
| 24/10/2026 | Rotina diária no GitHub Actions às 9h, salvando o relatório no repositório. | Gratuito em repositório público e ligado ao mesmo lugar do código. |
