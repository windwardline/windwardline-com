# windwardline.com

The apex site for Windward Line, a private holding company. Four divisions —
Labs, Capital, Strategy, Creative — and one affiliated venture,
[Refactored](https://wearerefactored.com). Labs and Capital are in service at
[labs.windwardline.com](https://labs.windwardline.com) and
[capital.windwardline.com](https://capital.windwardline.com).

Static site, no build step: one HTML file, one stylesheet, self-hosted
EB Garamond, and the house and division flags as inline SVG. Light and dark themes follow the
OS unless the lamp (light / dark / system) has stored a choice. Design spec: [docs/superpowers/specs/2026-07-25-apex-redesign-design.md](docs/superpowers/specs/2026-07-25-apex-redesign-design.md).

Deployed on Vercel; DNS on Cloudflare. Pushes to `main` deploy to production.
Security headers are set in [vercel.json](vercel.json).
