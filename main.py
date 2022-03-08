from Important.imports import telebot
from Important.key import api_key
from Web.searchTop30 import searchTop30
from Web.web import *

bot = telebot.TeleBot(api_key)

#Comandos
@bot.message_handler(commands=["pesquisar"])
def responder(msg):
    mensagem = msg.text.replace("/pesquisar", "").replace(" ", "+").rstrip().lstrip()
    if mensagem.strip() == "":
        bot.reply_to(msg, "Você precisa digitar o nome de um produto para eu pesquisar!")
    else:
        bot.reply_to(msg, "Vou pesquisar e já retorno. Isso pode demorar um pouco...")
        mensagem = msg.text.replace("/pesquisar", "").rstrip().lstrip()
        respostas = main(mensagem)
        for resposta in respostas:
            bot.send_message(msg.chat.id, resposta)
            

@bot.message_handler(commands=["top30"])
def responder(msg):
    bot.reply_to(msg, "Digite a data para eu pesquisar")

@bot.message_handler(commands=["abraco"])
def responder(msg):
    bot.reply_to(msg, "Riquetto te mandou um abraço de volta!")

#Precisa de DEF
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
    texto = f"""Seja bem vindo(a) {msg.from_user.first_name}. Clique em uma das opções a seguir:
/top30 - Buscar pelo top 30 hltv
/abraco - Mandar um abraçao para o Riquetto
/pesquisar - Caso queira pesquisar por preços de um produto específico, basta digitar "/pesquisar produto"
Caso queira pesquisar direto o TOP 30, você pode simplesmente digitar a data.
Qualquer outra opção, não irá funcionar!"""
    bot.reply_to(msg, texto)

bot.polling(timeout=10000)