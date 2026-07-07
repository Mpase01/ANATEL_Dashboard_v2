# Configuracao do Supabase

Este documento explica, em linguagem simples, como o Supabase entra no projeto.

## Projeto conectado

Projeto Supabase identificado:

```text
Nome: Mpase01's Project
Project ID: yzgdctkkxtulsvklyjlg
Regiao: sa-east-1
URL: https://yzgdctkkxtulsvklyjlg.supabase.co
Status: ACTIVE_HEALTHY
```

## Status atual

O schema inicial ja foi aplicado ao projeto Supabase.

Migracoes aplicadas:

```text
20260707174409_initial_anatel_dashboard_schema
add_import_foreign_key_indexes
```

Tabelas criadas:

```text
providers
provider_aliases
import_batches
import_files
subscription_records
```

Views criadas:

```text
provider_monthly_totals
national_monthly_totals
provider_monthly_fiber_totals
```

Foram feitas duas gravacoes pequenas:

1. Sprint 8: amostra ficticia para validar escrita.
2. Sprint 9: recorte real do CSV de 2026.

Contagem atual, incluindo as duas amostras:

```text
providers: 2
provider_aliases: 2
import_batches: 2
import_files: 2
subscription_records: 26
```

Recorte real gravado na Sprint 9:

```text
arquivo: Acessos_Banda_Larga_Fixa_2026_Colunas.csv
linhas de origem: 5
registros mensais: 24
total de acessos: 455
prestadora: NET-UAI INTERNET WIRELESS
cnpj: 10785849000171
```

As planilhas grandes da ANATEL ainda nao foram importadas por completo.

## O que ainda falta

Ainda falta preparar o dashboard inicial e, depois, planejar a carga completa com seguranca.

Voce nao deve colocar credenciais no GitHub.

## Variaveis usadas pelo backend

O arquivo `.env.example` mostra o formato esperado:

```text
DATABASE_URL=postgresql+psycopg://user:password@host:5432/database
SUPABASE_URL=https://yzgdctkkxtulsvklyjlg.supabase.co
SUPABASE_SERVICE_ROLE_KEY=replace-with-secret-key-only-on-backend
```

## Regra de seguranca

A chave `SUPABASE_SERVICE_ROLE_KEY` e sensivel.

Ela deve ficar somente no backend e nunca deve ser enviada para o frontend.

## Protecoes aplicadas

As tabelas foram criadas com RLS habilitado.

As roles publicas `anon` e `authenticated` nao receberam acesso direto as tabelas internas.

As views foram criadas com `security_invoker = true`.

## Uso normal depois da configuracao

Depois que o backend estiver conectado ao Supabase, o objetivo e que voce nao precise entrar no painel para operar o sistema.

O fluxo normal deve ser:

```text
Abrir o dashboard
↓
Enviar a planilha da ANATEL
↓
Clicar em atualizar
↓
Ver os dados atualizados
```
