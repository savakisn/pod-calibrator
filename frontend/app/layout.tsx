import type { Metadata, Viewport } from 'next'
import AnalyticsProvider from '@/components/AnalyticsProvider'
import './globals.css'

export const metadata: Metadata = {
  title: 'Caliber',
  description: 'Commander deck analyzer',
}

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>
        <AnalyticsProvider />
        {children}
      </body>
    </html>
  )
}
