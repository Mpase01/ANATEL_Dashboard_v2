# Sprint 8 - Gravacao controlada no banco

## Objetivo

Validar que o projeto consegue gravar dados normalizados no Supabase real sem importar ainda as planilhas grandes da ANATEL.

Esta sprint foi feita com uma amostra pequena e ficticia para reduzir risco.

## O que foi feito

- Confirmado acesso ao repositorio `Mpase01/ANATEL_Dashboard_v2` na branch `main`.
- Confirmado que o Supabase estava com as 5 tabelas principais criadas.
- Gravada uma amostra controlada no banco real.
- Validada a contagem das tabelas apos a gravacao.
- Criado o modulo `backend/app/importer/database_writer.py` para concentrar as regras de escrita no banco.

## Resultado da amostra

A amostra gravou:

```text
providers: 1
provider_aliases: 1
import_batches: 1
import_files: 1
subscription_records: 2
```

Os registros sao ficticios e servem apenas para testar o caminho de gravacao.

## Importante

As planilhas pesadas de 2025 e 2026 ainda nao foram importadas.

A importacao real deve acontecer em etapa separada, primeiro com um recorte pequeno e depois com a carga completa.

## Decisao tecnica

A gravacao deve ser idempotente quando possivel.

Isso significa que, se o mesmo arquivo ou a mesma linha normalizada aparecer novamente, o sistema deve atualizar o que mudou em vez de duplicar dados.

## Proxima sprint sugerida

Sprint 9:

- criar um fluxo de importacao pequeno de ponta a ponta pelo backend;
- usar um recorte dos CSVs reais;
- validar tempo de processamento;
- so depois preparar a carga completa.