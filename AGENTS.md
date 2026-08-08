# windwardline.com — operating contract

Operating contract for AI work in this repo; the global `~/AGENTS.md` still applies. The apex site of Windward Line — the Register of Divisions (Labs, Strategy, Media). Static HTML/CSS with one script, the theme lamp. Live at windwardline.com.

## Commands

Preview: `python3 -m http.server 4180` (mirrors the untracked `.claude/launch.json`). CI-equivalent: `npx --yes html-validate@9 index.html` · JSON-parse `vercel.json`.

## Gates

CI is html-validate on `index.html` plus the `vercel.json` parse — nothing else is validated. Push to main deploys production. A parallel `security.yml` (PRs, pushes, weekly cron) gates Semgrep and secret scan; a post-deploy job asserts the production security headers. An advisory Claude review runs on every same-repo PR via `claude-review.yml`, which deliberately calls the fleet reusable at `@main` — one merge updates every repo. It activates only when the `CLAUDE_CODE_OAUTH_TOKEN` secret is present — reviews bill the owner's Claude subscription, not Console credits; fork PRs never receive secrets, so they skip it by security design.

## Laws

- CSP in `vercel.json` is the hard constraint: `default-src 'self'`, no `frame-src`, `form-action 'none'`, `frame-ancestors 'none'`. No iframe, form, or inline script/style can ship without editing `vercel.json` — the only place headers exist. The apex deliberately carries no booking embed; `/schedule` pages live on the division sites.
- Design is spec-locked: `docs/superpowers/specs/2026-07-25-apex-redesign-design.md` and the fleet-register plan. One flag rule — fixed swallowtail geometry (`M0 0 H34 L23.5 10.5 L34 21 H0 Z`; the small ≤32px cut uses `L21.5`). Marks in type or ruled geometry only, no freehand SVG paths. Renditions switch by theme token, never by markup.
- The register lists live divisions only — labs, strategy, media as of 2026-08. Capital stood down and Refactored is retired; check history before re-adding anything.
- `script.js` loads blocking in `<head>` so the stored theme applies before first paint.
- Contact is hello@windwardline.com. `.vercelignore` excludes `docs/` — specs never serve.
