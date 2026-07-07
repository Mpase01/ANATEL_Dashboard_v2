# Registro de Decisoes

Este documento registra decisoes importantes do projeto.

O objetivo e evitar retrabalho e manter clareza sobre por que certas escolhas foram feitas.

## 001 - Manter historico no banco

Decisao:

O banco deve manter o historico importado, e nao apenas os ultimos 12 meses.

Motivo:

O dashboard pode exibir 12 meses por padrao, mas analises futuras podem precisar de historico maior.

Impacto:

Evita perda de dados e permite evolucao futura para analises historicas.

## 002 - Nao apagar tudo antes de importar

Decisao:

O importador nao deve apagar todos os registros antes de importar novamente.

Motivo:

Esse fluxo e arriscado se a importacao falhar no meio.

Impacto:

O sistema deve usar deteccao de mudancas, lotes de importacao e atualizacao controlada de registros.

## 003 - Usar modelo normalizado

Decisao:

As colunas mensais da planilha devem ser transformadas em linhas no banco.

Motivo:

Consultas por periodo, tecnologia, municipio e provedor ficam mais simples e eficientes.

Impacto:

A tabela principal tera uma linha por combinacao de provedor, periodo, localidade e tecnologia.

## 004 - Tratar provedores com CNPJ, nome e aliases

Decisao:

O sistema deve considerar que o mesmo provedor pode aparecer com variacoes de nome.

Motivo:

Bases reais podem ter inconsistencias de grafia ou nomenclatura.

Impacto:

O modelo tera uma tabela de provedores e uma tabela de aliases.

## 005 - Frontend nao acessa banco diretamente

Decisao:

O dashboard React deve consumir apenas a API.

Motivo:

Isso protege credenciais, centraliza regras de negocio e reduz acoplamento.

Impacto:

Toda regra de calculo e consulta deve ficar no backend.

## 006 - API deve entregar dados agregados

Decisao:

A API deve retornar dados ja preparados para as telas.

Motivo:

As planilhas sao pesadas e o navegador nao deve processar grandes volumes brutos.

Impacto:

O backend sera responsavel por agregacoes, filtros e calculos principais.

## 007 - Mapas ficam para depois

Decisao:

Mapas nao fazem parte da primeira versao funcional.

Motivo:

Eles podem adicionar complexidade e peso antes de provar valor real.

Impacto:

A primeira versao priorizara busca, indicadores, graficos e tabelas.

## 008 - Simplicidade acima de complexidade

Decisao:

O projeto deve priorizar uma solucao simples, funcional e eficiente.

Motivo:

O usuario principal nao e programador e precisa de uma ferramenta intuitiva para carregar planilhas e visualizar dados online.

Impacto:

Cada nova funcionalidade deve justificar seu valor antes de ser implementada.
