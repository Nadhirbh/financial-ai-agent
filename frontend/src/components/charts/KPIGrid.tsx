import React from 'react'

type KPI = { label: string; value: string }
type Props = { items: KPI[] }

export default function KPIGrid({ items }: Props) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {items.map((k, i) => (
        <div key={i} className="border rounded p-4 bg-white dark:bg-gray-800 dark:border-gray-700 transition hover:shadow-sm">
          <div className="text-sm text-gray-600 dark:text-gray-300">{k.label}</div>
          <div className="text-2xl font-semibold text-gray-900 dark:text-gray-100">{k.value}</div>
        </div>
      ))}
    </div>
  )
}
