'use client'

import type { DeckAnalysis } from './DeckCard'

const SPEED_TIER: Record<string, number> = {
  Turbo: 0, Fast: 1, Steady: 2, Slow: 3, Battlecruiser: 4,
}
const SPEED_LABEL = ['Turbo', 'Fast', 'Steady', 'Slow', 'Battlecruiser']

const COLOR_SYMBOLS: Record<string, string> = {
  white: 'W', blue: 'U', black: 'B', red: 'R', green: 'G', colorless: 'C',
}
const COLOR_ORDER = ['white', 'blue', 'black', 'red', 'green', 'colorless']
const COLOR_CLASSES: Record<string, string> = {
  white: 'bg-amber-50 text-amber-900 border border-amber-200',
  blue: 'bg-blue-600 text-white border border-blue-600',
  black: 'bg-slate-600 text-white border border-slate-600',
  red: 'bg-rose-600 text-white border border-rose-600',
  green: 'bg-amber-500 text-white border border-amber-500',
  colorless: 'bg-slate-500 text-white border border-slate-500',
}

type Severity = 'ok' | 'warn' | 'danger'

interface Verdict {
  label: string
  severity: Severity
}

function severity(s: Severity) {
  if (s === 'danger') return 'text-red-400'
  if (s === 'warn') return 'text-yellow-400'
  return 'text-teal-400'
}

function icon(s: Severity) {
  if (s === 'danger') return '⚠'
  if (s === 'warn') return '▲'
  return '✓'
}

function bracketVerdict(decks: DeckAnalysis[]): Verdict {
  const brackets = decks.map(d => d.bracket?.bracket ?? 3)
  const spread = Math.max(...brackets) - Math.min(...brackets)
  if (spread === 0) return { label: 'Even spread', severity: 'ok' }
  if (spread === 1) return { label: `Spread of ${spread}, minor`, severity: 'ok' }
  if (spread === 2) return { label: `Spread of ${spread}, noticeable`, severity: 'warn' }
  return { label: `Spread of ${spread}, unbalanced`, severity: 'danger' }
}

function speedVerdict(decks: DeckAnalysis[]): Verdict {
  const tiers = decks.map(d => SPEED_TIER[d.speed?.label ?? 'Steady'] ?? 2)
  const sorted = [...tiers].sort((a, b) => a - b)
  const median = sorted[Math.floor(sorted.length / 2)]
  const maxDev = Math.max(...tiers.map(t => Math.abs(t - median)))
  if (maxDev === 0) return { label: 'Aligned', severity: 'ok' }
  if (maxDev === 1) return { label: 'Minor gap', severity: 'ok' }
  if (maxDev === 2) return { label: `${SPEED_LABEL[Math.min(...tiers)]} vs ${SPEED_LABEL[Math.max(...tiers)]}, gap`, severity: 'warn' }
  return { label: `${SPEED_LABEL[Math.min(...tiers)]} vs ${SPEED_LABEL[Math.max(...tiers)]}, severe gap`, severity: 'danger' }
}

function winconVerdict(decks: DeckAnalysis[]): Verdict {
  const counts: Record<string, number> = {}
  for (const d of decks) {
    for (const wc of d.win_conditions ?? []) {
      if (wc === 'Goodstuff') continue
      counts[wc] = (counts[wc] ?? 0) + 1
    }
  }
  const overlaps = Object.entries(counts).filter(([, n]) => n >= Math.max(2, Math.ceil(decks.length / 2)))
  if (!overlaps.length) return { label: 'Diverse', severity: 'ok' }
  const names = overlaps.map(([k]) => k).join(', ')
  if (overlaps.some(([, n]) => n >= decks.length - 1)) return { label: `Heavy ${names} overlap`, severity: 'danger' }
  return { label: `${names} overlap`, severity: 'warn' }
}

function interactionVerdict(decks: DeckAnalysis[]): Verdict {
  const totals = decks.map(d =>
    (d.interaction?.removal ?? 0) + (d.interaction?.board_wipes ?? 0) + (d.interaction?.counterspells ?? 0)
  )
  const avg = totals.reduce((a, b) => a + b, 0) / totals.length
  const minTotal = Math.min(...totals)
  if (minTotal >= avg * 0.5) return { label: 'Balanced', severity: 'ok' }
  if (minTotal >= avg * 0.3) return { label: 'One deck is light on interaction', severity: 'warn' }
  return { label: 'One deck has almost no interaction', severity: 'danger' }
}

function overallVerdict(verdicts: Verdict[]): Verdict {
  if (verdicts.some(v => v.severity === 'danger')) return { label: 'Pod is unbalanced', severity: 'danger' }
  if (verdicts.some(v => v.severity === 'warn')) return { label: 'Pod has some tension', severity: 'warn' }
  return { label: 'Pod looks well-matched', severity: 'ok' }
}

interface RowProps {
  label: string
  values: React.ReactNode[]
  verdict?: Verdict
}

