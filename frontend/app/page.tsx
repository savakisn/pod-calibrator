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
  detected_combos: unknown[]
  bracket_score?: number
  power_label?: string
  precon_match?: string
  win_conditions: string[]
  speed?: number
}

export default function Home() {
  const [analysis, setAnalysis] = useState<DeckAnalysis | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleAnalyze = async (decklist: string) => {
    setLoading(true)
    setError('')
    try {
      const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
      const response = await fetch(`${apiUrl}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ decklist })
      })

      if (!response.ok) {
        throw new Error('Failed to analyze deck')
      }

      const data = await response.json()
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
            Analyze your Commander deck before you sit down at the table
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8 items-start lg:items-start">
          <div className="w-full lg:w-1/2">
            <DeclistForm onSubmit={handleAnalyze} loading={loading} />
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
