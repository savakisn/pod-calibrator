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
      <label className="block text-sm font-medium mb-2">
        Deck URL (Moxfield or Archidekt)
      </label>
      <div className="flex gap-2">
        <input
          type="url"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          placeholder="https://moxfield.com/decks/... or https://archidekt.com/decks/..."
          className="flex-1 p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || url.trim() === ''}
          className="bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed whitespace-nowrap"
        >
          {loading ? 'Analyzing...' : 'Analyze'}
        </button>
      </div>
    </form>
  )
}
