# Design QA

## Source

- Selected direction: `/Users/chaoyue/.codex/generated_images/019ed02c-a15f-7881-aab3-49ff394627b4/exec-e373a4be-af07-451b-937a-7cd5acbd9b12.png`
- Stack figure refresh: `/Users/chaoyue/.codex/generated_images/019ed02c-a15f-7881-aab3-49ff394627b4/exec-0e105db4-a098-48f5-b3f1-301d07cb21f6.png`
- Local prototype: repository `docs/` build served during QA
- Reference comparison: `/private/tmp/loop-design-comparison.png`

## Viewports And States

- Desktop first viewport: 1440 x 1024, page top, sticky navigation visible.
- Mobile first viewport: 390 x 844, page top, dedicated mobile mental model visible.
- Mobile navigation: menu expanded and collapsed; `aria-expanded` changed correctly.
- Pattern library: mobile, filter value `CI`, one matching pattern visible.
- Contract: mobile, first horizontal diagram position, labels readable.
- Social preview: 1280 x 640, exact resource, pattern, and contract counts.

## Comparison History

1. Compared the ChatGPT Image direction and the first implementation in one side-by-side input. The implementation preserved the light technical-field-guide palette, thin rules, flat surfaces, and restrained blue/cyan/green accents. The identity was intentionally centered to honor the repository requirement.
2. The first mobile pass scaled the desktop stack diagram too far down. This was a P2 legibility issue.
3. Added a dedicated mobile mental-model asset and horizontally inspectable contract and lifecycle diagrams. Rechecked at 390 x 844; headings, labels, controls, and section transitions are readable without overlap.
4. Tightened short-query filtering so `CI` returns the CI repair loop instead of substring matches inside unrelated words.
5. Compared the original stack figure and the ChatGPT Image revision side by side. The revision replaces empty overlapping outlines with four populated plates, aligned leader lines, a one-run bracket, and an explicit recurring-work governance badge. OCR and browser checks confirmed the required copy, 1666 x 944 dimensions, and error-free rendering.

## Findings

- P0: none.
- P1: none.
- P2: none after the mobile diagram and filter fixes.
- Console errors: none.
- Broken or clipped primary controls: none.
- Gradient, large-radius, negative-letter-spacing, and viewport-scaled typography checks: clean.

## Focused Evidence

- Desktop hero: `/private/tmp/awesome-loop-hero-desktop-final.png`
- Mobile hero: `/private/tmp/awesome-loop-mobile-final.png`
- Mobile contract: `/private/tmp/awesome-loop-contract-mobile.png`
- Mobile pattern filter: `/private/tmp/awesome-loop-patterns-mobile.png`
- Social preview: `/Users/chaoyue/Library/CloudStorage/Dropbox/Loop Engineering/awesome-loop-engineering/assets/social-preview.png`

final result: passed
