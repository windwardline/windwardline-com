# Fleet Register Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rebuild windwardline.com as the approved "Fleet Register" design with the reconciled house-flag identity, dual theme, and a tightened CSP.

**Architecture:** Static one-page site, no build step: one HTML file, one stylesheet, three self-hosted woff2 fonts, two icon assets. All marks are inline SVG styled through theme tokens; there is no JavaScript.

**Tech Stack:** HTML + CSS only. CI: `html-validate@9` via npx, `node` JSON parse check. Deploys to Vercel on push to `main`; DNS on Cloudflare.

**Spec:** `docs/superpowers/specs/2026-07-25-apex-redesign-design.md` (approved 2026-07-25). Copy, tokens, and geometry in this plan are copied from it verbatim and are final.

## Global Constraints

- Branch: all work on `redesign/fleet-register`, branched off `main`. Never commit to `main`. Conventional Commits (`feat:`, `chore:`, `docs:`).
- No JavaScript anywhere; `script-src 'none'` stays in the CSP.
- No build step, no package.json, no dependencies. CI-only tooling via `npx --yes`.
- One-flag rule: the only mark is the house flag — navy swallowtail, gold roundel at the hoist. Standard geometry `M0 0 H34 L23.5 10.5 L34 21 H0 Z` + circle `cx12 cy10.5 r3.2`; small cut (≤32px rendered width) `M0 0 H34 L21.5 10.5 L34 21 H0 Z` + `r4.6`. Renditions switch by theme tokens, never by markup.
- Fonts: EB Garamond only — files `fonts/EBGaramond-Roman.woff2` (variable roman, declared `font-weight: 400 800`) and `fonts/EBGaramond-Italic.woff2` (400 italic). Google serves one identical variable slice for discrete roman weights, so one roman file carries 400 and 600. Fallback `Georgia, serif`. No font CDNs.
- CI must pass at every commit: `npx --yes html-validate@9 index.html` and `node -e "JSON.parse(require('fs').readFileSync('vercel.json','utf8')); console.log('vercel.json ok')"`.
- Class vocabulary (authoritative for Tasks 4–5): `mast`, `mast-inner`, `mast-title`, `mast-kicker`, `mast-lede`, `rule-heavy`, `rule-thin`, `flag`, `flag--small`, `sec`, `sec-label`, `row`, `row-name`, `row-arrow`, `row-meta`, `row-class`, `row-status`, `dot`, `dot--open`, `row-desc`, `foot`, `foot-rules`, `foot-copy`, `foot-links`.
- Token vocabulary: `--paper`, `--ink`, `--rule`, `--muted`, `--line`, `--gold`, `--gold-ink`, `--hover`, `--flag-fill`, `--flag-stroke`, `--flag-sw`, `--flag-dot`.

---

### Task 1: Branch and spec commit

**Files:**
- Commit existing: `docs/superpowers/specs/2026-07-25-apex-redesign-design.md`

**Interfaces:**
- Consumes: clean `main` at or after commit `19070d8`.
- Produces: branch `redesign/fleet-register` that all later tasks commit to.

- [ ] **Step 1: Create the branch**

```bash
cd /Users/peacock/Projects/windwardline-com
git checkout main && git pull --ff-only
git checkout -b redesign/fleet-register
```

- [ ] **Step 2: Verify the spec file is present and staged cleanly**

```bash
git add docs/superpowers/specs/2026-07-25-apex-redesign-design.md
git status --short
```

Expected: only the spec file staged (`A  docs/...-design.md`). If `.claude/launch.json` shows as untracked, leave it untracked — do not commit it.

- [ ] **Step 3: Commit**

```bash
git commit -m "docs: add fleet-register design spec"
```

---

### Task 2: Self-hosted EB Garamond

**Files:**
- Create: `fonts/EBGaramond-Regular.woff2`, `fonts/EBGaramond-Italic.woff2`, `fonts/EBGaramond-SemiBold.woff2`

**Interfaces:**
- Consumes: nothing.
- Produces: the three font paths exactly as named — Task 4 preloads them and Task 5's `@font-face` blocks reference them.

- [ ] **Step 1: Download the latin subsets from Google Fonts**

