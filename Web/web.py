from Important.imports import *
from Classes.ClassPichau import Pichau
from Classes.ClassAmazon import Amazon

def return_message(lista):
    mensagens = []
    mensagem = "Essas foram as informações que eu obtive:\n"
    for index in lista:
        for loja, valor in index.items():
            try:
                mensagem = ""
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
            mensagens.append(mensagem)
    return mensagens

def main(product):
    listaK = []
    listaKA = Amazon(listaK, product).search_product_amazon()
    listaKAP = Pichau(listaKA, product).search_product_pichau()
    message = return_message(listaKAP)
    return message