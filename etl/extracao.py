# 1 - importando bibliotecas 
import urllib.request
import json

# 2 - montando endereço da página 1 de clientes
endereco = "http://127.0.0.1:8000/clientes?page=1&page_size=100"

# 3 - pedindo o endereço para a API:
resposta = urllib.request.urlopen(endereco)

#4 - lendo a resposta e transformando em dicionário
texto = resposta.read().decode("utf-8")
dados = json.loads(texto)

#5 - guardando o total de páginas
total_paginas = dados ["total_pages"]

# 6 - criando uma lisra vazia para guardar clientes
clientes = []

# 7 - percorrendo todas as páginas
for pagina in range (1, total_paginas + 1):

    # 7.1 - montando o endereço da página
    endereco_pagina = f"http://127.0.0.1:8000/clientes?page={pagina}&page_size=100"

    # 7.2 - buscando cada página oficial
    resposta_pagina = urllib.request.urlopen(endereco_pagina)
    texto_pagina = resposta_pagina.read().decode("utf-8")
    dados_pagina = json.loads(texto_pagina)

    # 7.3 - juntando os clientes da página na lista
    clientes.extend(dados_pagina["items"])

# 8 - mostrando os clientes extraídos
print(len(clientes))


