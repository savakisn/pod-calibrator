'use client'

import { useRef } from 'react'
import ShareCard from './ShareCard'

interface Card {
  name: string
  quantity: number
  cmc?: number
  colors?: string[]
  type_line?: string
  image_uris?: Record<string, string>
}

interface Combo {
  produces: string[]
  lines: string[][]
}

interface BracketResult {
  bracket: number
  bracket_label: string
  game_changer_count: number
  game_changers_found: string[]
  mass_land_denial: string[]
  extra_turns: string[]
  combos: Combo[]
  error?: string
}

interface SpeedResult {
  label: string
  avg_nonland_cmc: number
  ramp_count: number
}

interface Interaction {
  removal: number
  board_wipes: number
  counterspells: number
  tutors: number
}

export interface DeckAnalysis {
  cards: Card[]
  commander?: Card
  card_count: number
  avg_cmc: number
  colors: Record<string, number>
  card_types: Record<string, number>
  mana_curve: Record<string, number>
  bracket?: BracketResult
  speed?: SpeedResult
  interaction?: Interaction
  detected_combos: unknown[]
  precon_match?: string
  win_conditions: string[]
}

interface DeckCardProps {
  analysis: DeckAnalysis | null
}

const TYPE_ORDER = ['Creature', 'Planeswalker', 'Instant', 'Sorcery', 'Enchantment', 'Artifact', 'Land', 'Other']
const SUPERTYPES = new Set(['Basic', 'Legendary', 'Snow', 'World'])

function primaryType(type_line: string | undefined): string {
  if (!type_line) return 'Other'
  const part = type_line.split('—')[0].split('//')[0].trim()
  const words = part.split(' ').filter(w => !SUPERTYPES.has(w))
  const t = words[0] || 'Other'
  return TYPE_ORDER.includes(t) ? t : 'Other'
}

