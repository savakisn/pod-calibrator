'use client'

interface Card {
  name: string
  quantity: number
  cmc?: number
  colors?: string[]
  type_line?: string
  image_uris?: Record<string, string>
}

interface DeckAnalysis {
  cards: Card[]
  commander?: Card
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

interface DeckCardProps {
  analysis: DeckAnalysis | null
}

export default function DeckCard({ analysis }: DeckCardProps) {
  if (!analysis) return null

  const colorNames: Record<string, string> = {
    white: 'W',
    blue: 'U',
    black: 'B',
    red: 'R',
    green: 'G',
    colorless: 'C'
  }

  return (
    <div className="w-full max-w-2xl bg-white border-2 border-gray-800 rounded-lg p-6 shadow-lg">
      <div className="mb-4">
        <h2 className="text-2xl font-bold mb-1">
          {analysis.commander?.name || 'Deck'}
        </h2>
        <p className="text-gray-600">
          {analysis.card_count} cards · Avg CMC: {analysis.avg_cmc}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div>
          <h3 className="font-semibold text-sm uppercase text-gray-700 mb-2">
            Colors
          </h3>
          <div className="flex gap-2">
            {Object.entries(analysis.colors).map(([color, count]) => (
              <div key={color} className="flex items-center gap-1">
                <span className="text-sm font-medium">
                  {colorNames[color] || color}
                </span>
                <span className="text-xs text-gray-600">({count})</span>
              </div>
            ))}
            {Object.keys(analysis.colors).length === 0 && (
              <span className="text-sm text-gray-500">Colorless</span>
            )}
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-sm uppercase text-gray-700 mb-2">
            Card Types
          </h3>
          <div className="text-sm space-y-1 max-h-24 overflow-y-auto">
            {Object.entries(analysis.card_types)
              .sort((a, b) => b[1] - a[1])
              .slice(0, 5)
              .map(([type, count]) => (
                <div key={type} className="flex justify-between">
                  <span className="capitalize">{type}</span>
                  <span className="text-gray-600">{count}</span>
                </div>
              ))}
          </div>
        </div>
      </div>

      <div>
        <h3 className="font-semibold text-sm uppercase text-gray-700 mb-2">
          Mana Curve
        </h3>
        <div className="flex gap-1 h-24">
          {[0, 1, 2, 3, 4, 5, 6, 7].map((cmc) => {
            const count = analysis.mana_curve[String(cmc)] || 0
            const maxCount = Math.max(
              ...Object.values(analysis.mana_curve).map(Number)
            )
            const height = maxCount > 0 ? (count / maxCount) * 100 : 0
            return (
              <div key={cmc} className="flex-1 flex flex-col items-center gap-1">
                <div className="w-full bg-blue-300 rounded" style={{ height: `${height}%` }} />
                <span className="text-xs text-gray-600">{cmc}</span>
              </div>
            )
          })}
        </div>
      </div>

      {analysis.cards.length > 0 && (
        <div className="mt-6 pt-4 border-t">
          <h3 className="font-semibold text-sm uppercase text-gray-700 mb-3">
            Cards
          </h3>
          <div className="space-y-2 max-h-64 overflow-y-auto text-sm">
            {analysis.cards.slice(0, 15).map((card, i) => (
              <div key={i} className="flex justify-between">
                <span>{card.quantity}x {card.name}</span>
                {card.cmc && <span className="text-gray-600">{card.cmc}</span>}
              </div>
            ))}
            {analysis.cards.length > 15 && (
              <div className="text-gray-500 text-xs">
                ...and {analysis.cards.length - 15} more
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
