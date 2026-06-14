export function ComparisonTable({ rows }: { rows: Array<Record<string, string | number>> }) {
  const columns = Array.from(new Set(rows.flatMap(row => Object.keys(row)))).slice(0, 9);
  if (!rows.length) return null;
  return <div className="overflow-x-auto rounded-3xl border border-slate-200 bg-white"><table className="min-w-full text-left text-sm"><thead className="bg-slate-100 text-slate-700"><tr>{columns.map(c => <th className="px-4 py-3" key={c}>{c}</th>)}</tr></thead><tbody>{rows.map((row, i) => <tr className="border-t" key={i}>{columns.map(c => <td className="px-4 py-3" key={c}>{row[c] ?? '—'}</td>)}</tr>)}</tbody></table></div>;
}
