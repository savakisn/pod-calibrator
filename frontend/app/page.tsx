'use client'

import { useState } from 'react'
import DeckCard, { type DeckAnalysis, type ColorMode } from '@/components/DeckCard'
import PodView from '@/components/PodView'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

async function fetchDeck(url: string): Promise<DeckAnalysis> {
  const res = await fetch(`${API_URL}/api/import`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ url: url.trim() }),
  })
  const data = await res.json()
  if (!res.ok) throw new Error(data.error || 'Failed to import deck')
  return data
}

export default function Home() {
  const [decks, setDecks] = useState<DeckAnalysis[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [colorMode, setColorMode] = useState<ColorMode>('default')

  const loadUrls = async (raw: string) => {
    const urls = raw.split(/[\s,]+/).map(u => u.trim()).filter(Boolean)
    if (!urls.length) return
    setLoading(true)
    setError('')
    try {
      const results = await Promise.all(urls.map(fetchDeck))
      setDecks(prev => [...prev, ...results])
      setInput('')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to import deck')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    loadUrls(input)
  }

  const removeDeck = (i: number) => setDecks(prev => prev.filter((_, idx) => idx !== i))

  const isPod = decks.length >= 2

  return (
    <main className="min-h-screen bg-slate-950 p-4">
      <div className="max-w-5xl mx-auto">

        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2 text-amber-400">Pod Calibrator</h1>
          <p className="text-slate-500">Know your deck's power level before you sit down</p>
        </div>

        {/* Input */}
        <div className="w-full max-w-xl mx-auto mb-8">
          <form onSubmit={handleSubmit} className="w-full">
            <label className="block text-sm font-medium mb-2 text-slate-400">
              {decks.length === 0
                ? 'Paste one or more deck URLs (Moxfield or Archidekt)'
                : 'Add more decks (separate multiple URLs with a space or comma)'}
            </label>
            <div className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={e => setInput(e.target.value)}
                placeholder={decks.length === 0 ? 'https://moxfield.com/decks/... or paste multiple' : 'https://...'}
                className="flex-1 p-3 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-600"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !input.trim()}
                className="bg-amber-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed whitespace-nowrap transition-colors"
              >
                {loading ? 'Loading...' : decks.length === 0 ? 'Analyze' : 'Add to Pod'}
              </button>
            </div>
          </form>
          {decks.length > 0 && (
            <button
              onClick={() => setDecks([])}
              className="mt-2 text-xs text-slate-600 hover:text-slate-400 transition-colors"
            >
              Clear all decks
            </button>
          )}
        </div>

        {error && (
          <div className="bg-red-950/50 border border-red-800 text-red-300 p-4 rounded-lg mb-6 max-w-xl mx-auto">
            {error}
          </div>
        )}

        {decks.length > 0 && (
          <div className="flex gap-1 justify-center mb-6">
            {(['default', 'tritanopia'] as ColorMode[]).map(mode => (
              <button key={mode} onClick={() => setColorMode(mode)} className={`text-xs px-2 py-0.5 rounded border transition-colors ${colorMode === mode ? 'border-slate-500 bg-slate-700 text-slate-200' : 'border-slate-800 text-slate-600 hover:text-slate-400 hover:border-slate-700'}`}>
                {mode === 'default' ? 'Red/Green' : 'Tritanopia'}
              </button>
            ))}
          </div>
        )}

        {/* Solo view */}
        {decks.length === 1 && (
          <div className="flex justify-center">
            <div className="relative">
              <button
                onClick={() => removeDeck(0)}
                className="absolute -top-2 -right-2 z-10 text-slate-600 hover:text-red-400 text-xs border border-slate-700 hover:border-red-800 bg-slate-900 rounded-full w-5 h-5 flex items-center justify-center transition-colors"
              >
                ×
              </button>
              <DeckCard analysis={decks[0]} colorMode={colorMode} />
            </div>
          </div>
        )}

        {/* Pod view */}
        {isPod && (
          <PodView decks={decks} onRemove={removeDeck} />
        )}

      </div>
    </main>
  )
}
