# Mapa do ecossistema 2026

Material de revisão da live. Para cada termo: **o que é**, **quando usar**, **quando não usar** e **onde aprofundar na Jornada**. Organizado na ordem em que um projeto nasce.

---

## 1. Antes do código: entender o problema

| Termo | O que é | Quando usar | Quando não usar | Na Jornada |
|---|---|---|---|---|
| **Design Sprint** | Método de 5 etapas (entender, idear, decidir, prototipar, testar) para sair de um problema e chegar a um protótipo validado com usuários em poucos dias. | Problema grande e ambíguo, muita gente com opinião, risco de construir a coisa errada. | Problema já claro, ou correção pequena. Aí basta o PRD. | Engenharia de Dados › "Data Sprint – Das dores, aos requisitos até o Deploy" (módulo a gravar) |
| **Discovery** | Fase de investigar dores, usuários e dados antes de decidir o que construir. | Sempre que o pedido chega como solução ("quero um dashboard") e não como problema. | Quando o escopo já foi validado. | Trilha Databricks › Módulo 4 (requisitos, escopo e métricas) · Desafio de Agosto, aula 2 |
| **PRD** | Product Requirements Document: objetivo, usuários, requisitos, critério de aceite e o que fica fora. | Antes de pedir qualquer código ao agente. | Nunca é demais, mas pode ter meia página. | Trilha Claude Code › aula de PRD |
| **Spec-Driven Development** | Desenvolver a partir de especificações escritas: uma spec, uma branch, uma sessão. | Quando o agente implementa: a spec é o contrato. | Exploração rápida, protótipo descartável. | Trilha Claude Code › Módulo 4 · curso Agent Harness |
| **Critério de aceite** | Condição testável que diz se a entrega está pronta ("o relatório sai às 9h"). | Em toda tarefa entregue a um agente. | — | curso Agent Harness (Definição de Pronto) |

## 2. O ambiente de trabalho

| Termo | O que é | Quando usar | Quando não usar | Na Jornada |
|---|---|---|---|---|
| **Terminal** | Onde você digita comandos. Servidor, nuvem e o próprio agente vivem nele. | Sempre. | — | Trilha Claude Code › Módulo 1 |
| **Git** | Controle de versão: cada mudança vira um ponto para onde dá para voltar. | Todo projeto, desde o primeiro minuto. | — | curso Git e GitHub |
| **GitHub** | Onde o repositório Git mora na nuvem, com issues, pull requests e Actions. | Para compartilhar, revisar e automatizar. | — | curso Git e GitHub |
| **IDE** (VS Code, Cursor, Antigravity) | Editor de código com terminal, busca e extensões. | Sempre. A escolha é gosto. | — | Trilha Python › Preparando o ambiente |
| **uv** | Gerenciador de Python: versão, ambiente e dependências numa ferramenta só. | Todo projeto Python novo. | Projeto legado que já usa Poetry ou conda e funciona. | YouTube "Ambientes Virtuais com UV" (aula a incluir) |
| **`.env`** | Arquivo com chaves e senhas, fora do Git. | Sempre que houver chave. | Nunca suba o `.env` para o GitHub. | aula a gravar |

## 3. O agente e o harness

