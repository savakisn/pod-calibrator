'use client'

import React from 'react'
import { track } from '@/lib/analytics'

interface Card {
  name: string
  quantity: number
  cmc?: number
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
  removal_cards: string[]
  board_wipes: number
  board_wipe_cards: string[]
  counterspells: number
  counterspell_cards: string[]
  tutors: number
  tutor_cards: string[]
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
  _meta?: { cache_hit: boolean; ms: number }
  _diagnostics?: {
    interaction: {
      removal: string[]
      board_wipes: string[]
      counterspells: string[]
      tutors: string[]
    }
    wincons: Record<string, string[]>
  }
}

export type ColorMode = 'protanopia' | 'deuteranopia' | 'tritanopia'

const TYPE_ORDER = ['Creature', 'Planeswalker', 'Instant', 'Sorcery', 'Enchantment', 'Artifact', 'Land', 'Other']
const SUPERTYPES = new Set(['Basic', 'Legendary', 'Snow', 'World'])

function primaryType(type_line: string | undefined): string {
  if (!type_line) return 'Other'
  const part = type_line.split('—')[0].split('//')[0].trim()
  const words = part.split(' ').filter(w => !SUPERTYPES.has(w))
  return TYPE_ORDER.includes(words[0]) ? words[0] : 'Other'
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
                  {card.cmc !== undefined && <span className="text-slate-600 ml-2 shrink-0">{card.cmc}</span>}
                </div>
              ))}
          </div>
        </div>
      ))}
    </div>
  )
}

function Tooltip({ children, content, compact }: { children: React.ReactNode; content: React.ReactNode; compact?: boolean }) {
  return (
    <div className="relative group inline-block">
      {children}
      <div className={`absolute bottom-full left-0 mb-2 ${compact ? 'w-auto whitespace-nowrap' : 'w-64'} bg-slate-900 border border-slate-700 rounded-lg p-2.5 text-xs text-slate-300 opacity-0 group-hover:opacity-100 transition-opacity z-30 pointer-events-none shadow-2xl leading-relaxed`}>
        {content}
      </div>
    </div>
  )
}

// Protanopia: no red receptors — avoid red; R→orange, G→cyan
// Deuteranopia: no green receptors — avoid green; G→violet, R→rose
// Tritanopia: no blue receptors — avoid blue; U→violet
const BRACKET_PALETTE: Record<ColorMode, Record<number, { border: string; text: string }>> = {
  protanopia: {
    1: { border: 'border-cyan-500',    text: 'text-cyan-400' },
    2: { border: 'border-blue-500',    text: 'text-blue-400' },
    3: { border: 'border-violet-500',  text: 'text-violet-400' },
    4: { border: 'border-amber-500',   text: 'text-amber-400' },
    5: { border: 'border-fuchsia-500', text: 'text-fuchsia-400' },
  },
  deuteranopia: {
    1: { border: 'border-teal-500',    text: 'text-teal-400' },
    2: { border: 'border-blue-500',    text: 'text-blue-400' },
    3: { border: 'border-violet-400',  text: 'text-violet-400' },
    4: { border: 'border-orange-500',  text: 'text-orange-400' },
    5: { border: 'border-rose-500',    text: 'text-rose-400' },
  },
  tritanopia: {
    1: { border: 'border-green-500',   text: 'text-green-400' },
    2: { border: 'border-rose-400',    text: 'text-rose-400' },
    3: { border: 'border-violet-500',  text: 'text-violet-400' },
    4: { border: 'border-orange-500',  text: 'text-orange-400' },
    5: { border: 'border-red-600',     text: 'text-red-500' },
  },
}

const SPEED_PALETTE: Record<ColorMode, Record<string, string>> = {
  protanopia: {
    Turbo:        'bg-amber-900/50 border-amber-700 text-amber-300',
    Fast:         'bg-cyan-900/50 border-cyan-700 text-cyan-300',
    Steady:       'bg-blue-900/50 border-blue-700 text-blue-300',
    Slow:         'bg-violet-900/50 border-violet-700 text-violet-300',
    Battlecruiser:'bg-slate-700 border-slate-600 text-slate-300',
  },
  deuteranopia: {
    Turbo:        'bg-rose-900/50 border-rose-700 text-rose-300',
    Fast:         'bg-orange-900/50 border-orange-700 text-orange-300',
    Steady:       'bg-blue-900/50 border-blue-700 text-blue-300',
    Slow:         'bg-purple-900/50 border-purple-700 text-purple-300',
    Battlecruiser:'bg-slate-700 border-slate-600 text-slate-300',
  },
  tritanopia: {
    Turbo:        'bg-red-900/50 border-red-700 text-red-300',
    Fast:         'bg-orange-900/50 border-orange-700 text-orange-300',
    Steady:       'bg-violet-900/50 border-violet-700 text-violet-300',
    Slow:         'bg-rose-900/50 border-rose-700 text-rose-300',
    Battlecruiser:'bg-slate-700 border-slate-600 text-slate-300',
  },
}

