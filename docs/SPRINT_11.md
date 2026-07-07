# Sprint 11 - Rodar e polir localmente

## Objetivo

Deixar a primeira tela mais facil de visualizar localmente e preparar a interface para ajustes simples de recorte temporal.

## O que foi feito

- A tela foi rodada localmente em `http://127.0.0.1:5173/`.
- Foi adicionado modo demonstracao no frontend.
- Foi adicionado filtro de periodo na interface.
- O filtro permite alternar entre:
  - todos os meses;
  - ultimos 3 meses;
  - ultimo mes.
- O crescimento exibido nos cards passa a respeitar o recorte escolhido.
- A tela continua preparada para usar a API real quando o backend estiver configurado.

## Por que o modo demonstracao existe

O backend local ainda nao esta configurado com credenciais reais do Supabase.

Sem o modo demonstracao, a tela abriria vazia ou com erro enquanto a API local nao estivesse pronta.

Com o modo demonstracao, o usuario consegue ver e avaliar a experiencia visual imediatamente.

## Dados demonstrativos

Os dados demonstrativos usam a amostra real ja validada na Sprint 9:

```text
Prestadora: NET-UAI INTERNET WIRELESS
CNPJ: 10785849000171
Periodo: 2026-01 a 2026-05
Acessos no ultimo mes: 105
Municipios: 2
Fibra: 13 acessos
```

## Validacao local

O filtro foi validado com os seguintes resultados:

```text
Todos os meses: 5 barras, 01/2026 a 05/2026, crescimento 15,4%
Ultimos 3 meses: 3 barras, 03/2026 a 05/2026, crescimento 14,1%
Ultimo mes: 1 barra, 05/2026, crescimento 0,0%
```

## Proxima sprint sugerida

Sprint 12:

- configurar o backend local para consultar a API real;
- remover a dependencia do modo demonstracao no uso normal;
- preparar filtros reais por periodo no backend;
- iniciar planejamento da carga completa com barra de progresso e controle de erro.