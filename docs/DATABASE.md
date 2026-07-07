# Banco de Dados

## Banco escolhido

O projeto usara PostgreSQL hospedado no Supabase.

O banco sera acessado pelo backend. O frontend nao deve consultar o banco diretamente.

## Objetivo do modelo de dados

O modelo deve transformar planilhas largas da ANATEL, com uma coluna para cada mes, em uma estrutura normalizada e facil de consultar.

A prioridade e permitir consultas rapidas por provedor, periodo, estado, municipio e tecnologia.

## Retencao historica

O banco deve manter historico importado.

O dashboard pode usar os ultimos 12 meses como recorte padrao, mas os dados antigos nao devem ser descartados automaticamente.

Essa decisao evita perda de informacao e permite analises historicas no futuro.

## Tabelas planejadas

### providers

Armazena os provedores identificados nas bases da ANATEL.

Campos previstos:

- `id`
- `name`
- `cnpj`
- `created_at`
- `updated_at`

### provider_aliases

Armazena nomes alternativos ou variacoes de grafia de um mesmo provedor.

Campos previstos:

- `id`
- `provider_id`
- `alias_name`
- `created_at`

### import_batches

Registra cada tentativa de importacao.

Campos previstos:

- `id`
- `file_name`
- `file_hash`
- `status`
- `rows_processed`
- `started_at`
- `finished_at`
- `error_message`

### subscriptions

Tabela principal do sistema.

Armazena os assinantes por provedor, periodo, localidade e tecnologia.

Campos previstos:

- `id`
- `provider_id`
- `period`
- `state`
- `municipality_code`
- `municipality_name`
- `technology`
- `subscriptions_count`
- `import_batch_id`
- `created_at`

## Chave logica dos dados

Um registro de assinatura deve ser considerado unico pela combinacao:

- provedor;
- periodo;
- estado;
- municipio;
- tecnologia.

Essa regra permite atualizar dados sem duplicar registros.

## Indices planejados

Indices devem priorizar as consultas mais importantes do dashboard:

- busca por CNPJ;
- busca por nome do provedor;
- filtros por periodo;
- filtros por provedor e periodo;
- agregacoes por estado, municipio e tecnologia.

## Views e agregacoes

Quando necessario, o banco podera ter views ou materialized views para acelerar indicadores pesados.

Essas estruturas devem ser criadas apenas quando houver necessidade real de desempenho.

## Regra de seguranca

As credenciais sensiveis do Supabase devem ficar apenas no backend.

Nenhuma chave administrativa deve ser exposta no frontend.
