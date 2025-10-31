import React from 'react'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import ChatbotPage from './chatbot/ChatbotPage'
import DashboardPage from './dashboard/DashboardPage'

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <nav className="p-4 border-b bg-white flex gap-4">
        <Link to="/">Accueil</Link>
        <Link to="/chat">Chatbot</Link>
        <Link to="/dashboard">Dashboard</Link>
      </nav>
      <Routes>
        <Route path="/" element={<div className="p-6">Bienvenue</div>} />
        <Route path="/chat" element={<ChatbotPage />} />
        <Route path="/dashboard" element={<DashboardPage />} />
      </Routes>
    </BrowserRouter>
  )
}