export const COLOR_BADGE_PALETTE: Record<ColorMode, Record<string, string>> = {
  protanopia: {
    white:    'bg-amber-50 text-amber-900 border border-amber-200',
    blue:     'bg-blue-600 text-white border border-blue-600',
    black:    'bg-slate-600 text-white border border-slate-600',
    red:      'bg-orange-500 text-white border border-orange-500',
    green:    'bg-cyan-600 text-white border border-cyan-600',
    colorless:'bg-slate-500 text-white border border-slate-500',
  },
  deuteranopia: {
    white:    'bg-amber-50 text-amber-900 border border-amber-200',
    blue:     'bg-blue-600 text-white border border-blue-600',
    black:    'bg-slate-600 text-white border border-slate-600',
    red:      'bg-rose-500 text-white border border-rose-500',
    green:    'bg-violet-600 text-white border border-violet-600',
    colorless:'bg-slate-500 text-white border border-slate-500',
  },
  tritanopia: {
    white:    'bg-orange-200 text-orange-900 border border-orange-300',
    blue:     'bg-violet-600 text-white border border-violet-600',
    black:    'bg-slate-600 text-white border border-slate-600',
    red:      'bg-rose-600 text-white border border-rose-600',
    green:    'bg-green-600 text-white border border-green-600',
    colorless:'bg-slate-500 text-white border border-slate-500',
  },
}

const COLOR_SYMBOLS: Record<string, string> = {
  white: 'W', blue: 'U', black: 'B', red: 'R', green: 'G', colorless: 'C',
}

const SPEED_DESC: Record<string, string> = {
  Turbo:        'Extremely low curve, aims to close out by turns 2-3. Fast mana and explosive early turns.',
  Fast:         'Low curve with solid ramp, typically online turns 3-4. Strong early game pressure.',
  Steady:       'Mid-range curve, competitive around turns 4-5. Balances interaction with development.',
  Slow:         'High curve with limited ramp, takes until turns 5-6 to develop. Favors grindier games.',
  Battlecruiser:'Very high curve, wants long games and big spells. Will likely struggle against faster pods.',
}

const WIN_TOOLTIP: Record<string, string> = {
  Combo:        'Active infinite combo lines detected via Spellbook.',
  Tokens:       'Multiple token producers or doublers detected (e.g. Parallel Lives, Anointed Procession).',
  Aristocrats:  '3+ death-trigger payoffs detected (e.g. Blood Artist, Grave Pact).',
  Reanimator:   '3+ graveyard recursion spells detected.',
  Voltron:      '4+ equipment or aura pieces detected.',
  Stax:         '3+ tax or lock pieces detected (e.g. Winter Orb, Sphere of Resistance).',
  Lifegain:     '2+ life-total payoffs detected (e.g. Aetherflux Reservoir, Serra Ascendant).',
  Spellslinger: 'High instant/sorcery ratio with payoff cards detected (e.g. Guttersnipe, Talrand).',
  Superfriends: 'Commander implies a planeswalker-focused strategy.',
  Tribal:       'Tribal synergy detected via commander or card density.',
  Landfall:     'Land-based engine detected via commander.',
  Goodstuff:    'No single dominant strategy detected. Relies on card quality and flexible interaction.',
}

