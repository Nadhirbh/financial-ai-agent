import { api } from './apiClient'

export async function sendChat(message: string): Promise<string> {
  const { data } = await api.post('/api/v1/chat', { message })
  return data.reply as string
}
