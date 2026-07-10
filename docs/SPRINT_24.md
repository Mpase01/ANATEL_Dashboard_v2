# Sprint 24 - Ranking e leitura por estado

## Entrega

- A tabela de municipios passou a exibir os dados agrupados por estado.
- Cada estado mostra um resumo com acessos, participacao no estado, ranking estadual, fibra percentual, B2B e B2C.
- Cada cidade mostra ranking por acessos, participacao local, fibra percentual, B2B e B2C.
- A coluna de fibra deixou de mostrar o total bruto e passou a mostrar somente o percentual.

## Criterio de ranking

- Na visao de grupo economico, o ranking compara grupos economicos no mesmo municipio ou estado.
- Na visao de prestadora/CNPJ, o ranking compara prestadoras no mesmo municipio ou estado.
- O ranking sempre usa quantidade de acessos no periodo mais recente do recorte selecionado.

## Validacao

- Consulta de municipios do grupo TELECOM AMERICAS retornou ranking municipal e estadual.
- Consulta de municipios da prestadora Mhnet retornou ranking municipal e estadual.
- Backend compilado com sucesso.
- JavaScript da tela validado sem erro de sintaxe.
