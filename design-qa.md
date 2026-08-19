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
- Mobile navigation: nine links visible when expanded; Escape closes the menu, updates `aria-expanded`, and restores focus.
- Pattern library: 20 symptom-first entries; mobile query `accessibility` returns exactly one matching pattern.
- Contract and lifecycle: purpose-built mobile summaries replace desktop-wide figures at 560 px and below.
- Runtime map: desktop figure plus eight labeled starters in a balanced 4 x 2 grid; mobile uses the explanatory copy and one-column starter sequence instead of shrinking the wide figure.
- Maturity model: desktop figure plus semantic levels 00-06; mobile keeps the readable level rows and hides the wide supporting figure.
- Social preview: 1280 x 640, exact 669-resource, 20-pattern, 20-contract, and 8-starter counts, with the model-to-operations scope line.
- Interactive hero, desktop: 1440 x 1000, one ready WebGL canvas, no horizontal overflow, and meaningful agent-system labels.
- Interactive hero, mobile: 390 x 844, one ready WebGL canvas, no horizontal overflow, and all six stations inside the frame.
- Agent-loop semantics: the bounded agent workspace is the visual anchor; context and three scoped tools feed the agent, verification remains external, memory remains durable, and decision outcomes branch to retry, human handoff, or verified exit.
- Engineering-stack scene: desktop adds a second, independent WebGL canvas that separates one-run prompt/context/harness concerns from the outer recurring loop. The original SVG remains the WebGL fallback.
- Engineering-stack mobile fallback: the desktop canvas is removed from layout at 560 px and below; a four-row semantic stack preserves the same model without shrinking 3D labels.
- Interactive hero motion: the frame counter advanced by 47 frames during a 450 ms pointer-parallax check.
- Interactive hero efficiency: the frame counter advanced by zero during a 700 ms offscreen check at the Resources section.
- Future directions: three role-based tracks remain side by side at 1440 x 1000 and become a rule-separated single column at 390 x 844 without horizontal overflow.

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
11. Expanded the implementation kit to 22 patterns, 22 schema-checked contracts, and eight runtime starters. The runtime section now labels all five adaptable templates and all three executables, with use-case copy and an even desktop grid.
12. Rechecked the expanded pattern and runtime sections at 1440 x 1000 and 390 x 844. Anchor offsets clear the sticky header, the page width stays equal to the viewport, and headings, icons, labels, and descriptions remain aligned.
13. Added the role-based future-directions section and rechecked it at both target viewports. Resource Atlas expansion initially displaced direct links to later sections; post-load hash restoration now leaves `#future` 84 px below the desktop viewport top and 74 px below it on mobile.

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
- Desktop future directions: `/private/tmp/future-viewport-desktop.png`
- Mobile future directions: `/private/tmp/future-viewport-mobile.png`
- Three.js pointer-motion frame: `/private/tmp/awesome-loop-hero-three-motion-final.png`
- Social preview: `/Users/chaoyue/Library/CloudStorage/Dropbox/Loop Engineering/awesome-loop-engineering/assets/social-preview.png`
- Semantic agent loop, desktop: `/tmp/awesome-loop-agent-desktop.png`
- Semantic engineering stack, desktop: `/tmp/awesome-loop-stack-desktop.png`
- Semantic agent loop, mobile: `/tmp/awesome-loop-agent-mobile.png`

## 2026-07-20 Repository Audit

- Desktop: 1440 x 1000, no horizontal overflow, no hero text/scene overlap, and all nine section headings render without requiring scroll-triggered opacity changes.
- Tablet: 768 x 900. The first pass clipped the intake and decision stations. The responsive camera now fits an 11.2-unit horizontal view between 720 px and 900 px, keeping all six stations, the retry path, and the outcome node inside the canvas.
- Phone: 390 x 844, no horizontal overflow. The compact loop keeps all six stations, the moving work packet, legend, outcome key, and stage selector visible without crossing the hero copy.
- Mobile navigation: opens all nine project links, reports `aria-expanded="true"`, closes on Escape, and restores focus to the menu button.
- Pattern filter: `accessibility` returns exactly one of the 22 patterns.
- Resource Atlas: remains idle above the fold, loads on approach or a direct resource anchor, and reports `974 of 974 resources | showing 8` on a fresh mobile load.
- Resource interactions: the Model loop-layer filter returns 31 of 974 resources (30 papers plus Awesome Loop Models), paginates eight at a time on mobile, and renders Loopie and LoopWM with their 2026 arXiv records and adjacent-scope labels.
- Resource row schema: desktop exposes Work, Year, Published at, and Evidence; mobile stacks the same labels. A `ReasoningBank` query returns one row with its ICLR venue, arXiv identifier, Tier A evidence, task fit, and source record without horizontal overflow.
- Scene motion: the canvas frame counter advanced from 640 to 662 over 900 ms. Two canvas crops taken 1.2 seconds apart changed 17.79% of sampled RGB channels.
- Scene pixels: the current desktop canvas has 7,062 colors with RGB standard deviations of 35.93, 29.76, and 22.29; mobile has 5,755 colors with deviations of 40.73, 30.54, and 19.70. Both renders are nonblank and well contrasted.
- Runtime starters: desktop cards form two equal-height rows of four; mobile cards are 358 px wide within a 390 px document and preserve label, icon, heading, and copy alignment.
- Future directions: direct-anchor restoration waits for the Resource Atlas reflow, all three audience tracks remain readable, and the agenda CTA is fully visible at desktop and mobile widths.
- Console: no page-origin errors or warnings during mobile navigation, pattern filtering, and Resource Atlas interactions.
- Narrow phone: 320 x 844, document width equals viewport width; the headline stays within 16 px gutters and the Three.js canvas remains fully inside the 288 px content width.
- Source audit: 974 rows checked; 913 public sources reachable, 10 access-restricted, 51 repository-native, and 0 broken or unreachable as of 2026-08-20 UTC.
- Data and copy: the website, README, translations, social preview source, release copy, and Hugging Face card all report 974 resources, 22 patterns, 22 contracts, 8 runtime starters, and version 0.9.0. The dataset exposes 50 fields, including `loop_layer` and `scope_fit`.
- Semantic scene pass: the desktop hero crop paints 14.61% of pixels beyond the paper background with a 254.71 luminance range; the desktop stack paints 27.83% with a 249.98 range; the mobile hero paints 20.84% with a 229.45 range.
- Stage interaction: selecting Verify updates `aria-pressed` across all six controls and replaces the live detail with the independent evidence-gate explanation.
- Progressive enhancement: desktop loads the agent-loop and engineering-stack canvases; mobile loads only the agent-loop canvas and exposes the four-layer text stack. Both target viewports have zero horizontal overflow and no console messages.

final result: passed
