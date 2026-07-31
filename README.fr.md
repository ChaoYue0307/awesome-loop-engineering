# Awesome Loop Engineering

<!-- last-synced: 2026-07-20 -->

<p align="center">
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/"><img src="assets/awesome-loop-engineering-cover.png" alt="Awesome Loop Engineering cover" width="100%"></a>
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
  <a href="TRANSLATIONS.md">Aider à traduire</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Page d'accueil</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Miroir Hugging Face</a>
</p>

> Concevez des systèmes récurrents d'agents IA avec des déclencheurs explicites, une vérification externe, un état durable, des budgets bornés et un relais humain.

Le prompt engineering améliore ce que l'on demande au modèle. Le context engineering améliore ce que le modèle peut voir. Le harness engineering améliore les outils, permissions, sandboxes et vérifications autour d'une exécution d'agent. **Loop Engineering se situe au-dessus des trois** : il conçoit des systèmes qui déclenchent des agents, les supervisent, vérifient les résultats, persistent l'état et relancent le travail.

Un loop découvre du travail, le délègue à un ou plusieurs agents, vérifie le résultat, enregistre l'état, décide de l'action suivante et se relance selon une cadence ou jusqu'à atteindre un objectif vérifiable.

Loop Engineering couvre les systèmes récurrents d'agents IA et de coding agents avec des déclencheurs explicites, une vérification et un état durable. Il n'inclut ni les event loops logiciels, ni la théorie du contrôle, ni les growth loops, ni l'automatisation générique, ni les feedback loops sans rapport avec l'IA.

Commencez avec 863 ressources, 22 patterns opérationnels, 22 loop contracts validés par schéma et 8 points de départ d'exécution (3 exécutables et 5 modèles prêts à adapter), ainsi qu'une galerie communautaire et 8 langues.

## Modèle Mental

- Prompt engineering demande : que faut-il dire au modèle ?
- Context engineering demande : quel état et quelles connaissances le modèle doit-il voir ?
- Harness engineering demande : quels outils, permissions, tests, sandboxes et signaux de feedback doivent entourer l'agent ?
- Loop engineering demande : quel système récurrent doit découvrir le travail, déléguer aux agents, vérifier les résultats, persister l'état, décider des prochaines actions et se relancer ?

Prompt, context et harness engineering améliorent une exécution. Loop Engineering rend le travail des agents répétable, observable et gouvernable dans le temps.

## Loop Contract

Un loop utile rend généralement visibles ces éléments :

| Élément           | Question de conception                       | Artefact courant                                            |
| ----------------- | -------------------------------------------- | ----------------------------------------------------------- |
| Objective         | Que doit optimiser le loop ?                 | Goal, issue, PRD, runbook                                   |
| Trigger           | Quand le loop s'exécute-t-il ?               | Schedule, webhook, `/loop`, `/goal`, automation             |
| Discover / Intake | Comment le loop trouve-t-il le travail ?     | GitHub query, Linear filter, CI failure, feedback stream    |
| Workspace         | Où l'agent peut-il agir en sécurité ?        | Worktree, sandbox, branch, container                        |
| Context           | Quelles connaissances durables charger ?     | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                  |
| Delegation        | Quel agent fait quoi ?                       | Explorer, implementer, reviewer, judge                      |
| Verification      | Qu'est-ce qui décide succès ou échec ?       | Tests, typecheck, lint, evals, trace graders                |
| State             | Qu'est-ce qui survit au prochain passage ?   | Progress file, checkpoint, trace, issue comment             |
| Budget            | Quand faut-il arrêter de consommer ?         | Max turns, max retries, token budget, time box              |
| Escalation        | Quand une personne doit-elle reprendre ?     | PR, issue, Slack alert, triage inbox                        |
| Exit              | Comment sait-on que le loop est terminé ?    | Acceptance criteria, passing checks, no work found          |

## Modèle de Maturité

| Niveau | Nom                        | Description                                                                                 |
| ------ | -------------------------- | ------------------------------------------------------------------------------------------- |
| 0      | Manual prompting           | Une personne lit l'état et écrit le prompt suivant.                                         |
| 1      | Scripted retry             | Un script renvoie les erreurs à l'agent.                                                    |
| 2      | Scheduled loop             | L'agent s'exécute selon une cadence et rapporte ses résultats.                              |
| 3      | Stateful loop              | Le progrès survit via fichiers, issues, checkpoints ou traces.                              |
| 4      | Self-verifying loop        | Des vérifications déterministes ou évaluateurs empêchent une fausse validation.             |
| 5      | Multi-agent loop           | Des agents spécialisés séparent découverte, implémentation, revue et jugement.              |
| 6      | Production-supervised loop | Observabilité, budgets, approbations, rollback et escalade humaine sont de premier ordre.   |

## Premières Lectures

Explorez toutes les ressources dans le guide complet en anglais : [README.md](README.md).

Ressources recommandées pour commencer :

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - La définition d'Addy Osmani du passage du prompting manuel aux systèmes qui promptent, vérifient et continuent.
- [Peter Steinberger sur la conception de loops](https://x.com/steipete/status/2063697162748260627) - Le post de juin 2026 qui a catalysé la discussion : cessez de prompter les agents, concevez des loops qui les promptent.
- [Boris Cherny : cinq conseils pour exécuter des agents en autonomie](https://x.com/bcherny/status/2063792263067754658) - La recette compacte du créateur de Claude Code pour des loops autonomes de plusieurs heures ou jours.
- [The New Stack : du prompting aux loops](https://thenewstack.io/loop-engineering/) - Reportage sur le passage de Boris Cherny à l'écriture de loops pour le travail récurrent des agents.

## Contribuer

Les contributions sont bienvenues. Lis [CONTRIBUTING.md](CONTRIBUTING.md) avant d'ouvrir une pull request.

Processus rapide :

1. Vérifie que la ressource concerne Loop Engineering pour agents IA/coding agents ou une base directe.
1. Recherche dans le README pour éviter les doublons.
1. Choisis la catégorie la plus spécifique.
1. Ajoute une entrée dans ce format :

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. Explique dans la PR la pertinence, la catégorie, le type de ressource et l'intérêt pour les builders.

## Traductions

Pour maintenir ou ajouter une langue, lis [TRANSLATIONS.md](TRANSLATIONS.md). Les traductions doivent préserver le périmètre : ne pas inclure les event loops, growth loops ou automatisations génériques.
