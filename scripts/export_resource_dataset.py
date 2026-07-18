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
SITE_JSON_PATH = ROOT / "docs" / "assets" / "resources.json"
AUDIT_PATH = ROOT / "data" / "resource_source_audit.csv"
FIRST_SEEN_PATH = ROOT / "data" / "first_seen.json"
SOURCE_URL = "https://github.com/ChaoYue0307/awesome-loop-engineering/blob/main/README.md"
PROJECT_GITHUB_REPO = "chaoyue0307/awesome-loop-engineering"


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
TABLE_ENTRY_RE = re.compile(
    r"^\| (?P<marker>\S+) \*\*\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\*\*"
    r"<br><sub>(?P<resource_type>[^<]+)</sub>\s+\| (?P<metadata>.*?) \| "
    r"(?P<annotation>.*?) \| (?P<table_evidence>.+) \|$"
)
LEGACY_TABLE_ENTRY_RE = re.compile(
    r"^\| (?P<marker>\S+) \*\*\[(?P<title>[^\]]+)\]\((?P<url>[^)]+)\)\*\*"
    r"<br><sub>(?P<resource_type>[^<]+)</sub>\s+\| (?P<metadata>.*?) \| "
    r"(?P<annotation>.+) \|$"
)
HEADING_RE = re.compile(r"^(?P<level>#{2,3}) (?P<title>.+)$")
NON_SLUG_RE = re.compile(r"[^a-z0-9]+")

TYPE_MARKERS = {
    "Paper": "📄",
    "Blog": "📝",
    "Docs": "📚",
    "Tool": "🧰",
    "Benchmark": "🧪",
    "Pattern": "🔁",
    "Template": "🧾",
    "List": "🧭",
    "Critique": "⚠️",
}


def base_resource_type(value: str) -> str:
    cleaned = clean(value)
    return next(
        (
            resource_type
            for resource_type in TYPE_MARKERS
            if cleaned == resource_type or cleaned.startswith(f"{resource_type} ·")
        ),
        cleaned,
    )

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
    "collection",
    "collection_slug",
    "user_goal",
    "lifecycle_stages",
    "audience",
    "loop_layer",
    "scope_fit",
    "evidence_class",
    "evidence_tier",
    "source_status",
    "canonical_url",
    "source_title",
    "source_description",
    "authors",
    "publication_date",
    "publication_year",
    "publication_venue",
    "publisher",
    "doi",
    "publication_note",
    "primary_category",
    "metadata_source",
    "github_repo",
    "github_stars",
    "github_forks",
    "github_license",
    "github_created_at",
    "github_updated_at",
    "arxiv_id",
    "audited_at",
]

SITE_FIELDS = [
    "row_id",
    "title",
    "url",
    "canonical_url",
    "annotation",
    "key_contribution",
    "novelty",
    "impact",
    "signal",
    "resource_type",
    "collection",
    "user_goal",
    "section",
    "section_slug",
    "lifecycle_stages",
    "audience",
    "loop_layer",
    "scope_fit",
    "evidence_class",
    "evidence_tier",
    "signal_strength",
    "source_status",
    "authors",
    "publication_date",
    "publication_year",
    "publication_venue",
    "publisher",
    "doi",
    "publication_note",
    "primary_category",
    "metadata_source",
    "github_repo",
    "github_stars",
    "arxiv_id",
    "date_added",
]

COLLECTIONS = {
    "Concept Guides": ("Learn", "Understand the field and its boundaries."),
    "Start Here": ("Learn", "Understand the field and its boundaries."),
    "Research Foundations": ("Learn", "Understand the field and its boundaries."),
    "Model-Level Recurrence": ("Learn", "Understand how recurrent model computation can power, but not replace, a governed agent loop."),
    "Pattern Library": ("Design", "Specify a loop contract and operating pattern."),
    "Core Loop Primitives": ("Design", "Specify a loop contract and operating pattern."),
    "Agent Workflow Patterns": ("Design", "Specify a loop contract and operating pattern."),
    "Official Runtime Guides": ("Build", "Choose runtimes, tools, and delegation surfaces."),
    "Coding-Agent Loop Systems": ("Build", "Choose runtimes, tools, and delegation surfaces."),
    "Orchestration And Multi-Agent Delegation": ("Build", "Choose runtimes, tools, and delegation surfaces."),
    "State, Memory, And Context Persistence": ("Persist", "Carry context, state, and receipts across runs."),
    "Verification And Feedback Gates": ("Verify", "Gate progress with tests, evals, and evidence."),
    "Benchmarks And Evaluation": ("Verify", "Gate progress with tests, evals, and evidence."),
    "Securing Unattended Loops": ("Govern", "Bound permissions, cost, failure, and escalation."),
    "Operations Playbooks": ("Govern", "Bound permissions, cost, failure, and escalation."),
    "Critiques, Risks, And Limitations": ("Govern", "Bound permissions, cost, failure, and escalation."),
    "Templates And Patterns": ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."),
    "Examples And Schema": ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."),
    "Community Gallery": ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."),
    "Adjacent Awesome Lists": ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."),
    "Explore And Reuse": ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."),
    "Shape What Comes Next": ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."),
}

