# Design QA

## Source

- Selected direction: `/Users/chaoyue/.codex/generated_images/019ed02c-a15f-7881-aab3-49ff394627b4/exec-e373a4be-af07-451b-937a-7cd5acbd9b12.png`
- Stack figure refresh: `/Users/chaoyue/.codex/generated_images/019ed02c-a15f-7881-aab3-49ff394627b4/exec-0e105db4-a098-48f5-b3f1-301d07cb21f6.png`
- Runtime map: `/Users/chaoyue/.codex/generated_images/019ed02c-a15f-7881-aab3-49ff394627b4/exec-8abdd5c7-4c6a-4406-bd07-47dfbc6f1721.png`
- Maturity model: `/Users/chaoyue/.codex/generated_images/019ed02c-a15f-7881-aab3-49ff394627b4/exec-ed3a252d-15d6-4836-84cb-21ce313f10bb.png`
- Interactive hero: Three.js `0.185.1`, vendored under `docs/assets/vendor/three/` with its MIT license.
- Local prototype: repository `docs/` build served during QA
- Reference comparison: `/private/tmp/loop-design-comparison.png`

## Viewports And States

- Desktop first viewport: 1440 x 1000, page top, sticky navigation and the complete six-station agent loop visible.
- Mobile first viewport: 390 x 844, page top, compact six-station scene, stage selector, and next-section cue visible without horizontal overflow.
- Mobile navigation: eight links visible when expanded; Escape closes the menu, updates `aria-expanded`, and restores focus.
- Pattern library: 20 symptom-first entries; mobile query `accessibility` returns exactly one matching pattern.
- Contract and lifecycle: purpose-built mobile summaries replace desktop-wide figures at 560 px and below.
- Runtime map: desktop figure plus eight labeled starters in a balanced 4 x 2 grid; mobile uses the explanatory copy and one-column starter sequence instead of shrinking the wide figure.
- Maturity model: desktop figure plus semantic levels 00-06; mobile keeps the readable level rows and hides the wide supporting figure.
- Social preview: 1280 x 640, exact 545-resource, 20-pattern, 20-contract, and 8-starter counts.
- Interactive hero, desktop: 1440 x 1000, one ready WebGL canvas, no horizontal overflow, and meaningful agent-system labels.
- Interactive hero, mobile: 390 x 844, one ready WebGL canvas, no horizontal overflow, and all six stations inside the frame.
- Interactive hero motion: the frame counter advanced by 47 frames during a 450 ms pointer-parallax check.
- Interactive hero efficiency: the frame counter advanced by zero during a 700 ms offscreen check at the Resources section.

## Comparison History

1. Compared the ChatGPT Image direction and the first implementation in one side-by-side input. The implementation preserved the light technical-field-guide palette, thin rules, flat surfaces, and restrained blue/cyan/green accents. The identity was intentionally centered to honor the repository requirement.
2. The first mobile pass scaled the desktop stack diagram too far down. This was a P2 legibility issue.
3. Added a dedicated mobile mental-model asset and horizontally inspectable contract and lifecycle diagrams. Rechecked at 390 x 844; headings, labels, controls, and section transitions are readable without overlap.
4. Tightened short-query filtering so `CI` returns the CI repair loop instead of substring matches inside unrelated words.
5. Compared the original stack figure and the ChatGPT Image revision side by side. The revision replaces empty overlapping outlines with four populated plates, aligned leader lines, a one-run bracket, and an explicit recurring-work governance badge. OCR and browser checks confirmed the required copy, 1666 x 944 dimensions, and error-free rendering.
6. Audited the live README and site for visual gaps. Added coordinated runtime-selection and maturity-progression figures only where the existing presentation was text-only; retained the hero, cover, social preview, stack, contract, and lifecycle assets unchanged.
7. The responsive pass found the citation block widening the entire page to 618 px at a 390 px viewport. Setting footer grid children to `min-width: 0` restored a 390 px document width while preserving horizontal scrolling inside the four wide diagrams.
8. Compared the published static hero and the Three.js-enhanced hero at the same 1280 x 720 viewport. The enhancement keeps the existing identity, copy, actions, spacing, and section transition while adding a restrained evidence orbit, control-plane stack, verification gate, and six lifecycle nodes behind the content.
9. Moved the control-plane stack and verification gate outward after the first 3D pass so they frame the copy rather than crossing its reading path. Rechecked desktop and mobile rendering after the adjustment.
10. Verified progressive enhancement behavior: the semantic hero remains complete without WebGL, forced-colors and print hide the scene, reduced-motion renders a static frame, and the animation stops when the hero leaves the viewport.
11. Expanded the implementation kit to 20 patterns, 20 validated contracts, and eight runtime starters. The runtime section now labels all five adaptable templates and all three executables, with use-case copy and an even desktop grid.
12. Rechecked the expanded pattern and runtime sections at 1440 x 1000 and 390 x 844. Anchor offsets clear the sticky header, the page width stays equal to the viewport, and headings, icons, labels, and descriptions remain aligned.

