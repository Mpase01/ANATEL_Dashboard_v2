# Sprint 5 - Persistencia e API Inicial

## Objetivo

Preparar o backend para persistir os dados importados e iniciar a estrutura minima da API.

Nesta sprint ainda nao houve conexao com Supabase nem gravacao em banco real.

## Arquivos alterados

- `backend/app/core/__init__.py`
- `backend/app/core/config.py`
- `backend/app/importer/persistence.py`
- `backend/app/api/__init__.py`
- `backend/app/api/app.py`
- `backend/requirements.txt`
- `backend/tests/test_importer_persistence.py`
- `backend/README.md`
- `docs/SPRINT_5.md`
- `docs/README.md`
- `docs/ROADMAP.md`

## O que foi implementado

### Configuracao

Foi criada uma camada simples de configuracao baseada em variaveis de ambiente.

Ela prepara o projeto para usar futuramente:

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_SERVICE_ROLE_KEY`
- `BACKEND_HOST`
- `BACKEND_PORT`

### Persistencia

Foi criado o modulo `backend/app/importer/persistence.py`.

Ele transforma registros normalizados do importador em estruturas prontas para gravacao futura nas tabelas:

- `providers`
- `provider_aliases`
- `subscription_records`

### API inicial

Foi criado um esqueleto FastAPI com endpoint de saude:

```text
GET /health
```

Resposta esperada:

```json
{"status": "ok"}
```

## O que ainda nao foi implementado

- conexao real com PostgreSQL;
- aplicacao do schema no Supabase;
- gravacao de dados no banco;
- endpoints de busca de provedores;
- endpoints de indicadores;
- upload de arquivos;
- processamento em background.

## Testes realizados

Foi executado:

```text
python -m unittest discover -s backend/tests
```

Resultado:

```text
Ran 4 tests
OK
```

Os testes cobrem:

- importador inicial;
- descarte de zeros;
- normalizacao de campos;
- montagem de linhas para `providers`;
- montagem de aliases;
- montagem de linhas para `subscription_records`;
- erro quando um `provider_id` esperado nao existe.

## Proximos passos

A proxima etapa recomendada e conectar a persistencia a um banco real.

Para isso, sera necessario criar ou conectar um projeto Supabase e configurar as variaveis de ambiente localmente, sem expor segredos no repositorio.
