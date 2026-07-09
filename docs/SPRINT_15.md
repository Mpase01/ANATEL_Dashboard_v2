# Sprint 15 - Importacao ampliada dos CSVs reais

## Objetivo

Importar um volume maior do CSV real da ANATEL com seguranca, medindo tempo, volume e impacto antes de tentar uma carga completa.

## O que foi feito

- Criado o script `backend/scripts/import_csv_batched.py`.
- O importador agora consegue processar o CSV em lotes controlados.
- O limite padrao foi mantido em 5.000 registros normalizados para evitar cargas acidentais muito grandes.
- Foi adicionado modo de teste sem gravar no banco usando `--dry-run`.
- Cada lote e confirmado separadamente no banco.
- A importacao registra lote, arquivo e registros mensais no Supabase.

## Validacoes realizadas

Foi usado o arquivo real:

```text
Acessos_Banda_Larga_Fixa_2026_Colunas.csv
```

### Teste sem gravar

Configuracao:

```text
limite: 5.000 registros normalizados
lote: 1.000 registros
modo: dry-run
```

Resultado:

```text
lotes processados: 5
registros normalizados: 5.000
tempo: 0,28 segundo
```

### Importacao real no Supabase

Configuracao:

```text
limite: 5.000 registros normalizados
lote: 1.000 registros
modo: gravacao real
```

Resultado:

```text
lotes gravados: 5
registros normalizados: 5.000
registros enviados ao banco: 5.000
tempo: 107,86 segundos
```

## Estado do banco depois da importacao

A validacao do banco retornou:

```text
prestadoras: 6
registros mensais: 5.002
```

Observacao: os 5.002 registros incluem os registros de teste anteriores e a amostra ampliada importada nesta sprint.

## Validacao na API

O endpoint real do backend continuou respondendo corretamente.

Exemplo validado:

```text
prestadora: DUNET TECNOLOGIA E INFORMATICA
periodo: 2026-01 a 2026-05
assinantes no ultimo mes: 678
participacao de fibra: 97,79%
crescimento no periodo: 349,01%
```

## Resultado tecnico

A importacao ampliada funcionou corretamente, mas revelou um ponto importante de desempenho.

O tempo de 107,86 segundos para 5.000 registros indica que a estrategia atual, baseada em gravacoes linha a linha, ainda nao e adequada para importar o arquivo completo com conforto.

## Decisao

Antes de executar a carga completa, a proxima sprint deve otimizar a escrita no banco.

Prioridade da proxima etapa:

- reduzir chamadas individuais ao banco;
- usar gravacao em massa quando possivel;
- manter protecao contra duplicidade;
- manter registro de lote e arquivo;
- preservar simplicidade para o usuario final.

## Status

Concluida.
