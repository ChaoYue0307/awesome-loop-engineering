
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
| `signal_strength` | Calibrated confidence label (`high`, `medium`, `contextual`, or `unverified`). |
| `source_readme` | README file the row came from. |
| `source_line` | 1-based line number in that README. |
| `source_url` | Permalink to the source line on GitHub. |
| `date_added` | First-seen date when tracked; blank for resources added before tracking began. |
| `collection` | Task-oriented atlas group: Learn, Design, Build, Persist, Verify, Govern, or Apply. |
| `collection_slug` | Stable lowercase slug for the task-oriented collection. |
| `user_goal` | Reader outcome served by the collection. |
| `lifecycle_stages` | Semicolon-delimited Loop Contract stages addressed by the resource. |
| `audience` | Semicolon-delimited intended audiences, such as newcomer, builder, operator, evaluator, or security. |
| `evidence_class` | Source-provenance category, independent of popularity or editorial judgment. |
| `source_status` | Latest audit result: `ok`, `restricted`, `local_ok`, or an explicit failure state. |
| `canonical_url` | Redirect-resolved or repository-canonical URL used for source verification. |
| `source_title` | Title metadata retrieved during the latest source audit. |
| `source_description` | Description or abstract metadata retrieved from the primary source. |
| `authors` | Semicolon-delimited authors from primary bibliographic metadata when available. |
| `publication_date` | Primary-source publication or repository creation date in ISO format when available. |
| `publication_year` | Four-digit year derived from the verified publication date or identifier. |
| `publication_venue` | Journal, conference, repository, or named venue reported by the source. |
| `publisher` | Publishing organization or source platform; falls back to the canonical domain. |
| `doi` | Normalized DOI without a URL prefix when available. |
| `publication_note` | Primary-source journal reference, acceptance note, or publication comment when available. |
| `primary_category` | Primary arXiv category when applicable. |
| `metadata_source` | Provenance for bibliographic fields, such as `arxiv-api`, `github-api`, `html-meta`, or `domain-fallback`. |
| `github_repo` | Normalized GitHub `owner/repository` identifier where applicable. |
| `github_stars` | GitHub star count captured at audit time; context, not a reliability score. |
| `github_forks` | GitHub fork count captured at audit time. |
| `github_license` | Repository license identifier reported by GitHub where available. |
| `github_created_at` | Repository creation timestamp reported by GitHub. |
| `github_updated_at` | Latest repository update timestamp reported by GitHub. |
| `arxiv_id` | arXiv identifier extracted from a primary paper URL where applicable. |
| `audited_at` | UTC timestamp for the source metadata and availability snapshot. |

## Considerations and Limitations

- Annotations are written and curated by a single maintainer; they summarize each resource and are not the authors' own abstracts.
- URLs are third-party and can rot; `data/resource_source_audit.csv` carries a retrieval-time reachability snapshot, but it is a point-in-time check, not a live guarantee.
- `row_id` and `source_line` are positional and change when the README is reordered; join on `url` for anything durable.
- `signal_strength` is calibrated as `high`, `medium`, `contextual`, or `unverified`; GitHub stars and forks are reported only as adoption context.
- Coverage skews toward English-language, publicly available resources.

## Changelog

Versioned changes are published as [GitHub Releases](https://github.com/ChaoYue0307/awesome-loop-engineering/releases).

## Citation

```bibtex
@misc{chaoyue2026awesome_loop_engineering,
  author       = {He, Chaoyue},
  title        = {Awesome Loop Engineering},
  year         = {2026},
  howpublished = {\url{https://github.com/ChaoYue0307/awesome-loop-engineering}}
}
```