```bash
cd /Users/peacock/Projects/windwardline-com && mkdir -p fonts && python3 - <<'EOF'
import re, subprocess
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
css = subprocess.run(["curl","-sS","-A",UA,
  "https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap"],
  capture_output=True, text=True, check=True).stdout
blocks = re.findall(r'/\*\s*(latin)\s*\*/\s*(@font-face\s*\{[^}]+\})', css)
names = {("normal","400"):"EBGaramond-Regular.woff2",
         ("italic","400"):"EBGaramond-Italic.woff2",
         ("normal","600"):"EBGaramond-SemiBold.woff2"}
for _, block in blocks:
    style  = re.search(r'font-style:\s*(\w+)', block).group(1)
    weight = re.search(r'font-weight:\s*(\d+)', block).group(1)
    url    = re.search(r'url\((https://[^)]+\.woff2)\)', block).group(1)
    out    = "fonts/" + names[(style, weight)]
    subprocess.run(["curl","-sS","-A",UA,url,"-o",out], check=True)
    print(out)
EOF
```

Expected: prints the three font paths.

- [ ] **Step 2: Verify the files are real woff2**

```bash
file fonts/*.woff2 && ls -la fonts/
```

Expected: each file reported as `Web Open Font Format (Version 2)`, each larger than 20 KB. If `file` prints HTML or ASCII, the download failed — do not commit; re-run Step 1.

- [ ] **Step 3: Commit**

```bash
git add fonts && git commit -m "feat: self-host EB Garamond latin subsets"
```

---

### Task 3: House-flag icon assets

**Files:**
- Create: `favicon.svg`, `apple-touch-icon.png`

**Interfaces:**
- Consumes: flag geometry from Global Constraints.
- Produces: `favicon.svg` and `apple-touch-icon.png` at repo root — Task 4 links both by exactly these names.

