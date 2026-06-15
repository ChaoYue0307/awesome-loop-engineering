# Maintenance Calendar

A cadence for keeping Awesome Loop Engineering accurate, focused, and trustworthy. It complements the [maintenance guide](MAINTENANCE.md), which covers how each check works; this file covers when to run them.

Run the local checks in [MAINTENANCE.md](MAINTENANCE.md#local-verification) before any push. Keep the list selective: rejecting an off-scope resource is maintenance too.

## Weekly

- Review the latest Quality workflow run; if the scheduled link check failed, fix or replace the dead link.
- Triage new issues, pull requests, and discussion posts.
- Review candidate resources gathered during the week; add only those that pass [CURATION.md](CURATION.md) and reject the rest with a reason.
- Confirm no entry drifted off-scope into generic AI-agent, prompt, context, or harness content.

## Biweekly

- Add or upgrade one item: a new pattern, a new runnable variant, or one real or anonymized gallery case study.
- Re-read one pattern and its contract for accuracy against current runtime behavior.

## Monthly

- Refresh runtime docs: re-verify the Core Loop Primitives and Official Runtime Guides links and annotations against current product docs.
- Refresh benchmarks and evals: check that cited benchmarks, leaderboards, and eval papers are current and that links resolve.
- Stale-resource review: replace weak or superseded links with stronger primary sources; remove anything that rotted with no equivalent.
- Check repository topics, description, license detection, and the contributor list (owner-only).

## Quarterly

- Taxonomy review: confirm [TAXONOMY.md](../TAXONOMY.md) still covers how loops are being built in practice.
- Roadmap review: update [ROADMAP.md](../ROADMAP.md) with shipped work and the next pattern, gallery, and runtime priorities.
- Translation drift review: confirm each translated README still matches the canonical English overview and bump the `last-synced` markers; see [TRANSLATIONS.md](../TRANSLATIONS.md).

## Pre-Submission Checklist (before 2026-07-10)

The upstream Awesome 30-day rule opens the submission window on 2026-07-10. Before then:

- [ ] Run the full preflight in [AWESOME_SUBMISSION.md](AWESOME_SUBMISSION.md#required-preflight) and fix every actionable finding.
- [ ] Confirm `awesome-lint` passes locally and against the public GitHub URL.
- [ ] Confirm the README scope, contribution guide, license, and CI badge are present and current.
- [ ] Review at least four open PRs in `sindresorhus/awesome` with substantive comments.
- [ ] Draft the `Add Loop Engineering` PR title, entry (URL ending in `#readme`), and PR body.
- [ ] Confirm a tagged release and a green Quality run on `main`.

## Post-Submission Checklist (after 2026-07-10)

- [ ] Open the `sindresorhus/awesome` PR and comment `unicorn` to confirm the guidelines were read.
- [ ] Respond to maintainer feedback quickly; keep changes scoped and owner-authored.
- [ ] Once listed, add reciprocal entries on adjacent lists where appropriate, under your own identity.
- [ ] Run the distribution steps in [DISTRIBUTION.md](DISTRIBUTION.md): landing page, launch post, and author outreach.
- [ ] Keep public claims conservative: an early curated field guide, not a finished standard.

## See Also

- [Maintenance guide](MAINTENANCE.md) - how each check works.
- [Curation standard](CURATION.md) - what belongs in the list.
- [Awesome submission checklist](AWESOME_SUBMISSION.md) - upstream requirements and timing.
- [Distribution checklist](DISTRIBUTION.md) - launch and outreach.
