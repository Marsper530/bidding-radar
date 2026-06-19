import React, { useState } from 'react'
import './index.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import SearchPage from './pages/SearchPage'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 min
    },
  },
})

function App() {
  const [query, setQuery] = useState('')

  return (
    <QueryClientProvider client={queryClient}>
      <div className="min-h-screen bg-slate-50">
        {/* Header */}
        <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
          <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
                <span className="text-white text-sm font-bold">📡</span>
              </div>
              <h1 className="text-lg font-semibold text-slate-900">領標雷達</h1>
            </div>
            <nav className="flex gap-4 text-sm">
              <button className="text-primary-600 font-medium">找標案</button>
              <button className="text-slate-500 hover:text-slate-700">補助</button>
              <button className="text-slate-500 hover:text-slate-700">行情</button>
              <button className="text-slate-500 hover:text-slate-700">我的追蹤</button>
            </nav>
          </div>
        </header>

        {/* Main */}
        <main className="max-w-6xl mx-auto px-4 py-6">
          <SearchPage />
        </main>
      </div>
    </QueryClientProvider>
  )
}

export default App
