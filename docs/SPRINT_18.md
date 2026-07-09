# Sprint 18 - Carga completa do CSV de 2026

## Objetivo

Executar a carga completa do CSV real de 2026 e validar o dashboard com a base completa disponivel.

## Arquivo usado

```text
Acessos_Banda_Larga_Fixa_2026_Colunas.csv
```

Tamanho do arquivo:

```text
120.152.110 bytes
```

## Contagem completa sem gravar

Antes da carga real, foi feito um dry-run lendo o arquivo completo sem gravar no banco.

Resultado:

```text
registros normalizados: 3.222.220
lotes de 10.000: 323
ultimo lote: 2.220 registros
tempo de leitura: 50,17 segundos
```

## Ajustes feitos durante a sprint

A carga completa revelou dois problemas tecnicos que foram corrigidos no projeto.

### 1. Velocidades acima do limite inicial

A coluna `speed_mbps` estava como:

```text
numeric(12, 6)
```

A base real possui velocidades grandes o suficiente para estourar esse limite.

A coluna foi ajustada no Supabase e no schema do projeto para:

```text
numeric(18, 6)
```

### 2. Conexoes longas no pool do Supabase

Durante a carga longa, o pool passou a devolver sessoes em modo somente leitura.

Foram feitos dois ajustes:

- o importador passou a abrir uma sessao de banco por lote;
- o helper de banco passou a usar conexoes curtas e forcar transacao de escrita.

Arquivos alterados:

- `backend/app/db/session.py`
- `backend/scripts/import_csv_batched.py`
- `database/schema.sql`

## Carga parcial realizada

A carga conseguiu avancar ate uma base parcial grande antes de bater no limite de armazenamento do Supabase.

Estado validado pela API:

```text
prestadoras: 4.448
registros mensais: 1.590.002
```

## Bloqueio encontrado

A carga completa parou com erro de falta de espaco no banco:

```text
No space left on device
```

Isso significa que o projeto Supabase atual nao tem armazenamento suficiente para receber a carga completa de 2026 nesse formato.

## Testes

Os testes automatizados do backend continuaram passando:

```text
6 testes executados
resultado: OK
```

## Decisao

A Sprint 18 nao pode ser considerada concluida porque a carga completa depende de mais espaco no Supabase ou de uma estrategia de armazenamento mais enxuta.

Proximas alternativas:

- aumentar o armazenamento/plano do Supabase;
- limpar a carga parcial e reimportar de forma mais seletiva;
- agregar dados antes de gravar, reduzindo o volume bruto;
- revisar indices e colunas para diminuir o espaco ocupado;
- decidir se o dashboard precisa mesmo manter todos os registros detalhados.

## Status

Bloqueada por limite de armazenamento do Supabase.
