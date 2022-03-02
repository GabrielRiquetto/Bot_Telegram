import telebot
import re
from BeautSoup import searchTop30
from random import randint
from web import searchProduct
apiKey = "5184551074:AAG5MjlyPGGueIfRNjBlQUvVMoRe63j-Jnk"

bot = telebot.TeleBot(apiKey)

#Comandos
@bot.message_handler(commands=["pesquisar"])
def responder(msg):
    mensagem = msg.text.replace("/pesquisar", "").replace(" ", "+").rstrip().lstrip()
    if mensagem.strip() == "":
        bot.reply_to(msg, "Você precisa digitar o nome de um produto para eu pesquisar!")
    else:
        bot.reply_to(msg, "Vou pesquisar e já retorno. Isso pode demorar um pouco...")
        resposta = searchProduct(mensagem)
        tamanho = len(resposta)
        mensagem = "Essas foram as informações que eu consegui, espero ajudar em algo:\n\n"
        c = 0
        while True:
            if tamanho == 0:
                mensagem = "Ocorreu um erro e não consegui obter nenhum resultado, desculpe..."
                break
            else:
                try:
                    mensagem += f"Produto: {resposta[c]['produto']}\n"
                    mensagem += f"Avaliação: {resposta[c]['avaliacao']}\n"
                    mensagem += f"Valor: {resposta[c]['valor']}\n"
                    mensagem += f"Vendedor: {resposta[c]['vendedor']}\n"
                    mensagem += f"Link: {resposta[c]['link']}\n"
                    mensagem += "_"*48+"\n"
                    c+=1
                except:
                    break
        bot.send_message(msg.chat.id, mensagem)

@bot.message_handler(commands=["top30"])
def responder(msg):
    bot.reply_to(msg, "Digite a data para eu pesquisar")

@bot.message_handler(commands=["abraco"])
def responder(msg):
    bot.reply_to(msg, "Riquetto te mandou um abraço de volta!")

@bot.message_handler(commands=["casada"])
def responder(msg):
    num = randint(0, 1000)
    if num < 250:
        bot.reply_to(msg, f"Ta fraquinho(a) hoje em {msg.from_user.first_name}, comeu {num}")
    elif num < 750:
        bot.reply_to(msg, f"Ta na média hoje em {msg.from_user.first_name}, comeu {num}")
    else:
        bot.reply_to(msg, f"KOROI {msg.from_user.first_name.upper()} TA COMEDOR DE CASADAS HOJE HEIN, COMEU {num}")

#Precisa de DEF
def isGay(msg):
    if "gay" in msg.text.lower():
        return True
    else:
        return False

@bot.message_handler(func=isGay)
def responder(msg):
    bot.reply_to(msg, "GAY É O TEU PAI SEU CORNO.")


def isDate(msg):
    if re.search("(?=(\d{2}\/\d{2}\/\d{4}))", msg.text):
        return True
    else:
        return False

@bot.message_handler(func=isDate)
def responder(msg):
    bot.send_message(msg.chat.id, "Vou pesquisar e já te retorno!")
    response = searchTop30(msg.text)
    bot.send_message(msg.chat.id, response)
    

def verify(msg):
    return True

@bot.message_handler(func=verify)
def responder(msg):
    texto = """Seja bem vindo(a). Clique em uma das opções a seguir:
/top30 - Buscar pelo top 30 hltv
/abraco - Mandar um abraçao para o Riquetto
/casada - Quantas casadas você comeu hoje?
/pesquisar - Caso queira pesquisar por preços de um produto específico, basta digitar "/pesquisar produto"
Caso queira pesquisar direto o TOP 30, você pode simplesmente digitar a data.
Qualquer outra opção, não irá funcionar!"""
    bot.reply_to(msg, texto)

bot.polling(timeout=10000)