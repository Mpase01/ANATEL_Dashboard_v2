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

## Sprint 6 - Conexao com banco e busca inicial

Objetivo:

Preparar o backend para conectar ao PostgreSQL/Supabase e iniciar o primeiro endpoint de negocio.

Entregaveis:

- camada de sessao SQLAlchemy;
- repositorio inicial de provedores;
- endpoint `GET /providers/search`;
- guia `docs/SUPABASE_SETUP.md`;
- testes sem banco real.

Status:

Concluida.

## Sprint 7 - Supabase real e schema aplicado

Objetivo:

Conectar um projeto Supabase real e aplicar o schema inicial em banco vazio.

Entregaveis:

- projeto Supabase identificado;
- schema aplicado via migration;
- RLS habilitado;
- views criadas com `security_invoker`;
- indices de chaves estrangeiras adicionados;
- advisors de seguranca e performance revisados;
- guia Supabase atualizado.

Status:

Concluida.

## Sprint 8 - Gravacao controlada no banco

Objetivo:

Validar uma primeira gravacao pequena no Supabase real, sem importar ainda as planilhas grandes da ANATEL.

Entregaveis:

- confirmacao das tabelas reais no Supabase;
- criacao de `import_batch` e `import_file` de amostra;
- gravacao de uma prestadora ficticia e seu alias;
- gravacao de 2 registros mensais ficticios;
- validacao de contagens no banco;
- modulo `backend/app/importer/database_writer.py` para concentrar a escrita no banco.

Status:

Concluida.

## Sprint 9 - Importacao pequena de ponta a ponta

Objetivo:

Rodar um fluxo pequeno usando recorte dos CSVs reais, saindo do arquivo e chegando no Supabase.

Entregaveis:

- recorte controlado do CSV real de 2026;
- leitura e normalizacao de 5 linhas de origem;
- gravacao de 24 registros mensais reais;
- validacao de contagens;
- validacao de totais agregados por mes;
- script `backend/scripts/import_csv_preview.py` para futuras amostras pelo backend.

Status:

Concluida.

## Sprint 10 - Dashboard inicial

Objetivo:

Criar a primeira versao funcional do dashboard online consultando os dados ja gravados.

Entregaveis:

- endpoints de resumo, evolucao, tecnologias e municipios;
- tela de busca;
- cards de indicadores;
- grafico simples de evolucao;
- composicao por tecnologia;
- tabela por municipio;
- aviso de que os dados atuais ainda sao amostras.

Status:

Concluida.

## Sprint 11 - Rodar e polir localmente

Objetivo:

Rodar a tela localmente, permitir visualizacao mesmo sem API local configurada e adicionar primeiro controle de recorte temporal.

Entregaveis:

- previa local em `http://127.0.0.1:5173/`;
- modo demonstracao no frontend;
- filtro de periodo;
- recalculo de crescimento conforme recorte escolhido;
- validacao visual no navegador local;
- documentacao da sprint.

Status:

Concluida.

## Sprint 12 - API local de demonstracao

Objetivo:

Criar uma API local sem dependencias externas para validar o contrato do dashboard antes da conexao real ao Supabase.

Entregaveis:

- script `backend/scripts/demo_api.py`;
- API local em `http://127.0.0.1:8000`;
- endpoint de saude;
- busca de prestadora;
- endpoints de resumo, evolucao, tecnologias e municipios;
- dashboard consumindo a API local;
- documentacao da sprint.

Status:

Concluida.

## Sprint 13 - Filtro temporal no contrato da API

Objetivo:

Mover o recorte temporal para a API, mantendo a tela simples e preparando o sistema para bases maiores.

Entregaveis:

- parametro `period=all|last3|latest` nos endpoints do dashboard;
- frontend enviando o periodo selecionado para a API;
- API local de demonstracao respeitando o mesmo contrato;
- consultas reais preparadas para limitar os periodos no banco;
- validacao local no navegador.

Status:

Concluida.

## Sprint 14 - Backend real com Supabase

Objetivo:

Ligar a tela local ao backend real e ao Supabase, substituindo a API de demonstracao no uso normal.

Entregaveis:

- dependencias do backend instaladas ou preparadas;
- FastAPI real rodando localmente;
- carregamento local de `.env`;
- verificador de conexao com banco;
- `DATABASE_URL` local configurado com seguranca;
- endpoint `GET /health/database` validado;
- tela consumindo endpoints reais;
- mensagens melhores para erro de API;
- documentacao da conexao local.

Status:

Concluida.

## Sprint 15 - Importacao ampliada dos CSVs reais

Objetivo:

Importar um volume maior dos CSVs reais com seguranca, medindo tempo, volume e impacto antes da carga completa.

Entregaveis previstos:

- estrategia de importacao por lotes;
- medicao de tempo por lote;
- validacao de contagens depois da importacao;
- protecao contra duplicidade;
- preparacao para barra de progresso.

Status:

Planejada.

## Sprint futura - Mapas

Objetivo:

Avaliar se mapas realmente agregam valor ao produto.

Mapas so devem ser implementados se forem simples, leves e uteis para analise.
