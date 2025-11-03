import React, { useEffect, useMemo, useState } from 'react'
import KPIGrid from '../../components/charts/KPIGrid'
import ForecastChart from '../../components/charts/ForecastChart'
import Card from '../../components/ui/Card'
import Button from '../../components/ui/Button'
import { fetchForecast, fetchRecommendation, ForecastResponse, RecommendationResponse } from '../../services/mcpApi'

export default function DashboardPage() {
  const [ticker, setTicker] = useState('TSLA')
  const [horizon, setHorizon] = useState(7)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [fc, setFc] = useState<ForecastResponse | null>(null)
  const [rec, setRec] = useState<RecommendationResponse | null>(null)

  useEffect(() => {
    let cancelled = false
    async function run() {
      setLoading(true)
      setError(null)
      try {
        const [f, r] = await Promise.all([
          fetchForecast(ticker, horizon, 14),
          fetchRecommendation(ticker, 14),
        ])
        if (!cancelled) {
          setFc(f)
          setRec(r)
        }
      } catch (e: any) {
        if (!cancelled) setError(e?.message || 'Erreur chargement données')
      } finally {
        if (!cancelled) setLoading(false)
      }
    }
    run()
    return () => { cancelled = true }
  }, [ticker, horizon])

  const kpis = useMemo(() => {
    const lastDev = fc?.metrics?.last_deviation ?? 0
    const action = rec?.action?.toUpperCase?.() || '—'
    const conf = rec ? `${Math.round((rec.confidence || 0) * 100)}%` : '—'
    const histLen = fc?.history?.length || 0
    return [
      { label: 'Ticker', value: ticker },
      { label: 'Horizon', value: `${horizon} j` },
      { label: 'Obs. Hist.', value: `${histLen}` },
      { label: 'Last Δ vs EMA', value: `${lastDev}` },
      { label: 'Reco', value: action },
      { label: 'Confiance', value: conf },
    ]
  }, [fc, rec, ticker, horizon])

  return (
    <div className="max-w-6xl mx-auto p-4 sm:p-6 space-y-6">
      <div className="flex items-center gap-3">
        <h2 className="text-xl font-semibold text-gray-900 dark:text-gray-100">Dashboard</h2>
        <div className="ml-auto flex items-center gap-2">
          <Button variant="secondary" size="sm" onClick={() => alert('Export bientôt disponible')}>Export CSV</Button>
        </div>
      </div>

      <Card title="Filtres">
        <div className="flex flex-wrap gap-4 items-end">
          <div>
            <label className="block text-sm text-gray-600 dark:text-gray-300">Ticker</label>
            <input className="border rounded px-3 py-2 dark:bg-gray-900 dark:border-gray-700" value={ticker} onChange={e => setTicker(e.target.value.toUpperCase())} />
          </div>
          <div>
            <label className="block text-sm text-gray-600 dark:text-gray-300">Horizon (jours)</label>
            <select className="border rounded px-3 py-2 dark:bg-gray-900 dark:border-gray-700" value={horizon} onChange={e => setHorizon(parseInt(e.target.value))}>
              <option value={7}>7</option>
              <option value={14}>14</option>
              <option value={30}>30</option>
            </select>
          </div>
          {loading && <div className="text-sm text-gray-500">Chargement…</div>}
          {error && <div className="text-sm text-red-600">{error}</div>}
        </div>
      </Card>

      <Card title="KPIs">
        <KPIGrid items={kpis} />
      </Card>

      <Card title="Prévision">
        <ForecastChart history={fc?.history || []} forecast={fc?.forecast || []} />
      </Card>
    </div>
  )
}
