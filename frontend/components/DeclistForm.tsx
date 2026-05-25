'use client'

import { useState } from 'react'

interface FormProps {
  onSubmit: (url: string) => Promise<void>
  loading: boolean
}

export default function DeclistForm({ onSubmit, loading }: FormProps) {
  const [url, setUrl] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await onSubmit(url)
  }

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <label className="block text-sm font-medium mb-2 text-slate-400">
        Deck URL (Moxfield or Archidekt)
      </label>
      <div className="flex gap-2">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://moxfield.com/decks/..."
          className="flex-1 p-3 bg-slate-800 border border-slate-700 rounded-lg text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-600"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || url.trim() === ''}
          className="bg-amber-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-amber-500 disabled:bg-slate-700 disabled:text-slate-500 disabled:cursor-not-allowed whitespace-nowrap transition-colors"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </form>
  )
}
