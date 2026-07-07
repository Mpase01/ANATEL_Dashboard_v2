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

## Importador inicial

O modulo `app/importer/anatel_csv.py` ja consegue:

- ler CSV da ANATEL;
- detectar separador;
- detectar encoding;
- identificar colunas mensais no formato `YYYY-MM`;
- normalizar cabecalhos com ou sem acento;
- transformar meses em registros;
- ignorar meses com zero assinantes;
- calcular `source_row_hash` da linha original.

## Persistencia inicial

O modulo `app/importer/persistence.py` prepara os registros importados para gravacao futura nas tabelas:

- `providers`;
- `provider_aliases`;
- `subscription_records`.

Ele ainda nao grava em banco real.

## API inicial

O modulo `app/api/app.py` contem o esqueleto da API FastAPI.

Endpoint inicial:

```text
GET /health
```

## Dependencias planejadas

As dependencias iniciais do backend estao em:

```text
backend/requirements.txt
```

Elas ainda nao precisam ser instaladas para rodar os testes atuais.

## Testes

Para rodar os testes do backend:

```text
python -m unittest discover -s backend/tests
```

## Regra importante

O backend sera o unico lugar com acesso a credenciais sensiveis do banco.

Nenhuma chave administrativa do Supabase deve ir para o frontend.

## Status

A estrutura inicial existe, o primeiro modulo do importador foi criado e a preparacao de persistencia foi iniciada.

Ainda nao ha conexao com banco, gravacao no Supabase ou endpoints de negocio.
