import os
import time
import re
import requests
import json
from chatterbot.trainers import ListTrainer
from chatterbot import ChatBot
from selenium import webdriver

class wppbot:

    dir_path = os.getcwd()

    def __init__(self, nome_bot):
        print(self.dir_path)
        self.bot = ChatBot(nome_bot)
        self.bot.set_trainer(ListTrainer)

        self.chrome = self.dir_path+'\chromedriver'

        self.options = webdriver.ChromeOptions()
        self.options.add_argument(r"user-data-dir="+self.dir_path+"\profile\wpp")
        self.driver = webdriver.Chrome(self.chrome, chrome_options=self.options)

    def inicia(self,CCTISISTEMAS):

        self.driver.get('https://web.whatsapp.com/')
        self.driver.implicitly_wait(15)

        self.caixa_de_pesquisa = self.driver.find_element_by_class_name('jN-F5')


        self.caixa_de_pesquisa.send_keys('CCTI SISTEMAS VESP')
        time.sleep(2)
        print('CCTI SISTEMAS - VESP')
        self.contato = self.driver.find_element_by_xpath('//*[@id="pane-side"]/div/div/div/div[2]/div/div/div'.format('CCTI SISTEMAS - VESP'))
        self.contato.click()
        time.sleep(3)



    def saudacao(self,frase_inicial):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')

        if type(frase_inicial) == list:
            for frase in frase_inicial:
                self.caixa_de_mensagem.send_keys(frase)
                time.sleep(1)
                self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                self.botao_enviar.click()
                time.sleep(1)
        else:
            return False

    def escuta(self):
        post = self.driver.find_elements_by_class_name('_3_7SH')
        ultimo = len(post) - 1
        texto = post[ultimo].find_element_by_css_selector('span.selectable-text').text
        return texto

    def aprender(self,ultimo_texto,frase_inicial,frase_final,frase_erro):
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
        self.caixa_de_mensagem.send_keys(frase_inicial)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()
        self.x = True
        while self.x == True:
            texto = self.escuta()

            if texto != ultimo_texto and re.match(r'^Hud', texto):
                if texto.find('?') != -1:
                    ultimo_texto = texto
                    texto = texto.replace('Hud', '')
                    texto = texto.lower()
                    texto = texto.replace('?', '?*')
                    texto = texto.split('*')
                    novo = []
                    for elemento in texto:
                        elemento = elemento.strip()
                        novo.append(elemento)

                    self.bot.train(novo)
                    self.caixa_de_mensagem.send_keys(frase_final)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
                else:
                    self.caixa_de_mensagem.send_keys(frase_erro)
                    time.sleep(1)
                    self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
                    self.botao_enviar.click()
                    self.x = False
                    return ultimo_texto
            else:
                ultimo_texto = texto

    def noticias(self):

        req = requests.get('https://newsapi.org/v2/top-headlines?sources=globo&pageSize=5&apiKey=f6fdb7cb0f2a497d92dbe719a29b197f')
        noticias = json.loads(req.text)

        for news in noticias['articles']:
            titulo = news['title']
            link = news['url']
            new = 'BOT: ' + titulo + ' ' + link + '\n'

            self.caixa_de_mensagem.send_keys(new)
            time.sleep(1)

    def responde(self,texto):
        response = self.bot.get_response(texto)
        # if float(response.confidence) > 0.5:
        response = str(response)
        response = 'BOT: ' + response
        self.caixa_de_mensagem = self.driver.find_element_by_class_name('_2S1VP')
        self.caixa_de_mensagem.send_keys(response)
        time.sleep(1)
        self.botao_enviar = self.driver.find_element_by_class_name('_35EW6')
        self.botao_enviar.click()

    def treina(self,pastaTreino):
        for treino in os.listdir('pastaTreino'):
            conversas = open('pastaTreino'+'/'+treino , 'r').readlines()
            self.bot.train(conversas)
