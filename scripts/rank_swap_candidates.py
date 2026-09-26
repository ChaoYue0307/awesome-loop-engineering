#!/usr/bin/env python3
"""Propose README entries to retire when a new resource is swapped in.

The README is held at a fixed size, so each addition replaces an existing row. This
script only proposes; it never edits anything. A proposal is an entry whose ground is
already covered by a stronger source in the same section:

- The candidate is an external resource outside the protected sections, with
  signal_strength "contextual" (practice context rather than independent validation).
- Its nearest neighbour in the same section, by TF-IDF cosine similarity over title and
  annotation, has stronger evidence (higher signal_strength, then evidence_tier).

Similarity catches shared template wording as well as shared substance ("... Is Now
Generally Available" pairs unrelated products), so every proposal must be checked by hand
before removal and recorded with the entry that covers it. See meta/CURATION.md.
"""

from __future__ import annotations

import argparse
import collections
import csv
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESOURCES_CSV = ROOT / "data" / "resources.csv"

# Structural or deliberately curated sections whose rows are not swap candidates.
PROTECTED_SECTIONS = {
    "Model-Level Recurrence",
    "Adjacent Awesome Lists",
    "Start Here",
    "Pattern Library",
    "Concept Guides",
    "Templates And Patterns",
    "Community Gallery",
    "Explore And Reuse",
    "Shape What Comes Next",
    "Examples And Schema",
}
STRENGTH_RANK = {"contextual": 1, "medium": 2, "high": 3}
TIER_RANK = {"C": 1, "B": 2, "A": 3}
STOPWORDS = set(
    "the a an and or of to in for on with by from as is are be this that it its at into via over "
    "than not can how what when which their they them we our using use used new based".split()
)


def tokens(row: dict[str, str]) -> list[str]:
    words = re.findall(r"[a-z][a-z0-9-]{2,}", f"{row['title']} {row['annotation']}".lower())
    return [word for word in words if word not in STOPWORDS]


def tfidf_vectors(rows: list[dict[str, str]]) -> list[dict[str, float]]:
    docs = [tokens(row) for row in rows]
    document_frequency = collections.Counter(term for doc in docs for term in set(doc))
    total = len(docs)
    vectors = []
    for doc in docs:
        counts = collections.Counter(doc)
        weights = {term: (1 + math.log(n)) * math.log(total / document_frequency[term]) for term, n in counts.items()}
        norm = math.sqrt(sum(value * value for value in weights.values())) or 1.0
        vectors.append({term: value / norm for term, value in weights.items()})
    return vectors


def strength(row: dict[str, str]) -> tuple[int, int]:
    return STRENGTH_RANK.get(row["signal_strength"], 2), TIER_RANK.get(row["evidence_tier"], 2)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--limit", type=int, default=15, help="number of proposals to print")
    args = parser.parse_args()

    with RESOURCES_CSV.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    vectors = tfidf_vectors(rows)
    eligible = [i for i, row in enumerate(rows) if row["section"] not in PROTECTED_SECTIONS and row["url_kind"] == "external"]

    proposals = []
    for i in eligible:
        candidate = rows[i]
        if candidate["signal_strength"] != "contextual":
            continue
        best = None
        for j in eligible:
            neighbour = rows[j]
            if j == i or neighbour["section"] != candidate["section"] or strength(neighbour) <= strength(candidate):
                continue
            score = sum(weight * vectors[j].get(term, 0.0) for term, weight in vectors[i].items())
            if best is None or score > best[0]:
                best = (score, j)
        if best:
            proposals.append((best[0], i, best[1]))

    proposals.sort(reverse=True)
    print(f"{len(eligible)} swap-eligible rows; {len(proposals)} have a stronger same-section neighbour.")
    print("Check each by hand: high similarity can come from shared wording rather than shared ground.\n")
    for score, i, j in proposals[: args.limit]:
        candidate, neighbour = rows[i], rows[j]
        print(f"{score:.2f}  {candidate['row_id']}  {candidate['title']}")
        print(f"      {candidate['url']}")
        print(f"      covered by {neighbour['row_id']} [{neighbour['evidence_class']}, {neighbour['signal_strength']}] {neighbour['title']}")
        print(f"      section: {candidate['section']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
