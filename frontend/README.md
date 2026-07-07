# Frontend

Frontend do ANATEL Dashboard.

Esta camada sera responsavel por apresentar o dashboard online de forma simples, rapida e responsiva.

## Estrutura planejada

```text
frontend/
  src/
    charts/       # componentes e configuracoes de graficos
    components/   # componentes reutilizaveis
    pages/        # paginas principais
    services/     # comunicacao com a API
    styles/       # estilos globais e temas
  tests/          # testes automatizados do frontend
```

## Regra importante

O frontend deve consumir apenas a API do backend.

Ele nao deve acessar diretamente o Supabase ou qualquer credencial sensivel.

## Experiencia esperada

A interface deve ser simples para alguem nao tecnico:

- buscar um provedor;
- visualizar indicadores principais;
- entender se a base foi atualizada;
- navegar por graficos e tabelas sem lentidao.

## Status

Nesta sprint, apenas a estrutura inicial foi criada.

Nenhuma tela ou funcionalidade foi implementada ainda.
