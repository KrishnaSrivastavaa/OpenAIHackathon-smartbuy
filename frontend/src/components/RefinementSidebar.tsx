import { FormEvent, useState } from 'react';
import { MessageSquare } from 'lucide-react';
import type { ChatMessage } from '../types/commerce';
import { Button } from './ui/Button';
export function RefinementSidebar({ history, onAsk, loading }: { history: ChatMessage[]; onAsk: (query: string) => void; loading: boolean }) {
  const [query, setQuery] = useState('Show lighter options.');
  const submit = (event: FormEvent) => { event.preventDefault(); if (query.trim()) onAsk(query.trim()); };
  return <aside className="rounded-3xl border border-slate-200 bg-white p-5 shadow-xl"><h2 className="flex items-center gap-2 text-lg font-bold"><MessageSquare/> Refine results</h2><div className="mt-4 max-h-72 space-y-3 overflow-y-auto">{history.map((m,i) => <div key={i} className={m.role === 'user' ? 'rounded-2xl bg-indigo-50 p-3 text-sm' : 'rounded-2xl bg-slate-100 p-3 text-sm'}>{m.content}</div>)}</div><form onSubmit={submit} className="mt-4 space-y-3"><textarea className="min-h-24 w-full rounded-2xl border p-3 outline-indigo-500" value={query} onChange={e => setQuery(e.target.value)} placeholder="Prioritize battery life, exclude Lenovo..."/><Button className="w-full" disabled={loading}>{loading ? 'Updating...' : 'Send refinement'}</Button></form></aside>;
}