export default function DeckCard({ analysis, colorMode }: { analysis: DeckAnalysis | null; colorMode: ColorMode }) {

  if (!analysis) return null

  const bracket = analysis.bracket
  const bracketPalette = BRACKET_PALETTE[colorMode]
  const speedCls = SPEED_PALETTE[colorMode]
  const colorBadge = COLOR_BADGE_PALETTE[colorMode]

  const COLOR_ORDER = ['white', 'blue', 'black', 'red', 'green', 'colorless']
  const isColorlessOnly = Object.keys(analysis.colors).every(c => c === 'colorless')
  const colorKeys = COLOR_ORDER.filter(c => c in analysis.colors && (c !== 'colorless' || isColorlessOnly))

  const commanderArt = analysis.commander?.image_uris?.art_crop
    ?? (analysis.commander?.name
        ? `https://api.scryfall.com/cards/named?exact=${encodeURIComponent(analysis.commander.name)}&format=image&version=art_crop`
        : null)

  const handleExport = async () => {
    track('export_clicked', { format: 'single', deck_count: 1 })
    try {
      const res = await fetch('/api/export', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ analysis, colorMode }),
      })
      if (!res.ok) throw new Error('Export failed')
      const blob = await res.blob()
      const filename = res.headers.get('content-disposition')?.split('filename=')[1]?.replace(/"/g, '') || 'deck-pod-calibrator.jpg'
      const file = new File([blob], filename, { type: 'image/jpeg' })
      if (navigator.canShare?.({ files: [file] })) {
        await navigator.share({ files: [file] })
      } else {
        const url = URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = filename
        a.click()
        URL.revokeObjectURL(url)
      }
    } catch (err) {
      if (err instanceof Error && err.name === 'AbortError') return
      alert('Export failed: ' + (err instanceof Error ? err.message : 'Unknown error'))
    }
  }

  return (
    <div className="w-full max-w-2xl bg-slate-900 border border-slate-700 rounded-xl p-6 shadow-2xl">

      {/* Header */}
      <div className="flex items-start gap-4 mb-3">
        {commanderArt && (
          <img
            src={commanderArt}
            alt={analysis.commander?.name}
            className="w-20 h-14 object-cover rounded-lg shrink-0 border border-slate-700"
          />
        )}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-3">
            <div className="min-w-0">
              <h2 className="text-xl font-extrabold text-amber-400 mb-1 leading-tight break-words">
                {analysis.commander?.name || 'Deck'}
              </h2>
              <div className="flex items-center gap-2 flex-wrap">
                <p className="text-slate-500 text-sm shrink-0">{analysis.card_count} cards · avg CMC {analysis.avg_cmc}</p>
                <div className="flex gap-1">
                  {colorKeys.map(color => (
                    <span key={color} className={`text-xs font-black w-6 h-6 inline-flex items-center justify-center rounded ${colorBadge[color] || 'bg-slate-600 text-white border border-slate-600'}`}>
                      {COLOR_SYMBOLS[color] || color}
                    </span>
                  ))}
                </div>
              </div>
            </div>
            <button onClick={handleExport} className="text-xs text-slate-500 hover:text-amber-400 border border-slate-700 hover:border-amber-700/50 rounded-lg px-3 py-1.5 shrink-0 transition-colors">
              Export
            </button>
          </div>
        </div>
      </div>

      {/* Speed + Win Conditions */}
      <div className="flex flex-wrap items-center gap-2 mb-7">
        {analysis.speed && (
          <Tooltip content={<><div className="mb-1">{SPEED_DESC[analysis.speed.label]}</div><div className="text-slate-500">avg non-land CMC: {analysis.speed.avg_nonland_cmc} · ramp pieces: {analysis.speed.ramp_count}</div></>}>
            <span className={`text-xs px-2 py-0.5 rounded border font-bold tracking-wide cursor-help ${speedCls[analysis.speed.label] || ''}`}>
              {analysis.speed.label}
            </span>
          </Tooltip>
        )}
        {analysis.win_conditions?.map(wc => {
          const hasConfirmedCombos = (analysis.bracket?.combos?.length ?? 0) > 0
          const tooltip = wc === 'Combo'
            ? (hasConfirmedCombos ? 'Active infinite combo lines detected via Spellbook.' : 'Commander strategy suggests combo potential. No specific lines confirmed by Spellbook.')
            : (WIN_TOOLTIP[wc] ?? wc)
          return (
            <Tooltip key={wc} content={tooltip}>
              <span className="text-xs px-2 py-0.5 rounded border font-semibold bg-slate-800 text-slate-300 border-slate-600 cursor-help">{wc}</span>
            </Tooltip>
          )
        })}
        {analysis.speed && (
          <span className="text-xs text-slate-600">{analysis.speed.avg_nonland_cmc} avg CMC · {analysis.speed.ramp_count} ramp pieces</span>
        )}
      </div>

      {/* Bracket */}
      {bracket?.error && (
        <div className="border-l-4 border-slate-600 pl-4 mb-5 text-slate-500 text-sm py-1">Bracket unavailable (Spellbook offline)</div>
      )}
      {bracket && !bracket.error && (
        <div className="mb-5">
          <div className="text-xs text-slate-500 uppercase tracking-wider leading-none mb-1">Bracket</div>
          <div className={`border-l-4 pl-4 py-1 ${bracketPalette[bracket.bracket].border}`}>
          <div className="flex items-end gap-3 mb-2">
            <span className={`text-5xl font-black leading-none ${bracketPalette[bracket.bracket].text}`}>{bracket.bracket}</span>
            <div>
              <div className="text-base font-bold text-slate-200 leading-tight">{bracket.bracket_label}</div>
              <div className="text-xs text-slate-500">{bracket.game_changer_count} game changer{bracket.game_changer_count !== 1 ? 's' : ''}</div>
            </div>
          </div>
          <div className="space-y-1 text-sm text-slate-400">
            {bracket.game_changers_found.length > 0 && <div><span className="text-slate-500">Game changers: </span>{bracket.game_changers_found.join(', ')}</div>}
            {bracket.mass_land_denial.length > 0 && <div><span className="text-slate-500">MLD: </span>{bracket.mass_land_denial.join(', ')}</div>}
            {bracket.extra_turns.length > 0 && <div><span className="text-slate-500">Extra turns: </span>{bracket.extra_turns.join(', ')}</div>}
          </div>
          {bracket.combos.length > 0 && (
            <div className="mt-3 pt-3 border-t border-slate-700/50 space-y-2">
              <div className="text-xs text-slate-500 uppercase tracking-wider">{bracket.combos.length} combo{bracket.combos.length !== 1 ? 's' : ''} detected</div>
              {bracket.combos.map((combo, i) => (
                <div key={`${combo.produces.join('|')}:${i}`} className="text-sm">
                  <div className="text-slate-600 text-xs mb-0.5">{combo.produces.join(', ')}</div>
                  {combo.lines.map((cards, j) => (
                    <div key={cards.join('+')} className="text-slate-300 font-medium">{cards.join(' + ')}</div>
                  ))}
                </div>
              ))}
            </div>
          )}
          </div>
        </div>
      )}

      {/* Card Types + Interaction side by side */}
      <div className="grid grid-cols-2 divide-x divide-slate-700 mb-5">
        <div className="pr-2">
          <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-2">Card Types</h3>
          <div className="text-sm space-y-0.5">
            {Object.entries(analysis.card_types).sort((a, b) => b[1] - a[1]).map(([type, count]) => (
              <div key={type} className="flex items-baseline gap-2">
                <span className="capitalize text-slate-300">{type}</span>
                <span className="text-slate-600">{count}</span>
              </div>
            ))}
          </div>
        </div>
        {analysis.interaction && (
          <div className="pl-2">
            <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-2">Interaction</h3>
            <div className="grid grid-cols-2 border border-slate-700">
              {[
                { label: 'Removal',  value: analysis.interaction.removal,       cards: analysis.interaction.removal_cards },
                { label: 'Wipes',    value: analysis.interaction.board_wipes,   cards: analysis.interaction.board_wipe_cards },
                { label: 'Counters', value: analysis.interaction.counterspells, cards: analysis.interaction.counterspell_cards },
                { label: 'Tutors',   value: analysis.interaction.tutors,        cards: analysis.interaction.tutor_cards },
              ].map(({ label, value, cards }, idx) => (
                <Tooltip key={label} compact content={
                  cards?.length > 0
                    ? <ul className="space-y-0.5">{cards.map(c => <li key={c}>{c}</li>)}</ul>
                    : `No ${label.toLowerCase()} detected`
                }>
                  <div className={`cursor-help text-center py-2 px-1 ${idx % 2 === 0 ? 'border-r border-slate-700' : ''} ${idx >= 2 ? 'border-t border-slate-700' : ''}`}>
                    <div className="text-xl font-black text-slate-100">{value}</div>
                    <div className="text-xs text-slate-500 uppercase tracking-wider">{label}</div>
                  </div>
                </Tooltip>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Mana Curve */}
      <div className="mb-5">
        <h3 className="text-xs uppercase text-slate-600 tracking-wider mb-2">Mana Curve</h3>
        {(() => {
          const BAR_MAX_PX = 64
          const maxCount = Math.max(...Object.values(analysis.mana_curve).map(Number), 1)
          return (
            <div className="flex gap-1">
              {[0, 1, 2, 3, 4, 5, 6, 7].map(cmc => {
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
  )
}
