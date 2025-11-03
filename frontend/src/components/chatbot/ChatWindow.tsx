import React from 'react'
import MessageBubble from './MessageBubble'

export type ChatMessage = {
  role: 'user' | 'assistant'
  text: string
  sources?: { title: string; url: string }[]
}

type Props = { messages: ChatMessage[] }

export default function ChatWindow({ messages }: Props) {
  return (
    <div className="border rounded p-4 bg-white space-y-3">
      {messages.length === 0 && (
        <div className="text-gray-500">Posez une question pour commencer.</div>
      )}
      {messages.map((m, i) => (
        <div key={i} className="space-y-1">
          <MessageBubble role={m.role} text={m.text} />
          {m.role === 'assistant' && m.sources && m.sources.length > 0 && (
            <div className="text-xs text-gray-500 pl-2">
              Sources:
              <ul className="list-disc pl-5">
                {m.sources.map((s, j) => (
                  <li key={j}>
                    <a className="underline" href={s.url} target="_blank" rel="noreferrer">
                      {s.title}
                    </a>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      ))}
    </div>
  )}

