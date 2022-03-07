import requests
from bs4 import BeautifulSoup
import re

class Pichau:
    def __init__(self, lista, product):
        self.product = str(product).replace(" ", "-")
        self.lista = lista
    
    def __get_link(self, soup, c, dict_temp):
        link = soup.find_all('a')
        text = str(link[c])
        comeco = text.find('/')
        fim = text.find(">")
        link_final = text[comeco:fim].replace('"', "")
        dict_temp['link'] = f"pichau.com.br{link_final}"


    def __get_name(self, soup, c, dict_temp):
        name = soup.find_all('a')
        text = str(name[c].get_text())
        if "Esgotado" in text:
            text = text.replace("Esgotado", "")
            dict_temp['nome'] = text
            dict_temp['esgotado'] = "Esgotado"
        else:
            if 'de R$' in text:
                lugar = text.find('de R$')
                dict_temp['nome'] = text[:lugar]
            elif 'à vista' in text:
                lugar = text.find('à vista')
                dict_temp['nome'] = text[:lugar]
            else:
                dict_temp['nome'] = text
        
    def __get_price(self, soup, c, dict_temp):
        price = soup.find_all('a')
        text = str(price[c].get_text())
        if "de R$" in text:
            lugar = text.find('R$')
            por = text.find('por:')
            avista = text.find('à vista')
            no = text.find('no PIX')
            desconto = text.find("desconto") + 8
            emate = text.find("em até")
            sem_juros = text.find("sem juros")

            desconto_text = text[no:desconto]
            old_price = text[lugar:por]
            avista_price = text[avista+7:no]
            regular_price = text[desconto:emate]
            emate_text = text[emate:sem_juros]
            sem_juros_text = text[sem_juros:]

            dict_temp['old price'] = f"{old_price}"
            dict_temp['avista'] = f"{avista_price} {desconto_text}"
            dict_temp['regular price'] = f'{regular_price} {emate_text} {sem_juros_text}'
        elif 'à vista' in text:
            lugar = text.find('à vista')
            no = text.find('no PIX')
            desconto = text.find("desconto") + 8
            emate = text.find("em até")
            sem_juros = text.find("sem juros")

            preco1 = text[lugar+7:no]
            desconto_text = text[no:desconto]
            regular_price = text[desconto:emate]
            emate_text = text[emate:sem_juros]
            sem_juros_text = text[sem_juros:]

            dict_temp['avista'] = f"{preco1} {desconto_text}"
            dict_temp['regular price'] = f"{regular_price} {emate_text} {sem_juros_text}"

    def search_product_pichau(self):
        lista = self.lista
        dict_all = {}
        product = self.product
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
                self.__get_link(soup, c, dict_temp)
                self.__get_name(soup, c, dict_temp)
                self.__get_price(soup, c, dict_temp)
                dict_all[c] = dict_temp
                c+=1
            lista.append({"Pichau":dict_all})
            return lista

class Kabum:
    def __init__(self, product):
        self.product = product.replace(" ", "+")
    
    def __get_link(self, result, c):
        links = {}
        while c < 3:
            try:
                text = str(result[c])
                link = re.search('(?=href=).*(?="><i)', text).group().replace('href="', "")
                links[c] = f"https://kabum.com.br{link}"
                c+=1
            except IndexError:
                break
        return links
    
    def __get_name(self, soup, info_dict):
        name = soup.find("h1", itemprop="name")    
        if name != None:
            info_dict['nome'] = name.get_text()

    def __get_price(self, soup, info_dict):
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

    def search_product_kabum(self):
        c = 0
        product = self.product
        url = f'https://www.kabum.com.br/busca?query={product}'

        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        result = soup.find_all("div", class_="productCard")
        empty = soup.find("div", id="listingEmpty")
        if empty == None and site.status_code == 200:
            all_itens = {}
            links = self.__get_link(result=result, c=c)
            i = 0
            for chave, valor in links.items():
                while True: 
                    info_dict = {}
                    info_dict['link'] = valor
                    site = requests.get(valor)
                    soup = BeautifulSoup(site.content, 'html.parser')
                    self.__get_name(soup, info_dict)
                    self.__get_price(soup, info_dict)
                    all_itens[i] = info_dict
                    i+=1
                    break
            return [{"Kabum": all_itens}]
        elif site.status_code != 200:
            return [{"Kabum":"O site da Kabum está com algum problema.\n\n"}]
        else:
            return [{"Kabum":"Não consegui encontrar nada na Kabum =(\n\n"}]