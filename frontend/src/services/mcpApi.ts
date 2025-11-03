import { api } from './apiClient'

export type ForecastPoint = { ts: string; value: number }
export type HistoryPoint = { ts: string; value: number; ema: number }
export type ForecastResponse = {
  ticker: string
  history: HistoryPoint[]
  forecast: ForecastPoint[]
  metrics: { last_deviation?: number; window?: number }
}

export type RecommendationResponse = {
  ticker: string
  window: number
  action: 'buy' | 'sell' | 'neutral'
  confidence: number
  rationale: string
}

export async function fetchForecast(ticker: string, horizonDays = 7, window = 14): Promise<ForecastResponse> {
  const { data } = await api.post('/api/v1/mcp/forecast', { ticker, horizon_days: horizonDays, window })
  return data as ForecastResponse
}

export async function fetchRecommendation(ticker: string, window = 14): Promise<RecommendationResponse> {
  const { data } = await api.get('/api/v1/mcp/recommendation', { params: { ticker, window } })
  return data as RecommendationResponse
}
