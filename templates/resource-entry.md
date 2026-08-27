# Resource Entry Template

Use this when adding one resource to `README.md`.

```md
| 📄 **[Title](https://example.com)** | **2026** · arXiv<br><sub>First Author et al.</sub> | One sentence explaining the resource's concrete contribution, result, or limitation. | **Research preprint**<br><sub>Preprint; inspect methods and evaluation</sub> |
```

Match the evidence cell to the source. Published research, official documentation, implementation guides, reusable artifacts, benchmarks, critiques, and discovery indexes use different labels; follow the nearest row in the target section rather than copying `Research preprint` mechanically.

## Metadata To Mention In Your PR

- **Category**:
- **Source type**: Direct Loop Engineering source / paper / official docs / engineering note / tool / benchmark / critique / adjacent list
- **Resource label**: 📄 Paper / 📝 Blog / 📚 Docs / 🧰 Tool / 🧪 Benchmark / 🔁 Pattern / 🧾 Template / 🧭 List / ⚠️ Critique
- **Quality labels**: Primary source / Official docs / Implementation-heavy / Foundational / Cautionary / Adjacent
- **Evidence quality**: Tier A / B / C / D
- **Why it belongs**:
- **Primary or secondary source**:
- **Authors / organization**:
- **Publication year**:
- **Venue or source platform**:
- **DOI or arXiv ID**:
- **Any caveat**:

## Quality Bar

The entry should help readers design, run, verify, evaluate, or critique recurring agent systems that discover work, delegate to agents, coordinate context and harnesses, verify results, persist state, decide next actions, retry, and escalate. If the resource is just about agents in general, prompt writing, context stuffing, harness infrastructure, or generic automation, it probably does not belong.
