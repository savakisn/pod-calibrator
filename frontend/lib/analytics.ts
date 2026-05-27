import posthog from 'posthog-js'

type EventMap = {
  deck_imported: { source: 'moxfield' | 'archidekt' | 'unknown'; cache_hit: boolean; analysis_ms: number }
  import_failed: { source: 'moxfield' | 'archidekt' | 'unknown'; status?: number; error_message: string }
  pod_assembled: { deck_count: number }
  colorblind_mode_changed: { mode: 'protanopia' | 'deuteranopia' | 'tritanopia' }
  export_clicked: { format: 'single' | 'comparison_table' | 'all_combined'; deck_count: number }
}

export function initAnalytics() {
  if (typeof window === 'undefined') return
  const key = process.env.NEXT_PUBLIC_POSTHOG_KEY
  if (!key) return
  if (posthog.__loaded) return
  posthog.init(key, {
    api_host: process.env.NEXT_PUBLIC_POSTHOG_HOST || 'https://us.i.posthog.com',
    capture_pageview: true,
    person_profiles: 'identified_only',
  })
}

export function track<E extends keyof EventMap>(event: E, props: EventMap[E]) {
  if (typeof window === 'undefined') return
  if (!posthog.__loaded) return
  posthog.capture(event, props)
}

export function deckSource(url: string): 'moxfield' | 'archidekt' | 'unknown' {
  if (url.includes('moxfield.com')) return 'moxfield'
  if (url.includes('archidekt.com')) return 'archidekt'
  return 'unknown'
}
