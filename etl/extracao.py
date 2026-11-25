# 1 - importando bibliotecas 
import urllib.request
import json
import urllib.error
import csv
import os

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

    # 3.1 - montando endereço da página 1 de registros
    endereco = f"http://127.0.0.1:8000/{rota}?page=1&page_size=100"

    # 3.2 - pedindo a página 1 com o tratamento de erro
    dados = buscar_pagina(endereco)
    if dados is None:
        return [], 0

    #3.3 - guardando o total de páginas
    total_paginas = dados ["total_pages"]

    #3.4 - criando uma lisra vazia para guardar registros
    registros = []

    #3.5 - percorrendo todas as páginas
    for pagina in range (1, total_paginas + 1):

        # 3.5.1 - montando o endereço da página
        endereco_pagina = f"http://127.0.0.1:8000/{rota}?page={pagina}&page_size=100"

        # 3.5.2 - buscando cada página oficial
        dados_pagina = buscar_pagina(endereco_pagina)
        if dados_pagina is None:
            break

        # 3.5.3 - juntando os registros da página na lista
        registros.extend(dados_pagina["items"])
    return registros, total_paginas

# 4 - criando uma função que lê o catálogo de produtos CSV
def ler_produtos():
    with open ("insumos/dados/produtos.csv", encoding="utf-8") as arquivo:
        leitor = csv.DictReader(arquivo)
        linhas = list(leitor)
    return linhas

# 5 - extraindo clientes, pedidos/produtos e mostrando a quantidade
clientes, paginas_clientes = extrair("clientes")
print(f"extracao: clientes paginas={paginas_clientes} registros={len(clientes)}")

pedidos, paginas_pedidos = extrair("pedidos")
print(f"extracao: pedidos paginas={paginas_pedidos} registros_brutos={len(pedidos)}")

produtos = ler_produtos()
print(f"extracao: produtos registros={len(produtos)}")

#6 - salvando os dados brutos, antes mesmo de fazer alguma transformação
os.makedirs("brutos", exist_ok=True)

with open("brutos/clientes.json", "w", encoding="utf-8") as arquivo:
    json.dump(clientes, arquivo, ensure_ascii=False, indent=4)

with open("brutos/pedidos.json", "w", encoding="utf-8") as arquivo:
    json.dump(pedidos, arquivo, ensure_ascii=False, indent=4)

print("brutos: arquivos salvos em brutos")
