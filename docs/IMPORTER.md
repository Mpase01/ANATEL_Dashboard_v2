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
- O sistema deve preservar `Pessoa Fisica` e `Pessoa Juridica` para analise B2C/B2B.

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
Agregacao para o nivel usado pelo dashboard
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

## Estrategia agregada

A carga detalhada completa de 2026 nao coube no armazenamento atual do Supabase.

A estrategia recomendada passou a ser gravar uma tabela agregada, mantendo apenas os recortes essenciais para o dashboard:

```text
prestadora
nome da prestadora
mes
codigo IBGE do municipio
municipio
UF
tecnologia
meio de acesso
tipo de pessoa
assinantes somados
```

O campo `tipo de pessoa` deve ser mantido porque permite analisar:

```text
Pessoa Fisica  -> B2C
Pessoa Juridica -> B2B
```

## Simulacao de compactacao

Foi criado o script:

```text
backend/scripts/simulate_compaction.py
```

Resultado com o CSV real de 2026:

```text
base bruta: 3.222.220 registros
base compactada: 839.183 registros
reducao: 73,96%
tempo de simulacao: 47,16 segundos
```

A soma de assinantes foi preservada:

```text
base bruta: 280.681.407
base compactada: 280.681.407
```

Distribuicao por tipo de pessoa:

```text
Pessoa Fisica: 248.478.363 assinantes-mes
Pessoa Juridica: 32.203.044 assinantes-mes
```

## Deteccao de mudancas

Cada arquivo deve ter uma assinatura tecnica, chamada `file_hash`.

Na estrutura agregada, a chave de atualizacao deve considerar a combinacao dos campos agregados, incluindo periodo e tipo de pessoa.

## Validacoes esperadas

O importador deve validar pelo menos:

- existencia de colunas de periodo no formato `YYYY-MM`;
- presenca de CNPJ;
- presenca de nome da empresa;
- municipio e UF;
- codigo IBGE do municipio quando disponivel;
- tecnologia;
- meio de acesso;
- tipo de pessoa;
- valores numericos de assinantes;
- linhas vazias ou inconsistentes.

## Tratamento de erro

Uma falha de importacao nao deve deixar o banco em estado quebrado.

O sistema deve registrar o erro no lote de importacao e informar o usuario de forma clara.

## Desempenho

Como os arquivos sao pesados, o importador deve evitar carregar e gravar mais dados do que o necessario.

Decisao atual de desempenho:

- nao gravar registros mensais com zero assinantes;
- processar colunas mensais automaticamente;
- agregar antes de gravar;
- manter B2C/B2B;
- preparar consultas agregadas no backend;
- evitar enviar dados brutos grandes para o frontend.

## Experiencia do usuario

O usuario nao deve precisar entender banco de dados, Python ou estrutura interna da ANATEL.

A interface deve comunicar estados simples:

- arquivo recebido;
- importacao em andamento;
- importacao concluida;
- arquivo sem mudancas;
- erro encontrado.
