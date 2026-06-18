'use client'

import { forwardRef } from 'react'
import type { DeckAnalysis } from './DeckCard'

const CARD_W = 640
const PAD = 14
const BG = '#0f172a'
const BORDER = '#334155'
const TEXT = '#e2e8f0'
const MUTED = '#64748b'
const GOLD = '#f59e0b'

const BRACKET_COLOR: Record<number, string> = {
  1: '#22c55e', 2: '#3b82f6', 3: '#eab308', 4: '#f97316', 5: '#ef4444',
}

const SPEED_STYLE: Record<string, { bg: string; border: string; text: string }> = {
  Turbo: { bg: '#2d0808', border: '#991b1b', text: '#fca5a5' },
  Fast: { bg: '#2d1000', border: '#9a3412', text: '#fdba74' },
  Balanced: { bg: '#2d1a00', border: '#92400e', text: '#fde68a' },
  Slow: { bg: '#0c1a3a', border: '#1d4ed8', text: '#93c5fd' },
  Battlecruiser: { bg: '#1e293b', border: '#475569', text: '#94a3b8' },
}

const COLOR_BADGE: Record<string, { bg: string; text: string; label: string }> = {
  white: { bg: '#fef3c7', text: '#78350f', label: 'W' },
  blue: { bg: '#2563eb', text: '#ffffff', label: 'U' },
  black: { bg: '#475569', text: '#ffffff', label: 'B' },
  red: { bg: '#dc2626', text: '#ffffff', label: 'R' },
  green: { bg: '#16a34a', text: '#ffffff', label: 'G' },
  colorless: { bg: '#64748b', text: '#ffffff', label: 'C' },
}

const ShareCard = forwardRef<HTMLDivElement, { analysis: DeckAnalysis }>(
  function ShareCard({ analysis }, ref) {
    const bracket = analysis.bracket && !analysis.bracket.error ? analysis.bracket : null
    const maxCount = Math.max(...Object.values(analysis.mana_curve).map(Number), 1)

    return (
      <div ref={ref} style={{ width: CARD_W, backgroundColor: BG, fontFamily: 'system-ui, sans-serif', padding: PAD, boxSizing: 'border-box', color: TEXT }}>
        {/* Header */}
        <div style={{ marginBottom: 12 }}>
          <div style={{ fontSize: 18, fontWeight: 700, color: GOLD, marginBottom: 4 }}>{analysis.commander?.name || 'Deck'}</div>
          <div style={{ fontSize: 10, color: MUTED, marginBottom: 2 }}>{analysis.card_count} cards · avg CMC {analysis.avg_cmc}</div>
          {analysis.speed && <div style={{ fontSize: 9, color: MUTED }}>{analysis.speed.avg_nonland_cmc} non-land avg · {analysis.speed.ramp_count} ramp</div>}
        </div>

        {/* Bracket */}
        {bracket && (
          <div style={{ marginBottom: 12, paddingLeft: 10, borderLeft: `4px solid ${BRACKET_COLOR[bracket.bracket]}` }}>
            <div style={{ fontSize: 8, color: MUTED, fontWeight: 700, textTransform: 'uppercase', marginBottom: 2 }}>Bracket</div>
            <div style={{ fontSize: 28, fontWeight: 900, color: BRACKET_COLOR[bracket.bracket], marginBottom: 2 }}>{bracket.bracket}</div>
            <div style={{ fontSize: 10, fontWeight: 600, marginBottom: 1 }}>{bracket.bracket_label}</div>
            <div style={{ fontSize: 8, color: MUTED }}>{bracket.game_changer_count} GC{bracket.game_changer_count !== 1 ? 's' : ''}</div>
          </div>
        )}

        {/* Speed + Win Conditions */}
        <div style={{ marginBottom: 12, display: 'flex', gap: 5, flexWrap: 'wrap' }}>
          {analysis.speed && (() => {
            const s = SPEED_STYLE[analysis.speed.label] ?? SPEED_STYLE.Battlecruiser
            return <div key="speed" style={{ backgroundColor: s.bg, border: `1px solid ${s.border}`, color: s.text, borderRadius: 2, padding: '3px 7px', fontSize: 8, fontWeight: 700 }}>{analysis.speed.label}</div>
          })()}
          {analysis.win_conditions?.map(wc => (
            <div key={wc} style={{ backgroundColor: '#1e293b', border: `1px solid ${BORDER}`, color: TEXT, borderRadius: 2, padding: '3px 7px', fontSize: 8, fontWeight: 600 }}>{wc}</div>
          ))}
        </div>

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 10 }} />

        {/* Interaction Stats */}
        {analysis.interaction && (
          <div style={{ marginBottom: 10, display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 0 }}>
            {[
              { label: 'Removal', value: analysis.interaction.removal },
              { label: 'Wipes', value: analysis.interaction.board_wipes },
              { label: 'Counters', value: analysis.interaction.counterspells },
              { label: 'Tutors', value: analysis.interaction.tutors },
            ].map(({ label, value }) => (
              <div key={label} style={{ textAlign: 'center', padding: '6px 4px', borderRight: '1px solid ' + BORDER }}>
                <div style={{ fontSize: 14, fontWeight: 900, marginBottom: 3 }}>{value}</div>
                <div style={{ fontSize: 7, color: MUTED, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 10 }} />

        {/* Mana Curve */}
        <div style={{ marginBottom: 10 }}>
          <div style={{ fontSize: 8, color: MUTED, fontWeight: 700, textTransform: 'uppercase', marginBottom: 6 }}>Mana Curve</div>
          <div style={{ display: 'flex', gap: 3, height: 50, alignItems: 'flex-end' }}>
            {[0, 1, 2, 3, 4, 5, 6, 7].map(cmc => {
              const count = analysis.mana_curve[String(cmc)] || 0
              const barH = count > 0 ? Math.max(2, Math.round((count / maxCount) * 50)) : 1
              return (
                <div key={cmc} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-end' }}>
                  {count > 0 && <div style={{ fontSize: 7, color: MUTED, marginBottom: 2 }}>{count}</div>}
                  <div style={{ width: '100%', height: barH, backgroundColor: GOLD, borderRadius: '2px 2px 0 0' }} />
                </div>
              )
            })}
          </div>
          <div style={{ display: 'flex', gap: 3, marginTop: 4, fontSize: 7, color: MUTED, textAlign: 'center' }}>
            {[0, 1, 2, 3, 4, 5, 6, '7+'].map(label => (
              <div key={label} style={{ flex: 1 }}>{label}</div>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 10 }} />

        {/* Footer */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', gap: 3 }}>
            {Object.keys(analysis.colors).map(color => {
              const s = COLOR_BADGE[color]
              if (!s) return null
              return (
                <span key={color} style={{ backgroundColor: s.bg, color: s.text, borderRadius: 2, padding: '2px 6px', fontSize: 8, fontWeight: 900 }}>
                  {s.label}
                </span>
              )
            })}
          </div>
          <span style={{ fontSize: 9, color: '#1e3a5f' }}>caliber</span>
        </div>
      </div>
    )
  }
)

export default ShareCard
