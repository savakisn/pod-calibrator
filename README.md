# Pod Calibrator

Commander (MTG) deck analyzer. Paste a Moxfield or Archidekt deck URL and get a
shareable card showing bracket, speed tier, win conditions, ramp/removal counts,
and a mana curve. Add multiple decks to see a side-by-side pod comparison with
spread analysis and an exportable JPEG.

Hosted at [your Vercel URL]. Frontend on Vercel, backend on Railway.

## Stack

- Frontend: Next.js 14 (App Router), React, TypeScript, Tailwind
- Backend: Python 3.11, Flask, gunicorn, PIL for image generation
- Caching: in-memory LRU, 4-hour TTL, 500-entry cap
- External APIs: Moxfield, Archidekt, Commander Spellbook (for bracket scoring),
  Scryfall (card art only, on demand)
- Analytics: PostHog (optional, opt-in via `NEXT_PUBLIC_POSTHOG_KEY`)

No database. Everything is computed from the deck JSON returned by Moxfield or
Archidekt.

## Dev setup

```bash
# Frontend
cd frontend
npm install
npm run dev          # http://localhost:3000

# Backend (new terminal)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m flask --app src.main run --host 0.0.0.0 --port 8000
```

Frontend reads `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000`). For
analytics, set `NEXT_PUBLIC_POSTHOG_KEY` and optionally
`NEXT_PUBLIC_POSTHOG_HOST` (defaults to `https://us.i.posthog.com`).

## License

MIT. See `LICENSE`.
