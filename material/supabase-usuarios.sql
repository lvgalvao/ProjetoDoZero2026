-- Guardrail no banco: dois usuários, nenhum com DELETE ou DROP.
-- Rode no SQL Editor do Supabase, depois que a tabela indicadores existir
-- (a primeira carga cria a tabela). Troque as senhas antes de rodar e
-- guarde as connection strings só no .env.

-- 1. Usuário da carga: o upsert precisa só de SELECT, INSERT e UPDATE.
create role painel_carga with login password 'TROQUE-ESTA-SENHA';
grant usage on schema public to painel_carga;
grant select, insert, update on table public.indicadores to painel_carga;
-- Sem DELETE, sem TRUNCATE, e não é dono da tabela: não consegue DROP.

-- 2. Usuário do MCP: só lê.
create role painel_leitura with login password 'TROQUE-ESTA-OUTRA-SENHA';
grant usage on schema public to painel_leitura;
grant select on table public.indicadores to painel_leitura;

-- No .env:
--   DATABASE_URL    = connection string com o usuário painel_carga
--   DATABASE_URL_RO = connection string com o usuário painel_leitura
-- No pooler do Supabase, o usuário vem como painel_carga.<id-do-projeto>.

-- Teste: conectado como painel_carga, isto precisa falhar.
--   delete from indicadores where data >= '2026-09-01';
--   -> ERROR: permission denied for table indicadores
