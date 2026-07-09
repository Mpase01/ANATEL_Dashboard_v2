# Documentacao do ANATEL Dashboard

Esta pasta concentra as decisoes e regras principais do projeto.

O objetivo da documentacao e manter o projeto simples de entender, facil de evoluir e seguro para trabalhar ao longo de varios meses.

## Ordem recomendada de leitura

1. `VISION.md` - explica o objetivo do produto e o publico-alvo.
2. `PROJECT.md` - define a forma de trabalho e as regras gerais.
3. `ARCHITECTURE.md` - descreve a arquitetura do sistema.
4. `DATABASE.md` - descreve o modelo de dados planejado.
5. `IMPORTER.md` - descreve como as planilhas da ANATEL serao processadas.
6. `API.md` - descreve a API entre o backend e o dashboard.
7. `DASHBOARD.md` - descreve a experiencia visual e os indicadores.
8. `SUPABASE_SETUP.md` - explica como o Supabase sera configurado.
9. `SUPABASE_CONNECTION.md` - explica como conectar a API local ao Supabase com seguranca.
10. `ROADMAP.md` - organiza o projeto por fases e sprints.
11. `DECISIONS.md` - registra decisoes tecnicas importantes.
12. `SPRINT_1.md` - resume a primeira sprint de documentacao.
13. `SPRINT_2.md` - resume a estrutura inicial do projeto.
14. `SPRINT_3.md` - resume o modelo inicial do banco baseado nos CSVs reais.
15. `SPRINT_4.md` - resume o importador inicial dos CSVs da ANATEL.
16. `SPRINT_5.md` - resume a preparacao de persistencia e API inicial.
17. `SPRINT_6.md` - resume a preparacao de conexao com banco e busca inicial.
18. `SPRINT_7.md` - resume a aplicacao do schema no Supabase real.
19. `SPRINT_8.md` - resume a primeira gravacao controlada no Supabase real.
20. `SPRINT_9.md` - resume a primeira importacao pequena com dados reais da ANATEL.
21. `SPRINT_10.md` - resume o primeiro dashboard funcional com dados de amostra.
22. `SPRINT_11.md` - resume a previa local, modo demonstracao e filtro de periodo.
23. `SPRINT_12.md` - resume a API local de demonstracao para validar o contrato do dashboard.
24. `SPRINT_13.md` - resume o filtro temporal no contrato da API.
25. `SPRINT_14.md` - resume a preparacao local do backend real.
26. `SPRINT_15.md` - resume a importacao ampliada por lotes com dados reais.
27. `SPRINT_16.md` - resume a otimizacao da gravacao em lote no Supabase.
28. `SPRINT_17.md` - resume o teste ampliado com 50.000 registros normalizados.

## Principio central

O sistema deve ser simples, funcional e eficiente.

A prioridade nao e criar uma arquitetura complexa. A prioridade e permitir que uma planilha pesada da ANATEL seja enviada, processada com seguranca e transformada em um dashboard online rapido e confiavel.
