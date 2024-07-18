from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
from email.message import EmailMessage


class Previsao:

    def __init__(self) -> None:
        self.agora = datetime.datetime.now()
        self.data_hora_atual = self.agora.strftime('%d/%m - %H:%M')
        self.chuva = ''
        self.lista_data = []
        self.lista_temp_max = []
        self.lista_temp_min = []
        self.lista_condicoes = []
        self.lista_pronta = {}

    def coleta_chuva(self):

        url = 'https://www.climatempo.com.br/previsao-do-tempo/cidade/558/saopaulo-sp'
        page = requests.get(url, verify=False)
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')

        chuva = soup.find_all('span', {'class': '_margin-l-5'})

        try:
            for i in chuva:
                if i.text != '-' and i.text != '':
                    i = i.text
                    i = i.split('-')
                    i = f'{i[0].strip()} - {i[1].strip()}'
                    self.chuva = i
        except:
            pass

    def coleta_previsao_do_tempo(self):

        Previsao.coleta_chuva(self)

        url = 'https://www.climatempo.com.br/previsao-do-tempo/15-dias/cidade/558/saopaulo-sp'
        page = requests.get(url, verify=False)
        resposta = page.text
        soup = BeautifulSoup(resposta, 'html.parser')

        data = soup.find_all('div', {'class': 'date-inside-circle'})
        temp_min = soup.find_all('div', {'class': '_flex _margin-b-10'})
        temp_max = soup.find_all('span', {'class': '-gray'})
        condicao_tempo = soup.find_all(
            'p', {'class': '-gray -line-height-22 _margin-t-sm-20'})

        try:
            for i in data:
                i = i.text
                i = i.strip()
                i = i.split('\n')
                i = f'{i[0]} {i[1]}'
                self.lista_data.append(i)
        except:
            pass

        try:
            for i in temp_min:
                i = i.text
                i = i.strip()
                self.lista_temp_min.append(i)
        except:
            pass

        try:
            valido = False
            for i in temp_max:
                i = i.text
                i = i.strip()
                i = i.replace('°', '')
                if i.isdigit():
                    if valido == True:
                        i = f'{i}°'
                        self.lista_temp_max.append(i)
                        valido = False
                    else:
                        valido = True
        except:
            pass

        try:
            for i in condicao_tempo:
                i = i.text
                i = i.strip()
                self.lista_condicoes.append(i)
        except:
            pass

    def enviar_email(self):

        with open('email.txt', 'w', encoding='utf-8') as txt:

            email = f"""
Previsão do Tempo de São Paulo {self.data_hora_atual}
Máxima de {self.lista_temp_max[0]} e Mínima de {self.lista_temp_min[0]} - Chuva: {self.chuva}
{self.lista_condicoes[0]}\n
"""
            txt.write(email)

        with open('email.txt', 'a', encoding='utf-8') as txt:
            try:
                for i, day in enumerate(self.lista_data, start=1):

                    email = f"""
Dia {self.lista_data[i]} - Máxima de {self.lista_temp_max[i]} e Mínima de {self.lista_temp_min[i]}\n{self.lista_condicoes[i]}
"""
                    txt.write(email)
            except:
                pass

        with open('email.txt', 'r', encoding='utf-8') as txt:

            mensagem = txt.read()

            EMAIL_ADDRESS = ''
            EMAIL_PASSWORD = ''

            msg = EmailMessage()
            msg['Subject'] = 'Previsão do Tempo'
            msg['From'] = EMAIL_ADDRESS
            msg['To'] = EMAIL_ADDRESS
            password = EMAIL_PASSWORD
            msg.set_payload(mensagem)

            smtp = smtplib.SMTP('smtp.gmail.com: 587')
            smtp.starttls()
            smtp.login(msg['From'], password)
            smtp.sendmail(msg['From'], [msg['To']],
                          msg.as_string().encode('utf-8'))
            print('Email Enviado')


self = Previsao()
self.coleta_previsao_do_tempo()
self.enviar_email()
