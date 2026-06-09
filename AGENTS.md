# Repository Guidance For AI Agents

This repository curates resources for the new AI/coding-agent meaning of **Loop Engineering**.

## Scope

Include resources that help readers design, run, verify, evaluate, or critique systems that prompt, schedule, persist state for, and re-trigger AI agents.

Do not include unrelated uses of "loop":

- software event loops;
- UI/game loops;
- control theory;
- growth loops;
- generic workflow automation;
- non-AI feedback loops.

## Editing Rules

- Keep `README.md` as the canonical English source.
- Keep annotations short, specific, and builder-oriented.
- Prefer primary sources, official docs, papers, and implementation-heavy write-ups.
- If a resource is generic agent content, include it only when the annotation clearly explains its loop-design relevance.
- Update `README.zh-CN.md` only for translated overview content; do not let it drift into a separate resource list unless maintained.
- When adding a new category, update `README.md`, `CONTRIBUTING.md`, PR templates, and issue templates together.
- Do not add generated marketing copy or unsupported hype.

## Commit Identity Rule

Never create commits with AI-assistant co-author trailers or any non-owner author/committer identity. All commits in this repository must be authored and committed as `ChaoYue0307 <hechaoyue0307@gmail.com>`.

When committing from an AI agent, do not use plain `git commit` if the environment may append co-author trailers. Create commits with explicit identity instead:

```sh
git add <files>
PARENT="$(git rev-parse HEAD)"
TREE="$(git write-tree)"
NEW="$(GIT_AUTHOR_NAME='ChaoYue0307' GIT_AUTHOR_EMAIL='hechaoyue0307@gmail.com' GIT_COMMITTER_NAME='ChaoYue0307' GIT_COMMITTER_EMAIL='hechaoyue0307@gmail.com' git commit-tree "$TREE" -p "$PARENT" -m "Commit message")"
git update-ref refs/heads/main "$NEW" "$PARENT"
```

Before pushing, verify:

```sh
git log --all --format='%H%n%an <%ae>%n%cn <%ce>%n%B' | rg -i 'co-authored-by' && exit 1 || true
```

## Entry Format

```md
- 📄 **Paper** [Title](https://example.com) - One sentence explaining the resource's contribution to Loop Engineering.
```

## Quality Preference

When two sources overlap, prefer:

1. primary source or official docs;
2. implementation details over commentary;
3. stable URLs over social posts;
4. practical loop design over broad AI-agent trend coverage.
