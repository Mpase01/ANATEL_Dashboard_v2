# Sprint 16 - Otimizacao da importacao

## Objetivo

Otimizar a escrita dos dados no Supabase antes de tentar importar o arquivo completo da ANATEL.

## Problema encontrado

Na Sprint 15, a importacao de 5.000 registros normalizados funcionou corretamente, mas demorou 107,86 segundos.

A causa principal era a estrategia de gravacao linha a linha no banco.

## O que foi alterado

O modulo `backend/app/importer/database_writer.py` foi otimizado para enviar listas de registros ao banco em vez de executar uma gravacao individual por linha.

Foram otimizadas as gravacoes de:

- prestadoras;
- aliases de prestadoras;
- registros mensais de assinantes.

A regra de duplicidade foi mantida:

```text
period + source_row_hash
```

Ou seja, se o mesmo registro for importado novamente, ele e atualizado em vez de duplicado.

## Validacao realizada

Foi repetido o mesmo teste da Sprint 15 com o arquivo real de 2026.

Configuracao:

```text
limite: 5.000 registros normalizados
lote: 1.000 registros
modo: gravacao real no Supabase
```

Resultado depois da otimizacao:

```text
lotes gravados: 5
registros normalizados: 5.000
registros enviados ao banco: 5.000
tempo: 3,77 segundos
```

## Comparativo

```text
antes: 107,86 segundos
depois: 3,77 segundos
```

A importacao ficou cerca de 28 vezes mais rapida neste teste controlado.

## Validacao de integridade

Depois de repetir a importacao, a contagem do banco continuou correta:

```text
prestadoras: 6
registros mensais: 5.002
```

Isso confirma que a reimportacao nao duplicou os registros mensais existentes.

## Testes locais

Os testes automatizados do backend passaram:

```text
6 testes executados
resultado: OK
```

## Decisao

A importacao ja esta muito mais rapida, mas ainda deve ser testada com volumes maiores antes da carga completa.

A proxima etapa recomendada e testar 50.000 registros normalizados e medir:

- tempo total;
- estabilidade da conexao;
- contagem final;
- resposta do dashboard apos aumento da base.

## Status

Concluida.
