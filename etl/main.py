# no ETL Verdejar ele extrai da API e do CSV, transforma (armadilhas A1 a A6) e carrega no SQLite
from extracao import executar_extracao
from transformacao import transformar_clientes, transformar_pedidos
from carga import carregar_tudo
import sqlite3

# E - extração
clientes, pedidos, produtos = executar_extracao()


# Proteção em caso de: extração falhou (ex.: API desligada), não segue para a carga,
# porque a estratégia "limpar e recarregar" apagaria o banco
if not clientes or not pedidos:
    print("erro: extração vazia (a API está ligada?); carga cancelada para não apagar o banco")
    raise SystemExit(1)

# T - transformação
clientes_tratados = transformar_clientes(clientes)
pedidos_tratados = transformar_pedidos(pedidos)

# L - carga
carregar_tudo(produtos, clientes_tratados, pedidos_tratados)


# Reconciliação - compara a soma de valor_itens da origem com a do banco
soma_origem = round(sum(p["valor_itens"] for p in pedidos_tratados), 2)
conexao = sqlite3.connect("verdejar.db")
soma_destino = round(conexao.execute("SELECT SUM(valor_itens) FROM pedidos").fetchone()[0], 2)
conexao.close()
print(f"reconciliacao: soma_valor_itens_origem={soma_origem:.2f} soma_valor_itens_destino={soma_destino:.2f} diferenca={abs(soma_origem - soma_destino):.2f}")