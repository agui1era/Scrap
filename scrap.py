import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import xlsxwriter
import time
from datetime import datetime
from datetime import date
import math 
import os
import smtplib 
import logging
from pymongo import MongoClient

LIMITE = 20    

URLproductos=['https://listado.mercadolibre.cl/computador-gamer#D[A:computador%20gamer]',
      'https://listado.mercadolibre.cl/accesorios-para-consola#D[A:accesorios%20para%20consola]',
      'https://listado.mercadolibre.cl/accesorios-para-camaras#D[A:accesorios%20para%20camaras]',
      'https://listado.mercadolibre.cl/componentes-de-pc#D[A:%20componentes%20de%20pc]',
      'https://listado.mercadolibre.cl/conectividad-y-redes#D[A:conectividad%20y%20redes]',
      'https://listado.mercadolibre.cl/cables-y-hubs#D[A:cables%20y%20hubs]',
      'https://listado.mercadolibre.cl/accesorios-para-pc-gamming#D[A:accesorios%20para%20PC%20gamming]',
      'https://listado.mercadolibre.cl/estabilizadores-y-ups#D[A:estabilizadores%20y%20UPS]',
      'https://listado.mercadolibre.cl/monitores-y-accesorios#D[A:monitores%20y%20accesorios]',
      'https://listado.mercadolibre.cl/perifericos-de-pc#D[A:perifericos%20de%20PC]',
      'https://listado.mercadolibre.cl/notebook-y-accesorios#D[A:%20notebook%20y%20accesorios]',
      'https://listado.mercadolibre.cl/repuestos-para-celular#D[A:repuestos%20para%20celular]',
      'https://listado.mercadolibre.cl/dispensadores-y-purificadores#D[A:dispensadores%20y%20purificadores]',
      'https://listado.mercadolibre.cl/drones-y-accesorios#D[A:drones%20y%20accesorios]',
      'https://listado.mercadolibre.cl/antena-4g#D[A:antena%204g]',
      'https://listado.mercadolibre.cl/scanner-automotriz#D[A:scanner%20automotriz]',
      'https://listado.mercadolibre.cl/bebe#D[A:bebe]',
      'https://listado.mercadolibre.cl/accesorio-auto#D[A:accesorio%20auto]',
      'https://listado.mercadolibre.cl/decoracion-hogar#D[A:decoracion%20hogar]',
      'https://listado.mercadolibre.cl/accesorios-celulares#D[A:accesorios%20celulares]',
      'https://listado.mercadolibre.cl/celulares-telefonia/celulares/#menu=categories',
      'https://listado.mercadolibre.cl/repuestos-maquinaria-agricola/',
      'https://autos.mercadolibre.cl/accesorios/gps/',
      'https://motos.mercadolibre.cl/acc-cuatrimotos/',
      'https://vehiculos.mercadolibre.cl/acc-repuestos-camiones/',
      'https://autos.mercadolibre.cl/accesorios/audio/',
      'https://listado.mercadolibre.cl/infraestructura-rural/',
      'https://listado.mercadolibre.cl/electrodomesticos-belleza/',
      'https://listado.mercadolibre.cl/fotografia/accesorios/',
      'https://listado.mercadolibre.cl/drones-accesorios/',
      'https://listado.mercadolibre.cl/celulares-telefonia/accesorios-celulares/',
      'https://listado.mercadolibre.cl/handies-radiofrecuencia/',
      'https://listado.mercadolibre.cl/accesorios-antiestatica/',
      'https://listado.mercadolibre.cl/almacenamiento/',
      'https://listado.mercadolibre.cl/cables-hubs-usb/',
      'https://listado.mercadolibre.cl/cajas-sobres-porta-cds/',
      'https://listado.mercadolibre.cl/componentes-pc/',
      'https://listado.mercadolibre.cl/conectividad-redes/',
      'https://listado.mercadolibre.cl/estabilizadores-ups/',
      'https://listado.mercadolibre.cl/impresion/',
      'https://listado.mercadolibre.cl/lectores-scanners/',
      'https://listado.mercadolibre.cl/limpieza-cuidado-pcs/',
      'https://listado.mercadolibre.cl/monitores-accesorios/',
      'https://listado.mercadolibre.cl/notebooks-accesorios/',
      'https://listado.mercadolibre.cl/computacion/software/',
      'https://listado.mercadolibre.cl/accesorios-consolas/' ,
      'https://listado.mercadolibre.cl/consolas/',
      'https://listado.mercadolibre.cl/pinballs-arcade/',
      'https://listado.mercadolibre.cl/repuestos-consolas/',
      'https://listado.mercadolibre.cl/videojuegos/juegos/',
      'https://listado.mercadolibre.cl/electronica/accesorios-audio-video/',
      'https://listado.mercadolibre.cl/electronica/accesorios-audio-video/cables/',
      'https://listado.mercadolibre.cl/electronica/componentes-electronicos/',
      'https://listado.mercadolibre.cl/equipamiento-medic/']

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
workbook = xlsxwriter.Workbook('/home/oscar/informe_productos-' + str(date.today())+'.xlsx')
worksheet = workbook.add_worksheet()

        
for URL in URLproductos :
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
         
            bold = workbook.add_format({'bold': True})
            
            worksheet.write(3+a, 1,'UBICACION: '+str(i),bold)
            worksheet.write(5+a, 1,'PRODUCTO: '+title_element.text.strip(),bold)
            worksheet.write(7+a, 1,'PRECIO: '+price_element.text.strip(),bold)
            worksheet.write(9+a, 1,'CANTIDAD: '+cantidad,bold)
            worksheet.write(11+a, 1,'LINK: '+link_element.get('href'),bold)
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

workbook.close()   
