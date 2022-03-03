import requests
from bs4 import BeautifulSoup
import re

def search_product_kabum(product):
    c = 0
    product = product.replace(" ", "+")
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
            try:
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
            except:
                return [{"Kabum": 'Ocorreu algum erro e não consegui pesquisar nada'}]
        return [{"Kabum": all_itens}]
    elif site.status_code != 200:
        return [{"Kabum":"O site da Kabum está com algum problema."}]
    else:
        return [{"Kabum":"Não consegui encontrar nada na Kabum =("}]

def search_product_amazon(lista, product):
    product = product.replace(" ", "+")
    i = 2
    count = 0
    error = 0
    dict_append = {}
    url = f'https://www.amazon.com.br/s?k={product}'
    while True:
        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        informations = soup.find_all("div", class_="a-spacing-small")
        if informations != []:
            break
        elif error > 10 and site.status_code != 200:
            return lista.append({"Amazon": "O site da Amazon está com algum problema..."})
        error += 1

    while count < 3:
        if "R$" in informations[i].get_text():
            dict_temp = {}
            texto = str(informations[i].get_text())

            formated = str(informations[i])
            comeco_link = formated.find('href="')
            final_link = formated[comeco_link:].find('"><')
            comeco = formated[comeco_link:]
            completed = comeco[:final_link].replace('href="', "")
            dict_temp['link'] = f"amazon.com.br{completed}"    
            estrelas = texto.find("estrelas")

            cifrao = texto.find("R$")
            virgula = texto[cifrao:].find(",")
            comeco_preco = texto[cifrao:]
            dict_temp['regular price'] = comeco_preco[:virgula+3]
            try:
                parcela_comeco = texto.find("em até")
                if parcela_comeco != -1:
                    parcela_final = texto[parcela_comeco:].find("juros")
                    primeiro = texto[parcela_comeco:]
                    dict_temp['parcela'] = primeiro[:parcela_final+5].rstrip().lstrip()
            except:
                pass
            dict_temp['nome'] = texto[:estrelas-10].rstrip().lstrip()
            avaliacao = texto[estrelas-10: cifrao].rstrip().lstrip()
            if "Economize" in avaliacao:
                economize = avaliacao.find("Economize")
                dict_temp['avaliacao'] = f"{avaliacao[:economize].rstrip().lstrip()} avaliações"
            else:
                dict_temp['avaliacao'] = f"{avaliacao} avaliações"
            dict_append[count] = dict_temp
            count+=1
        i+=1
    lista.append({"Amazon":dict_append})
    return lista
    
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
                        mensagem += f"Parcelas: {value['parcela']}\n\n"
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

def call(product):
    kabum = search_product_kabum(product)
    amazon = search_product_amazon(kabum, product)
    mensagem = retorna_mensagem(amazon)
    return mensagem