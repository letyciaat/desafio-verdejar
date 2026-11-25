# ETL Verdejar - Desafio Final

O projeto desenvolvido é uma ETL, funciona tipo uma faxina com mudança: eu pego os dados de clientes e pedidos de uma API local, pego o catálogo de produtos de um arquivo CSV, arrumo a bagunça (seis problemas de qualidade que chamei de armadilhas A1 a A6) e guardo tudo arrumadinho num banco SQLite. No final, ainda faço uma conferência, tipo contar as caixas da mudança pra ver se nada ficou pelo caminho, usando contagens e somas.

## Banco de dados e bibliotecas
- Banco: **SQLite** (caminho C), com o módulo `sqlite3` do Python.
- API consumida com `urllib`, da biblioteca padrão (sem instalação).
- Testes com `pytest`, instalado com `sudo apt install python3-pytest` (no Debian/WSL o `pip` direto no sistema é bloqueado).
- Consultas rodadas com o `sqlite3` de linha de comando: `sudo apt install sqlite3`.

### Motivo do caminho C 
Escolhi o SQLite porque já vinha de brinde o python, não iria precisar montar um servidor.

## Como rodar
1. Ligar a API (deixar o terminal aberto):
   `cd insumos` e `python3 api_verdejar.py`
2. Em outro terminal, na raiz do projeto, rodar o ETL completo:
   `python3 etl/main.py`
3. Rodar os testes: `python3 -m pytest`
4. Rodar as consultas de validação:
   `sqlite3 -header -column verdejar.db < consultas_validacao.sql`

## Estrutura
- `etl/extracao.py`: extração paginada da API, tratamento de erros, leitura do CSV e dados brutos salvos em `brutos/`
- `etl/transformacao.py`: uma função por armadilha (A1 a A6) e os contadores
- `etl/carga.py`: carga no SQLite na ordem das chaves estrangeiras
- `etl/main.py`: roda o ETL completo (E → T → L) e a reconciliação
- `tests/`: testes das armadilhas e teste de reconciliação
- `CONTRATO_DE_DADOS.md`, `COMO_USEI_IA.md`, `consultas_validacao.sql`

## Idempotência
Usei a estratégia de "limpar e recarregar". Antes de cada carga, o ETL apaga as quatro tabelas, começando de trás pra frente por causa das chaves estrangeiras (itens_pedido, pedidos, clientes, produtos), e depois coloca tudo de volta na ordem certa (produtos, clientes, pedidos, itens_pedido). Temos o resultado que não importa se eu rodo uma vez ou dez, o banco sempre termina com as mesmas contagens. Cheguei a pensar em usar o INSERT OR IGNORE, devido uma sugestão da IA, mas descartei, e ele tem o seu mérito, é simples e também evita registros duplicados quando o ETL roda mais de uma vez. Poréem isso ao mesmo tempo é defeito, como só confere se já existe e não atualiza nada, se um registro mudasse na origem o banco ficaria com a versão velha. Por esse motivo, acabei descartando.

Prova: duas execuções seguidas do `python3 etl/main.py` terminam com as mesmas contagens:
`carga: clientes=1000 produtos=12 pedidos=5000 itens=12455`

## Saída do ETL

```
extracao: clientes paginas=10 registros=1000
extracao: pedidos paginas=51 registros_brutos=5100
extracao: produtos registros=12
brutos: arquivos salvos em brutos
transformacao: emails_nulos=81 estados_padronizados=151
transformacao: pedidos_unicos=5000 repetidos_descartados=100
transformacao: datas_convertidas=1037 valores_convertidos=1255
divergentes: 238 pedidos com valor_total diferente da soma dos itens
carga: clientes=1000 produtos=12 pedidos=5000 itens=12455
reconciliacao: soma_valor_itens_origem=311228.75 soma_valor_itens_destino=311228.75 diferenca=0.00
```

## Resultados das consultas de validação
### (a) Total de vendas por mês
Usei `valor_itens` em vez de `valor_total`

A IA sugeriu usar valor_total na soma das vendas, por ser a opção mais comum (o valor informado no pedido). Escolhi colocar valor_itens (a soma calculada a partir dos itens), devido ao fato de que ele é coerente com a reconciliação, que também compara essa coluna entre a origem e o banco, e em 238 pedidos o valor_total informado não bate com a soma dos itens, então preferi usar o valor calculado a partir dos dados de cada item.

| mês | total de vendas |
|---|---|
| 2026-01 | 30355.02 |
| 2026-02 | 33855.86 |
| 2026-03 | 30617.70 |
| 2026-04 | 31170.96 |
| 2026-05 | 30777.02 |
| 2026-06 | 31557.73 |
| 2026-07 | 32685.17 |
| 2026-08 | 29260.04 |
| 2026-09 | 29909.71 |
| 2026-10 | 31039.54 |

Teste de consulta: soma dos meses = **311228.75** = soma geral da tabela = **311228.75** ✅

### (b) Quantidade de pedidos por estado
| estado | pedidos |
|---|---|
| RS | 1543 |
| SC | 1127 |
| PR | 974 |
| SP | 880 |
| MG | 476 |

### (c) Pedidos divergentes
Total: **238 pedidos**. Exemplo: pedido 1, valor_total 125.84 e valor_itens 130.84 (diferença de -5.00). A lista completa sai rodando o `consultas_validacao.sql`.

Observação: Aqui foi por pouco, mas achei esquisito realmente, o pedido 81 tem valor_total negativo (-1.84), e eu tô é devendo a loja é (risos). Isso não estava entre as armadilhas declaradas, então o ETL manteve o valor do jeito que veio da API, sem mexer. Mas deixei registrado aqui, pode ser que seja erro meu.

## Testes

```
============================= test session starts ==============================
platform linux -- Python 3.13.5, pytest-8.3.5, pluggy-1.5.0
rootdir: /home/letycia/desafio-final-mletycia
configfile: pytest.ini
testpaths: tests
collected 9 items

tests/test_reconciliacao.py .                                            [ 11%]
tests/test_transformacao.py ........                                     [100%]

============================== 9 passed in 0.05s ===============================
```