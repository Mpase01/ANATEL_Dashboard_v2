# Arquitetura

## Objetivo da arquitetura

A arquitetura do ANATEL Dashboard deve ser simples, eficiente e preparada para evoluir sem reescrita completa.

O foco e permitir que o usuario envie planilhas pesadas da ANATEL e receba um dashboard online rapido, confiavel e facil de usar.

## Fluxo principal

```text
Planilhas ANATEL
↓
Importador Python
↓
Validacao e deteccao de mudancas
↓
PostgreSQL / Supabase
↓
FastAPI
↓
Dashboard React
```

## Responsabilidades

### Importador

Responsavel por ler os arquivos Excel, identificar colunas de meses no formato `YYYY-MM`, transformar os dados em formato normalizado, validar registros e gravar os dados no banco.

### Banco de dados

Responsavel por armazenar o historico importado, os provedores, os lotes de importacao e os registros mensais de assinantes.

### API

Responsavel por proteger o banco, centralizar regras de negocio e entregar ao frontend dados prontos para exibicao.

O frontend nao deve acessar diretamente o banco de dados.

### Dashboard

Responsavel por apresentar os indicadores de forma simples, rapida e visual.

O dashboard deve consumir endpoints da API ja agregados, evitando processar grandes volumes de dados no navegador.

## Decisoes estruturais

- Usar Python e FastAPI no backend.
- Usar PostgreSQL hospedado no Supabase.
- Usar React com TypeScript no frontend.
- Usar Apache ECharts para graficos.
- Adiar mapas complexos para uma fase posterior.
- Manter o frontend separado do acesso direto ao banco.
- Priorizar endpoints agregados e leves.

## Principio de simplicidade

A arquitetura nao deve ser mais complexa do que o problema exige.

Sempre que houver duas solucoes possiveis, a preferencia deve ser pela opcao mais simples de operar, explicar e manter, desde que ela continue segura e eficiente.
