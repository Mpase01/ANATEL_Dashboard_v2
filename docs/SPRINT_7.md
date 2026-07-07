# Sprint 7 - Supabase Real e Schema Aplicado

## Objetivo

Conectar um projeto Supabase real e aplicar o schema inicial do ANATEL Dashboard.

## Projeto Supabase usado

```text
Nome: Mpase01's Project
Project ID: yzgdctkkxtulsvklyjlg
Regiao: sa-east-1
Status: ACTIVE_HEALTHY
URL: https://yzgdctkkxtulsvklyjlg.supabase.co
```

## O que foi feito

- Confirmado que havia um unico projeto Supabase disponivel.
- Confirmado que o schema `public` estava vazio antes da aplicacao.
- Endurecido o `database/schema.sql` antes de aplicar.
- Aplicada a migration `initial_anatel_dashboard_schema`.
- Aplicada a migration `add_import_foreign_key_indexes`.
- Confirmado que as tabelas foram criadas.
- Confirmado que as tabelas estao vazias.
- Confirmado que RLS esta habilitado nas tabelas.
- Rodados advisors de seguranca e performance.
- Atualizado `docs/SUPABASE_SETUP.md`.
- Atualizado `database/schema.sql` para refletir o banco real.

## Tabelas criadas

```text
providers
provider_aliases
import_batches
import_files
subscription_records
```

## Views criadas

```text
provider_monthly_totals
national_monthly_totals
provider_monthly_fiber_totals
```

## Seguranca

As tabelas foram criadas com RLS habilitado.

As roles `anon` e `authenticated` tiveram acesso direto revogado.

As views foram criadas com `security_invoker = true`.

O Supabase informou avisos `RLS Enabled No Policy`. Neste momento isso e esperado, porque o acesso direto pela Data API nao sera usado pelo frontend. O backend acessara o banco de forma controlada.

## Performance

Foram adicionados indices para chaves estrangeiras apontados pelo advisor:

```text
idx_import_files_import_batch_id
idx_subscription_records_import_batch_id
idx_subscription_records_import_file_id
```

Os avisos restantes de `Unused Index` sao esperados porque as tabelas ainda estao vazias e sem consultas reais.

## Validacoes realizadas

Consulta de contagem retornou zero linhas em todas as tabelas principais:

```text
providers: 0
provider_aliases: 0
import_batches: 0
import_files: 0
subscription_records: 0
```

## O que ainda nao foi feito

- Configurar `.env` local com credenciais reais.
- Rodar o backend conectado diretamente ao banco.
- Gravar uma importacao real.
- Importar os CSVs grandes da ANATEL.

## Proximos passos

A proxima sprint deve implementar a gravacao controlada no banco usando o importador ja criado.

Antes disso, sera necessario configurar o `.env` local com `DATABASE_URL` e demais variaveis sensiveis.
