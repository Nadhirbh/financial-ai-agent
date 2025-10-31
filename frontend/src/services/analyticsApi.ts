import { api } from './apiClient'

export async function fetchHealth(): Promise<'healthy' | 'ok'> {
  const { data } = await api.get('/api/v1/health')
  return (data.status || 'ok') as any
}
