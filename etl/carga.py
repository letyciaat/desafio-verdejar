import sqlite3

# 1 - abrindo o banco, ligando as chaves estrageiras e cria tabelas (no caso daquelas que ainda não existem)
def abrir_banco():
    conexao = sqlite3.connect("verdejar.db")
    conexao.execute("PRAGMA foreign_keys = ON")
    with open("insumos/schema_sqlite.sql", encoding="utf-8") as arquivo:
        conexao.executescript(arquivo.read())
    return conexao

# 2 - usando da idempotência: ela apaga os dados antigos antes de carregar de novo
def limpar_tabelas(conexao):
    conexao.execute("DELETE FROM itens_pedido")
    conexao.execute("DELETE FROM pedidos")
    conexao.execute("DELETE FROM clientes")
    conexao.execute("DELETE FROM produtos")

# 3 - grava os produtos, convertendo os textos do CSV em números de acordo com o contrato
def carregar_produtos(conexao, produtos):
    for produto in produtos:
        conexao.execute(
            "INSERT INTO produtos (produto_id, nome, categoria, preco_base) VALUES (?,?,?,?)",
            (int(produto["produto_id"]), produto["nome"], produto["categoria"], round(float(produto["preco_base"]), 2)),

        )
# 4 - grava os clientes (já tratados lá na transformação, A1 e A2)
def carregar_clientes(conexao, clientes):
    for cliente in clientes:
        conexao.execute(
            "INSERT INTO clientes (id, nome, email, cidade, estado, cadastro_em) VALUES (?, ?, ?, ?, ?, ?)",
            (cliente["id"], cliente["nome"], cliente["email"], cliente["cidade"], cliente["estado"], cliente["cadastro_em"]),
        )

# 5 - gravando os pedidos (já tratados A3, A4, A5 e A6)
def carregar_pedidos(conexao, pedidos):
    for pedido in pedidos:
        conexao.execute(
            "INSERT INTO pedidos (id, cliente_id, data_pedido, status, valor_total, valor_itens, divergente) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pedido["id"], pedido["cliente_id"], pedido["data_pedido"], pedido["status"], pedido["valor_total"], pedido["valor_itens"], pedido["divergente"]),
        )
#6 - gravando itens, em que cada item vira uma linha, com o id do pedido "original" e a posição linha começando em 1
def carregar_itens(conexao, pedidos):
    for pedido in pedidos:
        for linha, item in enumerate(pedido["itens"], start=1):
            conexao.execute(
                "INSERT INTO itens_pedido (pedido_id, linha, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?, ?)",
                (pedido["id"], linha, item["produto_id"], item["quantidade"], round(item["preco_unitario"], 2)),
            )

# 7 - agora a carga completa, abre, limpa, carrega na ordem das chaves, confere as contagens e confirma
def carregar_tudo(produtos, clientes, pedidos):
    conexao = abrir_banco()
    limpar_tabelas(conexao)
    carregar_produtos(conexao, produtos)
    carregar_clientes(conexao, clientes)
    carregar_pedidos(conexao, pedidos)
    carregar_itens(conexao, pedidos)
    conexao.commit()

    contagens = {}
    for tabela in ["clientes", "produtos", "pedidos", "itens_pedido"]:
        contagens[tabela] = conexao.execute(f"SELECT COUNT(*) FROM {tabela}").fetchone()[0]
    print(f"carga: clientes={contagens['clientes']} produtos={contagens['produtos']} pedidos={contagens['pedidos']} itens={contagens['itens_pedido']}")

    conexao.close()