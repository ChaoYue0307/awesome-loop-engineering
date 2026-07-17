# Accessibility Regression Loop

## Objective

Turn newly introduced accessibility failures into small, verified fixes while preserving a human review path for criteria that automation cannot judge.

## Use This When

- A web or app surface changes frequently.
- Automated accessibility checks and keyboard or screen-reader smoke tests already exist.
- The team wants evidence attached to each fix instead of a periodic audit backlog.

Do not treat an automated pass as proof of full WCAG conformance. The loop handles detectable regressions; people still judge usability, semantics, and assistive-technology behavior.

## Trigger

- Event: an accessibility check fails on a pull request or deployment preview.
- Schedule: nightly scan of high-value user journeys.
- Manual bootstrap: "repair the accessibility regression in <route or component>."

## Intake

- Failing rule, selector, route, viewport, browser, and test artifact.
- The changed diff, component ownership, design-system guidance, and prior baseline.
- Manual-test checklist for keyboard order, focus behavior, names, roles, states, contrast, motion, and zoom.

## Agents

- Reproducer: confirms the failure on the reported route and viewport.
- Fixer: changes the smallest component or token responsible.
- Verifier: reruns automated checks and the focused interaction test.
- Accessibility reviewer: handles ambiguous semantics and manual criteria.

## Workspace And Permissions

- Use a branch or worktree based on the failing commit.
- Allow component, style, test, and documentation edits within the affected surface.
- Disallow suppressing rules, hiding content from assistive technology, lowering thresholds, or rewriting shared tokens without owner review.

## Durable State

- Rule ID, route, viewport, affected users, before/after result, screenshots or trace, commands, and manual-review status.

## Loop Steps

1. Reproduce the exact failing rule and interaction.
1. Classify whether the failure is automatable, manual, or mixed.
1. Inspect the changed component and its design-system primitive.
1. Apply the smallest semantic, focus, label, contrast, motion, or target-size fix.
1. Rerun the focused check, adjacent component tests, and relevant user journey.
1. Route manual criteria to an accessibility reviewer with a concise evidence packet.
1. Persist the receipt and stop when both automated and required human gates pass.

## Verification Gates

- The original rule passes at the same route, viewport, and browser.
- Keyboard order, visible focus, accessible name, role, and state remain coherent for the affected interaction.
- No rule is disabled or threshold weakened to obtain the pass.
- Required manual checks are signed off by a named reviewer.

## Budget And Exit

- Max retries: 3 fix attempts.
- Max runtime: 90 minutes before handoff.
- Stop on verified repair, inability to reproduce, design-system conflict, or a failure that requires product judgment.

## Escalation

Escalate for ambiguous content alternatives, complex screen-reader behavior, cross-product token changes, legal conformance claims, or any fix that materially changes the user flow.

## Loop Instruction

```text
Repair the accessibility regression reported for <route/component>.
Reproduce the exact rule, browser, viewport, and interaction before editing.
Make the smallest standards-aligned fix and rerun the focused automated check plus
the keyboard/focus smoke test. Never disable a rule or hide content to obtain a pass.
Record before/after evidence and escalate manual WCAG judgments to <reviewer>.
```

## Worked Example

A navigation redesign removes visible focus from mobile menu links. The loop reproduces the failed focus test at 390 px, traces the regression to a shared outline token, patches the menu component without changing the global token, reruns the keyboard path and automated scan, and records a short video for human review.

## Failure Modes

- Equating zero automated violations with accessibility.
- Fixing one viewport while breaking another.
- Adding `aria-*` attributes that conflict with native semantics.
- Hiding problematic content from the accessibility tree.
- Skipping the manual check because the scanner is green.

## Example Contract

- [`examples/accessibility-regression-loop.json`](../examples/accessibility-regression-loop.json)

## References

- [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/) - Normative, testable accessibility criteria with both automated and human evaluation.
- [Understanding Test Rules for WCAG 2.2](https://www.w3.org/WAI/WCAG22/Understanding/understanding-act-rules.html) - Explains the role and limits of automated accessibility rules.