COLLECTION_IMPACT = {
    "Learn": "understand the evidence, vocabulary, and lineage behind recurring agent systems",
    "Design": "turn a recurring-agent idea into an explicit loop contract",
    "Build": "choose an implementation surface for repeatable agent work",
    "Persist": "carry context, state, and receipts across runs and failures",
    "Verify": "measure progress and gate completion with repeatable evidence",
    "Govern": "bound risk before recurring or unattended execution",
    "Apply": "reuse a concrete artifact or connect it to the wider ecosystem",
}

SECTION_STAGE_DEFAULTS = {
    "Concept Guides": ["whole-loop"],
    "Start Here": ["whole-loop"],
    "Pattern Library": ["whole-loop"],
    "Research Foundations": ["whole-loop"],
    "Model-Level Recurrence": ["act"],
    "Official Runtime Guides": ["workspace", "context", "delegation", "state"],
    "Agent Workflow Patterns": ["delegation", "verification"],
    "Coding-Agent Loop Systems": ["workspace", "delegation", "verification", "state"],
    "Verification And Feedback Gates": ["verification"],
    "Securing Unattended Loops": ["workspace", "budget", "escalation"],
    "State, Memory, And Context Persistence": ["context", "state"],
    "Orchestration And Multi-Agent Delegation": ["delegation", "state"],
    "Benchmarks And Evaluation": ["verification"],
    "Operations Playbooks": ["trigger", "intake", "budget", "escalation", "exit"],
    "Critiques, Risks, And Limitations": ["budget", "escalation", "exit"],
    "Templates And Patterns": ["whole-loop"],
    "Examples And Schema": ["whole-loop"],
    "Community Gallery": ["whole-loop"],
}

STAGE_RULES = [
    ("objective", r"\bobjective(?:s)?\b|\bgoal(?:s)?\b|success criteria"),
    ("trigger", r"\btrigger(?:s|ed)?\b|\bschedul(?:e|ed|ing)\b|\bcadence\b|\bcron\b|\bevent-driven\b"),
    ("intake", r"\bintake\b|\bqueue(?:s)?\b|\bdiscover(?:y|s|ed)?\b|\btriage\b|\bissue(?:s)?\b"),
    ("workspace", r"\bworkspace(?:s)?\b|\bworktree(?:s)?\b|\bsandbox(?:es|ed|ing)?\b|\bpermission(?:s)?\b|\btool(?:s)?\b"),
    ("context", r"\bcontext\b|\bmemory\b|\bmemories\b|\bretrieval\b|\bdocument(?:s)?\b"),
    ("delegation", r"\bdelegat(?:e|es|ed|ion)\b|\bmulti-agent\b|\bsubagent(?:s)?\b|\bhandoff(?:s)?\b|\borchestrat(?:e|es|ed|ion|or|ors)\b"),
    ("verification", r"\bverif(?:y|ies|ied|ication)\b|\beval(?:s|uation)?\b|\btest(?:s|ed|ing)?\b|\bbenchmark(?:s)?\b|\bgrader(?:s)?\b|\bcritic(?:s)?\b"),
    ("state", r"\bstate(?:ful)?\b|\bpersist(?:s|ed|ence|ent)?\b|\bcheckpoint(?:s|ed|ing)?\b|\breplay\b|\breceipt(?:s)?\b"),
    ("budget", r"\bbudget(?:s)?\b|\bcost(?:s)?\b|\btoken(?:s)?\b|\bretr(?:y|ies)\b|\btimeout(?:s)?\b"),
    ("escalation", r"\bescalat(?:e|es|ed|ion)\b|\bhuman(?:-in-the-loop)?\b|\bapproval(?:s)?\b|\bhandoff\b"),
    ("exit", r"\bexit\b|\bstop(?:s|ped|ping)?\b|\bcompletion\b|\bdone\b|\btermination\b"),
]

