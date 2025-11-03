import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import ThemeToggle from '../components/ui/ThemeToggle'
import ChatbotPage from './chatbot/ChatbotPage'
import DashboardPage from './dashboard/DashboardPage'

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <nav className="sticky top-0 z-10 p-4 border-b bg-white/90 backdrop-blur flex gap-4 items-center dark:bg-gray-900/80 dark:border-gray-800">
        <div className="font-semibold">Financial AI</div>
        <Link className="hover:underline" to="/">Accueil</Link>
        <Link className="hover:underline" to="/chat">Chatbot</Link>
        <Link className="hover:underline" to="/dashboard">Dashboard</Link>
        <ThemeToggle />
      </nav>
      <Routes>
        <Route path="/" element={<div className="p-6">Bienvenue</div>} />
        <Route path="/chat" element={<ChatbotPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </BrowserRouter>
  )
}
