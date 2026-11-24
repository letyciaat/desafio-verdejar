# 1 - importando bibliotecas 
import urllib.request
import json
import urllib.error

def extrair(rota):

    # 2 - montando endereço da página 1 de clientes
    endereco = f"http://127.0.0.1:8000/{rota}?page=1&page_size=100"

    # 3 - pedindo o endereço para a API, trazendo o tratamento de erro
    try:
        resposta = urllib.request.urlopen(endereco)
    except urllib.error.URLError:
        print(f"error: não foi possível conectar a API na rota{rota}")
        return []

    #4 - lendo a resposta e transformando em dicionário
    texto = resposta.read().decode("utf-8")
    dados = json.loads(texto)

    #5 - guardando o total de páginas
    total_paginas = dados ["total_pages"]

    # 6 - criando uma lisra vazia para guardar clientes
    registros = []

    # 7 - percorrendo todas as páginas
    for pagina in range (1, total_paginas + 1):

        # 7.1 - montando o endereço da página
        endereco_pagina = f"http://127.0.0.1:8000/{rota}?page={pagina}&page_size=100"

        # 7.2 - buscando cada página oficial
        resposta_pagina = urllib.request.urlopen(endereco_pagina)
        texto_pagina = resposta_pagina.read().decode("utf-8")
        dados_pagina = json.loads(texto_pagina)

        # 7.3 - juntando os clientes da página na lista
        registros.extend(dados_pagina["items"])
    return registros

# 8 - extraindo clientes e pedindo/mostrando a quantidade
clientes = extrair("clientes")
print(len(clientes))

pedidos = extrair("pedidos")
print(len(pedidos))



