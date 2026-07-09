# Sprint 21 - Carga agregada real e dashboard com B2C/B2B

## Objetivo

Aplicar a estrutura agregada no Supabase real, limpar a carga detalhada parcial que estava ocupando espaco, importar o CSV 2026 completo em formato compactado e ajustar o dashboard para consultar a nova base.

## Banco de dados

Antes da carga agregada, a tabela detalhada parcial tinha:

```text
subscription_records: 1.590.002 registros
```

Essa carga parcial foi limpa para liberar espaco. Depois disso, a tabela agregada foi criada e importada com sucesso.

Resultado final validado:

```text
providers: 11.456
subscription_records: 0
aggregated_subscription_records: 839.183
aggregated_subscriptions_sum: 280.681.407
```

## Importacao

Arquivo usado:

```text
Acessos_Banda_Larga_Fixa_2026_Colunas.csv
```

Resultado da importacao completa agregada:

```text
raw_records: 3.222.220
aggregated_records: 839.183
reduction_percent: 73,96%
raw_subscriptions_sum: 280.681.407
aggregated_subscriptions_sum: 280.681.407
batches: 84
elapsed_seconds: 251,33
```

A soma total foi preservada.

## Backend

A API passou a consultar `public.aggregated_subscription_records` em vez de `public.subscription_records` para os endpoints do dashboard.

Tambem foi criado o endpoint:

```text
GET /providers/{provider_id}/person-types
```

Esse endpoint retorna a divisao entre:

```text
Pessoa Fisica  -> B2C
Pessoa Juridica -> B2B
```

## Frontend

A tela foi ajustada para:

- remover o aviso de base de amostra;
- buscar CLARO por padrao na abertura local;
- exibir o novo painel `Perfil do cliente`;
- mostrar os percentuais e acessos por B2C/B2B.

## Validacao

Validacoes executadas:

```text
8 testes automatizados passaram
API /health/database retornou 839.183 registros agregados
API /providers/1723/summary retornou dados reais da CLARO
API /providers/1723/person-types retornou Pessoa Fisica e Pessoa Juridica
```

Exemplo validado para CLARO no ultimo mes disponivel:

```text
Assinantes: 10.513.159
Pessoa Fisica: 9.729.178 (92,54%)
Pessoa Juridica: 783.981 (7,46%)
```

## Status

Concluida.

A base agregada de 2026 esta carregada no Supabase e a API local esta rodando em:

```text
http://127.0.0.1:8001
```

A tela local continua em:

```text
http://127.0.0.1:5173
```
