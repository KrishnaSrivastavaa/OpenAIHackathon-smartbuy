import axios from 'axios';
import type { ChatMessage, SearchResponse } from '../types/commerce';
const api = axios.create({ baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000', timeout: 30000 });
export async function searchProducts(query: string, sessionId?: string, history: ChatMessage[] = []): Promise<SearchResponse> {
  const { data } = await api.post<SearchResponse>('/api/search', { query, session_id: sessionId, history });
  return data;
}
