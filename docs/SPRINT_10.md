# Sprint 10 - Dashboard inicial

## Objetivo

Criar a primeira versao funcional do dashboard consultando os dados ja gravados no backend/Supabase.

Esta sprint ainda usa dados de amostra.

A carga completa das planilhas da ANATEL ainda nao foi feita.

## O que foi implementado

Backend:

- endpoint `GET /providers/{provider_id}/summary`;
- endpoint `GET /providers/{provider_id}/evolution`;
- endpoint `GET /providers/{provider_id}/technologies`;
- endpoint `GET /providers/{provider_id}/municipalities`;
- camada `backend/app/repositories/dashboard.py` com consultas agregadas;
- CORS liberado para desenvolvimento local.

Frontend:

- tela `frontend/index.html`;
- servico `frontend/src/services/api.js` para consumir a API;
- comportamento `frontend/src/pages/dashboard.js`;
- estilos `frontend/src/styles/app.css`.

## Indicadores exibidos

A primeira tela mostra:

- assinantes no ultimo mes disponivel;
- participacao de fibra;
- municipios atendidos;
- crescimento dentro do recorte disponivel;
- evolucao mensal;
- composicao por tecnologia;
- ranking de municipios.

## Dados usados na validacao

A validacao foi feita com os dados existentes no banco:

- amostra ficticia da Sprint 8;
- recorte real do CSV de 2026 da Sprint 9.

Prestadora real validada:

```text
NET-UAI INTERNET WIRELESS
CNPJ: 10785849000171
```

Totais mensais do recorte real:

```text
2026-01: 91
2026-02: 81
2026-03: 92
2026-04: 86
2026-05: 105
```

## Observacoes

O market share ainda deve ser interpretado com cuidado, porque a base no banco ainda e uma amostra pequena.

Quando a carga completa for feita, esse indicador passara a representar a comparacao real dentro da base ANATEL importada.

## Proxima sprint sugerida

Sprint 11:

- rodar o backend e a tela localmente;
- ajustar pequenos detalhes visuais;
- preparar o fluxo de importacao completa com progresso e seguranca;
- revisar performance antes de carregar muitos registros.