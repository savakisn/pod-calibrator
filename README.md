# Pod Calibrator

Commander (MTG) deck analyzer. Paste a Moxfield or Archidekt URL to get a shareable card with bracket, speed tier, win conditions, ramp/removal counts, and mana curve. Add multiple decks for a side-by-side pod comparison and exportable JPEG.

No database; everything is computed from the deck JSON. Frontend on Vercel, backend on Railway.

## Stack

- Frontend: Next.js 14, React 18, TypeScript, Tailwind
- Backend: Python, Flask, gunicorn, Pillow (image generation)
- External APIs: Moxfield, Archidekt, Commander Spellbook (bracket), Scryfall (card art)
- Caching: in-memory LRU, 4h TTL, 500-entry cap
- Analytics: PostHog (optional, via `NEXT_PUBLIC_POSTHOG_KEY`)

## Dev setup

```bash
# Frontend
cd frontend && npm install && npm run dev   # http://localhost:3000

# Backend (new terminal)
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python -m flask --app src.main run --host 0.0.0.0 --port 8000
```

Frontend reads `NEXT_PUBLIC_API_URL` (defaults to `http://localhost:8000`). For analytics, set `NEXT_PUBLIC_POSTHOG_KEY` and optionally `NEXT_PUBLIC_POSTHOG_HOST`.

## License

MIT. See `LICENSE`.
