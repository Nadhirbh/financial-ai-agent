import React from 'react'

type Props = {
  title?: string
  actions?: React.ReactNode
  className?: string
  children: React.ReactNode
}

export default function Card({ title, actions, className = '', children }: Props) {
  return (
    <section className={`border rounded-lg bg-white dark:bg-gray-800 dark:border-gray-700 ${className}`}>
      {(title || actions) && (
        <header className="px-4 py-3 border-b dark:border-gray-700 flex items-center gap-3">
          {title && <h3 className="text-sm font-semibold text-gray-900 dark:text-gray-100">{title}</h3>}
          <div className="ml-auto flex items-center gap-2">{actions}</div>
        </header>
      )}
      <div className="p-4">{children}</div>
    </section>
  )
}
