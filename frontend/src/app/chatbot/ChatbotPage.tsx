import React, { useState } from 'react'
import ChatWindow, { ChatMessage } from '../../components/chatbot/ChatWindow'
import InputBar from '../../components/chatbot/InputBar'
import { sendChat } from '../../services/chatbotApi'
import { fetchForecast, fetchRecommendation } from '../../services/mcpApi'

export default function ChatbotPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSend() {
    const q = input.trim()
    if (!q) return
    setInput('')
    const userMsg: ChatMessage = { role: 'user', text: q }
    setMessages((prev: ChatMessage[]) => [...prev, userMsg])
    setLoading(true)
    try {
      const resp = await sendChat(q)
      const assistant: ChatMessage = {
        role: 'assistant',
        text: resp.reply,
        sources: resp.sources?.map(s => ({ title: s.title, url: s.url })) || [],
      }
      setMessages((prev: ChatMessage[]) => [...prev, assistant])

      // Lightweight intent detection for MCP forecast/reco
      const intent = /\b(pr[eé]vision|forecast|reco|recommendation)\b/i.test(q)
      // Try to detect a ticker (simple heuristic: 2-5 uppercase letters)
      const m = q.match(/\b[A-Z]{2,5}\b/)
      const ticker = m?.[0]
      if (intent && ticker) {
        try {
          const [fc, rec] = await Promise.all([
            fetchForecast(ticker, 7, 14),
            fetchRecommendation(ticker, 14),
          ])
          const summary = `Prévision ${ticker} (7j): valeur projetée ~ ${fc.forecast?.[fc.forecast.length-1]?.value?.toFixed?.(2) ?? '—'} ; ` +
            `Reco: ${rec.action.toUpperCase()} (${Math.round((rec.confidence||0)*100)}%), ` +
            `${rec.rationale}`
          const mcpMsg: ChatMessage = { role: 'assistant', text: summary }
          setMessages((prev: ChatMessage[]) => [...prev, mcpMsg])
        } catch (e) {
          const mcpMsg: ChatMessage = { role: 'assistant', text: "(MCP) Impossible de calculer la prévision/reco maintenant." }
          setMessages((prev: ChatMessage[]) => [...prev, mcpMsg])
        }
      }
    } catch (e) {
      const assistant: ChatMessage = { role: 'assistant', text: "Erreur lors de l'appel au chatbot." }
      setMessages((prev: ChatMessage[]) => [...prev, assistant])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto space-y-4">
      <h2 className="text-lg font-semibold">Chatbot</h2>
      <ChatWindow messages={messages} />
      <div className="space-y-2">
        <InputBar value={input} onChange={setInput} onSend={onSend} />
        {loading && <div className="text-sm text-gray-500">Génération en cours…</div>}
      </div>
    </div>
  )
}
