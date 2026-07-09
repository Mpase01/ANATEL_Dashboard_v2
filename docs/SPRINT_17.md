# Sprint 17 - Teste com volume maior

## Objetivo

Testar a importacao otimizada com um volume maior antes da carga completa da planilha da ANATEL.

## Arquivo usado

Foi usado o arquivo real:

```text
Acessos_Banda_Larga_Fixa_2026_Colunas.csv
```

Tamanho do arquivo:

```text
120.152.110 bytes
```

## Estado inicial do banco

Antes do teste, o banco estava assim:

```text
prestadoras: 6
registros mensais: 5.002
```

## Configuracao do teste

```text
limite: 50.000 registros normalizados
tamanho do lote: 5.000 registros
lotes esperados: 10
modo: gravacao real no Supabase
```

## Resultado da importacao

```text
lotes gravados: 10
registros normalizados: 50.000
registros enviados ao banco: 50.000
tempo total: 11,3 segundos
```

## Estado final do banco

Depois da importacao, a validacao retornou:

```text
prestadoras: 6
registros mensais: 50.002
```

Isso indica que a importacao ampliou a base sem multiplicar prestadoras indevidamente.

## Validacao da API

A API real continuou respondendo corretamente.

Endpoint de saude do banco:

```text
status: ok
prestadoras: 6
registros mensais: 50.002
```

A busca de prestadoras tambem respondeu normalmente para o termo `NET`.

## Validacao do dashboard via endpoints

Foram testados os endpoints que a tela consome para a prestadora `DUNET TECNOLOGIA E INFORMATICA`.

Resumo validado:

```text
periodo final: 2026-05-01
assinantes: 678
fibra: 97,79%
municipio principal: Araputanga/MT
crescimento: 349,01%
```

Evolucao validada:

```text
2026-01: 151
2026-02: 305
2026-03: 499
2026-04: 666
2026-05: 678
```

Tecnologias validadas:

```text
FTTH/Fibra: 663 assinantes
Wi-Fi/Radio: 15 assinantes
```

Municipio validado:

```text
Araputanga/MT: 678 assinantes
```

## Testes automatizados

Os testes do backend foram executados depois da importacao:

```text
6 testes executados
resultado: OK
```

## Observacao sobre a tela

A tentativa de leitura visual pelo navegador interno travou, mas os endpoints reais usados pela tela responderam corretamente. Como o frontend consome esses mesmos endpoints, a validacao tecnica da tela foi considerada suficiente nesta sprint.

## Decisao

A importacao otimizada suportou bem 50.000 registros normalizados.

A proxima etapa recomendada e executar a carga completa do CSV de 2026, mantendo monitoramento de:

- tempo total;
- contagem final;
- resposta da API;
- desempenho do dashboard;
- possibilidade de limpar registros ficticios de teste antes do uso final.

## Status

Concluida.