OFFICIAL_DOC_DOMAINS = {
    "adk.dev",
    "learn.chatgpt.com",
    "code.claude.com",
    "docs.crewai.com",
    "docs.anthropic.com",
    "docs.github.com",
    "docs.langchain.com",
    "developers.openai.com",
    "learn.microsoft.com",
    "modelcontextprotocol.io",
    "opentelemetry.io",
    "openai.github.io",
    "strandsagents.com",
}

SECTION_IMPACT = {
    "Concept Guides": "Clarifies the scope, vocabulary, and boundaries of Loop Engineering for recurring, stateful, verified agent systems.",
    "Start Here": "Gives readers the origin story and first-principles framing for the new AI/coding-agent use of Loop Engineering.",
    "Core Loop Primitives": "Turns the concept into concrete loop mechanics: triggers, state, tools, worktrees, permissions, and recurring execution.",
    "Official Runtime Guides": "Anchors implementation choices in primary vendor and framework documentation instead of second-hand summaries.",
    "Research Foundations": "Connects Loop Engineering to prior work on agent loops, planning, reflection, feedback, and long-horizon autonomy.",
    "Model-Level Recurrence": "Explains the inner recurrent computation that can improve an agent's model while remaining distinct from the outer operating loop.",
    "Agent Workflow Patterns": "Shows reusable architecture patterns that compose agents, evaluators, workers, and durable workflow control.",
    "Coding-Agent Loop Systems": "Grounds the practice in real coding-agent systems, bare loops, orchestration tools, and long-running software tasks.",
    "Verification And Feedback Gates": "Identifies the feedback signals that make recurring agent work measurable, retryable, and safe to stop.",
    "Securing Unattended Loops": "Surfaces the security boundaries needed when loops ingest untrusted content or act without constant human supervision.",
    "State, Memory, And Context Persistence": "Explains how loop state survives across runs through memory, checkpointers, progress files, and context management.",
    "Orchestration And Multi-Agent Delegation": "Maps the runtimes and coordination patterns used to split loop work across specialized agents and durable workflows.",
    "Benchmarks And Evaluation": "Provides measurement targets for long-horizon, tool-using, coding, web, and terminal agents.",
    "Operations Playbooks": "Collects practitioner workflows for running agents as delegated work systems rather than isolated prompts.",
    "Templates And Patterns": "Provides reusable artifacts that builders can adapt into loop specs, resources, and examples.",
    "Examples And Schema": "Makes the loop contract executable and portable through validated JSON examples and runnable reference loops.",
    "Community Gallery": "Gives contributors a format for publishing real or anonymized loop cases with receipts and lessons learned.",
    "Explore And Reuse": "Makes the evidence browsable, queryable, and reusable across interactive and machine-readable formats.",
    "Shape What Comes Next": "Connects open questions, planned work, community feedback, and operating case studies.",
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
    "Templates And Patterns": "Turns the concept into reusable specifications, checklists, and operating patterns.",
    "Examples And Schema": "Makes loop contracts portable and validation-friendly through concrete examples.",
    "Community Gallery": "Turns loop adoption into shareable cases with enough structure to compare lessons learned.",
    "Explore And Reuse": "Turns the evidence into an interactive atlas and structured data.",
    "Shape What Comes Next": "Turns open questions and operating lessons into visible next work.",
    "Pattern Library": "Turns common recurring-agent jobs into named patterns with gates, budgets, and escalation paths.",
    "Critiques, Risks, And Limitations": "Keeps adoption grounded in known failure modes, economics, and operational limits.",
    "Adjacent Awesome Lists": "Connects neighboring ecosystems while preserving Loop Engineering as a narrower operating concept.",
    "Model-Level Recurrence": "Separates shared-block latent iteration inside one model inference from repeated, externally governed agent work.",
}

