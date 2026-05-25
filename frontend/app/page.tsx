'use client'

import { useState } from 'react'
import DeclistForm from '@/components/DeclistForm'
import DeckCard from '@/components/DeckCard'

export default function Home() {
  const [analysis, setAnalysis] = useState<unknown>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const handleAnalyze = async (url: string) => {
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

  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="max-w-4xl mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2">Pod Calibrator</h1>
          <p className="text-gray-600">
            Know your deck's power level before you sit down
          </p>
        </div>

        <div className="flex flex-col gap-8">
          <div className="w-full max-w-xl mx-auto">
            <DeclistForm onSubmit={handleAnalyze} loading={loading} />
          </div>

          {(error || analysis) && (
            <div className="w-full">
              {error && (
                <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-lg mb-4 max-w-xl mx-auto">
                  {error}
                </div>
              )}
              <div className="flex justify-center">
                <DeckCard analysis={analysis} />
              </div>
            </div>
          )}
        </div>
      </div>
    </main>
  )
}
