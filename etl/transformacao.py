import json

# A2 - padronizando a sigla do estado para maiúscula
def padronizar_estado(cliente):
    novo = dict(cliente)
    novo["estado"] = cliente["estado"].upper()
    return novo

# A1 - mantendo o cliente e apenas deixando que o email ausente fique como nulo
def tratar_email(cliente):
    novo = dict(cliente)
    if novo["email"] == "":
        novo["email"] = None
    return novo

# A4 - convertendo o valor total para número com duas casas decimais
def tratar_valor_total(pedido):
    novo = dict(pedido)
    novo["valor_total"] = round(float(str(novo["valor_total"]).replace(",", ".")), 2)
    return novo

# A3 - convertendo a data do pedido para o formato AAAA-MM-DD
def converter_data(pedido):
    novo = dict(pedido)
    data = novo["data_pedido"]
    if "/" in data:
        dia, mes, ano = data.split("/")
        novo["data_pedido"] = f"{ano}-{mes}-{dia}"
    return novo

# A5 - removendo pedidos repetidos pelo id, mantendo a primeira ocorrência
def remover_repetidos(pedidos):
    vistos = set()
    unicos = []
    for pedido in pedidos:
        if pedido["id"] not in vistos:
            unicos.append(pedido)
            vistos.add(pedido["id"])
    return unicos

#A6 - calculando o valor_itend e marca divergente quando a diferença passa de 1 centavo
def calcular_divergencia(pedido):
    novo = dict(pedido)
    soma = 0
    for item in novo["itens"]:
        soma = soma + item["quantidade"] * item["preco_unitario"]
    novo["valor_itens"] = round(soma, 2)
    diferenca = round(abs(novo["valor_total"] - novo["valor_itens"]), 2)
    if diferenca > 0.01:
        novo["divergente"] = 1
    else:
        novo["divergente"] = 0
    return novo


# Juntando as transformações de clientes (ou seja, A1 e A2) e contando as ocorrencias

def transformar_clientes(clientes):
    tratados = []
    emails_nulos = 0
    estados_padronizados = 0
    for cliente in clientes:
        novo = tratar_email(cliente)
        novo = padronizar_estado(novo)
        if novo["email"] is None:
            emails_nulos = emails_nulos + 1
        if novo["estado"] != cliente["estado"]:
            estados_padronizados = estados_padronizados + 1
        tratados.append(novo)
    print(f"transformacao: emails_nulos={emails_nulos} estados_padronizados={estados_padronizados}")
    return tratados

with open("brutos/clientes.json", encoding="utf-8") as arquivo:
    clientes = json.load(arquivo)
clientes_tratados = transformar_clientes(clientes)