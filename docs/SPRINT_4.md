# Sprint 4 - Importador Inicial

## Objetivo

Criar o primeiro modulo do importador da ANATEL, ainda sem gravar dados no Supabase.

O foco desta sprint foi transformar a estrutura dos CSVs em registros normalizados em memoria.

## Arquivos alterados

- `backend/app/__init__.py`
- `backend/app/importer/__init__.py`
- `backend/app/importer/anatel_csv.py`
- `backend/tests/test_anatel_csv_importer.py`
- `backend/tests/fixtures/sample_ascii.csv`
- `backend/tests/fixtures/sample_accented.csv`
- `backend/README.md`
- `docs/SPRINT_4.md`

## O que foi implementado

O importador inicial consegue:

- ler arquivos CSV;
- detectar encoding;
- detectar delimitador;
- identificar colunas mensais no formato `YYYY-MM`;
- aceitar cabecalhos com ou sem acento;
- normalizar CNPJ;
- normalizar UF;
- normalizar codigo IBGE do municipio;
- converter velocidade;
- converter assinantes;
- ignorar registros mensais com zero assinantes;
- gerar `source_row_hash` com base nas colunas fixas da ANATEL;
- gerar objetos normalizados `SubscriptionRecord`.

## O que ainda nao foi implementado

- gravacao no banco;
- criacao de lote de importacao;
- atualizacao incremental em PostgreSQL;
- interface de upload;
- API de importacao;
- processamento em background.

## Testes realizados

Foi executado o comando:

```text
python -m unittest discover -s backend/tests
```

Resultado:

```text
Ran 2 tests
OK
```

Os testes cobrem:

- deteccao de meses;
- descarte de meses com zero assinantes;
- normalizacao de CNPJ;
- normalizacao de UF;
- estabilidade do `source_row_hash` para a mesma linha fixa;
- leitura de cabecalhos reais com acento.

## Observacao

Nesta rodada nao foi feita nova leitura dos CSVs reais do Desktop porque o acesso de leitura nao foi concedido para este turno.

A implementacao foi baseada na analise realizada anteriormente sobre os arquivos reais de 2025 e 2026.

## Proximos passos

A proxima etapa recomendada e evoluir o importador para gerar lotes de importacao e preparar gravacao no banco.

Antes de gravar em Supabase, ainda precisamos conectar ou criar o projeto Supabase e configurar as variaveis de ambiente corretas.
