from transformacao import (
    tratar_email, padronizar_estado, converter_data,
    tratar_valor_total, remover_repetidos, calcular_divergencia,
)

# A3 - data no formato DD/MM/AAAA vira AAAA-MM-DD
def test_a3_converte_data_brasileira():
    pedido = {"id": 1, "data_pedido": "19/02/2026"}
    resultado = converter_data(pedido)
    assert resultado["data_pedido"] == "2026-02-19"


# A3 - data que já está em AAAA-MM-DD não muda mais 
def test_a3_mantem_data_ja_no_formato_certo():
    pedido = {"id": 2, "data_pedido": "2026-08-21"}
    resultado = converter_data(pedido)
    assert resultado["data_pedido"] == "2026-08-21"

# A4 - valor em texto com vírgula deve virar número com duas casas
def test_a4_converte_valor_com_virgula():
    pedido = {"id": 1, "valor_total": "125,84"}
    resultado = tratar_valor_total(pedido)
    assert resultado["valor_total"] == 125.84


# A4 - valor que já é número continua igual
def test_a4_mantem_valor_numerico():
    pedido = {"id": 2, "valor_total": 94.34}
    resultado = tratar_valor_total(pedido)
    assert resultado["valor_total"] == 94.34


# A5 - pedido repetido deve aparecer uma vez só, mantendo a primeira ocorrência
def test_a5_remove_pedido_repetido():
    pedidos = [
        {"id": 1, "valor_total": 10},
        {"id": 2, "valor_total": 20},
        {"id": 1, "valor_total": 10},
    ]
    resultado = remover_repetidos(pedidos)
    assert len(resultado) == 2
    assert [p["id"] for p in resultado] == [1, 2]


# A1 - e-mail vazio deve virar nulo, e o cliente continua existindo
def test_a1_email_vazio_vira_nulo():
    cliente = {"id": 3, "email": ""}
    resultado = tratar_email(cliente)
    assert resultado["email"] is None
    assert resultado["id"] == 3


# A2 - estado em minúsculas deve virar maiúsculas
def test_a2_estado_em_maiusculas():
    cliente = {"id": 2, "estado": "mg"}
    resultado = padronizar_estado(cliente)
    assert resultado["estado"] == "MG"


# A6 - pedido 1: itens somam 130.84 e o total informado é 125.84, então é divergente
def test_a6_marca_divergente():
    pedido = {"id": 1, "valor_total": 125.84, "itens": [
        {"produto_id": 2, "quantidade": 3, "preco_unitario": 4.3},
        {"produto_id": 9, "quantidade": 5, "preco_unitario": 15.86},
        {"produto_id": 7, "quantidade": 4, "preco_unitario": 9.66},
    ]}
    resultado = calcular_divergencia(pedido)
    assert resultado["valor_itens"] == 130.84
    assert resultado["divergente"] == 1