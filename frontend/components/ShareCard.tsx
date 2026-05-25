'use client'

import { forwardRef } from 'react'
import type { DeckAnalysis } from './DeckCard'

const BG = '#0f172a'
const SURFACE = '#1e293b'
const BORDER = '#334155'
const TEXT = '#e2e8f0'
const MUTED = '#64748b'
const GOLD = '#f59e0b'

const BRACKET_STYLE: Record<number, { bg: string; border: string; text: string }> = {
  1: { bg: '#052e16', border: '#166534', text: '#86efac' },
  2: { bg: '#0c1a3a', border: '#1d4ed8', text: '#93c5fd' },
  3: { bg: '#2d1a00', border: '#92400e', text: '#fde68a' },
  4: { bg: '#2d1000', border: '#9a3412', text: '#fdba74' },
  5: { bg: '#2d0808', border: '#991b1b', text: '#fca5a5' },
}

const SPEED_STYLE: Record<string, { bg: string; border: string; text: string }> = {
  Turbo:       { bg: '#2d0808', border: '#991b1b', text: '#fca5a5' },
  Fast:        { bg: '#2d1000', border: '#9a3412', text: '#fdba74' },
  Balanced:    { bg: '#2d1a00', border: '#92400e', text: '#fde68a' },
  Slow:        { bg: '#0c1a3a', border: '#1d4ed8', text: '#93c5fd' },
  Battlecruiser: { bg: '#1e293b', border: '#475569', text: '#94a3b8' },
}

const COLOR_BADGE_STYLE: Record<string, { bg: string; text: string; label: string }> = {
  white:     { bg: '#fef3c7', text: '#78350f', label: 'W' },
  blue:      { bg: '#2563eb', text: '#ffffff', label: 'U' },
  black:     { bg: '#334155', text: '#ffffff', label: 'B' },
  red:       { bg: '#dc2626', text: '#ffffff', label: 'R' },
  green:     { bg: '#16a34a', text: '#ffffff', label: 'G' },
  colorless: { bg: '#64748b', text: '#ffffff', label: 'C' },
}

const ShareCard = forwardRef<HTMLDivElement, { analysis: DeckAnalysis }>(
  function ShareCard({ analysis }, ref) {
    const bracket = analysis.bracket && !analysis.bracket.error ? analysis.bracket : null
    const bs = bracket ? BRACKET_STYLE[bracket.bracket] : null

    const BAR_MAX_PX = 72
    const maxCount = Math.max(...Object.values(analysis.mana_curve).map(Number), 1)

    return (
      <div
        ref={ref}
        style={{
          width: 640,
          backgroundColor: BG,
          fontFamily: 'ui-sans-serif, system-ui, -apple-system, sans-serif',
          padding: 28,
          boxSizing: 'border-box',
        }}
      >
        {/* Header row */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 16 }}>
          <div style={{ flex: 1, minWidth: 0, paddingRight: 16 }}>
            <div style={{ color: GOLD, fontSize: 26, fontWeight: 700, lineHeight: 1.2, marginBottom: 4 }}>
              {analysis.commander?.name || 'Deck'}
            </div>
            <div style={{ color: MUTED, fontSize: 13 }}>
              {analysis.card_count} cards · avg CMC {analysis.avg_cmc}
            </div>
          </div>
          {bracket && bs && (
            <div style={{
              backgroundColor: bs.bg,
              border: `1px solid ${bs.border}`,
              borderRadius: 10,
              padding: '8px 14px',
              textAlign: 'center',
              minWidth: 90,
            }}>
              <div style={{ color: bs.text, fontSize: 10, fontWeight: 700, letterSpacing: 1, textTransform: 'uppercase', marginBottom: 2 }}>Bracket</div>
              <div style={{ color: bs.text, fontSize: 28, fontWeight: 800, lineHeight: 1 }}>{bracket.bracket}</div>
              <div style={{ color: bs.text, fontSize: 11, marginTop: 2 }}>{bracket.bracket_label}</div>
            </div>
          )}
        </div>

        {/* Speed + win condition badges */}
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 20 }}>
          {analysis.speed && (() => {
            const s = SPEED_STYLE[analysis.speed.label] || SPEED_STYLE.Battlecruiser
            return (
              <span style={{ backgroundColor: s.bg, border: `1px solid ${s.border}`, color: s.text, borderRadius: 4, padding: '2px 8px', fontSize: 12, fontWeight: 700 }}>
                {analysis.speed.label}
              </span>
            )
          })()}
          {analysis.win_conditions?.map(wc => (
            <span key={wc} style={{ backgroundColor: SURFACE, border: `1px solid ${BORDER}`, color: TEXT, borderRadius: 4, padding: '2px 8px', fontSize: 12, fontWeight: 600 }}>
              {wc}
            </span>
          ))}
        </div>

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 20 }} />

        {/* Interaction stats */}
        {analysis.interaction && (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: 10, marginBottom: 20 }}>
            {[
              { label: 'Removal', value: analysis.interaction.removal },
              { label: 'Wipes', value: analysis.interaction.board_wipes },
              { label: 'Counters', value: analysis.interaction.counterspells },
              { label: 'Tutors', value: analysis.interaction.tutors },
            ].map(({ label, value }) => (
              <div key={label} style={{ backgroundColor: SURFACE, borderRadius: 8, padding: '12px 0', textAlign: 'center', border: `1px solid ${BORDER}` }}>
                <div style={{ color: TEXT, fontSize: 26, fontWeight: 700, lineHeight: 1 }}>{value}</div>
                <div style={{ color: MUTED, fontSize: 10, marginTop: 4, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 20 }} />

        {/* Mana curve */}
        <div style={{ marginBottom: 20 }}>
          <div style={{ color: MUTED, fontSize: 10, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 10 }}>Mana Curve</div>
          <div style={{ display: 'flex', gap: 4, alignItems: 'flex-end', height: BAR_MAX_PX + 24 }}>
            {[0, 1, 2, 3, 4, 5, 6, 7].map(cmc => {
              const count = analysis.mana_curve[String(cmc)] || 0
              const barH = count > 0 ? Math.max(4, Math.round((count / maxCount) * BAR_MAX_PX)) : 0
              return (
                <div key={cmc} style={{ flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'flex-end', height: BAR_MAX_PX + 24 }}>
                  {count > 0 && (
                    <div style={{ color: MUTED, fontSize: 10, marginBottom: 2 }}>{count}</div>
                  )}
                  <div style={{ width: '100%', backgroundColor: '#f59e0b', borderRadius: '3px 3px 0 0', height: barH }} />
                  <div style={{ color: MUTED, fontSize: 10, marginTop: 4 }}>{cmc === 7 ? '7+' : cmc}</div>
                </div>
              )
            })}
          </div>
        </div>

        {/* Footer: colors + branding */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <div style={{ display: 'flex', gap: 6 }}>
            {Object.keys(analysis.colors).map(color => {
              const s = COLOR_BADGE_STYLE[color]
              if (!s) return null
              return (
                <span key={color} style={{
                  backgroundColor: s.bg, color: s.text,
                  borderRadius: 4, padding: '2px 7px',
                  fontSize: 12, fontWeight: 700,
                }}>
                  {s.label}
                </span>
              )
            })}
          </div>
          <div style={{ color: '#334155', fontSize: 11 }}>pod-calibrator</div>
        </div>
      </div>
    )
  }
)

export default ShareCard
