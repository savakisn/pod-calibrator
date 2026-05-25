'use client'

import { forwardRef } from 'react'
import type { DeckAnalysis } from './DeckCard'

const CARD_W = 640
const PAD = 28
const CONTENT_W = CARD_W - PAD * 2  // 584px

const BG = '#0f172a'
const SURFACE = '#1e293b'
const BORDER = '#334155'
const TEXT = '#e2e8f0'
const MUTED = '#64748b'
const GOLD = '#f59e0b'

const BRACKET_STYLE: Record<number, { border: string; numColor: string }> = {
  1: { border: '#22c55e', numColor: '#4ade80' },
  2: { border: '#3b82f6', numColor: '#60a5fa' },
  3: { border: '#eab308', numColor: '#facc15' },
  4: { border: '#f97316', numColor: '#fb923c' },
  5: { border: '#ef4444', numColor: '#f87171' },
}

const SPEED_STYLE: Record<string, { bg: string; border: string; text: string }> = {
  Turbo:        { bg: '#2d0808', border: '#991b1b', text: '#fca5a5' },
  Fast:         { bg: '#2d1000', border: '#9a3412', text: '#fdba74' },
  Balanced:     { bg: '#2d1a00', border: '#92400e', text: '#fde68a' },
  Slow:         { bg: '#0c1a3a', border: '#1d4ed8', text: '#93c5fd' },
  Battlecruiser:{ bg: '#1e293b', border: '#475569', text: '#94a3b8' },
}

const COLOR_BADGE: Record<string, { bg: string; text: string; label: string }> = {
  white:    { bg: '#fef3c7', text: '#78350f', label: 'W' },
  blue:     { bg: '#2563eb', text: '#ffffff', label: 'U' },
  black:    { bg: '#475569', text: '#ffffff', label: 'B' },
  red:      { bg: '#dc2626', text: '#ffffff', label: 'R' },
  green:    { bg: '#16a34a', text: '#ffffff', label: 'G' },
  colorless:{ bg: '#64748b', text: '#ffffff', label: 'C' },
}

// Stat widths: 4 cols with 10px gaps
const STAT_GAP = 10
const STAT_W = Math.floor((CONTENT_W - STAT_GAP * 3) / 4)

// Bar widths: 8 bars with 5px gaps
const BAR_GAP = 5
const BAR_W = Math.floor((CONTENT_W - BAR_GAP * 7) / 8)
const BAR_MAX_PX = 60

