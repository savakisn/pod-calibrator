'use client'

interface Card {
  name: string
  quantity: number
  cmc?: number
  colors?: string[]
  type_line?: string
  image_uris?: Record<string, string>
}

interface BracketResult {
  bracket: number
  bracket_label: string
  game_changer_count: number
  game_changers_found: string[]
  mass_land_denial: string[]
  extra_turns: string[]
}

interface DeckAnalysis {
  cards: Card[]
  commander?: Card
  card_count: number
  avg_cmc: number
  colors: Record<string, number>
  card_types: Record<string, number>
  mana_curve: Record<string, number>
  bracket?: BracketResult
  detected_combos: unknown[]
  precon_match?: string
  win_conditions: string[]
}

interface DeckCardProps {
  analysis: DeckAnalysis | null
}

const BRACKET_COLORS: Record<number, string> = {
  1: 'bg-green-100 text-green-800 border-green-300',
  2: 'bg-blue-100 text-blue-800 border-blue-300',
  3: 'bg-yellow-100 text-yellow-800 border-yellow-300',
  4: 'bg-orange-100 text-orange-800 border-orange-300',
  5: 'bg-red-100 text-red-800 border-red-300',
}

const COLOR_SYMBOLS: Record<string, string> = {
  white: 'W', blue: 'U', black: 'B', red: 'R', green: 'G', colorless: 'C'
}

export default function DeckCard({ analysis }: DeckCardProps) {
  if (!analysis) return null

  const bracket = analysis.bracket

  return (
    <div className="w-full max-w-2xl bg-white border-2 border-gray-800 rounded-lg p-6 shadow-lg">

      {/* Header */}
      <div className="mb-5">
        <h2 className="text-2xl font-bold mb-1">
          {analysis.commander?.name || 'Deck'}
        </h2>
        <p className="text-gray-500 text-sm">
          {analysis.card_count} cards · Avg CMC: {analysis.avg_cmc}
        </p>
      </div>

      {/* Bracket */}
      {bracket && (
        <div className={`border rounded-lg p-4 mb-5 ${BRACKET_COLORS[bracket.bracket]}`}>
          <div className="flex items-center justify-between mb-2">
            <span className="text-xl font-bold">
              Bracket {bracket.bracket} — {bracket.bracket_label}
            </span>
            <span className="text-sm font-medium">
              {bracket.game_changer_count} game changer{bracket.game_changer_count !== 1 ? 's' : ''}
            </span>
          </div>
          {bracket.game_changers_found.length > 0 && (
            <div className="text-sm mt-1">
              <span className="font-medium">Found: </span>
              {bracket.game_changers_found.join(', ')}
            </div>
          )}
          {bracket.mass_land_denial.length > 0 && (
            <div className="text-sm mt-1">
              <span className="font-medium">MLD: </span>
              {bracket.mass_land_denial.join(', ')}
            </div>
          )}
          {bracket.extra_turns.length > 0 && (
            <div className="text-sm mt-1">
              <span className="font-medium">Extra turns: </span>
              {bracket.extra_turns.join(', ')}
            </div>
          )}
        </div>
      )}

      {/* Colors + Card Types */}
      <div className="grid grid-cols-2 gap-4 mb-5">
        <div>
          <h3 className="font-semibold text-xs uppercase text-gray-500 mb-2">Colors</h3>
          <div className="flex flex-wrap gap-2">
            {Object.entries(analysis.colors).map(([color, count]) => (
              <div key={color} className="flex items-center gap-1">
                <span className="text-sm font-medium">{COLOR_SYMBOLS[color] || color}</span>
                <span className="text-xs text-gray-500">({count})</span>
              </div>
            ))}
            {Object.keys(analysis.colors).length === 0 && (
              <span className="text-sm text-gray-400">Colorless</span>
            )}
          </div>
        </div>

        <div>
          <h3 className="font-semibold text-xs uppercase text-gray-500 mb-2">Card Types</h3>
          <div className="text-sm space-y-1">
            {Object.entries(analysis.card_types)
              .sort((a, b) => b[1] - a[1])
              .map(([type, count]) => (
                <div key={type} className="flex justify-between">
                  <span className="capitalize">{type}</span>
                  <span className="text-gray-500">{count}</span>
                </div>
              ))}
          </div>
        </div>
      </div>

      {/* Mana Curve */}
      <div className="mb-5">
        <h3 className="font-semibold text-xs uppercase text-gray-500 mb-2">Mana Curve</h3>
        <div className="flex gap-1 h-20 items-end">
          {[0, 1, 2, 3, 4, 5, 6, 7].map((cmc) => {
            const count = analysis.mana_curve[String(cmc)] || 0
            const maxCount = Math.max(...Object.values(analysis.mana_curve).map(Number), 1)
            const height = (count / maxCount) * 100
            return (
              <div key={cmc} className="flex-1 flex flex-col items-center gap-1">
                {count > 0 && (
                  <span className="text-xs text-gray-500">{count}</span>
                )}
                <div
                  className="w-full bg-blue-400 rounded-t"
                  style={{ height: `${height}%`, minHeight: count > 0 ? '4px' : '0' }}
                />
                <span className="text-xs text-gray-500">{cmc}</span>
              </div>
            )
          })}
        </div>
      </div>

      {/* Card list */}
      {analysis.cards.length > 0 && (
        <div className="pt-4 border-t">
          <h3 className="font-semibold text-xs uppercase text-gray-500 mb-3">Cards</h3>
          <div className="space-y-1 max-h-64 overflow-y-auto text-sm">
            {analysis.cards.map((card, i) => (
              <div key={i} className="flex justify-between">
                <span>{card.quantity}x {card.name}</span>
                {card.cmc !== undefined && (
                  <span className="text-gray-400">{card.cmc}</span>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