## Findings

- P0: none.
- P1: none.
- P2: none after the mobile diagram and filter fixes.
- Console errors: none.
- Broken or clipped primary controls: none.
- Gradient, large-radius, negative-letter-spacing, and viewport-scaled typography checks: clean.

## Focused Evidence

- Desktop hero: `/private/tmp/ale-site-v07-top-desktop.png`
- Mobile hero: `/private/tmp/ale-site-v07-top-mobile-final.png`
- Desktop pattern library: `/private/tmp/ale-site-v07-patterns-desktop.png`
- Mobile pattern library: `/private/tmp/ale-site-v07-patterns-mobile.png`
- Desktop runtime map and starter grid: `/private/tmp/ale-site-v07-runtime-desktop-final.png`
- Mobile runtime starters: `/private/tmp/ale-site-v07-runtime-mobile-final.png`
- Three.js pointer-motion frame: `/private/tmp/awesome-loop-hero-three-motion-final.png`
- Social preview: `/Users/chaoyue/Library/CloudStorage/Dropbox/Loop Engineering/awesome-loop-engineering/assets/social-preview.png`

## 2026-07-18 Repository Audit

- Desktop: 1440 x 1000, no horizontal overflow, no hero text/scene overlap, and all eight section headings render without requiring scroll-triggered opacity changes.
- Tablet: 768 x 900. The first pass clipped the intake and decision stations. The responsive camera now fits an 11.2-unit horizontal view between 720 px and 900 px, keeping all six stations, the retry path, and the outcome node inside the canvas.
- Phone: 390 x 844, no horizontal overflow. The compact loop keeps all six stations, the moving work packet, legend, outcome key, and stage selector visible without crossing the hero copy.
- Mobile navigation: opens all eight project links, reports `aria-expanded="true"`, closes on Escape, and restores focus to the menu button.
- Pattern filter: `accessibility` returns exactly one of the 20 patterns.
- Resource Atlas: remains idle above the fold, loads on approach or a direct resource anchor, and reports `545 of 545 resources | showing 8` on mobile.
- Resource interactions: `SWE-bench` returns 9 matches, the paper filter narrows those to 6, Reset restores all 545, and Show more expands the rendered set from 8 to 16.
- Scene motion: the canvas frame counter advanced from 640 to 662 over 900 ms. Two canvas crops taken 1.2 seconds apart changed 17.79% of sampled RGB channels.
- Scene pixels: the sampled desktop crop has 15.71% active pixels with RGB standard deviations of 35.83, 29.77, and 23.01; mobile has 27.84% active pixels with deviations of 41.27, 30.61, and 19.52. Both renders are nonblank and well contrasted.
- Runtime starters: desktop cards form two equal-height rows of four; mobile cards are 358 px wide within a 390 px document and preserve label, icon, heading, and copy alignment.
- Console: no page-origin errors or warnings during mobile navigation, pattern filtering, and Resource Atlas interactions.
- Source audit: 545 rows checked; 496 public sources reachable, 1 access-restricted, 48 repository-native, and 0 broken or unreachable as of 2026-07-17 UTC.
- Data and copy: the website, README, translations, social preview source, release copy, and Hugging Face card all report 545 resources, 20 patterns, 20 contracts, 8 runtime starters, and version 0.7.0.

final result: passed
