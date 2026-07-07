# Sprint 9 - Importacao pequena de ponta a ponta

## Objetivo

Validar o caminho completo usando dados reais da ANATEL, mas com um recorte pequeno para evitar risco e lentidao.

O fluxo testado foi:

```text
CSV real 2026
↓
recorte pequeno
↓
normalizacao em registros mensais
↓
gravacao no Supabase
↓
validacao por consultas agregadas
```

## Arquivo usado

Arquivo real analisado:

```text
Acessos_Banda_Larga_Fixa_2026_Colunas.csv
```

A importacao completa desse arquivo ainda nao foi feita.

## Recorte usado

Foram usadas as 5 primeiras linhas de origem do CSV de 2026.

Essas linhas viraram 24 registros mensais, porque cada linha pode ter varios meses preenchidos.

Resumo do recorte:

```text
linhas de origem: 5
registros mensais gerados: 24
prestadoras reais: 1
municipios: 2
meses: 2026-01 a 2026-05
total de acessos no recorte: 455
```

Prestadora real no recorte:

```text
CNPJ: 10785849000171
Empresa: NET-UAI INTERNET WIRELESS
```

Municipios no recorte:

```text
Lagoa Formosa/MG
Patos de Minas/MG
```

## Resultado no Supabase

O recorte foi gravado como um lote separado.

Resultado da gravacao:

```text
import_batch_id: 2
import_file_id: 2
registros mensais gravados: 24
total de acessos gravados: 455
```

Contagem geral apos Sprint 9, incluindo a amostra ficticia da Sprint 8:

```text
providers: 2
provider_aliases: 2
import_batches: 2
import_files: 2
subscription_records: 26
```

## Validacao agregada

Totais mensais da prestadora real no recorte:

```text
2026-01: 91
2026-02: 81
2026-03: 92
2026-04: 86
2026-05: 105
```

A soma desses meses e 455 acessos.

## Codigo adicionado

Foi criado o script:

```text
backend/scripts/import_csv_preview.py
```

Esse script servira para rodar importacoes pequenas pelo backend quando o ambiente local estiver com o `DATABASE_URL` configurado.

## Decisao

O importador deve continuar evoluindo em modo controlado.

Antes da carga completa, a proxima etapa deve melhorar a automacao e preparar o dashboard inicial para consultar os dados ja gravados.

## Importante

Ainda nao foi feita a importacao completa das planilhas de 2025 e 2026.

A carga completa deve ser feita somente depois de validar desempenho, progresso e recuperacao de erro.