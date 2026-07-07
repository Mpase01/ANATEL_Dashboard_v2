# Sprint 2 - Estrutura Inicial do Projeto

## Objetivo

Criar a fundacao inicial do projeto sem implementar funcionalidades grandes.

A sprint prepara o repositorio para receber backend, frontend, importador e testes nas proximas etapas.

## Arquivos alterados

- `.gitignore`
- `.env.example`
- `backend/README.md`
- `backend/app/api/.gitkeep`
- `backend/app/core/.gitkeep`
- `backend/app/db/.gitkeep`
- `backend/app/importer/.gitkeep`
- `backend/app/models/.gitkeep`
- `backend/app/repositories/.gitkeep`
- `backend/app/schemas/.gitkeep`
- `backend/app/services/.gitkeep`
- `backend/tests/.gitkeep`
- `frontend/README.md`
- `frontend/src/charts/.gitkeep`
- `frontend/src/components/.gitkeep`
- `frontend/src/pages/.gitkeep`
- `frontend/src/services/.gitkeep`
- `frontend/src/styles/.gitkeep`
- `frontend/tests/.gitkeep`
- `docs/SPRINT_2.md`

## Resumo tecnico

A estrutura inicial foi criada com separacao clara entre backend e frontend.

O backend foi organizado para receber futuramente:

- rotas da API;
- configuracoes centrais;
- conexao com banco;
- importador das planilhas;
- modelos;
- consultas;
- contratos de API;
- regras de negocio;
- testes.

O frontend foi organizado para receber futuramente:

- graficos;
- componentes reutilizaveis;
- paginas;
- servicos de comunicacao com a API;
- estilos;
- testes.

Tambem foi criado um `.env.example` para documentar variaveis de ambiente sem expor credenciais reais.

## Testes realizados

Nesta sprint nao houve implementacao executavel.

A verificacao foi feita confirmando que os arquivos principais foram criados no repositorio.

## Proximos passos

A proxima sprint sugerida e a Sprint 3: modelo de banco.

Antes da Sprint 3, o ideal e analisar uma planilha real da ANATEL para confirmar os nomes das colunas e ajustar o modelo ao dado real.