SECTION_LOOP_LAYERS = {
    "Concept Guides": "cross-layer",
    "Start Here": "cross-layer",
    "Pattern Library": "workflow",
    "Core Loop Primitives": "workflow",
    "Official Runtime Guides": "harness",
    "Research Foundations": "cross-layer",
    "Model-Level Recurrence": "model",
    "Agent Workflow Patterns": "workflow",
    "Coding-Agent Loop Systems": "agent",
    "Verification And Feedback Gates": "harness",
    "Securing Unattended Loops": "operations",
    "State, Memory, And Context Persistence": "harness",
    "Orchestration And Multi-Agent Delegation": "workflow",
    "Benchmarks And Evaluation": "evaluation",
    "Operations Playbooks": "operations",
    "Templates And Patterns": "workflow",
    "Examples And Schema": "workflow",
    "Community Gallery": "operations",
    "Critiques, Risks, And Limitations": "cross-layer",
    "Adjacent Awesome Lists": "cross-layer",
    "Explore And Reuse": "cross-layer",
    "Shape What Comes Next": "cross-layer",
}

TITLE_LOOP_LAYERS = {
    "Awesome Loop Models": "model",
}

DIRECT_SCOPE_SECTIONS = {
    "Concept Guides",
    "Start Here",
    "Pattern Library",
    "Core Loop Primitives",
    "Coding-Agent Loop Systems",
    "Operations Playbooks",
    "Templates And Patterns",
    "Examples And Schema",
    "Community Gallery",
}

ADJACENT_SCOPE_SECTIONS = {"Model-Level Recurrence", "Adjacent Awesome Lists"}

TYPE_SIGNAL = {
    "Paper": ("Research paper or preprint; strongest signal when the entry contributes a method, benchmark, measurement, or formal framing.", "high"),
    "Docs": ("Primary documentation from a platform, SDK, standard, or framework; strong implementation signal.", "high"),
    "Tool": ("Working implementation, framework, runtime, or repository; signal comes from usable code and ecosystem adoption.", "high"),
    "Benchmark": ("Evaluation artifact or leaderboard; signal comes from measurable tasks and repeatable scoring.", "high"),
    "Pattern": ("Operational pattern or playbook; signal comes from reusable loop structure and practical transferability.", "medium"),
    "Template": ("Reusable template, schema, checklist, or guide; signal comes from concrete adaptation and validation.", "medium"),
    "Blog": ("Practitioner essay or field note; signal comes from concrete experience, framing, examples, or adoption discussion.", "contextual"),
    "Critique": ("Risk or limitation analysis; signal comes from boundary conditions, failure modes, and adoption cautions.", "contextual"),
    "List": ("Adjacent directory or reading list; signal comes from ecosystem coverage rather than a single technical claim.", "contextual"),
}

EVIDENCE_TIERS = {
    "research-paper": "A",
    "research-preprint": "A",
    "official-documentation": "A",
    "technical-documentation": "A",
    "source-implementation": "A",
    "implementation": "A",
    "benchmark": "A",
    "repository-native": "A",
    "reusable-artifact": "A",
    "operational-pattern": "B",
    "practitioner-analysis": "B",
    "risk-analysis": "B",
    "curated-index": "C",
    "curated-source": "C",
}

