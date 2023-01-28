#coding:utf-8
import requests
import os
from bs4 import BeautifulSoup
import smtplib 
from email.message import EmailMessage
from dotenv import load_dotenv

config = load_dotenv(".env")


#Author: Juan Felipe Osorio (JF0z0r)
#Github: JFOZ1010
#Description: Automatization Both for Amazon - GPU'S
def bot_tarjetas_graficas(): 

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Opera/93.0.4585.52',
        'Accept-Language': 'es-ES,es;q=0.9'
    }

    #BLOQUE DE CONVERSION DE DOLAR A PESOS#
    dolar = requests.get("https://www.google.com/search?q=dolar+a+cop&sourceid=chrome&ie=UTF-8", headers=header)
    contentDolar = dolar.text
    dolarsoup = BeautifulSoup(contentDolar,'html.parser')

    dolarPrice = dolarsoup.find_all('span', class_= 'DFlfde SwHCTb')

    auxdolar = dolarPrice[0].text

    auxdolar = auxdolar.replace('.','')
    auxdolar = auxdolar.replace(',','.')

    dolar = float(auxdolar)
    dolar = int(dolar)

    url = 'https://www.amazon.com/-/es/Tarjetas-Gráficas-para-Computadoras-100-200/s?keywords=Tarjetas+Gráficas+para+Computadoras&i=computers&rh=n%3A284822%2Cp_36%3A1253506011%2Cp_n_deal_type%3A23566065011&dc&language=es&c=ts&qid=1674861924&rnid=23566063011&ts_id=284822&ref=sr_nr_p_n_deal_type_1&ds=v1%3AtjEkaGPV4qlKwlmfWgo%2FMoO4k9kCNZDma88Vm4gQi7M'

    response = requests.get(url, headers=header)
    response.status_code

    if response.status_code == 200:
        print('Todo bien')
    else:
        print('Algo salio mal')
    
    soup = BeautifulSoup(response.content, 'html.parser')

    #print('------------------TITULOS------------------')
    titulos = soup.find_all('span', {'class': 'a-size-medium a-color-base a-text-normal'})
    titulos = titulos[:10]
    titulos = [titulo.text + " " for titulo in titulos]
    #print(len(titulos))

    #print('------------------PRECIOS------------------')
    precios = soup.find_all('span', {'class': 'a-price-whole'})
    precios = [precio.text + " " for precio in precios]
    precios = precios[:10]
    precios = [int(float(precio.replace('.',''))) * dolar for precio in precios]
    #print(precios)

    #print('------------------LINKS------------------')
    links = soup.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})
    links = [link.get('href') + " " for link in links]
    links = links[:10]
    #dominio a los links
    links = ['https://www.amazon.com' + link for link in links]
    #print(links)

    precio_mas_bajo = min(precios)    

    #determinar la mejor opcion
    for i in range(len(precios)):
        if precios[i] == precio_mas_bajo:
            #print(f'La mejor opcion de los {len(precios)} mejores precios es: {titulos[i]}', 'aqui tienes el link: ', links[i])
            tituloCertero = titulos[i]
            linkCertero = links[i]
            break
    
    ###ENVIO DE CORREO ELECTRONICO###

    mensaje = EmailMessage() #creacion del mensaje. 

    email_subject = 'Mejor opción de tarjeta grafica en Amazon'
    
    SENDER_EMAIL = os.getenv('EMAIL_USER')
    SENDER_PASSWORD = os.getenv('EMAIL_PASS')
    RECEIVER_EMAIL = os.getenv('EMAIL_RECEIVER')

    #configure email headers. 
    mensaje['Subject'] = email_subject
    mensaje['From'] = SENDER_EMAIL
    mensaje['To'] = RECEIVER_EMAIL

    html = f"""\
        <!DOCTYPE html>
        <head>
        </head>
            <body>
                <h1>Mejor opcion de tarjeta grafica</h1>
                <p>Hello there, {RECEIVER_EMAIL}</p>
                <li>Este solo es un bot automatizado para ayudarte en la exhaustiva tarea de encontrar una buena tarjeta a un gran precio, sin ser tu el que está detras de la pantalla dia y noche revisando c: </li>
                <li>La mejor opcion de los {len(precios)} mejores precios es: {tituloCertero}</li>
                <li>El precio de esta tarjeta convertido a pesos COP es: {precio_mas_bajo}</li>
                <a href="{linkCertero}">Este es el link de la mejor opcion</a>
            </body>
        </html>
    """

    
    # Add message content as html type
    mensaje.set_content(html, subtype='html')

    #configure SMTP server and port. 
    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        smtp.send_message(mensaje)
        print('Email sent successfully')
        smtp.quit() #cerrar la conexion

if __name__ == '__main__':
    bot_tarjetas_graficas()
   

