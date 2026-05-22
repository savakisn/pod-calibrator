import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Pod Calibrator',
  description: 'Commander deck analyzer',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
