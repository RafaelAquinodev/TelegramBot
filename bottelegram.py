import requests
import json
import telebot

CHAVE_API = "6403436648:AAE6jgelEkVqYlEo0ZbrUAwRDaRwUc1ToFk"

bot = telebot.TeleBot(CHAVE_API)

def iniciar (mensagem):
    return True

@bot.message_handler(commands=["start"])
def responder(mensagem):
  bot.reply_to(mensagem, "Olá, seja bem vindo(a), sou um chatbot para ajudar com ferramentas de IA.")
  bot.reply_to(mensagem, "Para funcionar a pesquisa, digite: Preciso de 10 ferramentas para ( o que precisa)")

def verificar(mensagem):
   return True


@bot.message_handler(func=verificar)
def responder(mensagem):
    vazio = ""
    if vazio in mensagem.text:
        mensagem.text.replace(" ", "%20")
        inf = requests.get(
            f"http://searchia.us-east-1.elasticbeanstalk.com/busca/{mensagem.text}")
        inf = inf.json()

    array = []
    for m in inf:
        obj = {
                "relevancia": inf[m]['Relevance'],
                "nomeFerramenta": inf[m]['PositionTitle'],
                # "descricao": inf[m]['Description'],
                "link": inf[m]['PositionPlot'],
            },
        array.append(obj)

    if len(array) < 1:
        bot.reply_to(mensagem, "Não foi possivel processar a sua solicitação, tente novamente")
    else:
        formater = """
                    Aqui estão as ferramentas que podem te ajudar: 
                """
        for indice, value in enumerate(array):
            formater += """
            Nome da ferramenta: {}
            Índice de Relevância da ferramenta: {}
            Link: {}
            """.format(array[indice][0]['nomeFerramenta'],
                            array[indice][0]['relevancia'],
                            array[indice][0]['link'])

        bot.reply_to(mensagem, formater)

bot.polling()


    
