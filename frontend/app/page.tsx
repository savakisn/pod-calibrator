'use client'

import { useState } from 'react'
import DeclistForm from '@/components/DeclistForm'
import DeckCard from '@/components/DeckCard'

interface DeckAnalysis {
  cards: unknown[]
  commander?: unknown
  card_count: number
  avg_cmc: number
  colors: Record<string, number>
  card_types: Record<string, number>
  mana_curve: Record<string, number>
  bracket?: unknown
  detected_combos: unknown[]
  precon_match?: string
  win_conditions: string[]
}

export default function Home() {
  const [analysis, setAnalysis] = useState<DeckAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const handleAnalyzeUrl = async (url: string) => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${apiUrl}/api/import`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Failed to import deck')
      setAnalysis(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  const handleAnalyzeText = async (decklist: string) => {
    setLoading(true)
    setError('')
    try {
      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decklist })
      })
      const data = await response.json()
      if (!response.ok) throw new Error(data.error || 'Failed to analyze deck')
      setAnalysis(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2">Pod Calibrator</h1>
          <p className="text-gray-600">
            Know your deck's power level before you sit down
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8 items-start lg:items-start">
          <div className="w-full lg:w-1/2">
            <DeclistForm onSubmitUrl={handleAnalyzeUrl} onSubmitText={handleAnalyzeText} loading={loading} />
          </div>

          <div className="w-full lg:w-1/2">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-4">
                {error}
              </div>
            )}
            <DeckCard analysis={analysis} />
          </div>
        </div>
      </div>
    </main>
  )
}
