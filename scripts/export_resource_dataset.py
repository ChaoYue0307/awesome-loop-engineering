#!/usr/bin/env python3
"""Export README resource entries as tabular dataset files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CSV_PATH = ROOT / "data" / "resources.csv"
JSONL_PATH = ROOT / "data" / "resources.jsonl"
FIRST_SEEN_PATH = ROOT / "data" / "first_seen.json"
SOURCE_URL = "https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/README.md"


def load_first_seen() -> dict[str, str]:
    """url -> ISO date the entry was first added. Forward-only; empty for entries
    that predate per-entry date tracking (which began 2026-07-15)."""
    if FIRST_SEEN_PATH.exists():
        return json.loads(FIRST_SEEN_PATH.read_text(encoding="utf-8"))
    return {}


FIRST_SEEN = load_first_seen()

ENTRY_RE = re.compile(
    r"^- (?P<marker>\S+) \*\*(?P<resource_type>[^*]+)\*\* "
    r"\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\) - (?P<annotation>.+)$"
)
HEADING_RE = re.compile(r"^(?P<level>#{2,3}) (?P<title>.+)$")
NON_SLUG_RE = re.compile(r"[^a-z0-9]+")

FIELDS = [
    "row_id",
    "section",
    "section_slug",
    "resource_type",
    "marker",
    "title",
    "url",
    "url_kind",
    "domain",
    "annotation",
    "description",
    "key_contribution",
    "novelty",
    "impact",
    "signal",
    "signal_strength",
    "source_readme",
    "source_line",
    "source_url",
    "date_added",
]

SECTION_IMPACT = {
    "Concept Guides": "Clarifies the scope, vocabulary, and boundaries of Loop Engineering so the list does not drift into generic agent material.",
    "Start Here": "Gives readers the origin story and first-principles framing for the new AI/coding-agent use of Loop Engineering.",
    "Core Loop Primitives": "Turns the concept into concrete loop mechanics: triggers, state, tools, worktrees, permissions, and recurring execution.",
    "Official Runtime Guides": "Anchors implementation choices in primary vendor and framework documentation instead of second-hand summaries.",
    "Research Foundations": "Connects Loop Engineering to prior work on agent loops, planning, reflection, feedback, and long-horizon autonomy.",
    "Agent Workflow Patterns": "Shows reusable architecture patterns that compose agents, evaluators, workers, and durable workflow control.",
    "Coding-Agent Loop Systems": "Grounds the practice in real coding-agent systems, bare loops, orchestration tools, and long-running software tasks.",
    "Verification And Feedback Gates": "Identifies the feedback signals that make recurring agent work measurable, retryable, and safe to stop.",
    "Securing Unattended Loops": "Surfaces the security boundaries needed when loops ingest untrusted content or act without constant human supervision.",
    "State, Memory, And Context Persistence": "Explains how loop state survives across runs through memory, checkpointers, progress files, and context management.",
    "Orchestration And Multi-Agent Delegation": "Maps the runtimes and coordination patterns used to split loop work across specialized agents and durable workflows.",
    "Benchmarks And Evaluation": "Provides measurement targets for long-horizon, tool-using, coding, web, and terminal agents.",
    "Operations Playbooks": "Collects practitioner workflows for running agents as delegated work systems rather than isolated prompts.",
    "Templates And Patterns": "Provides reusable repository-native artifacts that contributors can adapt into loop specs, resources, and examples.",
    "Examples And Schema": "Makes the loop contract executable and portable through validated JSON examples and runnable reference loops.",
    "Community Gallery": "Gives contributors a format for publishing real or anonymized loop cases with receipts and lessons learned.",
    "Discovery And Distribution": "Documents how the project itself is packaged, indexed, mirrored, and made discoverable.",
    "Roadmap And Discussion": "Keeps future work, community feedback, and pattern submissions visible.",
    "Pattern Library": "Translates the abstract loop contract into operational patterns with triggers, gates, budgets, and escalation paths.",
    "Critiques, Risks, And Limitations": "Preserves cautionary evidence so adoption stays proportional to task risk, signal quality, and economics.",
    "Adjacent Awesome Lists": "Connects readers to neighboring ecosystems while keeping Loop Engineering's scope distinct.",
}

SECTION_NOVELTY = {
    "Start Here": "Captures the early community framing of Loop Engineering as repeated agent delegation rather than prompt craft.",
    "Core Loop Primitives": "Breaks loop design into operational primitives that can be combined across agents and runtimes.",
    "Official Runtime Guides": "Shows how production platforms expose loops through concrete tools, permissions, skills, agents, and automation features.",
    "Agent Workflow Patterns": "Distills reusable agent-control patterns that are not tied to a single vendor implementation.",
    "Coding-Agent Loop Systems": "Uses real automated software-engineering systems as evidence for practical loop architectures.",
    "Verification And Feedback Gates": "Treats feedback, telemetry, and deterministic artifacts as loop-control gates.",
    "Securing Unattended Loops": "Frames security as a recurring-loop boundary rather than a one-time prompt hygiene issue.",
    "State, Memory, And Context Persistence": "Makes persistence and context management visible as runtime design choices.",
    "Orchestration And Multi-Agent Delegation": "Shows how delegation, handoff, and workflow control turn one agent into a coordinated loop.",
    "Benchmarks And Evaluation": "Links loop design to measurable tasks where progress and failure can be compared.",
    "Operations Playbooks": "Translates agent-loop ideas into operator-facing workflows for repeated delegated work.",
    "Templates And Patterns": "Provides reusable repository-native artifacts rather than leaving the concept as prose.",
    "Examples And Schema": "Makes loop contracts portable and validation-friendly through concrete examples.",
    "Community Gallery": "Turns loop adoption into shareable cases with enough structure to compare lessons learned.",
    "Discovery And Distribution": "Makes the project discoverable as both documentation and machine-readable data.",
    "Roadmap And Discussion": "Keeps community evolution and evidence gathering part of the project surface.",
    "Pattern Library": "Turns common recurring-agent jobs into named patterns with gates, budgets, and escalation paths.",
    "Critiques, Risks, And Limitations": "Keeps adoption grounded in known failure modes, economics, and operational limits.",
    "Adjacent Awesome Lists": "Connects neighboring ecosystems while preserving Loop Engineering as a narrower operating concept.",
}

TYPE_SIGNAL = {
    "Paper": ("Research paper or preprint; strongest signal when the entry contributes a method, benchmark, measurement, or formal framing.", "high"),
    "Docs": ("Primary documentation from a platform, SDK, standard, or framework; strong implementation signal.", "high"),
    "Tool": ("Working implementation, framework, runtime, or repository; signal comes from usable code and ecosystem adoption.", "high"),
    "Benchmark": ("Evaluation artifact or leaderboard; signal comes from measurable tasks and repeatable scoring.", "high"),
    "Pattern": ("Operational pattern or playbook; signal comes from reusable loop structure and practical transferability.", "medium"),
    "Template": ("Repository-native template, schema, checklist, or guide; signal comes from reuse inside this project.", "medium"),
    "Blog": ("Practitioner essay or field note; signal comes from concrete experience, framing, examples, or adoption discussion.", "contextual"),
    "Critique": ("Risk or limitation analysis; signal comes from boundary conditions, failure modes, and adoption cautions.", "contextual"),
    "List": ("Adjacent curated collection; signal comes from ecosystem coverage rather than a single technical claim.", "contextual"),
}

NOVELTY_RULES = [
    (r"\bofficial\b|\bprimary-source\b", "Primary-source operational guidance rather than commentary."),
    (r"\bdurable\b|\breplay\b", "Durable execution and replay are treated as first-class loop infrastructure."),
    (r"\bcheckpoint(?:ing|ed|s)?\b", "Checkpointed state makes long-running agent work recoverable across failures."),
    (r"\bworktree(?:s)?\b", "Workspace isolation is part of the loop design, not an afterthought."),
    (r"\bdataset\b|\bresources\.csv\b|\bresources\.jsonl\b", "The list is made machine-readable as a tabular dataset rather than only a Markdown page."),
    (r"\bdag(?:s)?\b|\bgraph(?:s)?\b", "Control flow is represented as an inspectable graph rather than an opaque prompt loop."),
    (r"\bschedule(?:d|s)?\b|\bscheduling\b|\bcadence\b", "The trigger or cadence is explicit, making the workflow recurring rather than one-off."),
    (r"\bself-verification\b|\bself-verifying\b", "The agent workflow includes explicit self-checking or gated completion."),
    (r"\bverification\b|\bverifier\b|\bverified\b", "Verification is promoted from a final check to a loop-control signal."),
    (r"\beval(?:s|uation)?\b|\bgrader(?:s)?\b", "Evaluation data is used as the feedback signal for improving loop behavior."),
    (r"\bbenchmark(?:s)?\b|\bleaderboard\b", "The work turns loop quality into a measurable task or score."),
    (r"\bmemory\b|\bmemories\b", "Persistent memory is treated as an external runtime artifact."),
    (r"\bcontext\b|\bcontext-window\b", "Context is managed as durable loop state rather than a single prompt payload."),
    (r"\bmulti-agent\b|\bsubagent(?:s)?\b", "The work separates roles across agents, verifiers, or orchestration layers."),
    (r"\borchestrat(?:e|es|ed|ion|or|ors)\b", "Orchestration and control flow are made explicit and inspectable."),
    (r"\bsandbox(?:es|ed|ing)?\b", "Execution isolation and permission boundaries are part of the design."),
    (r"\bprompt injection\b|\buntrusted\b", "Untrusted intake is treated as a loop-level security boundary."),
    (r"\blong-horizon\b|\bmulti-hour\b|\bcontext window(?:s)?\b", "The work targets tasks that exceed a single context window or prompt session."),
    (r"\bstate\b|\bstateful\b|\bpersist(?:s|ed|ent|ence)?\b", "State persistence is explicit enough for repeated runs and handoff."),
    (r"\bschema\b|\bjson\b|\bmachine-readable\b", "The contribution is machine-readable and validation-friendly."),
    (r"\btemplate\b|\bchecklist\b|\bguide\b", "The resource is directly reusable as a starting artifact."),
]


def slugify(value: str) -> str:
    slug = NON_SLUG_RE.sub("-", value.lower()).strip("-")
    return slug or "section"


def clean(value: str) -> str:
    return " ".join(value.strip().split())


def classify_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return "external", parsed.netloc.lower()
    if url.startswith("#"):
        return "local_anchor", ""
    return "local_path", ""


def key_contribution(resource_type: str, annotation: str) -> str:
    lead = clean(annotation).rstrip(".")
    if resource_type in {"Paper", "Blog", "Docs"}:
        return lead + "."
    if resource_type == "Tool":
        return f"Provides an implementation surface for loop builders: {lead}."
    if resource_type == "Benchmark":
        return f"Provides an evaluation signal for loop builders: {lead}."
    if resource_type == "Pattern":
        return f"Provides a reusable loop pattern: {lead}."
    if resource_type == "Template":
        return f"Provides a reusable project artifact: {lead}."
    if resource_type == "Critique":
        return f"Names a risk or boundary condition: {lead}."
    if resource_type == "List":
        return f"Maps adjacent resources and ecosystems: {lead}."
    return lead + "."


def novelty(section: str, title: str, annotation: str) -> str:
    if section == "Concept Guides":
        return "Repository-native artifact that makes an otherwise informal practice concrete and reusable."

    text = f"{title} {annotation}".lower()
    for pattern, phrase in NOVELTY_RULES:
        if re.search(pattern, text):
            return phrase

    if section in {"Concept Guides", "Templates And Patterns", "Examples And Schema"}:
        return "Repository-native artifact that makes an otherwise informal practice concrete and reusable."
    if section == "Research Foundations":
        return "Connects Loop Engineering to prior agent-loop and feedback-loop research."
    return SECTION_NOVELTY.get(section, "Contributes a distinct loop-engineering angle beyond a generic agent resource.")


def impact(section: str) -> str:
    return SECTION_IMPACT.get(section, "Supports the project goal of making recurring AI-agent systems easier to design and evaluate.")


def signal(resource_type: str, domain: str, url_kind: str) -> tuple[str, str]:
    if url_kind != "external":
        return "Repository-native artifact maintained in this project; signal comes from local validation and reuse.", "medium"
    if domain in {"developers.openai.com", "code.claude.com", "docs.github.com", "modelcontextprotocol.io", "opentelemetry.io"}:
        return "Primary official documentation for a platform, SDK, or standard.", "high"
    if domain == "arxiv.org":
        return "Research preprint with stable arXiv identifier.", "high"
    if domain == "github.com":
        return "Source repository or implementation artifact that can be inspected directly.", "high"
    return TYPE_SIGNAL.get(resource_type, ("Curated source signal based on type, section fit, and annotation specificity.", "contextual"))


def iter_rows(readme_path: Path = README) -> list[dict[str, str]]:
    section = ""
    section_slug = ""
    rows: list[dict[str, str]] = []

    for line_number, raw_line in enumerate(readme_path.read_text(encoding="utf-8").splitlines(), 1):
        heading = HEADING_RE.match(raw_line)
        if heading:
            section = clean(heading.group("title"))
            section_slug = slugify(section)
            continue

        match = ENTRY_RE.match(raw_line)
        if not match:
            continue

        url = clean(match.group("url"))
        if "example.com" in url:
            continue

        url_kind, domain = classify_url(url)
        annotation = clean(match.group("annotation"))
        resource_type = clean(match.group("resource_type"))
        signal_text, signal_strength = signal(resource_type, domain, url_kind)
        row_number = len(rows) + 1
        rows.append(
            {
                "row_id": f"ale-{row_number:04d}",
                "section": section,
                "section_slug": section_slug,
                "resource_type": resource_type,
                "marker": clean(match.group("marker")),
                "title": clean(match.group("title")),
                "url": url,
                "url_kind": url_kind,
                "domain": domain,
                "annotation": annotation,
                "description": annotation,
                "key_contribution": key_contribution(resource_type, annotation),
                "novelty": novelty(section, clean(match.group("title")), annotation),
                "impact": impact(section),
                "signal": signal_text,
                "signal_strength": signal_strength,
                "source_readme": "README.md",
                "source_line": str(line_number),
                "source_url": f"{SOURCE_URL}#L{line_number}",
                "date_added": FIRST_SEEN.get(url, ""),
            }
        )

    if not rows:
        raise RuntimeError(f"No resource entries found in {readme_path}")

    return rows


def write_outputs(rows: list[dict[str, str]], csv_path: Path, jsonl_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=False))
            handle.write("\n")


def check_outputs(rows: list[dict[str, str]]) -> int:
    with TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        expected_csv = temp / "resources.csv"
        expected_jsonl = temp / "resources.jsonl"
        write_outputs(rows, expected_csv, expected_jsonl)

        failures = []
        for expected, actual in [(expected_csv, CSV_PATH), (expected_jsonl, JSONL_PATH)]:
            if not actual.exists():
                failures.append(f"{actual.relative_to(ROOT)} is missing")
                continue
            if expected.read_text(encoding="utf-8") != actual.read_text(encoding="utf-8"):
                failures.append(f"{actual.relative_to(ROOT)} is stale; run scripts/export_resource_dataset.py")

        if failures:
            for failure in failures:
                print(failure, file=sys.stderr)
            return 1

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if generated dataset files are stale")
    args = parser.parse_args()

    rows = iter_rows()
    if args.check:
        return check_outputs(rows)

    write_outputs(rows, CSV_PATH, JSONL_PATH)
    print(f"Wrote {len(rows)} rows to {CSV_PATH.relative_to(ROOT)} and {JSONL_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
