# Maintenance Guide

This guide keeps Awesome Loop Engineering useful, stable, and trustworthy over time. For the cadence of when to run each task, see the [maintenance calendar](MAINTENANCE_CALENDAR.md).

## Weekly Checks

- Review the latest Quality workflow result.
- Run the link checker if the scheduled workflow reports failures.
- Triage new issues and PRs.
- Reject resources that do not pass the curation standard.
- Prefer replacing unstable links with primary or official sources.

## Monthly Checks

- Re-read the `Start Here` and `Best First Reads` sections for freshness.
- Check whether direct Loop Engineering sources have changed, moved, or duplicated each other.
- Review pattern documents for outdated runtime assumptions.
- Record link-check or curation evidence in the PR summary when making maintenance changes.
- Check GitHub repository topics, description, license detection, and contributors.

## Link Rot Policy

When a link fails:

1. Check whether the original source moved.
1. Prefer an official canonical URL over mirrors.
1. If the source is gone, replace it with a stronger equivalent resource.
1. If no equivalent exists, remove the entry rather than linking to an unreliable archive.
1. Keep the annotation focused on what the replacement contributes to Loop Engineering.

## Contributor Identity Policy

The public contributor list for this repository should remain owned by `ChaoYue0307`. Do not merge commits with AI-assistant co-author trailers or non-owner author/committer identities into `main`.

Before pushing to `main`, verify:

```sh
python scripts/check_commit_identity.py
```

When creating commits locally, use explicit author and committer identity:

```sh
git add <files>
PARENT="$(git rev-parse HEAD)"
TREE="$(git write-tree)"
NEW="$(GIT_AUTHOR_NAME='ChaoYue0307' GIT_AUTHOR_EMAIL='hechaoyue0307@gmail.com' GIT_COMMITTER_NAME='ChaoYue0307' GIT_COMMITTER_EMAIL='hechaoyue0307@gmail.com' git commit-tree "$TREE" -p "$PARENT" -m "Commit message")"
git update-ref refs/heads/main "$NEW" "$PARENT"
```

For a root-history rebuild, omit `-p "$PARENT"` intentionally and verify the remote contributor API after push.

## Release And Social Updates

When making a major improvement:

- keep the README opening concise;
- mention concrete changes, not vague polish;
- avoid unsupported claims such as "definitive" or "complete";
- include the cover image or ecosystem map when sharing publicly.

## Local Verification

Run these before pushing:

```sh
npx --yes awesome-lint
npx --yes markdownlint-cli2 "**/*.md"
python3 -m py_compile scripts/*.py
python3 scripts/check_license.py
python3 scripts/check_resource_labels.py README.md
python3 scripts/check_loop_contract_examples.py
python3 scripts/check_pages_metadata.py
python3 scripts/check_internal_links.py
python3 scripts/check_commit_identity.py
python3 scripts/verify_urls.py . --timeout 12 --workers 20
git diff --check
```

If local `awesome-lint` reports `Awesome list must reside in a valid git repository` because the local `origin` uses SSH without an available key, run the public check after pushing:

```sh
npx --yes awesome-lint https://github.com/ChaoYue0307/awesome-loop-engineering
```
