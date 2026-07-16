# Maintenance Calendar

A cadence for keeping Awesome Loop Engineering accurate, focused, and trustworthy. It complements the [maintenance guide](MAINTENANCE.md), which covers how each check works; this file covers when to run them.

Run the local checks in [MAINTENANCE.md](MAINTENANCE.md#local-verification) before any push. Keep the list selective: rejecting an off-scope resource is maintenance too.

## Weekly

- Review the latest Quality workflow run; if the scheduled link check failed, fix or replace the dead link.
- Triage new issues, pull requests, and discussion posts.
- Record the 14-day traffic snapshot and referral mix beside the [measurement baseline](DISTRIBUTION.md#measurement-baseline) before GitHub expires the older daily rows.
- Review candidate resources gathered during the week; add only those that pass [CURATION.md](CURATION.md) and reject the rest with a reason.
- Confirm no entry drifted off-scope into generic AI-agent, prompt, context, or harness content.
- Confirm the [Hugging Face dataset mirror](https://huggingface.co/datasets/cy0307/awesome-loop-engineering) is in parity with `main` (the daily routine syncs it; spot-check after manual pushes).

## Biweekly

- Add or upgrade one item: a new pattern, a new runnable variant, or one real or anonymized gallery case study.
- Re-read one pattern and its contract for accuracy against current runtime behavior.

## Monthly

- Publish one concise Discussions digest covering new resources, corrected annotations, patterns, contracts, and open contributor tasks.
- Refresh runtime docs: re-verify the Core Loop Primitives and Official Runtime Guides links and annotations against current product docs.
- Refresh benchmarks and evals: check that cited benchmarks, leaderboards, and eval papers are current and that links resolve.
- Stale-resource review: replace weak or superseded links with stronger primary sources; remove anything that rotted with no equivalent.
- Check repository topics, description, license detection, and the contributor list (owner-only).

## Quarterly

- Taxonomy review: confirm [TAXONOMY.md](../TAXONOMY.md) still covers how loops are being built in practice.
- Roadmap review: update [ROADMAP.md](../ROADMAP.md) with shipped work and the next pattern, gallery, and runtime priorities.
- Translation drift review: confirm each translated README still matches the canonical English overview and bump the `last-synced` markers; see [TRANSLATIONS.md](../TRANSLATIONS.md).

## Canonical Awesome Submission Status

The 30-day age requirement has passed. [`sindresorhus/awesome#4339`](https://github.com/sindresorhus/awesome/pull/4339) is open and its lint check is passing as of 2026-07-17.

- Do not open a duplicate submission.
- Respond to maintainer feedback quickly and keep changes scoped and owner-authored.
- Re-run the full preflight in [AWESOME_SUBMISSION.md](AWESOME_SUBMISSION.md#required-preflight) after any structural README change.
- If accepted, submit to adjacent directories only where the normal editorial policy permits related lists.
- Keep public claims conservative: this is an early curated field guide, not a finished standard.

## See Also

- [Maintenance guide](MAINTENANCE.md) - how each check works.
- [Curation standard](CURATION.md) - what belongs in the list.
- [Awesome submission checklist](AWESOME_SUBMISSION.md) - upstream requirements and timing.
- [Distribution checklist](DISTRIBUTION.md) - launch and outreach.
