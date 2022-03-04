import requests
from bs4 import BeautifulSoup
import re
from time import sleep
def search_product_kabum(product):
    c = 0
    product = product.replace(" ", "+")
    print(product)
    url = f'https://www.kabum.com.br/busca?query={product}'

    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    result = soup.find_all("div", class_="productCard")
    empty = soup.find("div", id="listingEmpty")
    if empty == None and site.status_code == 200:
        all_itens = {}
        links = {}
        while c < 3:
            try:
                text = str(result[c])
                link = re.search('(?=href=).*(?="><i)', text).group().replace('href="', "")
                links[c] = f"https://kabum.com.br{link}"
                c+=1
            except IndexError:
                break
        i = 0
        for chave, valor in links.items():
            while True: 
                info_dict = {}
                info_dict['link'] = valor
                site = requests.get(valor)
                soup = BeautifulSoup(site.content, 'html.parser')

                info_dict['nome'] = soup.find("h1", itemprop="name").get_text()    

                old_price = soup.find("span", class_="oldPrice")
                if old_price != None:
                    info_dict["old price"] = old_price.get_text()
                
                avista = soup.find("h4", "finalPrice")
                if avista != None:
                    info_dict['avista'] = avista.get_text()
                
                price = soup.find("b", "regularPrice")
                if price != None:
                    info_dict['regular price'] = price.get_text()
                else:
                    try:    
                        info_dict['regular price'] = avista.get_text()
                    except AttributeError:
                        info_dict['regular price'] = "Não há estoque desse produto!"
                all_itens[i] = info_dict
                i+=1
                break
        return [{"Kabum": all_itens}]
    elif site.status_code != 200:
        return [{"Kabum":"O site da Kabum está com algum problema.\n\n"}]
    else:
        return [{"Kabum":"Não consegui encontrar nada na Kabum =(\n\n"}]

def retorna_mensagem(lista):
    mensagem = "Essas foram as informações que eu obtive:\n\n"
    for index in lista:
        for loja, valor in index.items():
            try:
                mensagem += f"Loja: {loja}\n"
                for chave, value in valor.items():
                    try:
                        mensagem += f"Produto: {value['nome']}\n\n"
                    except KeyError:
                        mensagem += f"Produto: Não consegui obter o nome do produto =(\n\n"
                    try:
                        mensagem += f"Avaliação: {value['avaliacao']}\n\n"
                    except:
                        pass
                    try:
                        mensagem += f"Preço antigo: {value['old price']}\n\n"
                    except KeyError:
                        pass
                    try:
                        mensagem += f"Preço a vista: {value['avista']}\n\n"
                    except KeyError:
                        pass
                    try:
                        if value['regular price'] != "Não há estoque desse produto!":
                            mensagem += f"Preço: {value['regular price']}\n\n"
                        else:
                            mensagem += f"{value['regular price']}\n\n"
                    except KeyError:
                        mensagem += "Não consegui pegar o preço do produto\n\n"
                    try:
                        mensagem += f"Parcela: {value['parcela']}\n\n"
                    except:
                        pass
                    try:
                        mensagem += f"Caso tenha te interessado, aqui está o link:\n{value['link']}\n"
                    except KeyError:
                        mensagem += f"Não consegui pegar o link, desculpe!\n"
                    mensagem += "_" * 50 + "\n"
            except:
                mensagem += f" {valor}"
    return mensagem