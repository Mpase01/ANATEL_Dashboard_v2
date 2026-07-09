# Sprint 20 - Importacao agregada para reduzir uso do Supabase

## Objetivo

Preparar uma alternativa de importacao que grave uma tabela agregada, menor e mais adequada para dashboard, mantendo os recortes que importam para analise:

- mes;
- prestadora;
- municipio;
- UF;
- tecnologia;
- meio de acesso;
- tipo de pessoa;
- quantidade de acessos.

## Por que isso foi feito

A importacao detalhada completa ficou grande demais para o plano gratuito do Supabase. A simulacao da Sprint 19 mostrou que a base de 2026 cai de 3.222.220 linhas normalizadas para 839.183 linhas agregadas, com reducao de 73,96%, sem perder a soma total de acessos.

## Arquivos criados

- `backend/app/importer/aggregation.py`: transforma registros normalizados em registros agregados.
- `backend/scripts/import_csv_aggregated.py`: importa CSVs para a tabela agregada.
- `database/aggregated_schema.sql`: define a tabela `aggregated_subscription_records`.
- `backend/tests/test_importer_aggregation.py`: valida que a agregacao preserva a soma.

## Arquivos alterados

- `backend/app/importer/database_writer.py`: recebeu a rotina de gravacao da tabela agregada.

## Decisao importante

O campo `Tipo de Pessoa` foi mantido na tabela agregada, porque ajuda a separar comportamento B2C e B2B:

- `Pessoa Fisica`;
- `Pessoa Juridica`.

## Limite desta sprint

Nenhum dado antigo foi apagado do Supabase nesta sprint. A estrutura e o importador foram preparados, mas a aplicacao no banco real depende de uma decisao explicita: limpar a carga detalhada parcial antiga ou aumentar o armazenamento.

## Proximo passo recomendado

Executar uma limpeza controlada da tabela detalhada parcial e, depois, criar a tabela agregada no Supabase para importar a base de forma menor.
