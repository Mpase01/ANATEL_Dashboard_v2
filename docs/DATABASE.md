# Banco de Dados

## Banco escolhido

O projeto usara PostgreSQL hospedado no Supabase.

O banco sera acessado pelo backend. O frontend nao deve consultar o banco diretamente.

## Base real analisada

Foram analisados dois arquivos CSV da ANATEL:

- `Acessos_Banda_Larga_Fixa_2025_Colunas.csv`
- `Acessos_Banda_Larga_Fixa_2026_Colunas.csv`

Caracteristicas encontradas:

- arquivos separados por `;`;
- codificacao lida como `utf-8-sig`;
- 2025 possui 990.497 linhas e 12 meses;
- 2026 possui 819.037 linhas e 5 meses;
- os meses aparecem como colunas no formato `YYYY-MM`;
- as colunas fixas sao iguais nos dois arquivos.

## Colunas fixas identificadas

```text
CNPJ
Velocidade
Municipio
UF
Faixa de Velocidade
Tecnologia
Empresa
Porte da Prestadora
Tipo de Pessoa
Tipo de Produto
Codigo IBGE Municipio
Grupo Economico
Meio de Acesso
```

## Objetivo do modelo de dados

O modelo deve transformar planilhas largas da ANATEL, com uma coluna para cada mes, em uma estrutura normalizada e facil de consultar.

A prioridade e permitir consultas rapidas por provedor, periodo, estado, municipio, tecnologia e fibra.

## Retencao historica

O banco deve manter historico importado.

O dashboard pode usar os ultimos 12 meses como recorte padrao, mas os dados antigos nao devem ser descartados automaticamente.

## Regra de volume

A normalizacao completa gera muitos registros.

Por isso, o banco deve armazenar somente registros mensais com `subscriptions_count > 0`.

Linhas/meses com zero assinantes nao devem ser gravados na tabela principal.

## Tabelas planejadas

### providers

Armazena os provedores identificados por CNPJ.

Campos principais:

- `id`
- `cnpj`
- `primary_name`
- `created_at`
- `updated_at`

### provider_aliases

Armazena nomes alternativos ou variacoes de grafia de um mesmo provedor.

Essa tabela e importante porque um CNPJ pode mudar de nome e um mesmo nome pode aparecer em mais de um CNPJ.

Campos principais:

- `id`
- `provider_id`
- `alias_name`
- `created_at`

### import_batches

Registra cada execucao de importacao.

Campos principais:

- `id`
- `status`
- `started_at`
- `finished_at`
- `rows_read`
- `rows_inserted`
- `rows_updated`
- `rows_skipped`
- `error_message`

### import_files

Registra cada arquivo processado.

Campos principais:

- `id`
- `import_batch_id`
- `file_name`
- `file_hash`
- `file_size_bytes`
- `detected_delimiter`
- `detected_encoding`
- `detected_months`
- `created_at`

### subscription_records

Tabela principal do sistema.

Armazena os assinantes por provedor, periodo, localidade, tecnologia e demais dimensoes da ANATEL.

Campos principais:

- `id`
- `provider_id`
- `import_batch_id`
- `import_file_id`
- `period`
- `source_row_hash`
- `cnpj`
- `company_name`
- `speed_mbps`
- `municipality_name`
- `state`
- `speed_range`
- `technology`
- `provider_size`
- `person_type`
- `product_type`
- `municipality_code`
- `economic_group`
- `access_medium`
- `subscriptions_count`
- `created_at`
- `updated_at`

## Chave logica dos dados

A chave tecnica principal da importacao sera:

```text
period + source_row_hash
```

`source_row_hash` deve ser calculado a partir das colunas fixas originais da linha.

Essa abordagem evita duplicidade quando a mesma planilha for importada novamente e permite atualizar meses novos quando o arquivo de 2026 vier com novas colunas.

## Views planejadas

O schema inicial inclui views simples para acelerar a construcao da API:

- `provider_monthly_totals`
- `national_monthly_totals`
- `provider_monthly_fiber_totals`

Views mais avancadas ou materialized views so devem ser criadas se houver necessidade real de desempenho.

## Indices planejados

Indices devem priorizar:

- busca por CNPJ;
- busca por nome/alias;
- filtros por periodo;
- filtros por provedor e periodo;
- agregacoes por UF;
- agregacoes por municipio;
- agregacoes por tecnologia;
- agregacoes por fibra.

## Arquivo SQL

O schema inicial esta em:

```text
database/schema.sql
```

Ele ainda nao foi aplicado em um projeto Supabase real.

## Regra de seguranca

As credenciais sensiveis do Supabase devem ficar apenas no backend.

Nenhuma chave administrativa deve ser exposta no frontend.
