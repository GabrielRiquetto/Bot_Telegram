import requests
from bs4 import BeautifulSoup
import re
from funcsGetInformations import *

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
            while True: 
                info_dict = {}
                info_dict['link'] = valor
                site = requests.get(valor)
                soup = BeautifulSoup(site.content, 'html.parser')
                
                name = soup.find("h1", itemprop="name")    
                if name != None:
                    info_dict['nome'] = name.get_text()

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

def search_product_amazon(lista, product):
    lista = lista
    product = product.replace(" ", "+")
    i = 0
    erro = 0
    count = 0
    dict_append = {}
    url = f'https://www.amazon.com.br/s?k={product}'
    while True:
        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        informations = soup.find_all("div", class_="a-spacing-small")
        if informations != []:
            break
        elif erro == 250:
            break
        erro += 1
    if informations !=[]:
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
    elif site.status_code != 200:
        lista.append({"Amazon":"Amazon está com algum problema..."})
        return lista
    else:
        lista.append({"Amazon":"Ocorreu algum problema comigo!"})
        return lista

def search_product_pichau(lista, product):
    lista = lista
    dict_all = {}
    product = product.replace(" ", "-")
    url = f"https://www.pichau.com.br/search?q={product}"
    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    erro = soup.find("p", class_="MuiTypography-h6")
    if site.status_code != 200:
        lista.append({"Pichau":"Pichau está com algum problema..."})
        return lista
    elif erro:
        erro = erro.get_text()
        lista.append({"Pichau":erro})
        return lista
    else:
        c = 2
        while c < 5:
            dict_temp = {}
            get_link_pichau(soup, c, dict_temp)
            get_name_pichau(soup, c, dict_temp)
            get_price_pichau(soup, c, dict_temp)
            dict_all[c] = dict_temp
            c+=1
        lista.append({"Pichau":dict_all})
        return lista

def return_message(lista):
    mensagem = "Essas foram as informações que eu obtive:\n"
    for index in lista:
        for loja, valor in index.items():
            try:
                mensagem += f"\nLoja: {loja}\n\n"
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
                        mensagem += f"Esse produto está {value['esgotado']}\n\n"
                    except:
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
                mensagem += f"{valor}\n"
    return mensagem


def main(product):
    listaK = search_product_kabum(product)
    listaKA = search_product_amazon(listaK, product)
    listaKAP = search_product_pichau(listaKA, product)
    message = return_message(listaKAP)
    return message