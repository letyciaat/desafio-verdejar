# Contrato de dados - ETL VERDEJAR 

Nesse documento, estamos definindo: que para cada tabela de destino, os campos, o tipo, se é nulo e também a regra de transformação aplicada pelo ETL.


## Tabela clientes
Origem: API, rota /clientes

| Campo | Tipo | Admite nulo? | Regra de transformação |
|---|---|---|---|
| id | inteiro | não | mantém como veio da API (identificador único) |
| nome | texto | não | mantém como veio da API |
| email | texto | sim | A1: se vier vazio, gravar como nulo; contar quantos |
| cidade | texto | não | mantém como veio da API |
| estado | texto (2 letras) | não | A2: converter para maiúscula e contar quantos foram corrigidos |
| cadastro_em | data (texto AAAA-MM-DD) | não | mantém como veio da API (formato já certo) |


## Tabela produtos
Origem: Arquivo CSV (insumos/dados/produtos.csv)

| Campo | Tipo | Admite nulo? | Regra de transformação |
|---|---|---|---|
| produto_id | inteiro | não | Converte texto para inteiro (identificador único) |
| nome | texto | não | Mantém como veio do CSV |
| categoria | texto | não | Mantém como veio do CSV |
| preco_base | decimal | não | Converte texto para decimal com até duas casas |

## Tabela pedidos
Origem: API, rota /pedidos.

Regra da tabela - A5: remover pedidos repetidos pelo id, mantendo a primeira vez, contar quantos foram descartados.

| Campo | Tipo | Admite nulo? | Regra de transformação |
|---|---|---|---|
| id | inteiro | não | mantém como veio da API (identificador único) |
| cliente_id | inteiro | não | Mantém como veio na API (por ser chave estrangeira, deve existir na tabela clientes) |
| data_pedido | data (texto AAAA-MM-DD) | não | A3: Converter os dois formatos para AAAA-MM-DD |
| status | texto | não | Mantém como está na API |
| valor_total | decimal | não | A4: Converter tudo para decimal com duas casas |
| valor_itens | decimal | não | A6: Devido ao calculo do ETL, somando qtde x preço unitario de todos os itens do pedido, com duas casas decimais |
| divergente | inteiro | não | A6: Aqui compara valores entre valor_total e valor_itens, se maior que 0,01 = 1 (divergente), se diferença ate 0,01 (não divergente), contar quantos ficaram com 1 |


## Tabela itens_pedido
Origem: API, rota /pedidos (lista "itens" dentro de cada pedido)

Regra da tabela - A5: os itens são gerados só a partir dos pedidos únicos (depois de remover os repetidos), os itens dos pedidos repetidos também não entram em dobro.

| Campo | Tipo | Admite nulo? | Regra de transformação |
|---|---|---|---|
| pedido_id | inteiro | não | colocar pelo ETL com o id do pedido que contém o item (chave estrangeira, deve existir na tabela pedidos) |
| linha | inteiro | não | feito pelo ETL, nº de ordem do item dentro do pedido, começa em 1 e recomeça em cada pedido |
| produto_id | inteiro | não | mantém como veio na API (chave estrangeira, deve ter na tabela produtos) |
| quantidade | inteiro | não | mantém como veio na API |
| preco_unitario | decimal | não | mantém como veio na API, com duas casas decimais |