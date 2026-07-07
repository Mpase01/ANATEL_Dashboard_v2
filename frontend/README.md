# Frontend

Frontend do ANATEL Dashboard.

Esta camada apresenta o dashboard online de forma simples, rapida e responsiva.

## Status atual

A primeira tela funcional foi criada na Sprint 10.

Ela permite:

- buscar uma prestadora pela API;
- selecionar uma prestadora encontrada;
- visualizar indicadores principais;
- ver a evolucao mensal;
- ver a composicao por tecnologia;
- ver os municipios do ultimo mes disponivel.

## Como abrir localmente

Primeiro, o backend precisa estar rodando em:

```text
http://localhost:8000
```

Depois, abra o arquivo:

```text
frontend/index.html
```

Por padrao, a tela consulta a API em `http://localhost:8000`.

Se precisar apontar para outro endereco, defina no navegador:

```text
window.ANATEL_API_BASE_URL = "http://outro-endereco"
```

## Regra importante

O frontend consome apenas a API do backend.

Ele nao acessa diretamente o Supabase e nao guarda credenciais sensiveis.

## Estrutura

```text
frontend/
  index.html
  src/
    pages/dashboard.js
    services/api.js
    styles/app.css
```

## Observacao

Os dados atuais ainda sao de amostra.

A carga completa das planilhas da ANATEL ainda nao foi feita.
