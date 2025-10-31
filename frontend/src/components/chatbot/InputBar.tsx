import React from 'react'

type Props = { value: string; onChange: (v: string) => void; onSend: () => void }
export default function InputBar({ value, onChange, onSend }: Props) {
  return (
    <div className="flex gap-2">
      <input className="flex-1 border rounded px-3 py-2" value={value} onChange={e => onChange(e.target.value)} />
      <button className="px-4 py-2 bg-blue-600 text-white rounded" onClick={onSend}>Envoyer</button>
    </div>
  )
}
