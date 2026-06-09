# Security Policy

This repository is a curated documentation and resource list. It does not ship a production service, package, or runtime. Security concerns can still appear in examples, scripts, links, or contribution material.

## Please Report

- A linked resource that appears malicious or impersonates another project.
- A script or example that could cause unsafe actions if copied directly.
- Accidentally committed credentials, tokens, private URLs, or sensitive data.
- Guidance that could encourage unsafe production autonomy without approvals or escalation.

## How To Report

Open a private security advisory if GitHub offers that option for this repository. If not, open an issue with sensitive details removed and ask for a maintainer response.

Do not post secrets, private customer data, exploit details, or internal URLs in public issues or pull requests.

## Security Review Standard

Loop Engineering examples should be conservative:

- sensitive actions require human approval;
- production actions should be read-only by default unless explicitly scoped;
- credentials and secrets must never be included in examples;
- loops should have retry budgets, exit conditions, and escalation paths;
- verification should rely on concrete evidence, not only model self-assessment.
