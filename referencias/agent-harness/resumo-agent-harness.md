# Resumo: Workshop Agent Harness (Jornada de Dados)

**Onde está:** área do aluno, curso "Agent Harness" (id 341, aula 2341), vídeo de 3h48 gravado em 28/06/2026 por Caio Machado de Oliveira. Complemento curto: Desafios Mensais › Desafio Agosto › "Aula 3 – Harness Engineering" (10 min).
**Material:** repositório público `github.com/caio-moliveira/workshop-agent-harness` (README, `CLAUDE.md`, `.claude/` completo e a apresentação em HTML).
**Fonte deste resumo:** o repositório, a descrição das aulas e a transcrição local do vídeo (`transcricao-agent-harness.md`, Whisper, 24/10/2026). Os minutos são aproximados.

## A ideia central

**Harness é o sistema ao redor do modelo** (estado, ferramentas, execução e validação) que faz um modelo virar um agente que entrega. O harness começa **antes da primeira linha de código**.

Princípios do workshop:

- **A IA é um amplificador**: amplifica o processo que já existe, bom ou ruim.
- **De instruir → informar → orquestrar.**
- **Todo erro vira um sinal permanente**: uma falha vira regra, hook, teste ou skill, não um "run ruim" para repetir.
- **A janela é transitória; os arquivos lembram.** O que sobrevive a um reset de contexto é o que está escrito no repositório (`CLAUDE.md`, ADRs, `HANDOFF.md`).
- **A maior falha não é o código, é o desalinhamento**: alinhar antes de gerar.
- **Comece mínimo**: o menor harness que cobre os riscos reais; subagente e orquestração só quando a tarefa pede.
- **O harness não encolhe, ele se move**: dimensionar pelos riscos do projeto, não pelo modelo do momento.

## O fluxo

`ideia.md` → `/grill-me` (entrevista que fecha cada decisão) → `/to-prd` (`PRD.md`) → **harness à mão** (`.claude/`) → `/to-issues` (fatias prontas para o agente) → implementar com gate, revisor e métricas.

Na aula de agosto: **uma spec, uma branch, uma sessão**.

## As peças do `.claude/` e a pergunta que cada uma responde

| Peça | Arquivo | Para quê |
|---|---|---|
| Índice do projeto | `CLAUDE.md` | O que vale sempre: stack, comandos, invariantes ("nunca quebrar"), onde fica cada coisa. Curto. |
| Regras por área | `.claude/rules/*.md` com `paths:` | Carregam só quando o agente mexe naquela pasta (backend, testes, agente). |
| Permissões | `.claude/settings.json` (`allow`/`deny`) | Perímetro: o que roda sem pedir e o que é proibido (ex.: apagar volume do banco, editar dados). |
| Hooks | `.claude/settings.json` | `PostToolUse` formata a cada edição; `Stop` roda ruff + mypy + pytest e **bloqueia** o fim se der vermelho. |
| MCP | `.mcp.json` | Postgres **somente leitura** para o agente ver o schema real antes de escrever SQL. |
| Subagente revisor | `.claude/agents/revisor-codigo.md` | Revisa o diff contra as regras numa janela nova. **Revisa, não edita.** |
| Comandos | `.claude/commands/` | Rituais que você chama: `/validar` (gate) e `/scorecard` (métricas). |
| Skills | `.claude/skills/` | Competências que o modelo carrega quando julga relevante; baixadas e travadas num lock. |
| Definição de Pronto | `.claude/rules/definicao-de-pronto.md` + `metrics/` | Contrato mensurável de "entregue": gate verde, regras respeitadas, revisor aprovou, critérios com evidência. |

Na aula de agosto, a regra de bolso: **`CLAUDE.md` para o que vale sempre, commands para rituais que você invoca, skills para competências que o modelo julga relevantes.** E mais:
- a verificação roda **em sessão nova, que nunca viu a implementação**;
- "**revisor que conserta código deixou de ser revisor**";
- duas camadas de teste (unitário para correção, segurança para garantia);
- evals (golden e adversariais) escritos **antes** do agente existir.

## Guardrails determinísticos (não dependem do LLM)

- SQL do agente: só `SELECT`/`WITH`, uma instrução, `LIMIT` garantido, papel somente leitura e timeout no banco.
- Toda recomendação amarrada a uma fonte recuperada: sem fonte é falha.
- Dados pré-carregados são "sagrados": comandos destrutivos ficam no `deny`.

## O que o vídeo acrescenta (com o minuto para ir direto)

### Linha do tempo

| Minuto | Assunto |
|---|---|
| 0:10 | A ferramenta passa e o fundamento fica: Claude Code e Codex já são harnesses. A IA amplifica o processo (relatório DORA). |
| 0:15 | Velocidade não é qualidade: "garbage in, garbage out". |
| 0:15–0:25 | A evolução: engenharia de prompt → de contexto → de harness. |
| 0:25–0:30 | O harness é a rédea do cavalo. "Tudo que não é o modelo é harness." |
| 0:35–0:45 | Arquivos e git como memória, sandbox, MCP, Ralph loop, o erro que vira aprendizado. |
| 0:50 | Modelo razoável com bom harness ganha de modelo top com harness ruim. |
| 0:55 | Caso real: 120 desenvolvedores. Desenvolver mais rápido, por si só, não significa nada. |
| 1:25–1:31 | Skills de terceiros (Matt Pocock); PRD com grill-me e to-prd; o que é probabilístico e o que é determinístico. |
| 1:36–1:51 | Passeio pelo `.claude/`: revisor, scorecard, rules, settings e `CLAUDE.md` como mapa. |
| 1:51–2:16 | `/to-issues` (7 fatias no GitHub), primeira issue, revisor, ADR, regra gravada sozinha na memória. |
| 2:21–2:26 | Subagentes e worktree: quando usar e quando não. |
| 2:41–2:56 | Medo de "atrofiar", vibe coder x engenheiro. |
| 3:01–3:16 | Janela de contexto, handoff, economia de token. |
| 3:26–3:46 | BDD, testes determinísticos x evals, guardrail, scorecard final, caso de prompt injection. |

