# Sprint 3 - Modelo Inicial do Banco

## Objetivo

Criar o modelo inicial do banco de dados com base na estrutura real dos arquivos da ANATEL.

## Arquivos analisados

- `Acessos_Banda_Larga_Fixa_2025_Colunas.csv`
- `Acessos_Banda_Larga_Fixa_2026_Colunas.csv`

## Principais achados

### Arquivo 2025

- 990.497 linhas.
- 25 colunas.
- 12 meses: `2025-01` ate `2025-12`.
- Tamanho aproximado: 150 MB.

### Arquivo 2026

- 819.037 linhas.
- 18 colunas.
- 5 meses: `2026-01` ate `2026-05`.
- Tamanho aproximado: 115 MB.

### Estrutura comum

Os dois arquivos usam separador `;` e possuem as mesmas colunas fixas:

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

Os meses aparecem como colunas no formato `YYYY-MM`.

## Decisoes tomadas

- Usar CNPJ como identificador principal do provedor.
- Tratar `Empresa` como nome exibivel e alias.
- Preservar historico no banco.
- Nao apagar dados antigos antes de importar.
- Ignorar registros mensais com zero assinantes.
- Usar `source_row_hash` para identificar a linha fixa original da ANATEL.
- Usar `period + source_row_hash` como chave logica da tabela principal.
- Criar views simples para totais mensais e fibra.

## Arquivos alterados

- `database/README.md`
- `database/schema.sql`
- `docs/DATABASE.md`
- `docs/IMPORTER.md`
- `docs/SPRINT_3.md`

## Resumo tecnico

Foi criado um schema inicial para PostgreSQL com as tabelas:

- `providers`
- `provider_aliases`
- `import_batches`
- `import_files`
- `subscription_records`

Tambem foram previstas views iniciais:

- `provider_monthly_totals`
- `national_monthly_totals`
- `provider_monthly_fiber_totals`

## Testes realizados

Nao houve aplicacao em banco real nesta sprint.

A verificacao feita foi estrutural, baseada na leitura dos CSVs reais e na confirmacao dos arquivos criados no repositorio.

## Pendencias

Antes de aplicar o schema no Supabase, ainda e necessario:

- criar ou conectar o projeto Supabase;
- revisar credenciais e variaveis de ambiente;
- rodar uma importacao pequena de teste;
- validar desempenho com dados reais;
- ajustar indices se necessario.

## Proximos passos

A proxima sprint sugerida e a Sprint 4: importador inicial.

Ela deve implementar a leitura dos CSVs, deteccao de meses, normalizacao, descarte de zeros e preparacao dos dados para gravacao no banco.
