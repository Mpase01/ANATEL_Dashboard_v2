# Sprint 23 - Dashboard orientado a negocio

## Objetivo

Simplificar a base e a tela para analisar os indicadores de negocio mais importantes, sem expor tecnologias tecnicas como FTTH, Wi-Fi ou Ethernet.

## O que mudou

- A tabela agregada deixou de armazenar `technology`.
- O dashboard passou a trabalhar com `access_medium` simplificado:
  - `Fibra`;
  - `Radio`;
  - `Cabo coaxial`;
  - `Outros`.
- A busca em `Grupo economico` agora mostra uma prestadora especifica quando a empresa esta no grupo generico `OUTROS`.
- A evolucao mensal mostra crescimento em relacao ao periodo anterior.
- A tela ganhou seletor de evolucao por mes ou trimestre.
- O indicador de crescimento no topo passou a representar crescimento LTM.
- O card de assinantes mostra tambem a mistura B2B/B2C.
- A tabela de municipios passou a mostrar:
  - acessos;
  - market share local;
  - acessos em fibra e percentual de fibra;
  - acessos B2B;
  - acessos B2C.

## Validacao

- CSV 2026 lido: 3.222.220 linhas.
- Registros agregados gravados: 731.172.
- Reducao da base agregada: 77,31%.
- Soma total preservada: 280.681.407 acessos.
- Busca por `CLARO`: retorna `TELECOM AMERICAS`.
- Busca por `MHNET`: retorna `Mhnet Telecom`, CNPJ `05245502000104`.
