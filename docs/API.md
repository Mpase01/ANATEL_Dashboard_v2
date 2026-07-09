# API

## Objetivo

A API sera a camada de comunicacao entre o dashboard React e o banco PostgreSQL.

Ela deve proteger o banco, centralizar regras de negocio e entregar dados prontos para exibicao.

## Regra principal

O frontend nunca deve acessar diretamente o banco de dados.

Toda consulta deve passar pela API.

## Stack planejada

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL / Supabase

## Principios

- Endpoints simples e bem nomeados.
- Respostas leves.
- Dados ja agregados quando possivel.
- Regras de calculo centralizadas no backend.
- Contratos de resposta documentados.

## Parametro de periodo

Os endpoints do dashboard aceitam o parametro opcional `period`.

Valores aceitos:

- `all` - todos os meses disponiveis para o provedor.
- `last3` - os 3 meses mais recentes disponiveis.
- `latest` - somente o mes mais recente disponivel.

Quando o parametro nao for informado, a API deve usar `all`.

## Endpoints planejados

### Saude da API

```text
GET /health
```

Retorna se a API esta online.

### Saude do banco

```text
GET /health/database
```

Retorna se a API consegue conectar ao banco configurado.

Quando `DATABASE_URL` ainda nao esta configurado, retorna erro controlado `503`.

Quando a conexao estiver funcionando, retorna:

```json
{
  "status": "ok",
  "providers_count": 0,
  "records_count": 0
}
```

### Busca de provedores

```text
GET /providers/search?query=...
```

Permite buscar provedores por nome ou CNPJ.

### Resumo do provedor

```text
GET /providers/{provider_id}/summary?period=all|last3|latest
```

Retorna os principais indicadores do provedor selecionado.

Indicadores previstos:

- total de assinantes;
- market share Brasil;
- participacao de fibra;
- numero de municipios;
- numero de estados;
- principal municipio;
- principal estado;
- crescimento dentro do periodo selecionado.

### Evolucao mensal

```text
GET /providers/{provider_id}/evolution?period=all|last3|latest
```

Retorna a serie mensal de assinantes no periodo selecionado.

### Distribuicao por estado

```text
GET /providers/{provider_id}/states?period=all|last3|latest
```

Retorna assinantes e participacao por UF.

### Distribuicao por municipio

```text
GET /providers/{provider_id}/municipalities?period=all|last3|latest&limit=20
```

Retorna assinantes por municipio no mes mais recente do periodo selecionado.

### Tecnologias

```text
GET /providers/{provider_id}/technologies?period=all|last3|latest
```

Retorna a composicao por tecnologia no mes mais recente do periodo selecionado, com destaque para fibra.

### Importacao

```text
POST /imports
GET /imports/{import_id}
```

Permite iniciar uma importacao e consultar o status do processamento.

## Regras de calculo

Calculos como market share, crescimento e participacao de fibra devem ser definidos no backend e documentados.

O frontend deve apenas apresentar os resultados.

## Desempenho

A API deve evitar retornar grandes volumes brutos de dados.

Sempre que possivel, deve retornar dados ja filtrados, paginados ou agregados.

## Seguranca

Credenciais sensiveis devem ficar apenas no backend.

O frontend deve consumir somente endpoints publicos ou autenticados da API, conforme a necessidade futura do produto.