function CardsByType({ cards }: { cards: Card[] }) {
  const groups: Record<string, Card[]> = {}
  for (const card of cards) {
    const t = primaryType(card.type_line)
    if (!groups[t]) groups[t] = []
    groups[t].push(card)
  }
  return (
    <div className="space-y-4 text-sm">
      {TYPE_ORDER.filter(t => groups[t]).map(type => (
        <div key={type}>
          <div className="font-semibold text-xs uppercase text-slate-500 tracking-wider mb-1">
            {type} ({groups[type].reduce((s, c) => s + c.quantity, 0)})
          </div>
          <div className="space-y-0.5">
            {groups[type]
              .sort((a, b) => (a.cmc ?? 0) - (b.cmc ?? 0))
              .map((card, i) => (
                <div key={i} className="flex justify-between">
                  <span className="text-slate-300">{card.quantity > 1 ? `${card.quantity}x ` : ''}{card.name}</span>
                  {card.cmc !== undefined && (
                    <span className="text-slate-600 ml-2 shrink-0">{card.cmc}</span>
                  )}
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  )
}

const SPEED_COLORS: Record<string, string> = {
  Turbo:        'bg-red-900/50 border-red-700 text-red-300',
  Fast:         'bg-orange-900/50 border-orange-700 text-orange-300',
  Balanced:     'bg-yellow-900/50 border-yellow-700 text-yellow-300',
  Slow:         'bg-blue-900/50 border-blue-700 text-blue-300',
  Battlecruiser:'bg-slate-700 border-slate-600 text-slate-300',
}

const BRACKET_BORDER: Record<number, string> = {
  1: 'border-green-500',
  2: 'border-blue-500',
  3: 'border-yellow-500',
  4: 'border-orange-500',
  5: 'border-red-500',
}

const BRACKET_NUM_COLOR: Record<number, string> = {
  1: 'text-green-400',
  2: 'text-blue-400',
  3: 'text-yellow-400',
  4: 'text-orange-400',
  5: 'text-red-400',
}

const COLOR_SYMBOLS: Record<string, string> = {
  white: 'W', blue: 'U', black: 'B', red: 'R', green: 'G', colorless: 'C'
}

const COLOR_BADGE: Record<string, string> = {
  white:    'bg-amber-50 text-amber-900',
  blue:     'bg-blue-600 text-white',
  black:    'bg-slate-600 text-white',
  red:      'bg-red-600 text-white',
  green:    'bg-green-600 text-white',
  colorless:'bg-slate-500 text-white',
}

export default function DeckCard({ analysis }: DeckCardProps) {
  const shareRef = useRef<HTMLDivElement>(null)

  if (!analysis) return null

  const bracket = analysis.bracket

  const handleExport = async () => {
    if (!shareRef.current) return
    const html2canvas = (await import('html2canvas')).default
    const canvas = await html2canvas(shareRef.current, {
      backgroundColor: '#0f172a',
      scale: 2,
      useCORS: true,
      logging: false,
    })
    const link = document.createElement('a')
    const name = analysis.commander?.name?.replace(/[^a-z0-9]/gi, '-') || 'deck'
    link.download = `${name}-pod-calibrator.jpg`
    link.href = canvas.toDataURL('image/jpeg', 0.92)
    link.click()
  }

  return (
    <>
      <div style={{ position: 'fixed', left: -9999, top: 0, zIndex: -1 }}>
        <ShareCard ref={shareRef} analysis={analysis} />
      </div>

      <div className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-xl p-6 shadow-2xl">

        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex-1 min-w-0">
            <h2 className="text-3xl font-black text-amber-400 mb-1 leading-tight truncate">
              {analysis.commander?.name || 'Deck'}
            </h2>
            <p className="text-slate-500 text-sm">
              {analysis.card_count} cards · avg CMC {analysis.avg_cmc}
            </p>
          </div>
          <button
            onClick={handleExport}
            className="ml-4 text-xs text-slate-500 hover:text-amber-400 border border-slate-700 hover:border-amber-700/50 rounded-lg px-3 py-1.5 transition-colors shrink-0"
          >
            Export
          </button>
        </div>

        {/* Speed + Win Conditions */}
        <div className="flex flex-wrap items-center gap-2 mb-5">
          {analysis.speed && (
            <span className={`text-xs px-2 py-0.5 rounded border font-bold tracking-wide ${SPEED_COLORS[analysis.speed.label] || ''}`}>
              {analysis.speed.label}
            </span>
          )}
          {analysis.win_conditions?.map(wc => (
            <span key={wc} className="text-xs px-2 py-0.5 rounded border font-semibold bg-slate-800 text-slate-300 border-slate-600">
              {wc}
            </span>
          ))}
          {analysis.speed && (
            <span className="text-xs text-slate-600">
              {analysis.speed.avg_nonland_cmc} avg · {analysis.speed.ramp_count} ramp
            </span>
          )}
        </div>

        {/* Bracket */}
        {bracket?.error && (
          <div className="border-l-4 border-slate-600 pl-4 mb-5 text-slate-500 text-sm py-1">
            Bracket unavailable (Spellbook offline)
          </div>
        )}
        {bracket && !bracket.error && (
          <div className={`border-l-4 pl-4 mb-5 py-1 ${BRACKET_BORDER[bracket.bracket]}`}>
            <div className="flex items-baseline gap-3 mb-2">
              <span className={`text-5xl font-black leading-none ${BRACKET_NUM_COLOR[bracket.bracket]}`}>
                {bracket.bracket}
              </span>
              <div>
                <div className="text-base font-bold text-slate-200 leading-tight">{bracket.bracket_label}</div>
                <div className="text-xs text-slate-500">
                  {bracket.game_changer_count} game changer{bracket.game_changer_count !== 1 ? 's' : ''}
                </div>
              </div>
            </div>
            <div className="space-y-1 text-sm text-slate-400">
              {bracket.game_changers_found.length > 0 && (
                <div><span className="text-slate-500">Found: </span>{bracket.game_changers_found.join(', ')}</div>
              )}
              {bracket.mass_land_denial.length > 0 && (
                <div><span className="text-slate-500">MLD: </span>{bracket.mass_land_denial.join(', ')}</div>
              )}
              {bracket.extra_turns.length > 0 && (
                <div><span className="text-slate-500">Extra turns: </span>{bracket.extra_turns.join(', ')}</div>
              )}
            </div>
            {bracket.combos.length > 0 && (
              <div className="mt-3 pt-3 border-t border-slate-700/50 space-y-2">
                <div className="text-xs text-slate-500 uppercase tracking-wider">
                  {bracket.combos.length} combo{bracket.combos.length !== 1 ? 's' : ''} detected
                </div>
                {bracket.combos.map((combo, i) => (
                  <div key={i} className="text-sm">
                    <div className="text-slate-600 text-xs mb-0.5">{combo.produces.join(', ')}</div>
                    {combo.lines.map((cards, j) => (
                      <div key={j} className="text-slate-300 font-medium">{cards.join(' + ')}</div>
                    ))}
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Interaction Stats — stat line, no boxes */}
        {analysis.interaction && (
          <div className="flex mb-5">
            {[
              { label: 'Removal', value: analysis.interaction.removal },
              { label: 'Wipes', value: analysis.interaction.board_wipes },
              { label: 'Counters', value: analysis.interaction.counterspells },
              { label: 'Tutors', value: analysis.interaction.tutors },
            ].map(({ label, value }, i) => (
              <div key={label} className={`flex-1 text-center ${i > 0 ? 'border-l border-slate-700' : ''}`}>
                <div className="text-2xl font-black text-slate-100">{value}</div>
                <div className="text-xs text-slate-500 uppercase tracking-wider mt-0.5">{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Colors + Card Types */}
        <div className="grid grid-cols-2 gap-4 mb-5">
          <div>
            <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-2">Colors</h3>
            <div className="flex flex-wrap gap-1.5">
              {Object.keys(analysis.colors).map(color => (
                <span key={color} className={`text-xs font-black px-2 py-0.5 rounded ${COLOR_BADGE[color] || 'bg-slate-600 text-white'}`}>
                  {COLOR_SYMBOLS[color] || color}
                </span>
              ))}
              {Object.keys(analysis.colors).length === 0 && (
                <span className="text-sm text-slate-500">Colorless</span>
              )}
            </div>
          </div>
          <div>
            <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-2">Card Types</h3>
            <div className="text-sm space-y-1">
              {Object.entries(analysis.card_types)
                .sort((a, b) => b[1] - a[1])
                .map(([type, count]) => (
                  <div key={type} className="flex justify-between">
                    <span className="capitalize text-slate-300">{type}</span>
                    <span className="text-slate-600">{count}</span>
                  </div>
                ))}
            </div>
          </div>
        </div>

        {/* Mana Curve */}
        <div className="mb-5">
          <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-2">Mana Curve</h3>
          {(() => {
            const BAR_MAX_PX = 64
            const maxCount = Math.max(...Object.values(analysis.mana_curve).map(Number), 1)
            return (
              <div className="flex gap-1">
                {[0, 1, 2, 3, 4, 5, 6, 7].map((cmc) => {
                  const count = analysis.mana_curve[String(cmc)] || 0
                  const barH = count > 0 ? Math.max(3, Math.round((count / maxCount) * BAR_MAX_PX)) : 0
                  return (
                    <div key={cmc} className="flex-1 flex flex-col items-center">
                      <div style={{ height: BAR_MAX_PX - barH }} />
                      {count > 0 && <span className="text-xs text-slate-600 leading-none mb-0.5">{count}</span>}
                      <div className="w-full bg-amber-500 rounded-t" style={{ height: barH }} />
                      <span className="text-xs text-slate-600 mt-1">{cmc === 7 ? '7+' : cmc}</span>
                    </div>
                  )
                })}
              </div>
            )
          })()}
        </div>

        {/* Card list */}
        {analysis.cards.length > 0 && (
          <div className="pt-4 border-t border-slate-800">
            <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-3">Cards</h3>
            <CardsByType cards={analysis.cards} />
          </div>
        )}
      </div>
    </>
  )
}
