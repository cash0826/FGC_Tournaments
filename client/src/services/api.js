const BASE_URL = import.meta.env.VITE_API_URL || '/api'

export class ApiError extends Error {
  constructor(message, status) {
    super(message)
    this.name = 'ApiError'
    this.status = status
  }
}

export async function apiFetch(path, { headers, ...options } ={} ) {
  const token = localStorage.getItem("token")

  const response = await fetch(`${BASE_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {} ),
      ...headers,
    },
    ...options
  })

  // Handle no body responses
  if (response.status === 204) {
    return null
  }

  const data = await response.json().catch( ()=> null)

  // Throw errors
  if (!response.ok) {
    throw new ApiError(data?.error || data?.msg || 'request failed', response.status)
  }

  return data
}

export const api = {
  get: (path) => apiFetch(path),
  post: (path, body) => apiFetch(path, { method: 'POST', body: JSON.stringify(body) }),
  patch: (path, body) => apiFetch(path, { method: 'PATCH', body: JSON.stringify(body) }),
  delete: (path) => apiFetch(path, { method: 'DELETE' }),
}