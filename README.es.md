# Awesome Loop Engineering

<!-- last-synced: 2026-07-18 -->

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
  <a href="TRANSLATIONS.md">Ayudar a traducir</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Página de inicio</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Espejo en Hugging Face</a>
</p>

> Diseña sistemas recurrentes de agentes de IA con disparadores explícitos, verificación externa, estado duradero, presupuestos limitados y traspaso a personas.

Prompt engineering mejora lo que le pides al modelo. Context engineering mejora lo que el modelo puede ver. Harness engineering mejora las herramientas, permisos, sandboxes y verificaciones alrededor de una ejecución de agente. **Loop Engineering está por encima de las tres**: diseña sistemas que activan agentes, los supervisan, verifican resultados, guardan estado y vuelven a ejecutarse.

Un loop descubre trabajo, lo delega a uno o más agentes, verifica el resultado, registra estado, decide la siguiente acción y vuelve a ejecutarse con una cadencia o hasta alcanzar un objetivo verificable.

Loop Engineering abarca sistemas recurrentes de agentes de IA y coding agents con disparadores explícitos, verificación y estado duradero. No incluye event loops de software, teoría de control, growth loops, automatización genérica ni feedback loops no relacionados con IA.

Empieza con 579 recursos, 20 patrones operativos, 20 loop contracts validados por esquema y 8 puntos de partida de runtime (3 ejecutables y 5 plantillas listas para adaptar), además de una galería comunitaria y 8 idiomas.

## Modelo Mental

- Prompt engineering pregunta: ¿qué debería decirle al modelo?
- Context engineering pregunta: ¿qué estado y conocimiento debería ver el modelo?
- Harness engineering pregunta: ¿qué herramientas, permisos, pruebas, sandboxes y feedback deberían rodear al agente?
- Loop engineering pregunta: ¿qué sistema recurrente debería descubrir trabajo, delegarlo a agentes, verificar resultados, persistir estado, decidir siguientes acciones y volver a ejecutarse?

Prompt, context y harness engineering mejoran una ejecución. Loop Engineering hace que el trabajo de agentes sea repetible, observable y gobernable en el tiempo.

## Loop Contract

Un loop útil normalmente necesita estas partes:

| Parte             | Pregunta de diseño                         | Artefacto común                                             |
| ----------------- | ------------------------------------------ | ----------------------------------------------------------- |
| Objective         | ¿Qué debe optimizar el loop?               | Goal, issue, PRD, runbook                                   |
| Trigger           | ¿Cuándo se ejecuta?                        | Schedule, webhook, `/loop`, `/goal`, automation             |
| Discover / Intake | ¿Cómo encuentra trabajo?                   | GitHub query, Linear filter, CI failure, feedback stream    |
| Workspace         | ¿Dónde puede actuar el agente con cuidado? | Worktree, sandbox, branch, container                        |
| Context           | ¿Qué conocimiento durable debe cargar?     | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                  |
| Delegation        | ¿Qué agente hace cada parte?               | Explorer, implementer, reviewer, judge                      |
| Verification      | ¿Qué decide éxito o fallo?                 | Tests, typecheck, lint, evals, trace graders                |
| State             | ¿Qué sobrevive a la siguiente iteración?   | Progress file, checkpoint, trace, issue comment             |
| Budget            | ¿Cuándo debe dejar de gastar?              | Max turns, max retries, token budget, time box              |
| Escalation        | ¿Cuándo interviene una persona?            | PR, issue, Slack alert, triage inbox                        |
| Exit              | ¿Cómo sabe que terminó?                    | Acceptance criteria, passing checks, no work found          |

## Modelo de Madurez

| Nivel | Nombre                     | Descripción                                                                               |
| ----- | -------------------------- | ----------------------------------------------------------------------------------------- |
| 0     | Manual prompting           | Una persona lee el estado y escribe el siguiente prompt.                                  |
| 1     | Scripted retry             | Un script devuelve errores al agente.                                                     |
| 2     | Scheduled loop             | El agente corre con una cadencia y reporta resultados.                                    |
| 3     | Stateful loop              | El progreso sobrevive mediante archivos, issues, checkpoints o traces.                    |
| 4     | Self-verifying loop        | Verificaciones deterministas o evaluadores bloquean un cierre incorrecto.                 |
| 5     | Multi-agent loop           | Agentes especializados dividen descubrimiento, implementación, revisión y juicio.         |
| 6     | Production-supervised loop | Observabilidad, presupuestos, aprobaciones, rollback y escalación humana son centrales.   |

## Por Dónde Empezar

Explora todos los recursos en la guía completa en inglés: [README.md](README.md).

Recursos iniciales recomendados:

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - Definición de Addy Osmani del cambio desde el prompting manual hacia sistemas que promptean, verifican y continúan.
- [Peter Steinberger sobre diseñar loops](https://x.com/steipete/status/2063697162748260627) - La publicación de junio de 2026 que catalizó la discusión: deja de promptear agentes y diseña loops que los prompteen.
- [Boris Cherny: cinco consejos para ejecutar agentes de forma autónoma](https://x.com/bcherny/status/2063792263067754658) - La receta compacta del creador de Claude Code para loops autónomos de horas o días.
- [The New Stack: de prompting a loops](https://thenewstack.io/loop-engineering/) - Reportaje sobre el cambio de Boris Cherny hacia escribir loops para trabajo recurrente de agentes.

## Contribuir

Las contribuciones son bienvenidas. Lee [CONTRIBUTING.md](CONTRIBUTING.md) antes de abrir un pull request.

Proceso rápido:

1. Confirma que el recurso trata de Loop Engineering para agentes de IA/coding agents o de una base directa para ello.
1. Busca en el README para evitar duplicados.
1. Elige la categoría más específica.
1. Añade una entrada con este formato:

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. Explica en el PR la relevancia, la categoría, el tipo de recurso y por qué ayuda a builders.

## Traducciones

Para mantener o añadir un idioma, lee [TRANSLATIONS.md](TRANSLATIONS.md). Las traducciones deben conservar el alcance estrecho: no mezclar event loops, growth loops ni automatización genérica.
