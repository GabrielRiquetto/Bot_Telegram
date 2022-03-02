import requests
from bs4 import BeautifulSoup
import re

def searchProduct(product):
    c = 0
    url = f'https://www.google.com/search?q={product}&tbm=shop'

    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    results = soup.find_all("div", class_="P8xhZc")
    lista_final = []
    while c < 1:
        temp_dict = {}
        try:
            result1 = results[c]
            resultStr = str(results[2].get_text())
            print(result1)
            try:
                estrela = resultStr.find("★")
                if estrela != -1:
                    produto = resultStr[:estrela]
                else:
                    cifrao = resultStr.find("R$")
                    produto = resultStr[:cifrao]
            except:
                produto = "Ocorreu um erro ao pegar o nome do produto"
            temp_dict["produto"] = produto
            try:
                link = re.search('(?=http).+?(?=">)', str(result1)).group()
            except:
                link = "Não consegui consultar o link"
            temp_dict["link"] = link
            try:
                avaliacao = re.search('(?=aria-label=").+(?=stars)', str(result1)).group()
                avaliacao = avaliacao.replace('aria-label="', "") + "estrelas"
            except:
                avaliacao = "Não consegui consultar a avaliação"
            temp_dict["avaliacao"] = avaliacao
            
            teste = resultStr
            cifrao = teste.find("R$")
            splitado = teste[cifrao:].split(" ")
            print(splitado)
            valor = splitado[0]
            temp_dict["valor"] = valor

            vendedor = teste[cifrao:].split("de")
            print(vendedor)
            try:
                vendedor = f"{vendedor[1].strip()} {vendedor[2].strip()}"
            except IndexError:
                try:
                    vendedor = vendedor[1].strip()
                except:
                    vendedor = "Não consegui consultar o vendedor, desculpe!"
            temp_dict["vendedor"] = vendedor
            lista_final.append(temp_dict)
            c+=1
        except:
            break
    tamanho = len(lista_final)
    mensagem = "Essas foram as informações que eu consegui, espero ajudar em algo:\n\n"
    c = 0
    while True:
        if tamanho == 0:
            mensagem = "Ocorreu um erro e não consegui obter nenhum resultado, desculpe..."
            break
        else:
            try:
                mensagem += f"Produto: {lista_final[c]['produto']}\n"
                mensagem += f"Avaliação: {lista_final[c]['avaliacao']}\n"
                mensagem += f"Valor: {lista_final[c]['valor']}\n"
                mensagem += f"Vendedor: {lista_final[c]['vendedor']}\n"
                mensagem += f"Link: {lista_final[c]['link']}\n"
                mensagem += "_"*48+"\n"
                c+=1
            except:
                break
    return mensagem