import React, { useEffect, useState } from 'react'

export default function ThemeToggle() {
  const [dark, setDark] = useState(false)

  useEffect(() => {
    const saved = localStorage.getItem('theme')
    const isDark = saved ? saved === 'dark' : window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
    setDark(isDark)
    document.documentElement.classList.toggle('dark', isDark)
  }, [])

  function toggle() {
    const next = !dark
    setDark(next)
    document.documentElement.classList.toggle('dark', next)
    localStorage.setItem('theme', next ? 'dark' : 'light')
  }

  return (
    <button
      type="button"
      onClick={toggle}
      className="ml-auto inline-flex items-center gap-2 px-3 py-2 rounded border text-sm hover:bg-gray-50 dark:hover:bg-gray-800 dark:border-gray-700"
      aria-label="Toggle theme"
      title="Toggle theme"
    >
      <span className="hidden sm:inline">{dark ? 'Dark' : 'Light'}</span>
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" className="text-gray-700 dark:text-gray-200">
        {dark ? (
          <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" stroke="currentColor" strokeWidth="2"/>
        ) : (
          <g stroke="currentColor" strokeWidth="2">
            <circle cx="12" cy="12" r="4"/>
            <path d="M12 2v2m0 16v2M2 12h2m16 0h2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M4.93 19.07l1.41-1.41M17.66 6.34l1.41-1.41"/>
          </g>
        )}
      </svg>
    </button>
  )
}
