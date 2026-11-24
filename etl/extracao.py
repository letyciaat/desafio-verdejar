# 1 - importando bibliotecas 
import urllib.request
import json

# 2 - montando endereço da página 1 de clientes
endereco = "http://127.0.0.1:8000/clientes?page=1&page_size=3"

# 3 - pedindo o endereço para a API:
resposta = urllib.request.urlopen(endereco)

#4 - lendo a resposta e transformando em dicionário
texto = resposta.read().decode("utf-8")
dados = json.loads(texto)

#5 - mostrando o total de páginas
print(dados["total_pages"])