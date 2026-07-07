# Sprint 13 - Filtro temporal no contrato da API

## Objetivo

Mover o recorte temporal do dashboard para o contrato da API.

Antes desta sprint, a tela conseguia filtrar os dados visualmente, mas esse comportamento ainda ficava concentrado no frontend. Para um projeto que vai lidar com arquivos pesados da ANATEL, o ideal e que a API ja entregue os dados no recorte certo.

## O que foi entregue

- Parametro `period` nos endpoints de dashboard.
- Valores aceitos: `all`, `last3` e `latest`.
- Frontend passando o periodo selecionado para a API.
- API local de demonstracao respeitando o mesmo contrato.
- Consultas reais preparadas para limitar os periodos no banco.
- Recalculo de crescimento conforme o periodo retornado pela API.
- Validacao local no navegador usando `http://127.0.0.1:5173/` e API local em `http://127.0.0.1:8000`.

## Endpoints afetados

```text
GET /providers/{provider_id}/summary?period=all|last3|latest
GET /providers/{provider_id}/evolution?period=all|last3|latest
GET /providers/{provider_id}/technologies?period=all|last3|latest
GET /providers/{provider_id}/municipalities?period=all|last3|latest&limit=20
```

## Resultado validado

Com a base de demonstracao:

- `all`: janeiro/2026 a maio/2026, 5 barras, crescimento de 15,4%.
- `last3`: marco/2026 a maio/2026, 3 barras, crescimento de 14,1%.
- `latest`: maio/2026, 1 barra, crescimento de 0,0%.

## Decisao importante

O dashboard deve continuar simples. A tela escolhe o periodo, mas quem calcula e reduz os dados e a API.

Isso evita que o navegador precise carregar informacoes demais quando a importacao completa da ANATEL estiver pronta.

## O que ainda nao foi feito

- Rodar o FastAPI real localmente com todas as dependencias instaladas.
- Configurar `DATABASE_URL` local com seguranca.
- Trocar definitivamente a API de demonstracao pela API real conectada ao Supabase.
- Criar importacao completa com barra de progresso.

Esses pontos ficam para a proxima sprint.