| Termo | O que é | Quando usar | Quando não usar | Na Jornada |
|---|---|---|---|---|
| **Claude Code** | Agente de programação que roda no terminal: lê o projeto, edita arquivos, roda comandos e testa. | Construir e operar projetos. | Tarefa que um script já resolve sozinho e de graça. | Trilha Claude Code |
| **Agent harness** | Tudo o que fica em volta do modelo (memória, ferramentas, execução, validação) e faz ele entregar com segurança. | Todo projeto em que um agente trabalha de verdade. | — | curso Agent Harness |
| **`CLAUDE.md`** | Índice do projeto lido em toda sessão: comandos, regras, "nunca quebrar". | Sempre. Curto. | Não vira documentação longa. | curso Agent Harness |
| **Rules** (`.claude/rules/`) | Regras por área do código que carregam só quando o agente mexe naquela pasta. | Projeto com áreas diferentes (backend, testes, agente). | Projeto pequeno: o `CLAUDE.md` basta. | curso Agent Harness |
| **Skill** | Pasta com um procedimento que o agente carrega quando julga relevante. | Tarefa que se repete ("atualizar indicadores", "relatório do dia"). | Regra que vale sempre (vai no `CLAUDE.md`). | Trilha Claude Code › Módulo 3 |
| **Command** | Ritual que você chama pelo nome (`/validar`). | Passo que você quer disparar na hora certa. | — | curso Agent Harness |
| **Subagente** | Outro agente com janela própria, para uma tarefa isolada (ex.: revisar o diff sem ter visto a implementação). | Revisão, pesquisa paralela. | Tarefa simples: atrapalha mais que ajuda. | curso Agent Harness · Engenharia de IA › Multi Agent Systems |
| **Hook** | Comando que roda sozinho num momento do agente (depois de editar, antes de terminar). | Formatar sempre, bloquear "pronto" com teste vermelho. | Coisa demorada a cada edição. | curso Agent Harness |
| **Permissões** (`settings.json`) | Lista do que o agente pode rodar sem pedir (`allow`) e do que é proibido (`deny`). | Sempre que houver ação destrutiva possível. | — | curso Agent Harness |
| **MCP** | Protocolo que liga o agente a sistemas externos (banco, CRM, Drive) como ferramentas. | Quando o agente precisa consultar ou agir num sistema. | Quando um script com a API resolve e é repetível. | Engenharia de IA › Tools e MCP |
| **Memória / handoff** | O que sobrevive entre sessões: `CLAUDE.md`, `HANDOFF.md`, memória do agente. | Projeto que dura mais de uma conversa. | — | curso Agent Harness |

## 4. Onde o dado vive

| Termo | O que é | Quando usar | Quando não usar | Na Jornada |
|---|---|---|---|---|
| **API** | Porta de entrada de um sistema por HTTP: você pede, ele responde (geralmente JSON). | Extrair dado de um sistema. | Quando o sistema oferece exportação em lote mais simples. | Trilha Python › APIs |
| **Postgres** | Banco relacional open source, o mais usado do mercado. | Dado estruturado de aplicação e de análise pequena ou média. | Volume enorme de análise (aí, warehouse). | Trilha SQL |
| **Supabase** | Postgres na nuvem com painel, autenticação, Storage (arquivos, compatível com S3), Edge Functions e plano gratuito. | Começar: banco, arquivos e backend de app sem montar servidor. | Big data e Spark. | aula a gravar (a live) |
| **Object storage / S3** | Lugar para guardar arquivos (CSV, JSON, Parquet, imagem). | Dado bruto antes de transformar. | Dado que precisa de consulta e atualização linha a linha. | Trilha Databricks |
| **Data warehouse** | Banco feito para análise em grande volume. | Muitas fontes, muito histórico, muitos analistas. | Projeto pequeno: Postgres resolve. | Trilha Databricks |
| **Lakehouse** | Arquivos no storage com camada de tabela (Delta, Iceberg): o barato do lake com o controle do warehouse. | Dados grandes, variados, com governança. | Projeto pequeno. | Trilha Databricks › Medalhão |
| **Arquitetura medalhão** | Camadas bronze (bruto), prata (limpo) e ouro (pronto para o negócio). | Qualquer pipeline com mais de uma etapa. | — | Trilha Databricks › Módulo 2 |
| **DuckDB** | Banco analítico que roda dentro do Python, sem servidor. SQL direto em CSV, JSON e Parquet. | Transformar e explorar localmente. | Muitos usuários ao mesmo tempo. | Trilha Python › Projeto 1 (1 bilhão de linhas) |

## 5. Databricks

| Termo | O que é | Quando usar |
|---|---|---|
| **Databricks** | Plataforma de dados e IA em cima de Spark e Delta Lake. Tem Free Edition. | Quando o projeto cresce, precisa de Spark, governança ou vai para a empresa. Bom para prova de conceito. |
| **Unity Catalog** | Governança: quem acessa qual tabela, linhagem, auditoria. | Sempre que há mais de uma pessoa ou dado sensível. |
| **Lakeflow Connect** | Ingestão gerenciada de fontes (bancos, SaaS). | Trazer dado de sistemas sem escrever extrator. |
| **Lakeflow Jobs** | Agendador e orquestrador de tarefas. | Rodar a pipeline sozinha, com dependências. |
| **Lakeflow Declarative Pipelines** | Pipelines descritas em SQL ou Python, com qualidade embutida. | Medalhão com regras de qualidade. |
| **Spark / PySpark** | Processamento distribuído. | Volume que não cabe numa máquina. |
| **SQL Warehouse** | Motor SQL para análise e dashboards. | Analistas consultando e BI. |

