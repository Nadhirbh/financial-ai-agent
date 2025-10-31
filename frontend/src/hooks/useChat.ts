import { useState } from 'react'
import { sendChat } from '../services/chatbotApi'

export function useChat() {
  const [messages, setMessages] = useState<{ role: 'user' | 'assistant'; text: string }[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  async function onSend() {
    if (!input.trim()) return
    const userMsg = { role: 'user' as const, text: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)
    try {
      const reply = await sendChat(userMsg.text)
      setMessages(prev => [...prev, { role: 'assistant', text: reply }])
    } finally {
      setLoading(false)
    }
  }

  return { messages, input, setInput, onSend, loading }
}
