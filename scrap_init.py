import requests
from bs4 import BeautifulSoup

getpage= requests.get('https://www.mercadolibre.cl/categorias#nav-header')

getpage_soup= BeautifulSoup(getpage.text, 'html.parser')

all_links= getpage_soup.findAll('a')

categorias =[]

for link in all_links:
    print (link.get('href'))
    categorias.append(link)
    
print(len(categorias))