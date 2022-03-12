from Important.imports import requests, BeautifulSoup, bs4

class Amazon:
    def __init__(self, lista, product):
        self.product = product.replace(" ", "+")
        self.lista = lista

    def __is_working(self):
        erro = 0
        url = f'https://www.amazon.com.br/s?k={self.product}'
        while True:
            site = requests.get(url)
            soup = BeautifulSoup(site.content, 'html.parser')
            informations = soup.find_all("div", class_="a-spacing-small")
            if informations != []:
                return informations
            elif erro == 250 and site.status_code != 200:
                return site.status_code
            elif erro == 250:
                return False
            erro += 1
    
    def __get_link(self, i, informations, dict_temp):
        formated = str(informations[i])
        comeco_link = formated.find('href="')
        final_link = formated[comeco_link:].find('"><')
        comeco = formated[comeco_link:]
        completed = comeco[:final_link].replace('href="', "")
        dict_temp['link'] = f"amazon.com.br{completed}"   
    
    def __get_name(self, estrelas, texto, dict_temp):
        dict_temp['nome'] = texto[:estrelas-10].rstrip().lstrip()

    def __get_price(self, cifrao, texto, dict_temp):
        virgula = texto[cifrao:].find(",")
        comeco_preco = texto[cifrao:]
        dict_temp['regular price'] = comeco_preco[:virgula+3]

    def __get_portion(self, texto, dict_temp):
        try:
            parcela_comeco = texto.find("em até")
            if parcela_comeco != -1:
                parcela_final = texto[parcela_comeco:].find("juros")
                primeiro = texto[parcela_comeco:]
                dict_temp['parcela'] = primeiro[:parcela_final+5].rstrip().lstrip()
        except:
            pass
    
    def __get_evaluation(self, texto, estrelas, cifrao, dict_temp):
        avaliacao = texto[estrelas-10: cifrao].rstrip().lstrip()
        if "Economize" in avaliacao:
            economize = avaliacao.find("Economize")
            dict_temp['avaliacao'] = f"{avaliacao[:economize].rstrip().lstrip()} avaliações"
        else:
            dict_temp['avaliacao'] = f"{avaliacao} avaliações"

    def search_product_amazon(self):
        lista = self.lista
        i = 0
        count = 0
        dict_append = {}
        informations = self.__is_working()
        if type(informations) == bs4.element.ResultSet:
            try:
                while count <= 5:
                    if "R$" in informations[i].get_text():
                        dict_temp = {}
                        texto = str(informations[i].get_text())
                        estrelas = texto.find("estrelas")
                        cifrao = texto.find("R$")
                        
                        self.__get_link(i, informations, dict_temp)
                        self.__get_name(estrelas, texto, dict_temp)
                        self.__get_price(cifrao, texto, dict_temp)
                        self.__get_portion(texto, dict_temp)
                        self.__get_evaluation(texto, estrelas, cifrao, dict_temp)
                        
                        dict_append[count] = dict_temp
                        count+=1
                    i+=1
                lista.append({"Amazon":dict_append})
            except:
                lista.append({"Amazon":"Algo aconteceu com a minha busca na Amazon..."})
            return lista
        elif type(informations) == int:
            lista.append({"Amazon":"Amazon está com algum problema..."})
            return lista
        else:
            lista.append({"Amazon":"Ocorreu algum problema comigo!"})
            return lista