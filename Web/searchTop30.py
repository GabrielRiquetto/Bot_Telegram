from Important.imports import *
from Web.data import *

def searchTop30(data):
    countPNP = 0
    countPlayers = 0
    countZero = 0
    date = data
    dia = date[:2]
    mes = date[3:5]
    ano = date[6:10]
    mes = transformDate(dia, mes ,ano)
    if mes == False:
        return "Você colocou uma data inválida ou não é Segunda-Feira"

    url = f'https://www.hltv.org/ranking/teams/{ano}/{mes}/{dia}'

    site = requests.get(url)
    soup = BeautifulSoup(site.content, 'html.parser')
    error = soup.find("div", class_="error-desc")
    if error == None:
        position = soup.find_all("span", class_="position")
        name = soup.find_all("span", class_="name")
        points = soup.find_all("span", class_="points")
        rankingNicknames = soup.find_all("div", class_="rankingNicknames")
        listaTeams = []

        while True:
            try:
                posicao = str(position[countPNP]).replace('<span class="position">', "").replace("</span>", "")
                nome = str(name[countPNP]).replace('<span class="name">', "").replace("</span>", "")
                pontos = str(points[countPNP]).replace('<span class="points">', "").replace("</span>", "")
                dict = {nome:[]}
                dict[nome].append(posicao)
                dict[nome].append(nome)
                dict[nome].append(pontos)
                while True:
                    if countZero == 5:
                        countZero = 0
                        break
                    elif countZero == 4:
                        listaTeams.append(dict)
                    playerTeam = str(rankingNicknames[countPlayers]).replace('<div class="rankingNicknames"><span>', "").replace("</span></div>", "")
                    dict[nome].append(playerTeam)
                    countPlayers +=1
                    countZero += 1
            except:
                break
            countPNP +=1
        total = len(listaTeams)
        c = 0
        text = ""
        linha = "_____________________________\n"
        while c < total:
            for chave in listaTeams[c].items():
                text += linha
                text += f"Posição: {chave[1][0]}\n"
                text += f"Time: {chave[1][1]}\n"
                text += f"Pontos: {chave[1][2]}\n"
                text += "Jogadores:\n"
                text += f"{chave[1][3]}\n"
                text += f"{chave[1][4]}\n"
                text += f"{chave[1][5]}\n"
                text += f"{chave[1][6]}\n"
                text += f"{chave[1][7]}\n"
            c+=1
        return text
    else:
        return "O site não está atualizado para eu pegar as informações dessa data, não consegui trazer a lista por culpa disso, desculpe!"
    