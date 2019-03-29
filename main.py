import re
from bot import wppbot

bot = wppbot('Hud')
bot.treina('treino')
bot.inicia('CCTI SISTEMAS - VESP')
bot.saudacao(['BOT: Oi, sou o Robô!','Bot: Use ->Hud<- no início para falar comigo'])
ultimo_texto = ''

while True:

    texto = bot.escuta()

    if texto != ultimo_texto and re.match(r'^Hud', texto):

        ultimo_texto = texto
        texto = texto.replace('Hud', '')
        texto = texto.lower()

        if (texto == 'aprender' or texto == ' aprender' or texto == 'ensinar' or texto == ' ensinar'):
            bot.aprender(texto,'BOT: Escreva a pergunta e após o ? a resposta.','BOT: Obrigado por ensinar! Agora já sei!','BOT: Você escreveu algo errado! Comece novamente..')
        elif (texto == 'noticias' or texto == ' noticias' or texto == 'noticia' or texto == ' noticia' or texto == 'notícias' or texto == ' notícias' or texto == 'notícia' or texto == ' notícia'):
            bot.noticias()
        else:
            bot.responde(texto)