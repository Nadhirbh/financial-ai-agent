import React from 'react'
import AppRoutes from './app/routes'

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <header className="p-4 border-b bg-white">
        <h1 className="text-xl font-semibold">Financial AI Agent</h1>
      </header>
      <main className="p-6">
        <AppRoutes />
      </main>
    </div>
  )
}

export default App
