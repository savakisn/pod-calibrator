'use client'

import { useState } from 'react'

interface FormProps {
  onSubmit: (decklist: string) => Promise<void>
  loading: boolean
}

export default function DeclistForm({ onSubmit, loading }: FormProps) {
  const [decklist, setDecklist] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    await onSubmit(decklist)
  }

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl">
      <div className="mb-4">
        <label className="block text-sm font-medium mb-2">
          Paste your decklist
        </label>
        <textarea
          value={decklist}
          onChange={(e) => setDecklist(e.target.value)}
          placeholder="1x Urza, Lord High Artificer&#10;1x Sol Ring&#10;98x Island"
          className="w-full h-64 p-3 border border-gray-300 rounded-lg font-mono text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
      </div>
      <button
        type="submit"
        disabled={loading || !decklist.trim()}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {loading ? 'Analyzing...' : 'Analyze Deck'}
      </button>
    </form>
  )
}
