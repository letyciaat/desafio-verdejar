import json
import sqlite3

from transformacao import transformar_pedidos


# Para a reconciliação, se compara a origem (brutos tratados) com o destino (banco)
def test_reconciliacao_pedidos_e_soma_valor_itens():

    # origem - pedidos brutos passando pela transformação (A3 a A6)
    with open("brutos/pedidos.json", encoding="utf-8") as arquivo:
        pedidos_brutos = json.load(arquivo)
    pedidos_origem = transformar_pedidos(pedidos_brutos)
    soma_origem = round(sum(p["valor_itens"] for p in pedidos_origem), 2)

    # destino - o que está gravado no banco
    conexao = sqlite3.connect("verdejar.db")
    quantidade_destino = conexao.execute("SELECT COUNT(*) FROM pedidos").fetchone()[0]
    soma_destino = conexao.execute("SELECT SUM(valor_itens) FROM pedidos").fetchone()[0]
    conexao.close()

    # as duas comparações
    assert len(pedidos_origem) == quantidade_destino
    assert abs(soma_origem - soma_destino) <= 0.01