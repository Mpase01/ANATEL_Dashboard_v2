# Importador

## Objetivo

O importador sera responsavel por transformar arquivos CSV pesados da ANATEL em dados estruturados no PostgreSQL.

A operacao desejada para o usuario deve ser simples:

```text
Enviar ou substituir a planilha
↓
Clicar em Atualizar Base
↓
Aguardar o processamento
↓
Ver o dashboard atualizado
```

## Base real analisada

Foram analisados os arquivos:

- `Acessos_Banda_Larga_Fixa_2025_Colunas.csv`
- `Acessos_Banda_Larga_Fixa_2026_Colunas.csv`

Caracteristicas relevantes:

- separador `;`;
- meses em colunas `YYYY-MM`;
- 2025 possui meses de `2025-01` ate `2025-12`;
- 2026 possui meses de `2026-01` ate `2026-05`;
- a base de 2026 deve receber novas colunas mensais ao longo do ano;
- os arquivos sao grandes, acima de 100 MB.

## Regras principais

- O sistema nao deve depender do nome do arquivo.
- O sistema deve identificar automaticamente colunas de meses no formato `YYYY-MM`.
- O sistema deve transformar colunas de meses em registros normalizados.
- O sistema nao deve apagar todo o banco antes de importar.
- O sistema deve detectar se um arquivo mudou.
- O sistema deve registrar cada importacao como um lote.
- O sistema deve evitar duplicidade de registros.
- O sistema deve ignorar registros mensais com zero assinantes.
- O sistema deve usar CNPJ como identificador principal do provedor.
- O sistema deve registrar nomes de empresa como aliases quando necessario.

## Fluxo planejado

```text
Arquivo CSV recebido
↓
Calculo do hash do arquivo
↓
Verificacao se o arquivo ja foi importado sem mudancas
↓
Leitura das colunas fixas
↓
Identificacao das colunas YYYY-MM
↓
Transformacao dos meses em linhas
↓
Descarte dos registros mensais com zero assinantes
↓
Calculo do source_row_hash da linha original
↓
Validacao dos registros
↓
Registro do lote de importacao
↓
Inclusao ou atualizacao dos dados no banco
↓
Finalizacao do lote
```

## Atualizacao mensal

A base de 2026 deve chegar mensalmente com novas colunas.

Exemplo:

```text
2026-01
2026-02
2026-03
2026-04
2026-05
2026-06
```

O importador deve detectar meses novos automaticamente.

Quando um arquivo atualizado for enviado, o sistema deve:

- identificar os meses existentes no arquivo;
- comparar com os meses ja importados;
- inserir meses novos;
- atualizar registros de meses antigos caso os valores tenham mudado;
- manter o historico anterior.

## Deteccao de mudancas

Cada arquivo deve ter uma assinatura tecnica, chamada `file_hash`.

Cada linha fixa da ANATEL tambem deve gerar um `source_row_hash`.

A combinacao `period + source_row_hash` sera usada para evitar duplicidade na tabela principal.

## Validacoes esperadas

O importador deve validar pelo menos:

- existencia de colunas de periodo no formato `YYYY-MM`;
- presenca de CNPJ;
- presenca de nome da empresa;
- municipio e UF;
- codigo IBGE do municipio quando disponivel;
- tecnologia;
- meio de acesso;
- valores numericos de assinantes;
- linhas vazias ou inconsistentes.

## Tratamento de erro

Uma falha de importacao nao deve deixar o banco em estado quebrado.

O sistema deve registrar o erro no lote de importacao e informar o usuario de forma clara.

## Desempenho

Como os arquivos sao pesados, o importador deve evitar carregar e gravar mais dados do que o necessario.

Decisao inicial de desempenho:

- nao gravar registros mensais com zero assinantes;
- processar colunas mensais automaticamente;
- preparar consultas agregadas no backend;
- evitar enviar dados brutos grandes para o frontend.

## Importacao por lotes

A primeira importacao ampliada foi feita com o script `backend/scripts/import_csv_batched.py`.

Resultado validado com o CSV real de 2026 antes da otimizacao:

```text
registros normalizados: 5.000
lotes: 5
tamanho do lote: 1.000 registros
tempo de gravacao no Supabase: 107,86 segundos
```

Depois da otimizacao da gravacao em lote, o mesmo teste ficou assim:

```text
registros normalizados: 5.000
lotes: 5
tamanho do lote: 1.000 registros
tempo de gravacao no Supabase: 3,77 segundos
```

Com volume maior, o resultado foi:

```text
registros normalizados: 50.000
lotes: 10
tamanho do lote: 5.000 registros
tempo de gravacao no Supabase: 11,3 segundos
```

A contagem final ficou em 50.002 registros mensais.

Decisao: a carga completa do CSV de 2026 pode ser testada na proxima sprint, com monitoramento de tempo e resposta da API.

## Experiencia do usuario

O usuario nao deve precisar entender banco de dados, Python ou estrutura interna da ANATEL.

A interface deve comunicar estados simples:

- arquivo recebido;
- importacao em andamento;
- importacao concluida;
- arquivo sem mudancas;
- erro encontrado.
