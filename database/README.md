# Database

Esta pasta guarda o modelo inicial do banco de dados do ANATEL Dashboard.

## Arquivos

- `schema.sql` - schema inicial planejado para PostgreSQL.

## Observacao importante

Este schema ainda nao foi aplicado em um projeto Supabase real.

Ele foi criado com base na analise dos arquivos CSV reais da ANATEL:

- `Acessos_Banda_Larga_Fixa_2025_Colunas.csv`
- `Acessos_Banda_Larga_Fixa_2026_Colunas.csv`

Antes de aplicar em producao, o schema deve ser revisado junto com uma importacao de teste.

## Principios

- Preservar historico.
- Nao apagar tudo antes de importar.
- Guardar somente registros mensais com assinantes maiores que zero.
- Usar CNPJ como identificador principal do provedor.
- Preservar nomes alternativos da empresa como aliases.
- Usar `source_row_hash` para evitar duplicidade e permitir atualizacoes seguras.
