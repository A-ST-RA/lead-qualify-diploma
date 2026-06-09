const API_BASE = import.meta.env.VITE_API_URL ?? '/api'

export async function predictLead(lead) {
  const response = await fetch(`${API_BASE}/predict`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(lead),
  })

  if (!response.ok) {
    const detail = await response.json().catch(() => null)
    throw new Error(detail?.detail ?? `Ошибка API (${response.status})`)
  }

  return response.json()
}

export async function checkHealth() {
  const response = await fetch(`${API_BASE}/health`)
  if (!response.ok) return { status: 'error', model_loaded: false }
  return response.json()
}
