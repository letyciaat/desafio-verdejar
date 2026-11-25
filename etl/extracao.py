# 1 - importando bibliotecas 
import urllib.request
import json
import urllib.error
import csv

# 2 - fazendo uma função que busque uma página API, onde ela confere o status e trata erros 
def buscar_pagina(endereco):
    try:
        resposta = urllib.request.urlopen(endereco)
        if resposta.status != 200:
            print(f"error: status {resposta.status} em {endereco}")
            return None
        texto = resposta.read().decode("utf-8")
        return json.loads(texto)
    except urllib.error.HTTPError as erro:
        print(f"erro: a API respondeu com status {erro.code} em {endereco}")
        return None
    except urllib.error.URLError:
        print(f"error: não foi possível conectar a API na rota{endereco}")
        return None

# 3 - função que percorre todas as páginas de uma rota;
def extrair(rota):

    # 3.1 - montando endereço da página 1 de clientes
    endereco = f"http://127.0.0.1:8000/{rota}?page=1&page_size=100"

    # 3.2 - pedindo a página 1 com o tratamento de erro
    dados = buscar_pagina(endereco)
    if dados is None:
        return []

    #3.3 - guardando o total de páginas
    total_paginas = dados ["total_pages"]

    #3.4 - criando uma lisra vazia para guardar clientes
    registros = []

    #3.5 - percorrendo todas as páginas
    for pagina in range (1, total_paginas + 1):

        # 3.5.1 - montando o endereço da página
        endereco_pagina = f"http://127.0.0.1:8000/{rota}?page={pagina}&page_size=100"

        # 3.5.2 - buscando cada página oficial
        dados_pagina = buscar_pagina(endereco_pagina)
        if dados_pagina is None:
            break

        # 3.5.3 - juntando os clientes da página na lista
        registros.extend(dados_pagina["items"])
    return registros

# 4 - criando uma função que lê o catálogo de produtos CSV
def ler_produtos():
    with open ("insumos/dados/produtos.csv", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)
    return linhas

# 5 - extraindo clientes, pedidos/produtos e mostrando a quantidade
clientes = extrair("clientes")
print(len(clientes))

pedidos = extrair("pedidos")
print(len(pedidos))

produtos = ler_produtos()
print(len(produtos))

