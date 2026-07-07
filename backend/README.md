# Backend

Backend do ANATEL Dashboard.

Esta camada sera responsavel por:

- receber solicitacoes do dashboard;
- executar regras de negocio;
- processar importacoes das planilhas da ANATEL;
- consultar o PostgreSQL;
- devolver dados agregados para o frontend.

## Estrutura planejada

```text
backend/
  app/
    api/            # rotas da API FastAPI
    core/           # configuracoes e utilitarios centrais
    db/             # conexao com banco e sessoes
    importer/       # leitura e tratamento das planilhas
    models/         # modelos de banco
    repositories/   # consultas ao banco
    schemas/        # contratos de entrada e saida da API
    services/       # regras de negocio
  tests/            # testes automatizados do backend
```

## Regra importante

O backend sera o unico lugar com acesso a credenciais sensiveis do banco.

Nenhuma chave administrativa do Supabase deve ir para o frontend.

## Status

Nesta sprint, apenas a estrutura inicial foi criada.

Nenhuma funcionalidade de API, banco ou importador foi implementada ainda.
