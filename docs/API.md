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

## Endpoints planejados

### Saude da API

```text
GET /health
```

Retorna se a API esta online.

### Busca de provedores

```text
GET /providers/search?query=...
```

Permite buscar provedores por nome ou CNPJ.

### Resumo do provedor

```text
GET /providers/{provider_id}/summary
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
- crescimento nos ultimos 12 meses.

### Evolucao mensal

```text
GET /providers/{provider_id}/evolution
```

Retorna a serie mensal de assinantes, por tecnologia quando necessario.

### Distribuicao por estado

```text
GET /providers/{provider_id}/states
```

Retorna assinantes e participacao por UF.

### Distribuicao por municipio

```text
GET /providers/{provider_id}/municipalities
```

Retorna assinantes por municipio.

### Tecnologias

```text
GET /providers/{provider_id}/technologies
```

Retorna a composicao por tecnologia, com destaque para fibra.

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
