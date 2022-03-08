from Important.imports import requests, BeautifulSoup, re

class Kabum:
    def __init__(self, product):
        self.product = product.replace(" ", "+")
    
    def __get_link(self, result):
        links = {}
        c = 0
        while c <= 5:
            try:
                text = str(result[c])
                link = re.search('(?=(href=)).*(?="><i)', text).group().replace('href="', "")
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
        product = self.product
        url = f'https://www.kabum.com.br/busca?query={product}'

        site = requests.get(url)
        soup = BeautifulSoup(site.content, 'html.parser')
        result = soup.find_all("div", class_="productCard")
        empty = soup.find("div", id="listingEmpty")
        if empty == None and site.status_code == 200:
            all_itens = {}
            links = self.__get_link(result=result)
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
