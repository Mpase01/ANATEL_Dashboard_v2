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

Em andamento.

## Sprint 2 - Estrutura inicial do projeto

Objetivo:

Criar a estrutura base do backend e do frontend, ainda sem funcionalidades completas.

Entregaveis previstos:

- pastas principais do backend;
- pastas principais do frontend;
- arquivos de configuracao iniciais;
- padrao de variaveis de ambiente;
- instrucoes de execucao local.

## Sprint 3 - Modelo de banco

Objetivo:

Criar o modelo inicial do PostgreSQL.

Entregaveis previstos:

- tabelas principais;
- indices iniciais;
- constraints importantes;
- registro de lotes de importacao.

## Sprint 4 - Importador inicial

Objetivo:

Ler planilhas da ANATEL, identificar meses automaticamente e transformar os dados em formato normalizado.

Entregaveis previstos:

- leitura de Excel;
- deteccao de colunas `YYYY-MM`;
- transformacao para linhas;
- validacoes iniciais;
- gravacao no banco.

## Sprint 5 - API inicial

Objetivo:

Disponibilizar endpoints para busca de provedores e indicadores principais.

Entregaveis previstos:

- busca por nome e CNPJ;
- resumo do provedor;
- evolucao mensal;
- distribuicao por UF e municipio.

## Sprint 6 - Dashboard inicial

Objetivo:

Criar a primeira versao funcional do dashboard online.

Entregaveis previstos:

- tela de busca;
- cards de indicadores;
- grafico de evolucao;
- tabelas por UF e municipio;
- composicao por tecnologia.

## Sprint 7 - Otimizacao e experiencia

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
