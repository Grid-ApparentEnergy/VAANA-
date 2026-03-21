const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function queryMDM({ query, device_id = '', period_type = 'THIS_WEEK' }) {
  const res = await fetch(`${BASE_URL}/query/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, device_id, period_type }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Query failed');
  }
  return res.json();
}

export async function submitFeedback({ query, sql_used, rating, comment = '' }) {
  const res = await fetch(`${BASE_URL}/feedback/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, sql_used, rating, comment }),
  });
  return res.json();
}
