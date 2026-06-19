import React, { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

const API_BASE = 'http://localhost:8003'

interface TenderRecord {
  filename: string
  date: number
  job_number: string
  unit_id: string
  unit_name: string
  brief: {
    title?: string
    category?: string
    type?: string
  }
}

interface SearchResult {
  query: string
  page: number
  total_records: number
  total_pages: number
  records: TenderRecord[]
}

function formatDate(n: number): string {
  const s = String(n)
  return `${s.slice(0, 4)}-${s.slice(4, 6)}-${s.slice(6, 8)}`
}

export default function SearchPage() {
  const [query, setQuery] = useState('')
  const [page, setPage] = useState(1)

  const { data, isLoading, isError, refetch } = useQuery<SearchResult>({
    queryKey: ['search', query, page],
    queryFn: async () => {
      const resp = await axios.get(`${API_BASE}/api/tenders/search`, {
        params: { q: query, page },
      })
      return resp.data
    },
    enabled: query.length > 0,
  })

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    if (query.trim()) {
      setPage(1)
      refetch()
    }
  }

  return (
    <div>
      {/* Search bar */}
      <form onSubmit={handleSearch} className="mb-6">
        <div className="flex gap-2">
          <input
            type="text"
            value={query}
            onChange={e => setQuery(e.target.value)}
            placeholder="輸入關鍵字，如「資訊」、「網站」、「系統」..."
            className="flex-1 px-4 py-3 border border-slate-300 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent shadow-sm"
          />
          <button
            type="submit"
            className="px-6 py-3 bg-primary-600 text-white rounded-xl text-sm font-medium hover:bg-primary-700 transition-colors shadow-sm"
          >
            搜尋
          </button>
        </div>
      </form>

      {/* Results */}
      {isLoading && (
        <div className="text-center py-12 text-slate-500">搜尋中...</div>
      )}

      {isError && (
        <div className="bg-red-50 border border-red-200 rounded-xl p-4 text-sm text-red-700">
          搜尋失敗，請確認後端已啟動（cd backend && uvicorn main:app --reload）
        </div>
      )}

      {data && (
        <div>
          {/* Stats */}
          <div className="mb-4 text-sm text-slate-500">
            找到 <span className="font-semibold text-slate-700">{data.total_records}</span> 筆標案，
            第 <span className="font-semibold">{data.page}</span> / {data.total_pages} 頁
          </div>

          {/* Tender list */}
          <div className="grid gap-3">
            {data.records.map((tender) => (
              <div key={tender.filename} className="tender-card">
                <div className="flex items-start justify-between gap-2">
                  <div className="flex-1 min-w-0">
                    <p className="font-medium text-slate-900 text-sm leading-snug line-clamp-2">
                      {tender.brief?.title || '（無標題）'}
                    </p>
                    <p className="text-xs text-slate-500 mt-1">
                      {tender.unit_name} · {formatDate(tender.date)}
                    </p>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {tender.brief?.category && (
                        <span className="px-2 py-0.5 bg-slate-100 text-slate-600 rounded text-xs">
                          {tender.brief.category}
                        </span>
                      )}
                      {tender.brief?.type && (
                        <span className="px-2 py-0.5 bg-blue-50 text-blue-600 rounded text-xs">
                          {tender.brief.type}
                        </span>
                      )}
                    </div>
                  </div>
                  <button className="text-primary-600 hover:text-primary-700 text-xs font-medium shrink-0">
                    查看 →
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {data.total_pages > 1 && (
            <div className="flex justify-center gap-2 mt-6">
              <button
                onClick={() => setPage(p => Math.max(1, p - 1))}
                disabled={page === 1}
                className="px-4 py-2 border border-slate-300 rounded-lg text-sm disabled:opacity-40 hover:bg-slate-50"
              >
                上一頁
              </button>
              <span className="px-4 py-2 text-sm text-slate-600">
                {page} / {data.total_pages}
              </span>
              <button
                onClick={() => setPage(p => p + 1)}
                disabled={page >= data.total_pages}
                className="px-4 py-2 border border-slate-300 rounded-lg text-sm disabled:opacity-40 hover:bg-slate-50"
              >
                下一頁
              </button>
            </div>
          )}
        </div>
      )}

      {/* Empty state */}
      {!query && (
        <div className="text-center py-16 text-slate-400">
          <div className="text-4xl mb-3">🔍</div>
          <p className="text-sm">輸入關鍵字開始搜尋政府標案</p>
        </div>
      )}
    </div>
  )
}
