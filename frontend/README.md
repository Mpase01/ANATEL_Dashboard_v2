# Frontend

Frontend do ANATEL Dashboard.

Esta camada apresenta o dashboard online de forma simples, rapida e responsiva.

## Status atual

A primeira tela funcional foi criada na Sprint 10 e polida na Sprint 11.

Ela permite:

- buscar uma prestadora;
- selecionar uma prestadora encontrada;
- visualizar indicadores principais;
- filtrar o recorte entre todos os meses, ultimos 3 meses e ultimo mes;
- ver a evolucao mensal;
- ver a composicao por tecnologia;
- ver os municipios do ultimo mes disponivel.

## Como abrir localmente

Durante o desenvolvimento, a tela pode ser servida localmente.

Exemplo:

```text
http://127.0.0.1:5173/
```

Por padrao, a tela tenta consultar a API em:

```text
http://localhost:8000
```

Se a API nao estiver rodando, a tela entra em modo demonstracao.

## Modo demonstracao

O modo demonstracao usa a amostra real validada na Sprint 9.

Ele existe para permitir que a interface seja avaliada antes de configurar o backend local com credenciais reais.

Dados demonstrativos atuais:

```text
Prestadora: NET-UAI INTERNET WIRELESS
CNPJ: 10785849000171
Periodo: 2026-01 a 2026-05
Ultimo mes: 105 acessos
Municipios: 2
```

## API customizada

Se precisar apontar para outro endereco de API, defina no navegador:

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
