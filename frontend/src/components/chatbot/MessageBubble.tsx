import React from 'react'

type Props = { role: 'user' | 'assistant'; text: string }
export default function MessageBubble({ role, text }: Props) {
  const isUser = role === 'user'
  return (
    <div className={`p-2 rounded ${isUser ? 'bg-blue-100' : 'bg-gray-100'}`}>{text}</div>
  )
}
