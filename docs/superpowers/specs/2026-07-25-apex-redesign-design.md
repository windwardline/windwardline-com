# windwardline.com apex redesign — design spec

Date: 2026-07-25. Status: approved direction, pending spec review.
Proof artifact: https://claude.ai/code/artifact/481687fe-d4fe-4aa4-b182-138266cc0f9e

## Decisions of record

- Direction: **Proof A, "Fleet Register."** Light archival paper, certificate rules,
  divisions presented as a shipping line's register. Dark "Builder's Plate" and
  chart-idiom "The Chart" directions were reviewed and rejected.
- Identity: **No. 6 wordmark system** (house flag over tracked "WINDWARD LINE" with
  "HOLDING COMPANY" kicker) plus the **roundel burgee** standing alone where space
  is tight. The lettered burgee (No. 5's WL-in-flag) is retired.
- One-flag rule: the device never varies — navy swallowtail, gold roundel at the
  hoist. Renditions vary by context: solid on paper, gold outline on navy, small
  cut below 32 px. Confirmed by owner 2026-07-25.
- Marks are set in type or ruled geometry only. No freehand SVG paths, no
  letter-spacing hacks, no raster logo art (original gilded art stays out unless
  the owner later adds files to the repo).

## The house flag

Canonical geometry, viewBox `0 0 34 21`:

```svg
<!-- standard: solid, on paper -->
<path d="M0 0 H34 L23.5 10.5 L34 21 H0 Z" fill="#202e4d"/>
<circle cx="12" cy="10.5" r="3.2" fill="#c9a25e"/>

<!-- rendition: outline, on navy -->
<path d="M0 0 H34 L23.5 10.5 L34 21 H0 Z" fill="none" stroke="#d9bd85" stroke-width="1.6"/>
<circle cx="12" cy="10.5" r="3.2" fill="#d9bd85"/>

<!-- rendition: small cut, at or below 32 px rendered width -->
<path d="M0 0 H34 L21.5 10.5 L34 21 H0 Z" fill="#202e4d"/>
<circle cx="12" cy="10.5" r="4.6" fill="#c9a25e"/>
```

Favicon is the small cut: `favicon.svg` checked in, carrying both renditions via
an internal `prefers-color-scheme` media query (solid for light UI, outline for
dark), plus `apple-touch-icon.png` (180×180, solid flag on paper ground)
rendered once from the canonical SVG and checked in. The old "WL text in a
square" data-URI favicon is removed.

Every flag placement is one inline SVG styled through the theme tokens — the
theme, not the markup, selects the rendition.

## Type

- Face: **EB Garamond**, self-hosted woff2 latin subsets, two files:
  `EBGaramond-Roman.woff2` (variable, declared `font-weight: 400 800` — serves
  both 400 and 600) and `EBGaramond-Italic.woff2` (400 italic). Fallback stack
  `Georgia, serif`. No Google Fonts CDN.
- Scale (desktop / clamp to mobile):
  - Masthead: 600, clamp(34–47px), tracking .28em, uppercase
  - Kicker and section labels: 600, 12px, tracking .26–.34em, uppercase
  - Division names: 600, 26px
  - Ledes and descriptions: 400 italic, 16–19px
  - Meta (class/status), footer: 400, 12px, tracking .18–.22em, uppercase
- Numerals in meta columns use `font-variant-numeric: tabular-nums`.

## Palette

Two themes, one document. Dark mode is the same register unlit — tokens flip,
nothing else does. It follows the OS (`prefers-color-scheme`); there is no
toggle, because there is no JavaScript.

| Token | Light | Dark | Role |
|---|---|---|---|
| `--paper` | `#f7f5ef` | `#0e1526` | page ground |
| `--ink` | `#1a2338` | `#ece7da` | headings, body |
| `--rule` | `#1a2338` | `#cfc9b8` | certificate rules |
| `--muted` | `#5d6473` | `#a2aaba` | descriptions, meta text |
| `--line` | `#d8d2c2` | `rgba(236,231,218,.16)` | hairlines, row borders |
| `--gold` | `#c9a25e` | `#c9a25e` | roundel, status-dot fills |
| `--gold-ink` | `#8a6b39` | `#d9bd85` | gold text at label sizes |
| `--hover` | `#f1ede1` | `#131e36` | linked-row hover ground |

`#a5814a` and lighter golds are decorative or ≥18px only in light theme; 12px
gold text always uses `--gold-ink`. Declared `color-scheme: light dark`. In dark
theme every flag placement switches to the outline rendition (`#d9bd85`); open
status dots outline in `#d9bd85`. Print always uses light tokens.

## Page structure and copy

One page. Copy is final as written here.

**Masthead** — flag (standard rendition, ~34px) over "WINDWARD LINE", kicker
"A PRIVATE HOLDING COMPANY" between hairlines, then the lede, italic: "One
founder, one name." (Masthead copy revised 2026-07-25 post-launch, owner's
choice: institutional kicker, spartan lede; the register carries the
enumeration.) Certificate rules top (2px over 1px) open the page.

**Division colors** (decided 2026-07-26, round 2 — replaces the recalled V1
margin rail; sizing standard set in round 3): a division's flag leads its
register row name once the division has colors — Labs flies the Blue Peter and
Capital flies Sierra (paper field, navy square — bordered rendition on paper
grounds via the --sf-* tokens) in their rows today. **Sizing standard for every division flag**: the flag is cut to
the row name's cap height and sits on the baseline — 27×18 against the 26px
name (vertical-align -0.5px, 14px gap). Set with the type, never floated
mid-line; the round-2 21×14 inline size read as an afterthought and is
retired. A flag appears ONLY
when assigned; absence is the held state, and the status column carries the
rest. No scaffolding, no ghost outlines, no JS.