NOVELTY_RULES = [
    (r"\bofficial\b|\bprimary-source\b", "Primary-source operational guidance rather than commentary."),
    (r"\bfuture directions?\b|\bresearch agenda\b", "Turns open gaps into measurable research, infrastructure, and product directions."),
    (r"\bdurable\b|\breplay\b", "Durable execution and replay are treated as first-class loop infrastructure."),
    (r"\bcheckpoint(?:ing|ed|s)?\b", "Checkpointed state makes long-running agent work recoverable across failures."),
    (r"\bworktree(?:s)?\b", "Workspace isolation is part of the loop design, not an afterthought."),
    (r"\bdataset\b|\bresources\.csv\b|\bresources\.jsonl\b", "Packages the evidence as queryable CSV and JSONL rather than only a rendered page."),
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


def parse_entry_line(raw_line: str) -> dict[str, str] | None:
    """Parse the legacy list syntax or the current tabular resource-row syntax."""
    match = ENTRY_RE.match(raw_line)
    if match:
        return match.groupdict()

    match = TABLE_ENTRY_RE.match(raw_line) or LEGACY_TABLE_ENTRY_RE.match(raw_line)
    if not match:
        return None

    entry = match.groupdict()
    for field in ("title", "url", "annotation"):
        entry[field] = entry[field].replace(r"\|", "|")
    return entry


def classify_url(url: str) -> tuple[str, str]:
    parsed = urlparse(url)
    if parsed.scheme in {"http", "https"}:
        return "external", parsed.netloc.lower()
    if url.startswith("#"):
        return "local_anchor", ""
    return "local_path", ""


def publication_source(
    url: str,
    url_kind: str,
    domain: str,
    audit: dict[str, str],
) -> tuple[str, str]:
    """Return the original publishing surface without using this project as a venue."""
    if url_kind != "external":
        return "GitHub", "GitHub"

    github_repo = audit.get("github_repo", "").lower()
    if github_repo == PROJECT_GITHUB_REPO:
        path = urlparse(url).path.lower()
        if "/releases" in path:
            return "GitHub Releases", "GitHub"
        if "/discussions" in path:
            return "GitHub Discussions", "GitHub"
        return "GitHub", "GitHub"

    venue = audit.get("publication_venue", "")
    publisher = audit.get("publisher", "") or domain or "Source not stated"
    return venue, publisher


def load_audit() -> dict[str, dict[str, str]]:
    if not AUDIT_PATH.exists():
        return {}
    with AUDIT_PATH.open(encoding="utf-8", newline="") as handle:
        return {row["url"]: row for row in csv.DictReader(handle)}


AUDIT_BY_URL = load_audit()


def key_contribution(annotation: str) -> str:
    return clean(annotation).rstrip(".") + "."


def novelty(section: str, title: str, annotation: str) -> str:
    if section == "Concept Guides":
        lens = "Makes an otherwise informal practice concrete and reusable."
        return f"{lens} {key_contribution(annotation)}"

    if section == "Model-Level Recurrence":
        lens = "Reuses learned computation inside one model inference rather than repeating a full agent run."
        return f"{lens} {key_contribution(annotation)}"

    text = f"{title} {annotation}".lower()
    for pattern, phrase in NOVELTY_RULES:
        if re.search(pattern, text):
            return f"{phrase} {key_contribution(annotation)}"

    if section in {"Concept Guides", "Templates And Patterns", "Examples And Schema"}:
        lens = "Makes an otherwise informal practice concrete and reusable."
    elif section == "Research Foundations":
        lens = "Connects Loop Engineering to prior agent-loop and feedback-loop research."
    else:
        lens = SECTION_NOVELTY.get(section, "Contributes a distinct loop-engineering angle beyond a generic agent resource.")
    return f"{lens} {key_contribution(annotation)}"


def collection_for(section: str) -> tuple[str, str]:
    return COLLECTIONS.get(section, ("Apply", "Reuse, adapt, and contribute concrete loop artifacts."))


def lifecycle_stages(section: str, title: str, annotation: str) -> str:
    text = f"{title} {annotation}".lower()
    stages = [stage for stage, pattern in STAGE_RULES if re.search(pattern, text)]
    if section == "Model-Level Recurrence" and "act" not in stages:
        stages.insert(0, "act")
    if not stages:
        stages = SECTION_STAGE_DEFAULTS.get(section, ["whole-loop"])
    return ";".join(dict.fromkeys(stages))


def audience_for(section: str, resource_type: str) -> str:
    audiences: list[str] = []
    if section in {"Concept Guides", "Start Here"}:
        audiences.append("newcomer")
    if resource_type in {"Docs", "Tool", "Pattern", "Template"}:
        audiences.append("builder")
    if resource_type in {"Paper", "Benchmark"}:
        audiences.extend(["researcher", "evaluator"])
    if section == "Model-Level Recurrence":
        audiences.extend(["model-builder", "agent-builder"])
    if section in {"Securing Unattended Loops", "Operations Playbooks", "Critiques, Risks, And Limitations"}:
        audiences.extend(["operator", "security"])
    if section in {"Verification And Feedback Gates", "Benchmarks And Evaluation"}:
        audiences.append("evaluator")
    if section in {"Templates And Patterns", "Examples And Schema", "Community Gallery"}:
        audiences.extend(["builder", "operator"])
    return ";".join(dict.fromkeys(audiences or ["builder"]))


def evidence_class(
    section: str,
    resource_type: str,
    domain: str,
    url_kind: str,
    audit: dict[str, str],
) -> str:
    if url_kind != "external":
        return "repository-native"
    if resource_type == "Benchmark":
        return "benchmark"
    if resource_type == "Docs" and (section == "Official Runtime Guides" or domain in OFFICIAL_DOC_DOMAINS):
        return "official-documentation"
    if domain == "arxiv.org":
        venue = audit.get("publication_venue", "").strip().lower()
        publisher = audit.get("publisher", "").strip().lower()
        return "research-preprint" if venue in {"", "arxiv"} or publisher == "arxiv" else "research-paper"
    if domain == "github.com" and resource_type == "Tool":
        return "source-implementation"
    return {
        "Paper": "research-paper",
        "Docs": "technical-documentation",
        "Tool": "implementation",
        "Pattern": "operational-pattern",
        "Template": "reusable-artifact",
        "Blog": "practitioner-analysis",
        "Critique": "risk-analysis",
        "List": "curated-index",
    }.get(resource_type, "curated-source")


def loop_layer(section: str, title: str) -> str:
    return TITLE_LOOP_LAYERS.get(title, SECTION_LOOP_LAYERS.get(section, "cross-layer"))


def scope_fit(section: str) -> str:
    if section in ADJACENT_SCOPE_SECTIONS:
        return "adjacent"
    if section in DIRECT_SCOPE_SECTIONS:
        return "direct"
    return "enabling"


def impact(collection: str, section: str, title: str) -> str:
    if section == "Model-Level Recurrence":
        return f"Use {title} to assess inner latent computation as a model capability inside a separately governed agent loop."
    goal = COLLECTION_IMPACT.get(collection, "apply the source to a recurring agent system")
    return f"Use {title} to {goal}."


def evidence_tier(evidence: str) -> str:
    return EVIDENCE_TIERS.get(evidence, "C")


def format_count(value: str) -> str:
    try:
        return f"{int(value):,}"
    except (TypeError, ValueError):
        return ""


def signal(
    resource_type: str,
    domain: str,
    url_kind: str,
    evidence: str,
    audit: dict[str, str],
) -> tuple[str, str]:
    status = audit.get("audit_status", "")
    if status in {"broken", "unreachable", "local_missing"}:
        return "The linked source was unavailable at the latest check; treat its claims and availability as unverified.", "unverified"
    if url_kind != "external":
        return "Repository file; inspect the linked schema, example, guide, or implementation.", "medium"
    if evidence == "official-documentation":
        return f"Primary official documentation from {domain}; use it for current product or standard behavior.", "high"
    if evidence in {"research-preprint", "research-paper"}:
        arxiv_id = audit.get("arxiv_id", "")
        identifier = f" arXiv:{arxiv_id}" if arxiv_id else ""
        return f"Research source{identifier}; inspect its method and evaluation before treating results as production evidence.", "medium"
    if evidence == "benchmark":
        return "Benchmark or leaderboard source with repeatable tasks or scores; compare systems only after checking setup and scope.", "high"
    if domain == "github.com":
        stars = format_count(audit.get("github_stars", ""))
        forks = format_count(audit.get("github_forks", ""))
        license_id = audit.get("github_license", "")
        updated = audit.get("github_updated_at", "")[:10]
        facts = []
        if stars:
            facts.append(f"{stars} stars")
        if forks:
            facts.append(f"{forks} forks")
        if license_id:
            facts.append(f"{license_id} license")
        if updated:
            facts.append(f"updated {updated}")
        detail = f" ({'; '.join(facts)})" if facts else ""
        return f"Inspectable GitHub source{detail}; popularity is context, not proof of reliability.", "medium"
    if evidence in {"practitioner-analysis", "risk-analysis", "curated-index"}:
        return f"Contextual source from {domain}; useful for practice signals or boundary conditions, not independent validation.", "contextual"
    return TYPE_SIGNAL.get(resource_type, (f"Background source from {domain}; verify fit against the linked artifact.", "contextual"))


def iter_rows(readme_path: Path = README) -> list[dict[str, str]]:
    section = ""
    section_slug = ""
    rows: list[dict[str, str]] = []

    for line_number, raw_line in enumerate(readme_path.read_text(encoding="utf-8").splitlines(), 1):
        heading = HEADING_RE.match(raw_line)
        if heading:
            if heading.group("level") == "##":
                section = clean(heading.group("title"))
                section_slug = slugify(section)
            continue

        entry = parse_entry_line(raw_line)
        if not entry:
            continue

        url = clean(entry["url"])
        if "example.com" in url:
            continue

        url_kind, domain = classify_url(url)
        annotation = clean(entry["annotation"])
        resource_type = base_resource_type(entry["resource_type"])
        row_number = len(rows) + 1
        row_id = f"ale-{row_number:04d}"
        collection, user_goal = collection_for(section)
        audit = AUDIT_BY_URL.get(url, {})
        evidence = evidence_class(section, resource_type, domain, url_kind, audit)
        signal_text, signal_strength = signal(resource_type, domain, url_kind, evidence, audit)
        publication_venue, publisher = publication_source(url, url_kind, domain, audit)
        rows.append(
            {
                "row_id": row_id,
                "section": section,
                "section_slug": section_slug,
                "resource_type": resource_type,
                "marker": clean(entry["marker"]),
                "title": clean(entry["title"]),
                "url": url,
                "url_kind": url_kind,
                "domain": domain,
                "annotation": annotation,
                "description": annotation,
                "key_contribution": key_contribution(annotation),
                "novelty": novelty(section, clean(entry["title"]), annotation),
                "impact": impact(collection, section, clean(entry["title"])),
                "signal": signal_text,
                "signal_strength": signal_strength,
                "source_readme": "README.md",
                "source_line": line_number,
                "source_url": f"{SOURCE_URL}#L{line_number}",
                "date_added": FIRST_SEEN.get(url, ""),
                "collection": collection,
                "collection_slug": slugify(collection),
                "user_goal": user_goal,
                "lifecycle_stages": lifecycle_stages(section, clean(entry["title"]), annotation),
                "audience": audience_for(section, resource_type),
                "loop_layer": loop_layer(section, clean(entry["title"])),
                "scope_fit": scope_fit(section),
                "evidence_class": evidence,
                "evidence_tier": evidence_tier(evidence),
                "source_status": audit.get("audit_status", "not-audited"),
                "canonical_url": audit.get("canonical_url", "") or audit.get("final_url", "") or url,
                "source_title": audit.get("source_title", ""),
                "source_description": audit.get("source_description", ""),
                "authors": audit.get("authors", ""),
                "publication_date": audit.get("publication_date", ""),
                "publication_year": audit.get("publication_year", ""),
                "publication_venue": publication_venue,
                "publisher": publisher,
                "doi": audit.get("doi", ""),
                "publication_note": audit.get("publication_note", ""),
                "primary_category": audit.get("primary_category", ""),
                "metadata_source": audit.get("metadata_source", "not-audited"),
                "github_repo": audit.get("github_repo", ""),
                "github_stars": audit.get("github_stars", ""),
                "github_forks": audit.get("github_forks", ""),
                "github_license": audit.get("github_license", ""),
                "github_created_at": audit.get("github_created_at", ""),
                "github_updated_at": audit.get("github_updated_at", ""),
                "arxiv_id": audit.get("arxiv_id", ""),
                "audited_at": audit.get("retrieved_at", ""),
            }
        )

    if not rows:
        raise RuntimeError(f"No resource entries found in {readme_path}")

    return rows


def write_outputs(rows: list[dict[str, str]], csv_path: Path, jsonl_path: Path, site_json_path: Path) -> None:
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=False))
            handle.write("\n")

    site_json_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "count": len(rows),
        "resources": [{field: row[field] for field in SITE_FIELDS} for row in rows],
    }
    site_json_path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def check_outputs(rows: list[dict[str, str]]) -> int:
    with TemporaryDirectory() as temp_dir:
        temp = Path(temp_dir)
        expected_csv = temp / "resources.csv"
        expected_jsonl = temp / "resources.jsonl"
        expected_site_json = temp / "resources.json"
        write_outputs(rows, expected_csv, expected_jsonl, expected_site_json)

        failures = []
        for expected, actual in [
            (expected_csv, CSV_PATH),
            (expected_jsonl, JSONL_PATH),
            (expected_site_json, SITE_JSON_PATH),
        ]:
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

    write_outputs(rows, CSV_PATH, JSONL_PATH, SITE_JSON_PATH)
    print(
        f"Wrote {len(rows)} rows to {CSV_PATH.relative_to(ROOT)}, "
        f"{JSONL_PATH.relative_to(ROOT)}, and {SITE_JSON_PATH.relative_to(ROOT)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
