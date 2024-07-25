# Previsão do Tempo
Uma automação criada para verificação da previsão do tempo. A automação acesso o site climatempo.com.br e verifica a temperatura do dia atual e de mais 15 dias pra frente. Após a verificação a automação envia um e-mail para o seu e-mail desejado com todas as informações da Previsão.

## Funcionalidade
* Acessar o site climatempo.com.br
* Verifica a temperatura do dia atual e de mais 15 dias pra frente.
* Envia um e-mail para o seu e-mail desejado com todas as informações da Previsão.

### Requirements
* Python 3.10.12
* BeautifulSoup
* EmailMessage
* requests
* datetime
* smtplib
