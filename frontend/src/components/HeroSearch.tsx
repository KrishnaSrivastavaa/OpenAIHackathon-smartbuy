import { FormEvent, useState } from 'react';
import { Search, Sparkles } from 'lucide-react';
import { Button } from './ui/Button';

type Props = { onSearch: (query: string) => void; loading?: boolean };
export function HeroSearch({ onSearch, loading }: Props) {
  const [query, setQuery] = useState('I need a gaming laptop under ₹80,000 for coding and occasional gaming.');
  const submit = (event: FormEvent) => { event.preventDefault(); if (query.trim()) onSearch(query.trim()); };
  return <section className="relative overflow-hidden bg-slate-950 px-6 py-20 text-white">
    <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,#6366f1,transparent_35%),radial-gradient(circle_at_bottom_right,#14b8a6,transparent_30%)] opacity-70" />
    <div className="relative mx-auto max-w-5xl text-center">
      <div className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/20 px-4 py-2 text-sm"><Sparkles size={16}/> AI-powered shopping co-pilot</div>
      <h1 className="text-5xl font-black tracking-tight md:text-7xl">CommercePilot</h1>
      <p className="mx-auto mt-5 max-w-2xl text-lg text-slate-200">Describe what you need in plain language. Our LangGraph agents extract requirements, search products, filter trade-offs, analyze reviews, and explain the best picks.</p>
      <form onSubmit={submit} className="glass mx-auto mt-10 flex max-w-3xl flex-col gap-3 rounded-3xl p-3 md:flex-row">
        <div className="flex flex-1 items-center gap-3 px-4 text-slate-500"><Search size={22}/><input className="w-full bg-transparent py-3 text-slate-900 outline-none" value={query} onChange={e => setQuery(e.target.value)} placeholder="What are you shopping for?" /></div>
        <Button disabled={loading}>{loading ? 'Piloting...' : 'Find products'}</Button>
      </form>
    </div>
  </section>;
}