function Row({ label, values, verdict }: RowProps) {
  return (
    <tr className="border-t border-slate-800">
      <td className="py-2 pr-4 text-xs text-slate-500 uppercase tracking-wider whitespace-nowrap font-medium">{label}</td>
      {values.map((v, i) => (
        <td key={i} className="py-2 px-3 text-center text-sm text-slate-200">{v}</td>
      ))}
      {verdict && (
        <td className={`py-2 pl-3 text-xs whitespace-nowrap ${severity(verdict.severity)}`}>
          {icon(verdict.severity)} {verdict.label}
        </td>
      )}
    </tr>
  )
}

export default function PodView({ decks, onRemove }: { decks: DeckAnalysis[]; onRemove: (i: number) => void }) {
  const bv = bracketVerdict(decks)
  const sv = speedVerdict(decks)
  const wv = winconVerdict(decks)
  const iv = interactionVerdict(decks)
  const ov = overallVerdict([bv, sv, wv, iv])

  return (
    <div className="w-full">

      {/* Overall verdict */}
      <div className={`mb-6 px-4 py-3 rounded-lg border text-sm font-semibold flex items-center gap-2 ${
        ov.severity === 'danger' ? 'bg-red-950/40 border-red-800 text-red-300' :
        ov.severity === 'warn'   ? 'bg-yellow-950/40 border-yellow-800 text-yellow-300' :
                                   'bg-teal-950/40 border-teal-800 text-teal-300'
      }`}>
        <span className="text-lg">{icon(ov.severity)}</span>
        {ov.label}
        <span className="ml-auto font-normal text-xs opacity-70">{decks.length} decks in pod</span>
      </div>

      {/* Comparison table */}
      <div className="overflow-x-auto">
        <table className="w-full bg-slate-900 border border-slate-700 rounded-xl">
          <thead>
            <tr>
              <th className="p-3 text-left" />
              {decks.map((d, i) => {
                const isColorlessOnly = Object.keys(d.colors).every(c => c === 'colorless')
                const colorKeys = COLOR_ORDER.filter(c => c in d.colors && (c !== 'colorless' || isColorlessOnly))
                const artUrl = d.commander?.image_uris?.art_crop
                  ?? (d.commander?.name
                    ? `https://api.scryfall.com/cards/named?exact=${encodeURIComponent(d.commander.name)}&format=image&version=art_crop`
                    : null)
                return (
                  <th key={i} className="p-3 text-center border-l border-slate-700 min-w-[140px]">
                    <div className="flex flex-col items-center">
                      <div className="relative mb-1">
                        <button
                          onClick={() => onRemove(i)}
                          className="absolute -top-1 -right-1 z-10 text-slate-600 hover:text-red-400 text-xs border border-slate-700 hover:border-red-800 bg-slate-900 rounded-full w-4 h-4 flex items-center justify-center transition-colors"
                        >
                          ×
                        </button>
                        {artUrl && (
                          <img src={artUrl} alt={d.commander?.name} className="w-20 h-14 object-cover rounded-lg border border-slate-700" />
                        )}
                      </div>
                      <div className="text-xs font-bold text-amber-400 leading-tight mt-1 px-1 text-center w-full truncate">
                        {d.commander?.name ?? 'Unknown'}
                      </div>
                    </div>
                    <div className="flex justify-center gap-0.5 mt-1 flex-wrap">
                      {colorKeys.map(c => (
                        <span key={c} className={`text-xs font-black w-5 h-5 inline-flex items-center justify-center rounded ${COLOR_CLASSES[c]}`}>
                          {COLOR_SYMBOLS[c]}
                        </span>
                      ))}
                    </div>
                  </th>
                )
              })}
              <th className="p-3 text-left text-xs text-slate-600 uppercase tracking-wider border-l border-slate-700 whitespace-nowrap">
                Verdict
              </th>
            </tr>
          </thead>
          <tbody>
            <Row
              label="Bracket"
              values={decks.map(d => (
                <span className="font-black text-lg">{d.bracket?.bracket ?? '—'}</span>
              ))}
              verdict={bv}
            />
            <Row
              label="Speed"
              values={decks.map(d => d.speed?.label ?? '—')}
              verdict={sv}
            />
            <Row
              label="Win Cons"
              values={decks.map(d => (
                <div className="flex flex-wrap justify-center gap-0.5">
                  {(d.win_conditions ?? []).map(wc => (
                    <span key={wc} className="text-xs px-1.5 py-0.5 rounded bg-slate-800 border border-slate-600 text-slate-300">{wc}</span>
                  ))}
                </div>
              ))}
              verdict={wv}
            />
            <Row
              label="Ramp"
              values={decks.map(d => d.speed?.ramp_count ?? '—')}
            />
            <Row
              label="Removal"
              values={decks.map(d => d.interaction?.removal ?? '—')}
            />
            <Row
              label="Wipes"
              values={decks.map(d => d.interaction?.board_wipes ?? '—')}
            />
            <Row
              label="Counters"
              values={decks.map(d => d.interaction?.counterspells ?? '—')}
            />
            <Row
              label="Tutors"
              values={decks.map(d => d.interaction?.tutors ?? '—')}
              verdict={iv}
            />
          </tbody>
        </table>
      </div>
    </div>
  )
}
