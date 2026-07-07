# Roadmap

## Diretriz

O projeto sera desenvolvido em sprints pequenas.

Cada sprint deve entregar uma parte clara do produto e aguardar revisao antes da proxima etapa.

## Sprint 1 - Documentacao base

Objetivo:

Criar a documentacao inicial do projeto e registrar as decisoes arquiteturais principais.

Entregaveis:

- estrutura `docs/`;
- visao do produto;
- regras de projeto;
- arquitetura inicial;
- modelo de dados planejado;
- fluxo do importador;
- API planejada;
- dashboard planejado;
- roadmap;
- registro de decisoes.

Status:

Concluida.

## Sprint 2 - Estrutura inicial do projeto

Objetivo:

Criar a estrutura base do backend e do frontend, ainda sem funcionalidades completas.

Entregaveis:

- pastas principais do backend;
- pastas principais do frontend;
- arquivos de configuracao iniciais;
- padrao de variaveis de ambiente;
- instrucoes iniciais de organizacao.

Status:

Concluida.

## Sprint 3 - Modelo de banco

Objetivo:

Criar o modelo inicial do PostgreSQL com base nos CSVs reais da ANATEL.

Entregaveis:

- analise estrutural dos arquivos 2025 e 2026;
- tabelas principais;
- indices iniciais;
- constraints importantes;
- registro de lotes de importacao;
- schema SQL inicial em `database/schema.sql`.

Status:

Concluida.

## Sprint 4 - Importador inicial

Objetivo:

Ler planilhas da ANATEL, identificar meses automaticamente e transformar os dados em formato normalizado.

Entregaveis:

- leitura de CSV separado por `;`;
- deteccao de colunas `YYYY-MM`;
- transformacao para linhas;
- descarte de registros mensais com zero assinantes;
- calculo de `source_row_hash`;
- validacoes iniciais;
- testes com fixtures pequenas.

Status:

Concluida.

## Sprint 5 - Persistencia e API inicial

Objetivo:

Preparar a gravacao dos dados importados e iniciar a estrutura minima da API.

Entregaveis:

- configuracao por variaveis de ambiente;
- preparacao de linhas para `providers`, `provider_aliases` e `subscription_records`;
- esqueleto FastAPI;
- endpoint `GET /health`;
- dependencias planejadas do backend;
- testes de persistencia sem banco real.

Status:

Concluida.

## Sprint 6 - Conexao com banco e endpoints iniciais

Objetivo:

Conectar o backend ao PostgreSQL/Supabase e iniciar endpoints de negocio.

Entregaveis previstos:

- orientacao para criar/conectar Supabase;
- configuracao local segura do `.env`;
- aplicacao revisada do schema;
- gravacao inicial de importacoes;
- endpoint de busca por provedor;
- endpoint de resumo basico.

## Sprint 7 - Dashboard inicial

Objetivo:

Criar a primeira versao funcional do dashboard online.

Entregaveis previstos:

- tela de busca;
- cards de indicadores;
- grafico de evolucao;
- tabelas por UF e municipio;
- composicao por tecnologia.

## Sprint 8 - Otimizacao e experiencia

Objetivo:

Melhorar desempenho, mensagens de usuario e estabilidade do fluxo de importacao.

Entregaveis previstos:

- feedback de progresso;
- tratamento de erros;
- otimizacoes de consulta;
- ajustes visuais.

## Sprint futura - Mapas

Objetivo:

Avaliar se mapas realmente agregam valor ao produto.

Mapas so devem ser implementados se forem simples, leves e uteis para analise.