### Ideias que não estavam no repositório

- **Prompt → contexto → harness** (0:15–0:25). Prompt é uma interação. Contexto é janela grande com ferramentas. Harness é o agente operando um sistema inteiro (git, bash, arquivos) que você construiu.
- **Modelo novo não dispensa harness** (0:30). As versões novas são ajustadas para usar ferramentas, memória, git e bash. O harness não encolhe.
- **Sandbox** (0:35). Ao aceitar a permissão da pasta, o estrago possível fica dentro do repositório.
- **Ralph loop** (0:40). A janela enche, a sessão recomeça do zero e segue bem porque lê o repositório e o `.claude/`.
- **`CLAUDE.md` é mapa, não manual** (1:46–1:51). Até cerca de 200 linhas (o da demo tem 67). Sem ele o agente faz grep e lê tudo. Dá para ter um por pasta.
- **Skill custa contexto** (1:41). O nome e a descrição de todas as skills carregam em toda sessão; a descrição é o que faz o agente escolher a skill.
- **`settings.local.json`** (1:46). O "sim, sempre" das perguntas de permissão vai para ele; o `settings.json` é o fixo do time.
- **Plano fechado** (2:06). Sem plano combinado, quando algo falha o agente muda o plano para caber no código. Com PRD e issues fechados, ele muda o código para caber no plano. Fechar toda instrução com "quais skills usar" e "me pergunte quando não tiver certeza".
- **ADR** (2:11). Registro de decisão: contexto, decisão e consequência.
- **Handoff é passagem de turno** (3:01). Só o crítico ("fiz X, parei em Y"); o resto já está no harness.
- **Guardrail × harness** (3:36). O guardrail protege em produção; o harness organiza o desenvolvimento.
- **Testes determinísticos × evals** (3:26–3:36). O que tem resposta certa vira teste (BDD: dado, quando, então). O que a IA gera pede eval: golden dataset feito por humano, métricas como faithfulness e LLM-as-judge.
- **Scorecard** (3:41). Change failure rate, taxa de autonomia e lead time por issue.

### O que deu errado ao vivo (e virou lição)

- `docker compose up` falhou porque as imagens do backend e do front ainda não existiam. Solução: subir só os bancos (1:20).
- O `/to-issues` pegou issues de outro usuário do repositório público. Corrigido com "só as do meu usuário", e o agente **gravou isso como regra na memória**: o erro virou sinal permanente ao vivo (2:11–2:16).
- O revisor aprovou "com ressalvas" sem dizer quais (2:11): o parecer precisa listar as ressalvas.
- O contexto chegou a 97–100% sem gerar handoff (3:01–3:11).
- O Claude Code assumiu chave da Anthropic quando o projeto usava OpenAI: é preciso dizer explicitamente (3:11).

### Perguntas do público que servem para iniciantes

- **O que é MCP?** (0:40) Como um `pip install` para o agente: alguém já escreveu as ferramentas daquele sistema.
- **Perguntas com muitos joins?** (1:15) Entregue ao agente a camada ouro ou uma view pronta, nunca um monte de tabelas.
- **Descrevo as colunas no prompt?** (1:20) Melhor deixar as consultas dos indicadores prontas e acessíveis por ferramenta: menos token e menos query errada.
- **Ler o `.md` é garantido?** (1:31) Não, tudo que é IA é probabilístico. O que precisa acontecer sempre vai num hook.
- **CLI ou extensão?** (1:51) Ele prefere a CLI. Codex com `AGENTS.md` funciona igual, desde que instrua a ler o mapa.
- **Quando usar subagente?** (2:16–2:26) Tarefas independentes ou uma verificação fixa que roda e fecha. Squad de subagentes leva para o software o problema de comunicação de um time.
- **Terceirizar o código atrofia?** (2:41–2:56) No trabalho, a concorrência não deixa escolha. Para estudar fundamento, desligue a IA.

### As 8 ideias para a aula de revisão

1. **0:50**: modelo razoável com bom harness ganha de modelo top com harness ruim.
2. **0:25–0:30**: harness é a rédea; tudo que não é o modelo é harness.
3. **1:46–1:51**: `CLAUDE.md` é mapa, até 200 linhas.
4. **2:06**: com plano fechado, o agente muda o código e não o plano.
5. **2:16**: a correção que virou regra gravada na memória.
6. **0:40 e 3:01**: a janela acaba, a memória é o repositório; handoff é passagem de turno.
7. **1:41 e 2:21**: MCP de banco só leitura; revisor como verificação fixa, sem squad.
8. **1:20 e 3:26**: consultas prontas para os indicadores; teste determinístico (`/validar`) e eval para o que a IA gera.
