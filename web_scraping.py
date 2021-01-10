from requests import get
from bs4 import BeautifulSoup
from smtplib import SMTP
from time import sleep

def get_soup(url):
	headers = {"User-Agent":"Chrome/39.0.2171.95"}
	response = get(url, headers=headers)
	soup = BeautifulSoup(response.text, 'lxml')
	return soup

def format_price(price):
	return int(price[1:8].replace('.',''))

def send_mail(store, price, url):
	server = SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.ehlo()
	server.login('from_mail@gmail.com', 'dosmtdvgiblpbslf')
	
	subjet = f'El precio ha bajado en {store}'
	body = f'El nuevo precio en {store} es de: {price} \nLink: {url}'
	msg = f'Subject: {subjet}\n\n{body}'

	server.sendmail('from_mail@gmail.com', 'to_mail@gmail.com', msg)
	print('Correo Enviado')
	server.quit()

def check_price(good_price):
	store = ['zmart', 'sepuls', 'gameslegends']
	price = []
	url = ["https://www.zmart.cl/scripts/prodView.asp?idProduct=80081", "https://www.sepuls.cl/sillas/drift-dr111-black/", "https://www.gameslegends.cl/silla-gaming-drift-dr111-black-preventa"]
	# Zmart.cl
	soup = get_soup(url[0])
	price.append(format_price(soup.find(id="PriceProduct").text.strip()))

	# Sepuls.cl
	soup = get_soup(url[1])
	price.append(format_price(str(soup.find('p', class_="price").text).strip()))

	# GamesLegends.cl
	soup = get_soup(url[2])
	price.append(format_price(soup.find('div', class_="form-price_desktop").span.text.strip()))

	for value in range(0,len(price)):
		if price[value] < good_price:
			print(f'En {store[value].title()} bajó de precio')
			send_mail(store[value].title(), price[value], url[value])

		print(f'Tienda: {store[value].title()}\tPrecio: {price[value]} \n')

while(True):
	check_price(300000)
	sleep(43200)





