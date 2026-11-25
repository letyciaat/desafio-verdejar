# no ETL Verdejar ele extrai da API e do CSV, transforma (armadilhas A1 a A6) e carrega no SQLite
from extracao import executar_extracao
from transformacao import transformar_clientes, transformar_pedidos
from carga import carregar_tudo

# E - extração
clientes, pedidos, produtos = executar_extracao()

# T - transformação
clientes_tratados = transformar_clientes(clientes)
pedidos_tratados = transformar_pedidos(pedidos)

# L - carga
carregar_tudo(produtos, clientes_tratados, pedidos_tratados)