import { api } from './apiClient'

export type ChatResponse = {
  reply: string
  sources: { score: number; title: string; url: string; content?: string }[]
}

export async function sendChat(message: string): Promise<ChatResponse> {
  const { data } = await api.post('/api/v1/chat', { message })
  return data as ChatResponse
}
