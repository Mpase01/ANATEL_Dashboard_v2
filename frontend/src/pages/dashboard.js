import { checkHealth, getProviderDashboard, isDemoMode, searchProviders } from "../services/api.js";

const formatInteger = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
const formatPercent = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

const elements = {
  apiStatus: document.querySelector("#apiStatus"),
  providerQuery: document.querySelector("#providerQuery"),
  searchButton: document.querySelector("#searchButton"),
  providerSelect: document.querySelector("#providerSelect"),
  periodFilter: document.querySelector("#periodFilter"),
  metricSubscriptions: document.querySelector("#metricSubscriptions"),
  metricFiber: document.querySelector("#metricFiber"),
  metricMunicipalities: document.querySelector("#metricMunicipalities"),
  metricGrowth: document.querySelector("#metricGrowth"),
  providerSubtitle: document.querySelector("#providerSubtitle"),
  latestPeriod: document.querySelector("#latestPeriod"),
  evolutionChart: document.querySelector("#evolutionChart"),
  technologyList: document.querySelector("#technologyList"),
  municipalityRows: document.querySelector("#municipalityRows"),
};

async function init() {
  bindEvents();
  await verifyApi();
  await runSearch();
}

function bindEvents() {
  elements.searchButton.addEventListener("click", runSearch);
  elements.providerQuery.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      runSearch();
    }
  });
  elements.providerSelect.addEventListener("change", () => {
    const providerId = Number(elements.providerSelect.value);
    if (providerId) {
      loadDashboard(providerId);
    }
  });
  elements.periodFilter.addEventListener("change", () => {
    const providerId = Number(elements.providerSelect.value);
    if (providerId) {
      loadDashboard(providerId);
    }
  });
}

async function verifyApi() {
  await checkHealth();
  setStatus(isDemoMode() ? "Modo demonstracao" : "API online", isDemoMode() ? "loading" : "ok");
}

async function runSearch() {
  const query = elements.providerQuery.value.trim();
  if (!query) {
    return;
  }

  setStatus("Buscando...", "loading");
  try {
    const providers = await searchProviders(query);
    renderProviderOptions(providers);
    setStatus(
      providers.length ? (isDemoMode() ? "Modo demonstracao" : "Busca concluida") : "Nenhum resultado",
      providers.length ? "ok" : "error",
    );

    if (providers[0]) {
      elements.providerSelect.value = String(providers[0].id);
      await loadDashboard(providers[0].id);
    }
  } catch (error) {
    setStatus("Erro na busca", "error");
  }
}

async function loadDashboard(providerId) {
  setStatus("Carregando painel...", "loading");
  try {
    const dashboard = await getProviderDashboard(providerId);
    renderDashboard(dashboard);
    setStatus(isDemoMode() ? "Modo demonstracao" : "Painel atualizado", isDemoMode() ? "loading" : "ok");
  } catch (error) {
    setStatus("Erro ao carregar painel", "error");
  }
}

function renderProviderOptions(providers) {
  elements.providerSelect.innerHTML = "";
  for (const provider of providers) {
    const option = document.createElement("option");
    option.value = provider.id;
    option.textContent = `${provider.name} - ${provider.cnpj}`;
    elements.providerSelect.append(option);
  }
}

function renderDashboard({ summary, evolution, technologies, municipalities }) {
  const filteredEvolution = filterEvolution(evolution);
  const firstValue = Number(filteredEvolution[0]?.subscriptions_count || 0);
  const lastValue = Number(filteredEvolution.at(-1)?.subscriptions_count || summary.subscriptions_count || 0);
  const filteredGrowth = firstValue > 0 ? ((lastValue - firstValue) / firstValue) * 100 : 0;
  const fiberShare = Number(summary.fiber_share_percent || 0);

  elements.metricSubscriptions.textContent = formatInteger.format(lastValue);
  elements.metricFiber.textContent = `${formatPercent.format(fiberShare)}%`;
  elements.metricMunicipalities.textContent = formatInteger.format(summary.municipalities_count || 0);
  elements.metricGrowth.textContent = `${formatPercent.format(filteredGrowth)}%`;
  elements.providerSubtitle.textContent = `${summary.name} - CNPJ ${summary.cnpj}`;
  elements.latestPeriod.textContent = periodLabel(filteredEvolution);

  renderEvolution(filteredEvolution);
  renderTechnologies(technologies);
  renderMunicipalities(municipalities);
}

function filterEvolution(rows) {
  const selected = elements.periodFilter.value;
  if (selected === "latest") {
    return rows.slice(-1);
  }
  if (selected === "last3") {
    return rows.slice(-3);
  }
  return rows;
}

function periodLabel(rows) {
  if (!rows.length) {
    return "-";
  }
  if (rows.length === 1) {
    return formatPeriod(rows[0].period);
  }
  return `${formatPeriod(rows[0].period)} a ${formatPeriod(rows.at(-1).period)}`;
}

function renderEvolution(rows) {
  elements.evolutionChart.innerHTML = "";
  const maxValue = Math.max(...rows.map((row) => Number(row.subscriptions_count || 0)), 1);

  for (const row of rows) {
    const value = Number(row.subscriptions_count || 0);
    const item = document.createElement("div");
    item.className = "bar-item";
    item.innerHTML = `
      <span>${formatPeriod(row.period)}</span>
      <div class="bar-track"><div class="bar-fill" style="width: ${(value / maxValue) * 100}%"></div></div>
      <strong>${formatInteger.format(value)}</strong>
    `;
    elements.evolutionChart.append(item);
  }
}

function renderTechnologies(rows) {
  elements.technologyList.innerHTML = "";
  for (const row of rows) {
    const item = document.createElement("div");
    const isFiber = String(row.access_medium || "").toLowerCase().includes("fibra")
      || String(row.technology || "").toLowerCase().includes("ftth");
    item.className = `stack-item${isFiber ? " stack-item-featured" : ""}`;
    item.innerHTML = `
      <div>
        <strong>${row.technology || "-"}</strong>
        <span>${row.access_medium || "-"}</span>
      </div>
      <div class="stack-numbers">
        <strong>${formatInteger.format(row.subscriptions_count || 0)}</strong>
        <span>${formatPercent.format(Number(row.share_percent || 0))}%</span>
      </div>
    `;
    elements.technologyList.append(item);
  }
}

function renderMunicipalities(rows) {
  elements.municipalityRows.innerHTML = "";
  for (const row of rows) {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.municipality_name}</td>
      <td>${row.state}</td>
      <td>${formatInteger.format(row.subscriptions_count || 0)}</td>
    `;
    elements.municipalityRows.append(tr);
  }
}

function formatPeriod(value) {
  if (!value) {
    return "-";
  }
  const [year, month] = String(value).split("-");
  return `${month}/${year}`;
}

function setStatus(text, kind) {
  elements.apiStatus.textContent = text;
  elements.apiStatus.dataset.kind = kind;
}

init();
