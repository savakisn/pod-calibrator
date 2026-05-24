'use client'

import { useState } from 'react'

type Mode = 'url' | 'text'

interface FormProps {
  onSubmitUrl: (url: string) => Promise<void>
  onSubmitText: (decklist: string) => Promise<void>
  loading: boolean
}

export default function DeclistForm({ onSubmitUrl, onSubmitText, loading }: FormProps) {
  const [mode, setMode] = useState<Mode>('url')
  const [url, setUrl] = useState('')
  const [decklist, setDecklist] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (mode === 'url') {
      await onSubmitUrl(url)
    } else {
      await onSubmitText(decklist)
    }
  }

  const canSubmit = mode === 'url' ? url.trim() !== '' : decklist.trim() !== ''

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl">
      <div className="flex mb-4 border border-gray-300 rounded-lg overflow-hidden">
        <button
          type="button"
          onClick={() => setMode('url')}
          className={`flex-1 py-2 text-sm font-medium transition-colors ${
            mode === 'url'
              ? 'bg-blue-600 text-white'
              : 'bg-white text-gray-600 hover:bg-gray-50'
          }`}
        >
          Import from URL
        </button>
        <button
          type="button"
          onClick={() => setMode('text')}
          className={`flex-1 py-2 text-sm font-medium transition-colors ${
            mode === 'text'
              ? 'bg-blue-600 text-white'
              : 'bg-white text-gray-600 hover:bg-gray-50'
          }`}
        >
          Paste Decklist
        </button>
      </div>

      <div className="mb-4">
        {mode === 'url' ? (
          <>
            <label className="block text-sm font-medium mb-2">
              Moxfield URL
            </label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://moxfield.com/decks/..."
              className="w-full p-3 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              disabled={loading}
            />
          </>
        ) : (
          <>
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
          </>
        )}
      </div>

      <button
        type="submit"
        disabled={loading || !canSubmit}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
      >
        {loading ? 'Analyzing...' : 'Analyze Deck'}
      </button>
    </form>
  )
}
