# Sprint 22 - Visao por grupo economico

## Objetivo

Permitir que o dashboard mostre uma empresa consolidada pelo campo `Grupo Economico` da ANATEL, sem perder a opcao de analisar uma prestadora/CNPJ especifico.

## Por que isso foi feito

Ao buscar CLARO por prestadora, a tela podia mostrar apenas um CNPJ com cerca de 271 mil acessos. Na base da ANATEL, os CNPJs da CLARO aparecem consolidados no grupo economico `TELECOM AMERICAS`, com 10.784.341 acessos no ultimo mes da base 2026.

## O que mudou

- A tabela agregada `aggregated_subscription_records` passou a armazenar `economic_group`.
- O importador agregado passou a considerar `economic_group` na chave de agregacao.
- A API recebeu endpoints para busca e dashboard por grupo economico.
- A busca por grupo economico tambem encontra o grupo quando o usuario digita o nome de uma empresa dentro dele, como `CLARO`.
- A tela recebeu o seletor `Grupo economico` / `Prestadora/CNPJ`.

## Validacao

- CSV 2026 lido: 3.222.220 linhas.
- Registros agregados gravados: 839.183.
- Soma total preservada: 280.681.407 acessos.
- Grupos economicos encontrados: 24.
- Busca por `CLARO`: retorna `TELECOM AMERICAS`.
- Total no ultimo mes para `TELECOM AMERICAS`: 10.784.341 acessos.

## Decisao de produto

A visao padrao da tela fica em `Grupo economico`, porque ela representa melhor grupos grandes com varios CNPJs. A visao por `Prestadora/CNPJ` continua disponivel para investigacoes mais detalhadas.
