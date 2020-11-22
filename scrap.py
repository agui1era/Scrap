import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import time
from datetime import datetime
from datetime import date
import math 
import os
import smtplib 
import logging
from pymongo import MongoClient

#cantidad de productos por categoria
LIMITE = 10    

def escribir_log(cadena):

    logging.basicConfig(filename='scrap.log',level=logging.DEBUG)

    end_date = datetime.now()
    str_date=end_date.strftime("%d/%m/%Y %H:%M:%S")
    logging.info(str_date+": "+cadena)
    print(str_date+": "+cadena)

    return 0

def get_qty(URL):
  
    page = requests.get(URL)

    results = BeautifulSoup(page.content, 'html.parser')

    job_elems = results.find_all( class_='ui-pdp-buybox__quantity')
    for job_elem in job_elems:
        
        for job_elem in job_elems:
        # Each job_elem is a new BeautifulSoup object.
        # You can use the same methods on it as you did before.
            
            qty_elem = job_elem.find( class_='ui-pdp-buybox__quantity__available')
            cantidad_string=qty_elem.text.strip()
            cantidad_string=cantidad_string.replace('(','')
            cantidad_string=cantidad_string.replace(')','')
            cantidad_string=cantidad_string.replace('disponibles','')

            return(cantidad_string)
    
a=0

getpage= requests.get('https://www.mercadolibre.cl/categorias#nav-header')

getpage_soup= BeautifulSoup(getpage.text, 'html.parser')

all_links= getpage_soup.findAll('a')

categorias =[]

for link in all_links:
    print (link.get('href'))
    categorias.append(link.get('href'))
        
for URL in categorias :

   try:
      
      page = requests.get(URL)

      results = BeautifulSoup(page.content, 'html.parser')

      i=1
      job_elems = results.find_all( class_='ui-search-result__content-wrapper')
      for job_elem in job_elems:
         
         for job_elem in job_elems:
         # Each job_elem is a new BeautifulSoup object.
         # You can use the same methods on it as you did before.
            
            title_element = job_elem.find( class_='ui-search-item__title')
            link_element = job_elem.find(class_='ui-search-item__group__element ui-search-link')
            price_element = job_elem.find(class_='price-tag-fraction')

            try:
               cantidad=get_qty(link_element.get('href'))
            except:
               cantidad="1"
         
            print('UBICACION: ',i)
            print('PRODUCTO: '+title_element.text.strip())       
            print('PRECIO: '+price_element.text.strip()) 
            print('CANTIDAD: '+cantidad)
            print('LINK: '+link_element.get('href')) 
            print()          
            print('-------------------------------------------------------------------------------------------------------------')
            print()           
         
            a=a+13 
            i=i+1
            client = MongoClient()
            client = MongoClient('localhost', 27017)

            # connecting or switching to the database
            db = client.scrapDB

            # creating or switching to demoCollection
            collection = db.ML2

            # first document
            document1 = {
                  "UBICACION":str(i),
                  "PRODUCTO":title_element.text.strip(),
                  "PRECIO":price_element.text.strip(),
                  "CANTIDAD":cantidad,
                  "LINK":link_element.get('href'),
                  "FECHA":str(str(date.today()))
                  }

            # Inserting both document one by one
            collection.insert_one(document1)
         
            if i > LIMITE :
               break
            
         if i > LIMITE :
            break 
   except:  
      print('ERROR')        


