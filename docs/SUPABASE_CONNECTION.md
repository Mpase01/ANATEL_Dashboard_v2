# Conexao local com Supabase

## Objetivo

Este guia explica como conectar a API real local ao banco Supabase sem colocar senha no GitHub.

## Regra de seguranca

Nunca coloque `DATABASE_URL`, senha do banco ou `service_role_key` em arquivos que serao enviados ao GitHub.

O arquivo `.env` fica apenas no computador local e ja esta ignorado pelo `.gitignore`.

## Passo a passo

1. Abra o painel do Supabase.
2. Entre no projeto do dashboard.
3. Va em `Project Settings`.
4. Va em `Database`.
5. Procure a area de connection string.
6. Copie a connection string de PostgreSQL.
7. Crie um arquivo `.env` na raiz do projeto.
8. Coloque a variavel abaixo, trocando pela connection string real:

```text
DATABASE_URL=postgresql+psycopg://postgres:SUA-SENHA@SEU-HOST:5432/postgres
```

## Conferir se funcionou pelo terminal

Depois de configurar o `.env`, rode o verificador:

```text
python backend/scripts/check_database.py
```

Quando estiver correto, ele deve mostrar:

```text
Conexao com o banco OK.
Prestadoras: ...
Registros mensais: ...
```

## Conferir se funcionou pelo navegador

Com a API real rodando, abra:

```text
http://127.0.0.1:8001/health/database
```

Quando estiver correto, a resposta sera parecida com:

```json
{
  "status": "ok",
  "providers_count": 2,
  "records_count": 26
}
```

Se ainda faltar configuracao, a resposta sera `503` com uma mensagem como:

```json
{"detail":"DATABASE_URL is not configured."}
```

## Rodar a API real local

```text
python backend/scripts/run_api_local.py
```

Por padrao, a API real sobe em:

```text
http://127.0.0.1:8001
```

## Como a tela passa a usar a API real

A tela local deve apontar para:

```text
http://127.0.0.1:8001
```

Enquanto a conexao real nao estiver pronta, a tela pode continuar usando a API de demonstracao em:

```text
http://127.0.0.1:8000
```
