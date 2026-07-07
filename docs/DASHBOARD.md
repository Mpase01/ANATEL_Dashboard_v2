# Dashboard

## Objetivo

O dashboard deve permitir que o usuario analise rapidamente a posicao de mercado de um provedor de banda larga fixa com base nos dados publicos da ANATEL.

A experiencia deve ser simples, visual e rapida.

## Tela principal

A tela principal sera a busca de provedor.

O usuario podera pesquisar por:

- nome;
- CNPJ.

Apos selecionar um provedor, o dashboard exibira os indicadores principais.

## Indicadores principais

Indicadores previstos para a primeira versao funcional:

- total de assinantes;
- market share Brasil;
- participacao da fibra;
- crescimento dos ultimos 12 meses;
- numero de municipios atendidos;
- numero de estados atendidos;
- municipio com maior numero de assinantes;
- estado com maior numero de assinantes.

## Visualizacoes

Visualizacoes previstas:

- grafico de evolucao mensal;
- composicao por tecnologia;
- tabela por estado;
- tabela por municipio.

A tecnologia fibra deve sempre receber destaque visual.

As demais tecnologias devem aparecer de forma discreta, mas disponivel para analise.

## Mapas

Mapas ficam fora da primeira versao funcional.

Embora os arquivos possam conter codigo IBGE dos municipios, o mapa sera avaliado em uma fase posterior.

A decisao atual e evitar adicionar peso e complexidade antes de confirmar que o mapa realmente agrega valor ao produto.

## Desempenho

O dashboard deve ser leve.

O navegador nao deve receber planilhas inteiras nem grandes volumes brutos de dados.

A API deve enviar informacoes ja preparadas para cada tela.

## Experiencia do usuario

O usuario nao precisa ser tecnico.

Por isso, a interface deve ter:

- busca simples;
- botoes claros;
- mensagens de carregamento;
- mensagens de erro compreensiveis;
- indicadores com nomes objetivos;
- tabelas legiveis;
- layout responsivo.

## Estilo visual

O visual deve ser profissional, limpo e direto.

A interface deve parecer uma ferramenta de analise, nao uma pagina promocional.

A prioridade e leitura rapida, comparacao facil e confianca nos numeros.
