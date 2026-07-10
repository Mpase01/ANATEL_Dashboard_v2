import {
  checkHealth,
  getEconomicGroupDashboard,
  getProviderDashboard,
  isDemoMode,
  searchEconomicGroups,
  searchProviders,
} from "../services/api.js";

const formatInteger = new Intl.NumberFormat("pt-BR", { maximumFractionDigits: 0 });
const formatPercent = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});

const elements = {
  apiStatus: document.querySelector("#apiStatus"),
  entityMode: document.querySelector("#entityMode"),
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
  personTypeList: document.querySelector("#personTypeList"),
  municipalityRows: document.querySelector("#municipalityRows"),
};

async function init() {
  bindEvents();
  await verifyApi();
  await runSearch();
}

function bindEvents() {
  elements.searchButton.addEventListener("click", runSearch);
  elements.entityMode.addEventListener("change", runSearch);
  elements.providerQuery.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
      runSearch();
    }
  });
  elements.providerSelect.addEventListener("change", () => {
    const selectedValue = elements.providerSelect.value;
    if (selectedValue) {
      loadDashboard(selectedValue);
    }
  });
  elements.periodFilter.addEventListener("change", () => {
    const selectedValue = elements.providerSelect.value;
    if (selectedValue) {
      loadDashboard(selectedValue);
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
    const mode = elements.entityMode.value;
    const results = mode === "group" ? await searchEconomicGroups(query) : await searchProviders(query);
    renderEntityOptions(results, mode);
    setStatus(
      results.length ? (isDemoMode() ? "Modo demonstracao" : "Busca concluida") : "Nenhum resultado",
      results.length ? "ok" : "error",
    );

    if (results[0]) {
      elements.providerSelect.value = entityValue(results[0], mode);
      await loadDashboard(elements.providerSelect.value);
    }
  } catch (error) {
    setStatus("Erro na busca", "error");
  }
}

async function loadDashboard(selectedValue) {
  setStatus("Carregando painel...", "loading");
  try {
    const dashboard = elements.entityMode.value === "group"
      ? await getEconomicGroupDashboard(selectedValue, elements.periodFilter.value)
      : await getProviderDashboard(Number(selectedValue), elements.periodFilter.value);
    renderDashboard(dashboard);
    setStatus(isDemoMode() ? "Modo demonstracao" : "Painel atualizado", isDemoMode() ? "loading" : "ok");
  } catch (error) {
    setStatus("Erro ao carregar painel", "error");
  }
}

function renderEntityOptions(results, mode) {
  elements.providerSelect.innerHTML = "";
  for (const result of results) {
    const option = document.createElement("option");
    option.value = entityValue(result, mode);
    const subscribers = Number(result.latest_subscriptions_count || 0);
    const suffix = subscribers ? ` - ${formatInteger.format(subscribers)} acessos` : "";
    option.textContent = mode === "group"
      ? `${result.name}${suffix}`
      : `${result.name} - ${result.cnpj}${suffix}`;
    elements.providerSelect.append(option);
  }
}

function entityValue(result, mode) {
  return mode === "group" ? result.name : String(result.id);
}

function renderDashboard({ summary, evolution, technologies, personTypes = [], municipalities }) {
  const lastValue = Number(evolution.at(-1)?.subscriptions_count || summary.subscriptions_count || 0);
  const growth = Number(summary.growth_percent || 0);
  const fiberShare = Number(summary.fiber_share_percent || 0);

  elements.metricSubscriptions.textContent = formatInteger.format(lastValue);
  elements.metricFiber.textContent = `${formatPercent.format(fiberShare)}%`;
  elements.metricMunicipalities.textContent = formatInteger.format(summary.municipalities_count || 0);
  elements.metricGrowth.textContent = `${formatPercent.format(growth)}%`;
  elements.providerSubtitle.textContent = summary.cnpj
    ? `${summary.name} - CNPJ ${summary.cnpj}`
    : `${summary.name} - Grupo economico`;
  elements.latestPeriod.textContent = periodLabel(evolution);

  renderEvolution(evolution);
  renderTechnologies(technologies);
  renderPersonTypes(personTypes);
  renderMunicipalities(municipalities);
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

function renderPersonTypes(rows) {
  elements.personTypeList.innerHTML = "";
  for (const row of rows) {
    const item = document.createElement("div");
    const label = String(row.person_type || "-");
    const isBusiness = label.toLowerCase().includes("juridica");
    item.className = `stack-item${isBusiness ? " stack-item-featured" : ""}`;
    item.innerHTML = `
      <div>
        <strong>${personTypeLabel(label)}</strong>
        <span>${isBusiness ? "B2B" : "B2C"}</span>
      </div>
      <div class="stack-numbers">
        <strong>${formatInteger.format(row.subscriptions_count || 0)}</strong>
        <span>${formatPercent.format(Number(row.share_percent || 0))}%</span>
      </div>
    `;
    elements.personTypeList.append(item);
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

function personTypeLabel(value) {
  if (value.toLowerCase().includes("juridica")) {
    return "Pessoa Juridica";
  }
  if (value.toLowerCase().includes("fisica")) {
    return "Pessoa Fisica";
  }
  return value;
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
