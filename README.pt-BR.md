# Awesome Loop Engineering

<!-- last-synced: 2026-06-11 -->

<p align="center">
  <img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%">
</p>

<p align="center">
  <a href="README.md">English</a> |
  <a href="README.zh-CN.md">中文</a> |
  <a href="README.es.md">Español</a> |
  <a href="README.fr.md">Français</a> |
  <a href="README.de.md">Deutsch</a> |
  <a href="README.ja.md">日本語</a> |
  <a href="README.ko.md">한국어</a> |
  <a href="README.pt-BR.md">Português</a> |
  <a href="TRANSLATIONS.md">Ajudar a traduzir</a>
</p>

> Uma lista curada e orientada à implementação para **Loop Engineering**: a camada acima de prompt, context e harness engineering para projetar sistemas recorrentes de agentes de IA.

Prompt engineering melhora o que você pede ao modelo. Context engineering melhora o que o modelo consegue ver. Harness engineering melhora ferramentas, permissões, sandboxes e verificações ao redor de uma execução de agente. **Loop Engineering fica acima das três**: projeta sistemas que acionam agentes, supervisionam, verificam resultados, persistem estado e executam novamente.

Um loop descobre trabalho, delega para um ou mais agentes, verifica o resultado, registra estado, decide a próxima ação e executa novamente em uma cadência ou até atingir um objetivo verificável.

Este repositório trata do novo significado de Loop Engineering no contexto de AI agents e coding agents. Ele não trata de event loops de software, teoria de controle, growth loops, automação genérica ou feedback loops não relacionados a IA.

## Modelo Mental

- Prompt engineering pergunta: o que devo dizer ao modelo?
- Context engineering pergunta: que estado e conhecimento o modelo deve ver?
- Harness engineering pergunta: quais ferramentas, permissões, testes, sandboxes e feedback devem cercar o agente?
- Loop engineering pergunta: que sistema recorrente deve descobrir trabalho, delegar para agentes, verificar resultados, persistir estado, decidir próximas ações e rodar de novo?

Prompt, context e harness engineering melhoram uma execução. Loop Engineering torna o trabalho de agentes repetível, observável e governável ao longo do tempo.

## Loop Contract

Um loop útil normalmente precisa deixar estes elementos visíveis:

| Parte             | Pergunta de design                         | Artefato comum                                             |
| ----------------- | ------------------------------------------ | ---------------------------------------------------------- |
| Objective         | O que o loop deve otimizar?                | Goal, issue, PRD, runbook                                  |
| Trigger           | Quando o loop roda?                        | Schedule, webhook, `/loop`, `/goal`, automation            |
| Discover / Intake | Como o loop encontra trabalho?             | GitHub query, Linear filter, CI failure, feedback stream   |
| Workspace         | Onde o agente pode agir com segurança?     | Worktree, sandbox, branch, container                       |
| Context           | Que conhecimento durável deve carregar?    | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                 |
| Delegation        | Qual agente faz qual parte?                | Explorer, implementer, reviewer, judge                     |
| Verification      | O que decide sucesso ou falha?             | Tests, typecheck, lint, evals, trace graders               |
| State             | O que sobrevive para a próxima execução?   | Progress file, checkpoint, trace, issue comment            |
| Budget            | Quando deve parar de gastar?               | Max turns, max retries, token budget, time box             |
| Escalation        | Quando uma pessoa assume?                  | PR, issue, Slack alert, triage inbox                       |
| Exit              | Como o loop sabe que terminou?             | Acceptance criteria, passing checks, no work found         |

## Modelo de Maturidade

| Nível | Nome                       | Descrição                                                                                |
| ----- | -------------------------- | ---------------------------------------------------------------------------------------- |
| 0     | Manual prompting           | Uma pessoa lê o estado e escreve o próximo prompt.                                       |
| 1     | Scripted retry             | Um script devolve erros ao agente.                                                       |
| 2     | Scheduled loop             | O agente roda em uma cadência e reporta resultados.                                      |
| 3     | Stateful loop              | O progresso sobrevive por arquivos, issues, checkpoints ou traces.                       |
| 4     | Self-verifying loop        | Checks determinísticos ou evaluator agents bloqueiam conclusões erradas.                 |
| 5     | Multi-agent loop           | Agentes especializados dividem discovery, implementation, review e judgment.             |
| 6     | Production-supervised loop | Observabilidade, budgets, approvals, rollback e escalonamento humano são centrais.       |

## Primeiras Leituras

A lista completa de recursos fica no README canônico em inglês: [README.md](README.md).

Leituras recomendadas:

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - Define a mudança de prompting manual para sistemas que promptam, verificam e continuam.
- [Run long horizon tasks with Codex](https://developers.openai.com/blog/run-long-horizon-tasks-with-codex) - Runbook prático para plan-edit-test-observe-repair-document-repeat.
- [Run prompts on a schedule](https://code.claude.com/docs/en/scheduled-tasks) - Mecânica oficial para `/loop`, scheduled tasks e prompts recorrentes.
- [Building Effective Agents](https://www.anthropic.com/engineering/building-effective-agents) - Patterns componíveis para workflows e agentes.

## Contribuir

Contribuições são bem-vindas. Leia [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir um pull request.

Fluxo rápido:

1. Confirme que o recurso trata de Loop Engineering para AI/coding agents ou de uma base direta para isso.
1. Pesquise no README para evitar duplicatas.
1. Escolha a categoria mais específica.
1. Adicione uma entrada neste formato:

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. Explique no PR a relevância, a categoria, o tipo de recurso e por que ele ajuda builders.

## Traduções

Para manter ou adicionar um idioma, leia [TRANSLATIONS.md](TRANSLATIONS.md). As traduções devem preservar o escopo estreito: não incluir event loops, growth loops ou automação genérica.
