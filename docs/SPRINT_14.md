# Sprint 14 - Backend real local

## Objetivo

Preparar o backend real para rodar localmente com FastAPI e ligar a tela local ao Supabase.

## O que foi feito

- Dependencias Python do backend foram instaladas localmente em `.python_deps`.
- A API real subiu localmente em `http://127.0.0.1:8001`.
- O endpoint `GET /health` respondeu com sucesso.
- Foi criado o endpoint `GET /health/database` para diagnosticar a conexao com o banco.
- Foi criado o script `backend/scripts/run_api_local.py` para facilitar a execucao local da API real.
- Foi criado o script `backend/scripts/check_database.py` para verificar a conexao com o banco.
- O backend passou a carregar `.env` automaticamente quando o arquivo existir.
- O `.gitignore` foi atualizado para ignorar dependencias, temporarios locais e `.env`.
- Foi criado o guia `docs/SUPABASE_CONNECTION.md` para configurar a conexao local com seguranca.
- A `DATABASE_URL` local foi configurada usando o Session pooler do Supabase.
- O frontend local passou a apontar para `http://localhost:8001` por padrao.

## Validacao feita

A API real respondeu:

```json
{"status":"ok"}
```

O verificador local confirmou a conexao com o Supabase:

```text
Conexao com o banco OK.
Prestadoras: 2
Registros mensais: 26
```

O endpoint `GET /health/database` confirmou:

```json
{
  "status": "ok",
  "providers_count": 2,
  "records_count": 26
}
```

A busca real retornou a prestadora de amostra:

```json
{
  "id": 2,
  "cnpj": "10785849000171",
  "name": "NET-UAI INTERNET WIRELESS"
}
```

A tela local em `http://127.0.0.1:5173/` foi recarregada e exibiu dados vindos da API real:

- status: `Painel atualizado`;
- periodo: `01/2026 a 05/2026`;
- barras de evolucao: 5;
- assinantes no ultimo mes: 105.

## Ponto importante

A senha do banco fica somente no arquivo local `.env` e nao deve ser enviada ao GitHub.

Como a senha chegou a aparecer no chat durante a configuracao assistida, recomenda-se trocar a senha novamente no Supabase antes de uso definitivo/publicacao.

## Status

Concluida.

## Proximo passo

A proxima sprint deve preparar a importacao completa ou semi-completa dos CSVs reais, com cuidado para nao travar o banco nem a maquina local.
