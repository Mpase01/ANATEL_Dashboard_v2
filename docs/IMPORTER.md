# Importador

## Objetivo

O importador sera responsavel por transformar planilhas pesadas da ANATEL em dados estruturados no PostgreSQL.

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

## Regras principais

- O sistema nao deve depender do nome do arquivo.
- O sistema deve identificar automaticamente colunas de meses no formato `YYYY-MM`.
- O sistema deve transformar colunas de meses em registros normalizados.
- O sistema nao deve apagar todo o banco antes de importar.
- O sistema deve detectar se um arquivo mudou.
- O sistema deve registrar cada importacao como um lote.
- O sistema deve evitar duplicidade de registros.

## Fluxo planejado

```text
Arquivo Excel recebido
↓
Calculo do hash do arquivo
↓
Verificacao se o arquivo ja foi importado sem mudancas
↓
Leitura das abas e colunas necessarias
↓
Identificacao das colunas YYYY-MM
↓
Transformacao dos meses em linhas
↓
Validacao dos registros
↓
Registro do lote de importacao
↓
Inclusao ou atualizacao dos dados no banco
↓
Finalizacao do lote
```

## Deteccao de mudancas

Cada arquivo deve ter uma assinatura tecnica, chamada `file_hash`.

Se o mesmo arquivo ja foi importado e o hash nao mudou, o sistema pode ignorar a nova importacao.

Se o hash mudou, o sistema deve processar novamente os dados e atualizar os registros afetados.

## Validacoes esperadas

O importador deve validar pelo menos:

- existencia de colunas de periodo no formato `YYYY-MM`;
- presenca de informacoes minimas do provedor;
- valores numericos de assinantes;
- municipio e estado quando disponiveis;
- tecnologia quando disponivel;
- linhas vazias ou inconsistentes.

## Tratamento de erro

Uma falha de importacao nao deve deixar o banco em estado quebrado.

O sistema deve registrar o erro no lote de importacao e informar o usuario de forma clara.

## Desempenho

Como as planilhas podem ser pesadas, o importador deve evitar carregar e processar mais dados do que o necessario.

O processamento deve ser feito de forma previsivel, com logs e mensagens de progresso quando possivel.

## Experiencia do usuario

O usuario nao deve precisar entender banco de dados, Python ou estrutura interna da ANATEL.

A interface deve comunicar estados simples:

- arquivo recebido;
- importacao em andamento;
- importacao concluida;
- arquivo sem mudancas;
- erro encontrado.
