# Pod Calibrator

Commander deck analyzer for Magic: The Gathering. Users paste a decklist, get a shareable deck card showing bracket score, power level, win conditions, and stats.

## Stack

- Frontend: Next.js 14, React, TypeScript, Tailwind
- Backend: Python FastAPI
- Database: Supabase PostgreSQL
- APIs: Scryfall, Commander Spellbook

## Dev Setup

```bash
# Frontend
cd frontend
npm install
npm run dev

# Backend (new terminal)
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000
```

Frontend: http://localhost:3000
Backend: http://localhost:8000
