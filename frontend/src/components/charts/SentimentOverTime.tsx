import React from 'react'

type Point = { date: string; sentiment_avg: number; volume: number }
type Props = { series: Point[]; title?: string }

export default function SentimentOverTime({ series, title = 'Sentiment (moyenne quotidienne)' }: Props) {
  const width = 600
  const height = 180
  const pad = 24
  if (!series || series.length === 0) {
    return <div className="border rounded p-4 bg-white">Aucune donnée</div>
  }
  const xs = series.map((_, i) => i)
  const ys = series.map(p => p.sentiment_avg)
  const minY = Math.min(-1, ...ys)
  const maxY = Math.max(1, ...ys)
  const xScale = (i: number) => pad + (i * (width - 2 * pad)) / Math.max(1, series.length - 1)
  const yScale = (v: number) => height - pad - ((v - minY) / (maxY - minY || 1)) * (height - 2 * pad)
  const path = xs.map((i, idx) => `${idx === 0 ? 'M' : 'L'} ${xScale(i)} ${yScale(series[i].sentiment_avg)}`).join(' ')

  return (
    <div className="border rounded p-4 bg-white">
      <div className="mb-2 font-medium">{title}</div>
      <svg width={width} height={height} className="w-full h-44">
        <line x1={pad} y1={yScale(0)} x2={width - pad} y2={yScale(0)} stroke="#ddd" />
        <path d={path} fill="none" stroke="#2563eb" strokeWidth={2} />
      </svg>
      <div className="text-xs text-gray-500">{series[0].date} → {series[series.length - 1].date}</div>
    </div>
  )
}
