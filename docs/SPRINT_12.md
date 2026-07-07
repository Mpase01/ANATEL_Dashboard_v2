# Sprint 12 - API local de demonstracao

## Objetivo

Permitir que o dashboard rode contra uma API local com os mesmos endpoints planejados, mesmo antes de configurar FastAPI, dependencias e credenciais reais do Supabase na maquina local.

## O que foi feito

Foi criado o script:

```text
backend/scripts/demo_api.py
```

Ele usa apenas a biblioteca padrao do Python e sobe uma API local em:

```text
http://127.0.0.1:8000
```

## Endpoints disponiveis

```text
GET /health
GET /providers/search?query=NET
GET /providers/2/summary
GET /providers/2/evolution
GET /providers/2/technologies
GET /providers/2/municipalities
```

Esses endpoints seguem o mesmo contrato que o frontend ja espera.

## Validacao

A API local respondeu corretamente:

```text
/health -> status ok
/providers/search?query=NET -> NET-UAI INTERNET WIRELESS
/providers/2/summary -> 105 acessos no ultimo mes
```

O dashboard em `http://127.0.0.1:5173/` foi recarregado e passou a consumir a API local.

Estado validado na tela:

```text
Status: Painel atualizado
Prestadora: NET-UAI INTERNET WIRELESS
Periodo: 01/2026 a 05/2026
Acessos: 105
Grafico mensal: 5 barras
Tecnologias: 2
Municipios: 2
```

## Observacao importante

Esta ainda nao e a API real conectada ao Supabase.

A API local de demonstracao serve para validar a tela, o contrato dos endpoints e o fluxo visual sem depender de credenciais locais.

## Bloqueio atual para API real

O ambiente local ainda nao possui as dependencias instaladas, como FastAPI.

Tambem ainda falta configurar uma conexao local segura com o Supabase.

## Proxima sprint sugerida

Sprint 13:

- instalar ou preparar as dependencias do backend;
- configurar `DATABASE_URL` local com seguranca;
- rodar o FastAPI real;
- trocar a API de demonstracao pela API real conectada ao Supabase;
- manter o modo demonstracao apenas como fallback.