const ShareCard = forwardRef<HTMLDivElement, { analysis: DeckAnalysis }>(
  function ShareCard({ analysis }, ref) {
    const bracket = analysis.bracket && !analysis.bracket.error ? analysis.bracket : null
    const bs = bracket ? BRACKET_STYLE[bracket.bracket] : null
    const maxCount = Math.max(...Object.values(analysis.mana_curve).map(Number), 1)

    return (
      <div
        ref={ref}
        style={{
          width: CARD_W,
          backgroundColor: BG,
          fontFamily: 'ui-sans-serif, system-ui, -apple-system, sans-serif',
          padding: PAD,
          paddingBottom: PAD + 8,
          boxSizing: 'border-box',
        }}
      >
        {/* Header: commander name left, bracket badge right — table layout */}
        <div style={{ display: 'table', width: '100%', marginBottom: 16 }}>
          <div style={{ display: 'table-cell', verticalAlign: 'top' }}>
            <div style={{ color: GOLD, fontSize: 22, fontWeight: 700, lineHeight: 1.25, marginBottom: 4 }}>
              {analysis.commander?.name || 'Deck'}
            </div>
            <div style={{ color: MUTED, fontSize: 12 }}>
              {analysis.card_count} cards · avg CMC {analysis.avg_cmc}
            </div>
            {analysis.speed && (
              <div style={{ color: MUTED, fontSize: 10, marginTop: 2 }}>
                {analysis.speed.avg_nonland_cmc} non-land avg · {analysis.speed.ramp_count} ramp
              </div>
            )}
          </div>
          {bracket && bs && (
            <div style={{ display: 'table-cell', verticalAlign: 'top', width: 100, paddingLeft: 16 }}>
              <div style={{
                borderLeft: `4px solid ${bs.border}`,
                paddingLeft: 10,
              }}>
                <div style={{ color: MUTED, fontSize: 9, fontWeight: 700, letterSpacing: 1, textTransform: 'uppercase' }}>Bracket</div>
                <div style={{ color: bs.numColor, fontSize: 38, fontWeight: 900, lineHeight: 1 }}>{bracket.bracket}</div>
                <div style={{ color: TEXT, fontSize: 11, fontWeight: 600 }}>{bracket.bracket_label}</div>
                <div style={{ color: MUTED, fontSize: 9, marginTop: 2 }}>
                  {bracket.game_changer_count} GC{bracket.game_changer_count !== 1 ? 's' : ''}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Speed + win condition badges — inline-block, no wrapping issues */}
        <div style={{ marginBottom: 18, lineHeight: '26px' }}>
          {analysis.speed && (() => {
            const s = SPEED_STYLE[analysis.speed.label] ?? SPEED_STYLE.Battlecruiser
            return (
              <span style={{
                display: 'inline-block',
                backgroundColor: s.bg, border: `1px solid ${s.border}`, color: s.text,
                borderRadius: 4, padding: '2px 8px', fontSize: 11, fontWeight: 700,
                marginRight: 6, verticalAlign: 'middle',
              }}>
                {analysis.speed.label}
              </span>
            )
          })()}
          {analysis.win_conditions?.map(wc => (
            <span key={wc} style={{
              display: 'inline-block',
              backgroundColor: SURFACE, border: `1px solid ${BORDER}`, color: TEXT,
              borderRadius: 4, padding: '2px 8px', fontSize: 11, fontWeight: 600,
              marginRight: 6, verticalAlign: 'middle',
            }}>
              {wc}
            </span>
          ))}
        </div>

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 18 }} />

        {/* Interaction stats — 4 fixed-width inline-block columns */}
        {analysis.interaction && (
          <div style={{ marginBottom: 18, whiteSpace: 'nowrap' }}>
            {[
              { label: 'Removal',  value: analysis.interaction.removal },
              { label: 'Wipes',    value: analysis.interaction.board_wipes },
              { label: 'Counters', value: analysis.interaction.counterspells },
              { label: 'Tutors',   value: analysis.interaction.tutors },
            ].map(({ label, value }, i) => (
              <div key={label} style={{
                display: 'inline-block',
                verticalAlign: 'top',
                width: STAT_W,
                marginLeft: i === 0 ? 0 : STAT_GAP,
                borderLeft: i > 0 ? `1px solid ${BORDER}` : undefined,
                paddingLeft: i > 0 ? STAT_GAP : 0,
                textAlign: 'center',
                boxSizing: 'border-box',
              }}>
                <div style={{ color: TEXT, fontSize: 26, fontWeight: 900, lineHeight: 1 }}>{value}</div>
                <div style={{ color: MUTED, fontSize: 9, marginTop: 5, textTransform: 'uppercase', letterSpacing: 0.5 }}>{label}</div>
              </div>
            ))}
          </div>
        )}

        {/* Divider */}
        <div style={{ height: 1, backgroundColor: BORDER, marginBottom: 18 }} />

        {/* Mana curve — absolute positioning within fixed-height container */}
        <div style={{ marginBottom: 20 }}>
          <div style={{ color: MUTED, fontSize: 9, fontWeight: 700, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 8 }}>
            Mana Curve
          </div>
          {/* Outer wrapper gives the chart its height */}
          <div style={{ position: 'relative', height: BAR_MAX_PX + 32, width: CONTENT_W }}>
            {[0, 1, 2, 3, 4, 5, 6, 7].map((cmc, i) => {
              const count = analysis.mana_curve[String(cmc)] || 0
              const barH = count > 0 ? Math.max(4, Math.round((count / maxCount) * BAR_MAX_PX)) : 0
              const left = i * (BAR_W + BAR_GAP)
              // Layout from bottom: [cmc label 12px][bar barH px][count label 12px]
              return (
                <div key={cmc} style={{ position: 'absolute', left, width: BAR_W, bottom: 0, top: 0 }}>
                  {/* CMC label at very bottom */}
                  <div style={{
                    position: 'absolute', bottom: 0, left: 0, width: BAR_W,
                    textAlign: 'center', color: MUTED, fontSize: 9, lineHeight: '12px',
                  }}>
                    {cmc === 7 ? '7+' : cmc}
                  </div>
                  {/* Bar sitting above cmc label */}
                  {barH > 0 && (
                    <div style={{
                      position: 'absolute', bottom: 14, left: 0, width: BAR_W, height: barH,
                      backgroundColor: GOLD, borderRadius: '3px 3px 0 0',
                    }} />
                  )}
                  {/* Count label above bar */}
                  {count > 0 && (
                    <div style={{
                      position: 'absolute', bottom: 14 + barH + 2, left: 0, width: BAR_W,
                      textAlign: 'center', color: MUTED, fontSize: 9, lineHeight: '12px',
                    }}>
                      {count}
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Footer: color pips left, branding right — table layout */}
        <div style={{ display: 'table', width: '100%' }}>
          <div style={{ display: 'table-cell', verticalAlign: 'middle' }}>
            {Object.keys(analysis.colors).map(color => {
              const s = COLOR_BADGE[color]
              if (!s) return null
              return (
                <span key={color} style={{
                  display: 'inline-block',
                  backgroundColor: s.bg, color: s.text,
                  borderRadius: 4, padding: '2px 7px',
                  fontSize: 11, fontWeight: 900,
                  marginRight: 5, verticalAlign: 'middle',
                }}>
                  {s.label}
                </span>
              )
            })}
          </div>
          <div style={{ display: 'table-cell', verticalAlign: 'middle', textAlign: 'right' }}>
            <span style={{ color: '#1e3a5f', fontSize: 11 }}>pod-calibrator</span>
          </div>
        </div>
      </div>
    )
  }
)

export default ShareCard
