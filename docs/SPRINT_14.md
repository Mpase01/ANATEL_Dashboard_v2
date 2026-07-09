# Sprint 14 - Backend real local

## Objetivo

Preparar o backend real para rodar localmente com FastAPI, como passo anterior a ligar a tela diretamente ao Supabase.

## O que foi feito

- Dependencias Python do backend foram instaladas localmente em `.python_deps`.
- A API real subiu localmente em `http://127.0.0.1:8001`.
- O endpoint `GET /health` respondeu com sucesso.
- Foi criado o endpoint `GET /health/database` para diagnosticar a conexao com o banco.
- Foi criado o script `backend/scripts/run_api_local.py` para facilitar a execucao local da API real.
- Foi criado o script `backend/scripts/check_database.py` para verificar a conexao com o banco.
- O backend passou a carregar `.env` automaticamente quando o arquivo existir.
- O `.gitignore` foi atualizado para ignorar dependencias e temporarios locais.
- Foi criado o guia `docs/SUPABASE_CONNECTION.md` para configurar a conexao local com seguranca.

## Validacao feita

A API real respondeu:

```json
{"status":"ok"}
```

Tambem foi confirmado que os endpoints que dependem do banco retornam erro controlado quando `DATABASE_URL` nao esta configurado.

Resposta observada em `GET /health/database`:

```json
{"detail":"DATABASE_URL is not configured."}
```

O verificador local tambem retorna uma mensagem simples quando a configuracao ainda falta:

```text
Configuracao pendente: DATABASE_URL is not configured.
```

## Ponto importante

A API real ja roda, mas ainda nao esta conectada ao Supabase localmente.

Para conectar, sera necessario configurar a variavel `DATABASE_URL` com uma string segura de conexao do banco Supabase. Essa informacao nao deve ser colocada no codigo nem enviada ao GitHub.

## Status

Em andamento.

## Proximo passo

Configurar `DATABASE_URL` localmente e testar:

```text
python backend/scripts/check_database.py
GET /health/database
GET /providers/search?query=NET
GET /providers/{provider_id}/summary?period=all
GET /providers/{provider_id}/evolution?period=all
```

Depois disso, a tela podera apontar para a API real em vez da API de demonstracao.