- [ ] **Step 1: Write `favicon.svg`** (small cut; theme-aware via internal media query)

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 34 21">
  <style>
    path{fill:#202e4d}circle{fill:#c9a25e}
    @media (prefers-color-scheme:dark){
      path{fill:none;stroke:#d9bd85;stroke-width:2.4}circle{fill:#d9bd85}
    }
  </style>
  <path d="M0 0 H34 L21.5 10.5 L34 21 H0 Z"/>
  <circle cx="12" cy="10.5" r="4.6"/>
</svg>
```

- [ ] **Step 2: Generate `apple-touch-icon.png`** (180×180, solid standard-cut flag centered on paper; stdlib-only rasterizer, 4× supersampled)

```bash
cd /Users/peacock/Projects/windwardline-com && python3 - <<'EOF'
import zlib, struct
W = H = 180
PAPER, NAVY, GOLD = (247,245,239), (32,46,77), (201,162,94)
fw = 132.0; s = fw/34.0; fh = 21.0*s
x0 = (W-fw)/2.0; y0 = (H-fh)/2.0
def color(px, py):
    fx, fy = (px-x0)/s, (py-y0)/s          # flag-local coords, 0..34 x 0..21
    if not (0 <= fx <= 34 and 0 <= fy <= 21): return PAPER
    if fx > 23.5 and abs(fy-10.5) < (fx-23.5): return PAPER   # swallowtail notch
    if (fx-12)**2 + (fy-10.5)**2 <= 3.2**2: return GOLD
    return NAVY
rows = []
SS = 4
for y in range(H):
    row = bytearray([0])
    for x in range(W):
        r=g=b=0
        for sy in range(SS):
            for sx in range(SS):
                c = color(x+(sx+.5)/SS, y+(sy+.5)/SS)
                r+=c[0]; g+=c[1]; b+=c[2]
        n = SS*SS
        row += bytes((r//n, g//n, b//n))
    rows.append(bytes(row))
raw = b"".join(rows)
def chunk(tag, data):
    return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag+data))
png = (b"\x89PNG\r\n\x1a\n"
  + chunk(b"IHDR", struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0))
  + chunk(b"IDAT", zlib.compress(raw, 9))
  + chunk(b"IEND", b""))
open("apple-touch-icon.png","wb").write(png)
print("wrote apple-touch-icon.png", len(png), "bytes")
EOF
```

- [ ] **Step 3: Verify both assets**

```bash
sips -g pixelWidth -g pixelHeight apple-touch-icon.png && head -c 200 favicon.svg
```

Expected: `pixelWidth: 180`, `pixelHeight: 180`; favicon output starts `<svg xmlns=`. Open `apple-touch-icon.png` and confirm by eye: navy swallowtail with gold roundel, centered on warm paper, no artifacts.

- [ ] **Step 4: Commit**

```bash
git add favicon.svg apple-touch-icon.png
git commit -m "feat: add house-flag favicon and touch icon"
```

---

### Task 4: index.html — the register

**Files:**
- Modify: `index.html` (full rewrite; replaces all current content)

**Interfaces:**
- Consumes: `fonts/EBGaramond-*.woff2` names (Task 2), `favicon.svg` / `apple-touch-icon.png` (Task 3).
- Produces: the exact class vocabulary from Global Constraints, consumed by Task 5's stylesheet. Copy is final — do not edit it.

- [ ] **Step 1: Replace `index.html` with exactly this content**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Windward Line</title>
<meta name="description" content="Windward Line is a founder-held holding company. Software in production, capital at work, and select engagements — one founder, one name.">
<link rel="preload" href="fonts/EBGaramond-SemiBold.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/EBGaramond-Regular.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/EBGaramond-Italic.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
</head>
<body>

<header class="mast">
  <div class="rule-heavy" aria-hidden="true"></div>
  <div class="rule-thin" aria-hidden="true"></div>
  <div class="mast-inner">
    <svg class="flag" width="34" height="21" viewBox="0 0 34 21" role="img" aria-label="Windward Line house flag">
      <path d="M0 0 H34 L23.5 10.5 L34 21 H0 Z"/>
      <circle cx="12" cy="10.5" r="3.2"/>
    </svg>
    <h1 class="mast-title">Windward Line</h1>
    <p class="mast-kicker">A Founder-Held Holding Company</p>
    <p class="mast-lede">Software in production, capital at work, and select engagements. One founder, one name.</p>
  </div>
</header>

<main>
  <section class="sec" aria-labelledby="divisions-h">
    <h2 class="sec-label" id="divisions-h">Register of Divisions</h2>

    <a class="row" href="https://portfolio.windwardline.com">
      <span class="row-name">Windward Labs<span class="row-arrow" aria-hidden="true">↗</span></span>
      <span class="row-meta">
        <span class="row-class">Software</span>
        <span class="row-status"><span class="dot" aria-hidden="true"></span>In Service</span>
      </span>
      <span class="row-desc">Product software built end-to-end and run in production: Pathfinder, LevelFlow Cloud, TimeShift, Mimic.</span>
    </a>

    <div class="row">
      <span class="row-name">Windward Strategy</span>
      <span class="row-meta">
        <span class="row-class">Advisory</span>
        <span class="row-status"><span class="dot dot--open" aria-hidden="true"></span>By Engagement</span>
      </span>
      <span class="row-desc">Operations and technology: the plan, the sequence, the follow-through.</span>
    </div>

    <div class="row">
      <span class="row-name">Windward Creative</span>
      <span class="row-meta">
        <span class="row-class">Media</span>
        <span class="row-status"><span class="dot dot--open" aria-hidden="true"></span>In Development</span>
      </span>
      <span class="row-desc">Writing and film under the Windward name.</span>
    </div>
  </section>
</main>

<footer class="foot">
  <div class="foot-rules" aria-hidden="true">
    <div class="rule-thin"></div>
    <div class="rule-heavy"></div>
  </div>
  <svg class="flag flag--small" width="24" height="15" viewBox="0 0 34 21" role="img" aria-label="Windward Line house flag">
    <path d="M0 0 H34 L21.5 10.5 L34 21 H0 Z"/>
    <circle cx="12" cy="10.5" r="4.6"/>
  </svg>
  <p class="foot-copy">© 2026 Windward Line</p>
  <nav class="foot-links" aria-label="Footer">
    <a href="https://portfolio.windwardline.com">Portfolio</a>
    <a href="https://github.com/windwardline">GitHub</a>
    <a href="mailto:support@windwardline.com">Contact</a>
  </nav>
</footer>

</body>
</html>
```

- [ ] **Step 2: Run the HTML validator (the test for this task)**

```bash
npx --yes html-validate@9 index.html
```

Expected: exits 0, no errors. If it flags anything, fix the markup — do not disable rules.

- [ ] **Step 3: Commit**

```bash
git add index.html && git commit -m "feat: rebuild apex page as the fleet register"
```

Note: the page is intentionally unstyled until Task 5 lands; CI stays green because the validator does not require the stylesheet's classes to exist.

---

### Task 5: style.css — tokens, register, dual theme

**Files:**
- Modify: `style.css` (full rewrite; replaces all current content)

**Interfaces:**
- Consumes: class vocabulary from Task 4, font files from Task 2.
- Produces: the shipped visual system. No later task edits CSS.

- [ ] **Step 1: Replace `style.css` with exactly this content**

```css
/* Windward Line — fleet register. Spec: docs/superpowers/specs/2026-07-25-apex-redesign-design.md */

:root {
  color-scheme: light dark;
  --paper: #f7f5ef;
  --ink: #1a2338;
  --rule: #1a2338;
  --muted: #5d6473;
  --line: #d8d2c2;
  --gold: #c9a25e;
  --gold-ink: #8a6b39;
  --hover: #f1ede1;
  --flag-fill: #202e4d;
  --flag-stroke: transparent;
  --flag-sw: 0;
  --flag-dot: #c9a25e;
}

@media (prefers-color-scheme: dark) {
  :root {
    --paper: #0e1526;
    --ink: #ece7da;
    --rule: #cfc9b8;
    --muted: #a2aaba;
    --line: rgba(236, 231, 218, 0.16);
    --gold: #c9a25e;
    --gold-ink: #d9bd85;
    --hover: #131e36;
    --flag-fill: transparent;
    --flag-stroke: #d9bd85;
    --flag-sw: 1.6;
    --flag-dot: #d9bd85;
  }
}

@font-face {
  font-family: "EB Garamond";
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(fonts/EBGaramond-Regular.woff2) format("woff2");
}
@font-face {
  font-family: "EB Garamond";
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url(fonts/EBGaramond-Italic.woff2) format("woff2");
}
@font-face {
  font-family: "EB Garamond";
  font-style: normal;
  font-weight: 600;
  font-display: swap;
  src: url(fonts/EBGaramond-SemiBold.woff2) format("woff2");
}

* { box-sizing: border-box; margin: 0; }

body {
  font-family: "EB Garamond", Georgia, serif;
  background: var(--paper);
  color: var(--ink);
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

/* certificate rules and the flag */
.rule-heavy { border-top: 2px solid var(--rule); }
.rule-thin { border-top: 1px solid var(--rule); margin-top: 3px; }
.flag path { fill: var(--flag-fill); stroke: var(--flag-stroke); stroke-width: var(--flag-sw); }
.flag circle { fill: var(--flag-dot); }

/* masthead */
.mast { max-width: 760px; margin: 0 auto; padding: 76px 28px 0; }
.mast-inner { text-align: center; padding: 44px 0 40px; }
.mast-inner .flag { margin-bottom: 22px; }
.mast-title {
  font-size: clamp(34px, 6vw, 47px);
  font-weight: 600;
  letter-spacing: 0.28em;
  padding-left: 0.28em;
  line-height: 1.1;
  text-transform: uppercase;
  text-wrap: balance;
}
.mast-kicker {
  margin-top: 16px;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.34em;
  padding-left: 0.34em;
  text-transform: uppercase;
  color: var(--gold-ink);
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
}
.mast-kicker::before,
.mast-kicker::after { content: ""; width: 44px; border-top: 1px solid var(--line); }
.mast-lede {
  margin: 26px auto 0;
  font-style: italic;
  font-size: 19px;
  color: var(--muted);
  max-width: 46ch;
  line-height: 1.55;
}

/* register */
main { max-width: 760px; margin: 0 auto; padding: 0 28px; }
.sec { margin-top: 52px; }
.sec-label {
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.26em;
  text-transform: uppercase;
  color: var(--gold-ink);
  padding-bottom: 12px;
}
.row {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 4px 28px;
  align-items: baseline;
  padding: 26px 10px;
  border-top: 1px solid var(--line);
  text-decoration: none;
  color: inherit;
}
.sec .row:last-child { border-bottom: 1px solid var(--line); }
.row-name { font-size: 26px; font-weight: 600; line-height: 1.2; }
.row-arrow { display: inline-block; font-size: 17px; color: var(--gold-ink); margin-left: 6px; }
.row-meta {
  text-align: right;
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--muted);
  line-height: 1.9;
  white-space: nowrap;
  font-variant-numeric: tabular-nums;
}
.row-class { display: block; }
.row-status { display: flex; align-items: center; justify-content: flex-end; gap: 7px; }
.dot { width: 6px; height: 6px; border-radius: 50%; background: var(--gold); flex: none; }
.dot--open { background: transparent; border: 1px solid var(--gold-ink); }
.row-desc {
  grid-column: 1;
  font-style: italic;
  font-size: 16px;
  color: var(--muted);
  line-height: 1.5;
  max-width: 56ch;
}

/* footer */
.foot { max-width: 760px; margin: 0 auto; padding: 64px 28px 72px; text-align: center; }
.foot-rules { margin-bottom: 30px; }
.foot-rules .rule-thin { margin-top: 0; }
.foot-rules .rule-heavy { margin-top: 3px; }
.foot-copy { font-size: 12px; letter-spacing: 0.22em; text-transform: uppercase; color: var(--muted); margin-top: 20px; }
.foot-links { margin-top: 14px; display: flex; justify-content: center; gap: 30px; }
.foot-links a {
  font-size: 12px;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: var(--gold-ink);
  text-decoration: none;
}

/* interaction — motion only when welcome */
a.row:focus-visible,
.foot-links a:focus-visible { outline: 2px solid var(--gold); outline-offset: 3px; }
a.row:hover { background: var(--hover); }
a.row:hover .row-name { color: var(--gold-ink); }
.foot-links a:hover { text-decoration: underline; text-underline-offset: 4px; }
@media (prefers-reduced-motion: no-preference) {
  .row { transition: background 0.15s ease; }
  .row-name { transition: color 0.15s ease; }
  .row-arrow { transition: transform 0.15s ease; }
  a.row:hover .row-arrow { transform: translate(2px, -2px); }
}

/* small screens */
@media (max-width: 640px) {
  .row { grid-template-columns: 1fr; }
  .row-desc { grid-column: auto; }
  .row-meta { order: 3; text-align: left; margin-top: 8px; white-space: normal; }
  .row-status { justify-content: flex-start; }
}

/* print: the register is a light paper document */
@media print {
  :root {
    --paper: #ffffff;
    --ink: #1a2338;
    --rule: #1a2338;
    --muted: #5d6473;
    --line: #d8d2c2;
    --gold: #c9a25e;
    --gold-ink: #8a6b39;
    --hover: transparent;
    --flag-fill: #202e4d;
    --flag-stroke: transparent;
    --flag-sw: 0;
    --flag-dot: #c9a25e;
  }
  .row-arrow { display: none; }
}
```

- [ ] **Step 2: Re-run the validator**

```bash
npx --yes html-validate@9 index.html
```

Expected: exits 0.

- [ ] **Step 3: Visual verification (both themes, mobile, print)**

Serve locally and inspect:

```bash
python3 -m http.server 4180 --bind 127.0.0.1
```

Checklist (use browser devtools rendering emulation for `prefers-color-scheme` and print):
- Light: paper ground, navy solid flag with gold roundel, certificate rules top and bottom, three register rows + affiliated row, statuses right-aligned with dots (filled gold ×1, open ×2), italic descriptions.
- Dark: deep navy ground, flag switches to gold outline rendition, rules soften to `#cfc9b8`, text warm off-white; nothing else moves.
- 320–640px: rows stack name → description → meta; no horizontal scroll.
- Print preview: light tokens, no hover chrome, no arrows, hairlines visible.
- EB Garamond renders (serif with true italic — if you see Georgia everywhere, a font path is wrong).

- [ ] **Step 4: Commit**

```bash
git add style.css && git commit -m "feat: register stylesheet with dual theme and print styles"
```

---

### Task 6: CSP tighten, README

**Files:**
- Modify: `vercel.json:11` (the Content-Security-Policy value)
- Modify: `README.md`

**Interfaces:**
- Consumes: self-hosted font paths (Task 2) that make dropping the Google hosts safe.
- Produces: final deploy configuration.

- [ ] **Step 1: Update the CSP value in `vercel.json`**

Replace the `Content-Security-Policy` value with exactly:

```
default-src 'self'; style-src 'self'; font-src 'self'; img-src 'self' data:; script-src 'none'; base-uri 'none'; form-action 'none'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests
```

(The only change: `style-src` loses `https://fonts.googleapis.com`, `font-src` becomes `'self'` instead of `https://fonts.gstatic.com`. All other headers stay untouched.)

- [ ] **Step 2: Run the JSON parse check (the test for this file)**

```bash
node -e "JSON.parse(require('fs').readFileSync('vercel.json','utf8')); console.log('vercel.json ok')"
```

Expected: `vercel.json ok`.

- [ ] **Step 3: Replace `README.md` body with exactly this content**

```markdown
# windwardline.com

The apex site for Windward Line, a founder-held holding company. Three divisions —
Labs, Strategy, Creative.

Static site, no build step: one HTML file, one stylesheet, self-hosted
EB Garamond, and the house flag as inline SVG. Light and dark themes follow the
OS. Design spec: [docs/superpowers/specs/2026-07-25-apex-redesign-design.md](docs/superpowers/specs/2026-07-25-apex-redesign-design.md).

Deployed on Vercel; DNS on Cloudflare. Pushes to `main` deploy to production.
Security headers are set in [vercel.json](vercel.json).
```

- [ ] **Step 4: Commit**

```bash
git add vercel.json README.md
git commit -m "chore: tighten CSP to self-hosted assets; update README"
```

---

### Task 7: Verification sweep and PR

**Files:**
- No new files. Runs checks; opens the PR.

**Interfaces:**
- Consumes: everything above.
- Produces: a reviewable PR from `redesign/fleet-register` into `main`.

- [ ] **Step 1: Run both CI commands exactly as CI does**

```bash
npx --yes html-validate@9 index.html && node -e "JSON.parse(require('fs').readFileSync('vercel.json','utf8')); console.log('vercel.json ok')"
```

Expected: both pass.

- [ ] **Step 2: Contrast audit (stdlib script; all pairs must meet the floor)**

```bash
python3 - <<'EOF'
def L(hex):
    c = [int(hex[i:i+2],16)/255 for i in (1,3,5)]
    c = [x/12.92 if x <= .03928 else ((x+.055)/1.055)**2.4 for x in c]
    return .2126*c[0] + .7152*c[1] + .0722*c[2]
def ratio(a, b):
    la, lb = sorted((L(a), L(b)), reverse=True)
    return (la+.05)/(lb+.05)
pairs = [  # (fg, bg, floor, label)
  ("#1a2338","#f7f5ef",4.5,"light ink/paper"),
  ("#5d6473","#f7f5ef",4.5,"light muted/paper"),
  ("#8a6b39","#f7f5ef",4.5,"light gold-ink/paper"),
  ("#ece7da","#0e1526",4.5,"dark ink/paper"),
  ("#a2aaba","#0e1526",4.5,"dark muted/paper"),
  ("#d9bd85","#0e1526",4.5,"dark gold-ink/paper"),
]
ok = True
for fg, bg, floor, label in pairs:
    r = ratio(fg, bg)
    ok &= r >= floor
    print(f"{label}: {r:.2f} (floor {floor})", "PASS" if r >= floor else "FAIL")
print("ALL PASS" if ok else "CONTRAST FAILURE")
EOF
```

Expected: `ALL PASS`. (Status dots are exempt from non-text contrast: they are
redundant with the adjacent status words.)

- [ ] **Step 3: Link inventory**

Confirm `index.html` contains exactly these outbound references and no others:
`https://portfolio.windwardline.com` (×2), `https://levelflow.windwardline.com`,
`https://github.com/windwardline`,
`mailto:support@windwardline.com`.

```bash
grep -o 'href="[^"]*"' index.html | sort | uniq -c
```

- [ ] **Step 4: Final visual pass**

Repeat Task 5 Step 3's checklist once on the finished branch (both themes, 320px, print).

- [ ] **Step 5: Push and open the PR — confirm with the owner first**

Per repo policy, pushing publishes. Get an explicit go-ahead, then:

```bash
git push -u origin redesign/fleet-register
gh pr create --title "Rebuild apex as the fleet register" --body "$(cat <<'EOF'
## Summary
- Rebuilds the apex page as the approved Fleet Register design (spec in docs/superpowers/specs/)
- One-flag identity: roundel burgee, three renditions, theme-aware favicon
- Self-hosted EB Garamond; CSP tightened to 'self' for styles and fonts
- Dual light/dark theme by OS preference; print styles; no JavaScript

## Verification
- html-validate@9 and vercel.json parse check pass (CI commands run locally)
- Contrast audit: all six text/ground pairs ≥ 4.5:1 in both themes
- Visual pass: light, dark, 320px, and print
EOF
)"
```

Expected: PR URL printed. Merging to `main` deploys to production via Vercel.

- [ ] **Step 6: Post-merge live check** (after the owner merges)

Once the production deploy finishes, load https://windwardline.com and verify:
fonts served from windwardline.com (network panel, no third-party hosts), zero
CSP violations in the console, favicon renders in both browser themes.

