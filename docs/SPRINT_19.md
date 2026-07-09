# Sprint 19 - Decisao de armazenamento e volume

## Objetivo

Descobrir se a base da ANATEL pode caber no Supabase usando uma estrutura agregada, sem perder os recortes importantes para o dashboard.

## Decisao de negocio

O campo `tipo de pessoa` deve ser mantido.

Ele separa:

```text
Pessoa Fisica  -> B2C
Pessoa Juridica -> B2B
```

Esse recorte e importante para entender o perfil dos clientes das prestadoras.

## Agregacao simulada

A simulacao manteve os seguintes campos:

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

Campos mais detalhados, como velocidade exata, faixa de velocidade, porte da prestadora, grupo economico e tipo de produto, nao entraram nessa primeira compactacao.

## Script criado

Foi criado o script:

```text
backend/scripts/simulate_compaction.py
```

Ele le o CSV completo, agrupa os registros no formato proposto e compara a base bruta com a base compactada.

## Arquivo analisado

```text
Acessos_Banda_Larga_Fixa_2026_Colunas.csv
```

Tamanho:

```text
120.152.110 bytes
```

Meses identificados:

```text
2026-01
2026-02
2026-03
2026-04
2026-05
```

## Resultado da simulacao

```text
base bruta: 3.222.220 registros
base compactada: 839.183 registros
reducao: 73,96%
tempo de simulacao: 47,16 segundos
```

A soma de assinantes foi preservada:

```text
assinantes na base bruta: 280.681.407
assinantes na base compactada: 280.681.407
```

## Dimensoes encontradas

```text
prestadoras: 11.455
municipios: 5.595
tecnologias: 31
meios de acesso: 5
```

## B2C e B2B

Distribuicao por tipo de pessoa:

```text
Pessoa Fisica: 248.478.363 assinantes-mes
Pessoa Juridica: 32.203.044 assinantes-mes
```

Essa informacao deve virar um recorte do dashboard.

## Principais tecnologias

```text
FTTH: 213.057.946
HFC: 39.012.725
ETHERNET: 12.465.877
VSAT: 4.459.236
Wi-Fi: 4.421.321
FWA: 2.968.086
FTTB: 2.045.394
ADSL2: 722.738
HDSL: 592.652
ADSL1: 455.318
```

## Principais meios de acesso

```text
Fibra: 224.182.569
Cabo Coaxial: 39.531.247
Radio: 9.237.285
Satelite: 4.500.741
Cabo Metalico: 3.229.565
```

## Conclusao

A compactacao reduz bastante o volume, mas ainda gera 839.183 registros para apenas 5 meses de 2026.

Isso e muito melhor do que 3.222.220 registros, mas ainda exige cuidado porque o Supabase ja atingiu limite de armazenamento com a base detalhada parcial.

## Decisao recomendada

Seguir para uma nova estrutura de dados agregada, mantendo `tipo de pessoa`, antes de tentar nova carga completa.

A proxima sprint deve criar a tabela agregada e migrar o dashboard para consultar essa tabela mais leve.

## Status

Concluida.
