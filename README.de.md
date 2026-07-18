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
  <a href="TRANSLATIONS.md">Beim Übersetzen helfen</a> |
  <a href="https://chaoyue0307.github.io/awesome-loop-engineering/">Landingpage</a> |
  <a href="https://huggingface.co/datasets/cy0307/awesome-loop-engineering">Hugging-Face-Spiegel</a>
</p>

> Entwirf wiederkehrende KI-Agenten-Systeme mit klaren Auslösern, externer Verifikation, dauerhaftem Zustand, begrenzten Budgets und menschlicher Übergabe.

Prompt Engineering verbessert, was man dem Modell sagt. Context Engineering verbessert, was das Modell sehen kann. Harness Engineering verbessert Werkzeuge, Berechtigungen, Sandboxes und Prüfungen rund um einen einzelnen Agentenlauf. **Loop Engineering liegt über allen drei Ebenen**: Es entwirft Systeme, die Agenten auslösen, überwachen, Ergebnisse prüfen, Zustand speichern und erneut laufen.

Ein Loop entdeckt Arbeit, übergibt sie an einen oder mehrere Agenten, prüft das Ergebnis, speichert Zustand, entscheidet den nächsten Schritt und läuft erneut nach Zeitplan oder bis ein überprüfbares Ziel erreicht ist.

Loop Engineering umfasst wiederkehrende KI-Agenten- und Coding-Agent-Systeme mit expliziten Auslösern, Verifikation und dauerhaftem Zustand. Software-Event-Loops, Regelungstechnik, Growth Loops, generische Automatisierung und nicht-KI-bezogene Feedback-Loops gehören nicht dazu.

Starte mit 579 geprüften Ressourcen, 20 operativen Loop-Patterns, 20 schemavalidierten Loop-Contracts und 8 Runtime-Startern (3 ausführbare Programme und 5 anpassbare Vorlagen), ergänzt durch eine Community-Galerie und 8 Sprachen.

## Mentales Modell

- Prompt Engineering fragt: Was soll ich dem Modell sagen?
- Context Engineering fragt: Welchen Zustand und welches Wissen soll das Modell sehen?
- Harness Engineering fragt: Welche Werkzeuge, Berechtigungen, Tests, Sandboxes und Feedback-Signale sollen den Agenten umgeben?
- Loop Engineering fragt: Welches wiederkehrende System soll Arbeit entdecken, an Agenten delegieren, Ergebnisse prüfen, Zustand speichern, nächste Aktionen entscheiden und erneut laufen?

Prompt, Context und Harness Engineering verbessern einen einzelnen Lauf. Loop Engineering macht Agentenarbeit über Zeit wiederholbar, beobachtbar und steuerbar.

## Loop Contract

Ein nützlicher Loop macht normalerweise diese Bestandteile sichtbar:

| Teil              | Designfrage                                      | Typisches Artefakt                                          |
| ----------------- | ------------------------------------------------ | ----------------------------------------------------------- |
| Objective         | Was soll der Loop optimieren?                    | Goal, issue, PRD, runbook                                   |
| Trigger           | Wann läuft der Loop?                             | Schedule, webhook, `/loop`, `/goal`, automation             |
| Discover / Intake | Wie findet der Loop Arbeit?                      | GitHub query, Linear filter, CI failure, feedback stream    |
| Workspace         | Wo kann der Agent sicher handeln?                | Worktree, sandbox, branch, container                        |
| Context           | Welches dauerhafte Wissen wird geladen?          | `AGENTS.md`, `CLAUDE.md`, `SKILL.md`, docs                  |
| Delegation        | Welcher Agent übernimmt welche Aufgabe?          | Explorer, implementer, reviewer, judge                      |
| Verification      | Was entscheidet über Erfolg oder Fehler?         | Tests, typecheck, lint, evals, trace graders                |
| State             | Was bleibt für den nächsten Lauf erhalten?       | Progress file, checkpoint, trace, issue comment             |
| Budget            | Wann soll der Loop aufhören zu verbrauchen?      | Max turns, max retries, token budget, time box              |
| Escalation        | Wann übernimmt ein Mensch?                       | PR, issue, Slack alert, triage inbox                        |
| Exit              | Woher weiß der Loop, dass er fertig ist?         | Acceptance criteria, passing checks, no work found          |

## Reifegradmodell

| Stufe | Name                       | Beschreibung                                                                                  |
| ----- | -------------------------- | --------------------------------------------------------------------------------------------- |
| 0     | Manual prompting           | Ein Mensch liest den Zustand und schreibt den nächsten Prompt.                                |
| 1     | Scripted retry             | Ein Skript gibt Fehler an den Agenten zurück.                                                 |
| 2     | Scheduled loop             | Der Agent läuft nach Zeitplan und berichtet Ergebnisse.                                       |
| 3     | Stateful loop              | Fortschritt bleibt über Dateien, Issues, Checkpoints oder Traces erhalten.                    |
| 4     | Self-verifying loop        | Deterministische Checks oder Evaluator-Agenten blockieren falsche Abschlüsse.                 |
| 5     | Multi-agent loop           | Spezialisierte Agenten teilen Discovery, Implementierung, Review und Urteil auf.              |
| 6     | Production-supervised loop | Observability, Budgets, Freigaben, Rollback und menschliche Eskalation sind zentral.          |

## Erste Lektüre

Die vollständige Ressourcenliste bleibt im kanonischen englischen README: [README.md](README.md).

Empfohlene Einstiege:

- [Loop Engineering](https://addyosmani.com/blog/loop-engineering/) - Addy Osmanis Definition des Wechsels vom manuellen Prompting zu Systemen, die selbst prompten, verifizieren und weiterlaufen.
- [Peter Steinberger über das Entwerfen von Loops](https://x.com/steipete/status/2063697162748260627) - Der Post vom Juni 2026, der die Diskussion auslöste: Agents nicht mehr prompten, sondern Loops entwerfen, die sie prompten.
- [Boris Cherny: fünf Tipps für autonome Agent-Läufe](https://x.com/bcherny/status/2063792263067754658) - Das kompakte Loop-Rezept des Claude-Code-Schöpfers für stunden- bis tagelange autonome Läufe.
- [The New Stack: vom Prompting zu Loops](https://thenewstack.io/loop-engineering/) - Bericht über Boris Chernys Wechsel zum Schreiben von Loops für wiederkehrende Agent-Arbeit.

## Beitragen

Beiträge sind willkommen. Bitte lies [CONTRIBUTING.md](CONTRIBUTING.md), bevor du einen Pull Request öffnest.

Schneller Ablauf:

1. Prüfe, ob die Ressource Loop Engineering für KI-Agenten/Coding Agents oder eine direkte Grundlage dafür behandelt.
1. Suche im README, um Duplikate zu vermeiden.
1. Wähle die spezifischste Kategorie.
1. Füge einen Eintrag in diesem Format hinzu:

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

1. Erkläre im PR Relevanz, Kategorie, Ressourcentyp und Nutzen für Builders.

## Übersetzungen

Wenn du eine Sprache pflegen oder hinzufügen möchtest, lies [TRANSLATIONS.md](TRANSLATIONS.md). Übersetzungen müssen den engen Scope bewahren und dürfen Event Loops, Growth Loops oder generische Automatisierung nicht in den Umfang ziehen.