Quando **não** usar Databricks: projeto pessoal pequeno, protótipo de uma tarde, dado que cabe no Postgres. Na Jornada: Trilha Databricks.

## 6. Colocar no ar e rodar sozinho

| Termo | O que é | Quando usar | Quando não usar | Na Jornada |
|---|---|---|---|---|
| **Vercel** | Hospedagem de sites e APIs (Next.js, FastAPI) com deploy a cada `git push`. | Expor uma aplicação ou API leve. | Streamlit e processos que ficam rodando o tempo todo. | Trilha Claude Code › Projeto 1 |
| **Lovable** | Construtor de aplicações por conversa (gera React + Supabase). | Landing page e protótipo de produto rápido. | Lógica de dados complexa. Cada mudança gasta crédito. | Trilha Claude Code |
| **CI/CD** | Integração e entrega contínuas: testes rodam sozinhos e o deploy sai sozinho. | Todo projeto com mais de uma pessoa ou em produção. | — | Engenharia de Dados › DevOps (módulo a gravar) |
| **GitHub Actions** | CI/CD e agendamento do GitHub. | Testes no pull request e rotina diária gratuita. | Pipeline pesada e longa. | aula a gravar (a live) |
| **Airflow** | Orquestrador de pipelines com dependências. | Muitas pipelines encadeadas. | Uma rotina por dia: GitHub Actions basta. | Engenharia de Dados › Airflow |
| **n8n** | Automação visual que liga sistemas sem código. | Integração simples entre ferramentas (formulário → CRM → e-mail). | Transformação pesada de dados. | Trilha n8n |
| **Docker** | Empacota o projeto com tudo o que precisa para rodar igual em qualquer lugar. | Deploy em servidor, ambiente complexo. | Começo: uv resolve o ambiente Python. | Engenharia de Dados › Infra, Linux, Docker (módulo a gravar) |

## 7. Qualidade e confiança

| Termo | O que é | Quando usar | Na Jornada |
|---|---|---|---|
| **Teste (pytest)** | Código que prova que outro código faz o que deveria. | Toda regra de negócio e toda conversão de dado. | aula a gravar |
| **Gate** | Verificação que bloqueia o avanço se falhar (testes, lint, conferência). | Antes de dar uma tarefa como pronta. | curso Agent Harness |
| **Data quality / contrato** | Regras que o dado precisa cumprir antes de seguir (Pydantic, expectativas). | Antes de carregar no banco. | Engenharia de Dados › "Pydantic, Data Quality e TDD" (módulo a gravar) |
| **Observabilidade** | Saber o que a pipeline ou o agente fez, quanto custou e onde falhou. | Tudo que roda sozinho. | Engenharia de Dados › Observabilidade · Engenharia de IA › Evaluation |
| **Eval** | Conjunto de casos (golden e adversariais) para medir se o agente responde certo. | Todo agente que responde ou decide. | Engenharia de IA › Evaluation · curso Agent Harness |

## 8. IA aplicada

| Termo | O que é | Na Jornada |
|---|---|---|
| **LLM** | Modelo de linguagem (Claude, GPT, Gemini). | Engenharia de IA › Fundamentos |
| **RAG** | Buscar documentos relevantes e entregar ao modelo antes de responder. | Engenharia de IA › Módulo 2 |
| **Agente** | Modelo que decide passos e usa ferramentas para cumprir um objetivo. | Engenharia de IA › Módulo 3 |
| **LangGraph** | Framework para agentes com fluxo controlado (grafo). | Engenharia de IA › LangGraph |
| **Human in the loop** | O agente para e pede aprovação antes de uma ação. | Engenharia de IA › Human in the Loop |
| **Fine-tuning** | Treinar um modelo com seus exemplos. Raramente é o primeiro passo. | Engenharia de IA › Módulo 5 |

---

**Regra de bolso:** comece pelo mais simples que resolve (Postgres, script, GitHub Actions) e suba de degrau (Databricks, Airflow, Docker) quando o problema pedir, não antes.
