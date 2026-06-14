export type ChatMessage = { role: 'user' | 'assistant'; content: string };
export type RequirementProfile = { category: string | null; budget_max: number | null; currency: string; brands_excluded: string[]; priorities: string[]; use_cases: string[]; constraints: Record<string, unknown> };
export type Product = { id: string; title: string; brand: string; category: string; image: string; price: number; currency: string; rating: number; specs: Record<string, string>; reviews: string[] };
export type Recommendation = { product: Product; score: number; pros: string[]; cons: string[]; explanation: string };
export type SearchResponse = { session_id: string; requirements: RequirementProfile; recommendations: Recommendation[]; comparison: Array<Record<string, string | number>>; assistant_message: string };
