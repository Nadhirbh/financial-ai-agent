import React from 'react'

type Pt = { ts: string; value: number }

type Props = {
  history: { ts: string; value: number; ema?: number }[]
  forecast: Pt[]
  title?: string
}

export default function ForecastChart({ history, forecast, title = 'Prévision (EMA)' }: Props) {
  const width = 720
  const height = 220
  const pad = 32
  const hist = history || []
  const fcast = forecast || []
  const all = [...hist.map(h => ({ ts: h.ts, value: h.value })), ...fcast]
  if (all.length === 0) return <div className="border rounded p-4 bg-white">Aucune donnée</div>
  const xs = all.map((_, i) => i)
  const ys = all.map(p => p.value)
  const minY = Math.min(...ys)
  const maxY = Math.max(...ys)
  const xScale = (i: number) => pad + (i * (width - 2 * pad)) / Math.max(1, all.length - 1)
  const yScale = (v: number) => height - pad - ((v - minY) / (maxY - minY || 1)) * (height - 2 * pad)
  const pathHist = hist.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${xScale(idx)} ${yScale(p.value)}`).join(' ')
  const startF = hist.length > 0 ? hist.length - 1 : 0
  const pathF = fcast.map((p, k) => `${k === 0 ? 'M' : 'L'} ${xScale(startF + k)} ${yScale(p.value)}`).join(' ')
  const pathEma = hist.map((p, idx) => `${idx === 0 ? 'M' : 'L'} ${xScale(idx)} ${yScale(p.ema ?? p.value)}`).join(' ')

  return (
    <div className="border rounded p-4 bg-white">
      <div className="mb-2 font-medium">{title}</div>
      <svg width={width} height={height} className="w-full h-56">
        <path d={pathHist} fill="none" stroke="#1f2937" strokeWidth={1.5} />
        <path d={pathEma} fill="none" stroke="#2563eb" strokeWidth={2} />
        <path d={pathF} fill="none" stroke="#ef4444" strokeWidth={2} strokeDasharray="6,6" />
      </svg>
      <div className="text-xs text-gray-500">Historique: {hist[0]?.ts} → {hist[hist.length-1]?.ts} • Horizon: {fcast.length}j</div>
    </div>
  )
}
