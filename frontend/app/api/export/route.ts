import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const res = await fetch('http://localhost:8000/api/export', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!res.ok) {
    return NextResponse.json({ error: 'Export failed' }, { status: 500 })
  }
  const blob = await res.arrayBuffer()
  const contentDisposition = res.headers.get('content-disposition') ?? 'attachment; filename="deck-pod-calibrator.jpg"'
  return new NextResponse(blob, {
    headers: {
      'Content-Type': 'image/jpeg',
      'Content-Disposition': contentDisposition,
    },
  })
}
