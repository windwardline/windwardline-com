# windwardline.com

The apex site for Windward Line, a founder-held holding company. Four divisions —
Labs, Capital, Strategy, Creative — and one affiliated venture,
[Refactored](https://wearerefactored.com).

Static site, no build step: one HTML file, one stylesheet, self-hosted
EB Garamond, and the house flag as inline SVG. Light and dark themes follow the
OS. Design spec: [docs/superpowers/specs/2026-07-25-apex-redesign-design.md](docs/superpowers/specs/2026-07-25-apex-redesign-design.md).

Deployed on Vercel; DNS on Cloudflare. Pushes to `main` deploy to production.
Security headers are set in [vercel.json](vercel.json).
