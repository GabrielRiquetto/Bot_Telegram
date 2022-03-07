from Libraries.imports import *
from Classes.ClassPichau import Pichau
from Classes.ClassKabum import Kabum

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
    listaK = Kabum(product).search_product_kabum()
    listaKA = search_product_amazon(listaK, product)
    listaKAP = Pichau(listaKA, product).search_product_pichau()
    message = return_message(listaKAP)
    return message