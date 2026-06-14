import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { HeroSearch } from '../components/HeroSearch';
import { ProductCard } from '../components/ProductCard';
import { ComparisonTable } from '../components/ComparisonTable';
import { RefinementSidebar } from '../components/RefinementSidebar';
import { searchProducts } from '../api/client';
import type { ChatMessage, SearchResponse } from '../types/commerce';
export function ResultsPage() {
  const [params, setParams] = useSearchParams();
  const [data, setData] = useState<SearchResponse | null>(null);
  const [history, setHistory] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const run = async (query: string) => { setLoading(true); setError(null); try { const nextHistory: ChatMessage[] = [...history, { role: 'user', content: query }]; const result = await searchProducts(query, data?.session_id, nextHistory); setData(result); setHistory([...nextHistory, { role: 'assistant', content: result.assistant_message }]); setParams({ q: query }); } catch { setError('Unable to fetch recommendations. Check that the FastAPI backend is running.'); } finally { setLoading(false); } };
  useEffect(() => { const q = params.get('q'); if (q && !data && !loading) void run(q); }, []);
  return <div className="min-h-screen bg-slate-50"><HeroSearch onSearch={run} loading={loading}/><main className="mx-auto grid max-w-7xl gap-8 px-6 py-10 lg:grid-cols-[1fr_340px]"><section><h2 className="text-3xl font-black text-slate-950">Top recommendations</h2>{error && <div className="mt-4 rounded-2xl bg-rose-50 p-4 text-rose-700">{error}</div>}{loading && <div className="mt-6 grid gap-5 md:grid-cols-2">{[1,2,3,4].map(i => <div key={i} className="h-96 animate-pulse rounded-3xl bg-slate-200" />)}</div>}<div className="mt-6 grid gap-5 md:grid-cols-2">{data?.recommendations.map(r => <ProductCard key={r.product.id} recommendation={r}/>)}</div>{data && <><h2 className="mt-10 text-2xl font-black text-slate-950">Product comparison</h2><div className="mt-4"><ComparisonTable rows={data.comparison}/></div></>}</section><RefinementSidebar history={history} onAsk={run} loading={loading}/></main></div>;
}
