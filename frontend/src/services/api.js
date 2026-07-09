const API_BASE_URL = window.ANATEL_API_BASE_URL || "http://localhost:8001";

const demoProvider = {
  id: 2,
  cnpj: "10785849000171",
  name: "NET-UAI INTERNET WIRELESS",
};

const demoDashboard = {
  summary: {
    provider_id: 2,
    cnpj: "10785849000171",
    name: "NET-UAI INTERNET WIRELESS",
    period: "2026-05-01",
    subscriptions_count: 105,
    fiber_count: 13,
    fiber_share_percent: 12.38,
    market_share_percent: 100,
    municipalities_count: 2,
    states_count: 1,
    top_municipality_name: "Lagoa Formosa",
    top_municipality_state: "MG",
    growth_percent: 15.38,
  },
  evolution: [
    { period: "2026-01-01", subscriptions_count: 91 },
    { period: "2026-02-01", subscriptions_count: 81 },
    { period: "2026-03-01", subscriptions_count: 92 },
    { period: "2026-04-01", subscriptions_count: 86 },
    { period: "2026-05-01", subscriptions_count: 105 },
  ],
  technologies: [
    { technology: "ETHERNET", access_medium: "Radio", subscriptions_count: 92, share_percent: 87.62 },
    { technology: "FTTH", access_medium: "Fibra", subscriptions_count: 13, share_percent: 12.38 },
  ],
  municipalities: [
    { municipality_name: "Lagoa Formosa", state: "MG", municipality_code: "3137502", subscriptions_count: 84 },
    { municipality_name: "Patos de Minas", state: "MG", municipality_code: "3148004", subscriptions_count: 21 },
  ],
};

let demoMode = false;

async function request(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);
  if (!response.ok) {
    throw new Error(`Erro ${response.status}`);
  }
  return response.json();
}

export async function checkHealth() {
  try {
    const result = await request("/health");
    demoMode = false;
    return result;
  } catch (error) {
    demoMode = true;
    return { status: "demo" };
  }
}

export async function searchProviders(query) {
  if (demoMode) {
    const text = query.trim().toLowerCase();
    const matchesName = demoProvider.name.toLowerCase().includes(text);
    const matchesCnpj = demoProvider.cnpj.includes(text.replace(/\D/g, ""));
    return matchesName || matchesCnpj || text === "" ? [demoProvider] : [];
  }

  const params = new URLSearchParams({ query, limit: "20" });
  return request(`/providers/search?${params.toString()}`);
}

export async function getProviderDashboard(providerId, period = "all") {
  if (demoMode) {
    return buildDemoDashboard(period);
  }

  const params = new URLSearchParams({ period });
  const [summary, evolution, technologies, municipalities] = await Promise.all([
    request(`/providers/${providerId}/summary?${params.toString()}`),
    request(`/providers/${providerId}/evolution?${params.toString()}`),
    request(`/providers/${providerId}/technologies?${params.toString()}`),
    request(`/providers/${providerId}/municipalities?${new URLSearchParams({ period, limit: "20" }).toString()}`),
  ]);

  return { summary, evolution, technologies, municipalities };
}

export function isDemoMode() {
  return demoMode;
}

function buildDemoDashboard(period) {
  const evolution = filterEvolution(demoDashboard.evolution, period);
  const firstValue = Number(evolution[0]?.subscriptions_count || 0);
  const lastValue = Number(evolution.at(-1)?.subscriptions_count || 0);
  const growth = firstValue > 0 ? ((lastValue - firstValue) / firstValue) * 100 : 0;
  return {
    ...demoDashboard,
    summary: {
      ...demoDashboard.summary,
      period: evolution.at(-1)?.period || demoDashboard.summary.period,
      subscriptions_count: lastValue || demoDashboard.summary.subscriptions_count,
      growth_percent: growth,
    },
    evolution,
  };
}

function filterEvolution(rows, period) {
  if (period === "latest") {
    return rows.slice(-1);
  }
  if (period === "last3") {
    return rows.slice(-3);
  }
  return rows;
}
