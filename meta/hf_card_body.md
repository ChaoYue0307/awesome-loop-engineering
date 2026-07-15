
## Dataset Structure

Each row in `data/resources.jsonl` (and the equivalent `data/resources.csv`) is one curated resource, exported from the English `README.md`.

| Field | Description |
| --- | --- |
| `row_id` | Positional identifier (`ale-NNNN`); not stable across README reorders. |
| `section` | The `##` section the entry lives under. |
| `section_slug` | Anchor-style slug of the section. |
| `resource_type` | Paper, Blog, Docs, Tool, Benchmark, Pattern, Template, List, or Critique. |
| `marker` | Emoji shown before the entry in the README. |
| `title` | Linked entry title. |
| `url` | Resource URL. |
| `url_kind` | `external` or `local_path` (a file inside the repository). |
| `domain` | Host of an external URL (empty for local paths). |
| `annotation` | The one-line description as written in the README. |
| `description` | Copy of the annotation for tooling that expects a `description` field. |
| `key_contribution` | Short statement of what the resource adds. |
| `novelty` | Why the entry is distinct within its section. |
| `impact` | Who benefits and how. |
| `signal` | Why the entry is trustworthy (adoption, venue, authorship). |
| `signal_strength` | Coarse confidence label (`strong`, `medium`, `contextual`). |
| `source_readme` | README file the row came from. |
| `source_line` | 1-based line number in that README. |
| `source_url` | Permalink to the source line on GitHub. |

## Considerations and Limitations

- Annotations are written and curated by a single maintainer; they summarize each resource and are not the authors' own abstracts.
- URLs are third-party and can rot; `data/resource_source_audit.csv` carries a retrieval-time reachability snapshot, but it is a point-in-time check, not a live guarantee.
- `row_id` and `source_line` are positional and change when the README is reordered; join on `url` for anything durable.
- Coverage skews toward English-language, publicly available resources.

## Changelog

Versioned changes are published as GitHub Releases: https://github.com/ChaoYue0307/awesome-loop-engineering/releases

## Citation

```bibtex
@misc{chaoyue2026awesome_loop_engineering,
  author       = {He, Chaoyue},
  title        = {Awesome Loop Engineering},
  year         = {2026},
  howpublished = {\url{https://github.com/ChaoYue0307/awesome-loop-engineering}}
}
```
