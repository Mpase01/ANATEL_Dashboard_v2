# Configuracao do Supabase

Este documento explica, em linguagem simples, como o Supabase entrara no projeto.

## Quando o Supabase sera necessario

O Supabase sera necessario quando o sistema comecar a gravar dados reais no banco.

Antes disso, o importador e a API podem ser desenvolvidos e testados parcialmente sem banco real.

## O que voce precisara fazer

Quando chegarmos na etapa de conexao real, voce precisara:

1. Criar um projeto no Supabase.
2. Abrir as configuracoes do projeto.
3. Copiar a string de conexao do PostgreSQL.
4. Criar um arquivo `.env` local no backend.
5. Colocar as credenciais no `.env`.

As credenciais reais nunca devem ser colocadas no GitHub.

## Variaveis usadas pelo backend

O arquivo `.env.example` mostra o formato esperado:

```text
DATABASE_URL=postgresql+psycopg://user:password@host:5432/database
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=replace-with-secret-key-only-on-backend
```

## Regra de seguranca

A chave `SUPABASE_SERVICE_ROLE_KEY` e sensivel.

Ela deve ficar somente no backend e nunca deve ser enviada para o frontend.

## Aplicacao do schema

O schema inicial esta em:

```text
database/schema.sql
```

Antes de aplicar esse schema em um projeto real, ele deve ser revisado.

O ideal e aplicar primeiro em um projeto vazio ou ambiente de teste.

## Uso normal depois da configuracao

Depois que o Supabase estiver configurado, o objetivo e que voce nao precise entrar no painel para operar o sistema.

O fluxo normal deve ser:

```text
Abrir o dashboard
↓
Enviar a planilha da ANATEL
↓
Clicar em atualizar
↓
Ver os dados atualizados
```
