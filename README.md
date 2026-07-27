# windwardline.com

The apex site for Windward Line, a private holding company. Four divisions —
Labs, Capital, Strategy, Media — and one affiliated venture,
[Refactored](https://wearerefactored.com). Every division flies at its own
subdomain, and the footer musters all four flags beneath the house flag.

Static site, no build step: one HTML file, one stylesheet, self-hosted
EB Garamond, and the house and division flags as inline SVG. Light and dark themes follow the
OS unless the lamp (light / dark / system) has stored a choice. Design spec: [docs/superpowers/specs/2026-07-25-apex-redesign-design.md](docs/superpowers/specs/2026-07-25-apex-redesign-design.md).

Deployed on Vercel; DNS on Cloudflare. Pushes to `main` deploy to production.
Security headers are set in [vercel.json](vercel.json).
