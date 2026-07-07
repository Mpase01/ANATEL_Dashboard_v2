const API_BASE_URL = window.ANATEL_API_BASE_URL || "http://localhost:8000";

async function request(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Erro ${response.status}`);
  }
  return response.json();
}

export async function checkHealth() {
  return request("/health");
}

export async function searchProviders(query) {
  const params = new URLSearchParams({ query, limit: "20" });
  return request(`/providers/search?${params.toString()}`);
}

export async function getProviderDashboard(providerId) {
  const [summary, evolution, technologies, municipalities] = await Promise.all([
    request(`/providers/${providerId}/summary`),
    request(`/providers/${providerId}/evolution`),
    request(`/providers/${providerId}/technologies`),
    request(`/providers/${providerId}/municipalities?limit=20`),
  ]);

  return { summary, evolution, technologies, municipalities };
}