**STANDING RULE — division-flag renditions** (owner, corrected 2026-07-26):
a division flag's own colors NEVER change — Labs is always navy field with a
paper square, Sierra always paper field with a navy square, in both themes.
The only theme-dependent part is a uniform outline stroke around every
division flag: navy (#202e4d) in day mode, gold (#d9bd85) in night mode
(--dv-stroke, 1.4). Identity is constant; only the mounting changes. (The
house swallowtail keeps its own hollow-gold night rendition — this rule is for
division flags.)

**STANDING RULE — the lamp**: three states, labeled Light / Dark / System
exactly, on every property with a theme choice. Per-site phrasings are retired
(2026-07-26).

**STANDING RULE — contact and help email**: division pages use
<division>@windwardline.com; the apex uses hello@windwardline.com; all
help/support links anywhere use help@windwardline.com. Every mailto carries a
subject tag "[<Property>] Contact" or "[<Property>] Help" so the owner's
central inbox stays sortable. All windwardline.com addresses route via the
domain catch-all (owner-confirmed 2026-07-26).

**STANDING RULE — division links**: a division's apex row links to its own
subdomain from the day that landing exists (Labs → labs.windwardline.com and Capital →
capital.windwardline.com, both 2026-07-26). Never leave a
stand-in link behind after a launch.

**STANDING DECISION — the footer station**: when the fleet fills out (all four
divisions flying, or earlier at the owner's call), add round-2 variant C in
addition: assigned division flags muster in a small centered row beneath the
house flag in the footer (proof: artifact 4fe10411, "C · Footer station").
Every future division launch therefore touches the apex twice: its flag joins
its register row at launch, and the footer station ships when the set is
complete. (History: V1 margin rail, PR #9, reverted in PR #10 — floating
scaffolding against a centered document, held outlines read as broken UI.)

**Register of divisions** — label, then four rows. Row grammar: name (linked
rows get a NE arrow ↗), right column class over status with dot (filled gold =
in service, open = otherwise), italic description beneath the name.

| Name | Class | Status | Description | Link |
|---|---|---|---|---|
| Windward Labs | SOFTWARE | IN SERVICE | Product software built end-to-end and run in production: Pathfinder, LevelFlow Cloud, TimeShift, Mimic. | labs.windwardline.com |
| Windward Capital | MARKETS | IN SERVICE | Markets and trading discipline. LevelFlow Cloud is built here. | capital.windwardline.com |
| Windward Strategy | ADVISORY | BY ENGAGEMENT | Operations and technology: the plan, the sequence, the follow-through. | — |
| Windward Creative | MEDIA | IN DEVELOPMENT | Writing and film under the Windward name. | — |

**Affiliated venture** — label, one row: Refactored ↗, meta
"WEAREREFACTORED.COM", description "Founded by Windward Line. Pathfinder is its
first proof." Links to https://wearerefactored.com.

**Footer** — mirrored certificate rules (1px over 2px), flag at 24px (small
cut, per the one-flag rule), "© 2026 WINDWARD LINE", single link CONTACT
(mailto:hello@windwardline.com, subject tag "[Windward Line] Contact"; help
requests anywhere use help@windwardline.com). Portfolio and GitHub links removed 2026-07-25: they belong
to the portfolio site and the Labs division page, not the apex.

## Implementation

- Keep the current shape: static site, no build step. `index.html`, `style.css`,
  plus `fonts/` (three woff2 files), `favicon.svg`, `apple-touch-icon.png`.
- Fonts preloaded (`<link rel="preload" as="font">`), `font-display: swap`.
- Tighten CSP in `vercel.json`: `style-src 'self'; font-src 'self'` — drop the
  Google Fonts allowances. All other headers unchanged.
- Interaction is CSS-only except the lamp, the family-wide three-state theme
  control (added 2026-07-25 at owner request, presented after the portfolio's
  "Night passage" lamp with per-site language). Apex phrasing: DAY / NIGHT /
  SHIP'S TIME. Default is Ship's time (the OS preference); choosing Day or
  Night stores the choice in localStorage and sets `data-theme`, which outranks
  the media query; Ship's time clears it. A small self-hosted `script.js` runs
  blocking in `<head>` so a stored choice applies before first paint. CSP is
  `script-src 'self'` accordingly — still no inline script and no third
  parties. The lamp is hidden in print.
- Owner policy (2026-07-25): every `http(s)` link opens a new tab —
  `target="_blank" rel="noopener"`. `mailto:` links are exempt (they open the
  mail client and never navigate the page). Applies to all Windward Line sites.
- Meta description updated to match the lede; `<title>` stays "Windward Line".

## Quality floor

- Semantic landmarks (`header/main/section/footer`), one `h1`, labeled sections.
- Visible `:focus-visible` states; hover states never the only affordance.
- Transitions only (no animations); wrapped in `prefers-reduced-motion` guard.
- Contrast: all text AA at rendered size in both themes (gold text via
  `--gold-ink` only).
- Responsive to 320px: register rows stack name → desc → meta; masthead clamps.
- Print: the register prints as a clean one-page document (hairlines survive,
  hover chrome and interactive affordances drop).
- CI must stay green: `html-validate` on `index.html`, `vercel.json` parse check.
- Verify live at deploy: fonts load from `'self'`, no CSP violations in console.

## Out of scope

- Rejected directions B and C; interlock, crown, and seal marks (archived in the
  proof artifact for the record).
- Any change to subdomain sites (portfolio, levelflow, pathfinder).
- README update to reflect the new design is in scope; content changes beyond
  that are not.
