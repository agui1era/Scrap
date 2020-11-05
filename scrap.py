import requests
from bs4 import BeautifulSoup
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders 
import xlsxwriter
import time
import datetime
import math 
import os
import smtplib 
import logging


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
        
       
URL = 'https://listado.mercadolibre.cl/computador-gamer#D[A:computador%20gamer]'
BUSQUEDA='Computador gamer'
page = requests.get(URL)

results = BeautifulSoup(page.content, 'html.parser')

i=1
a=0
workbook = xlsxwriter.Workbook('/home/oscar/'+BUSQUEDA+'-' + str(datetime.date.today())+'.xlsx')
worksheet = workbook.add_worksheet()

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
        print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
        print()           
     
        bold = workbook.add_format({'bold': True})
        
        worksheet.write(3+a, 1,'UBICACION: '+str(i),bold)
        worksheet.write(5+a, 1,'PRODUCTO: '+title_element.text.strip(),bold)
        worksheet.write(7+a, 1,'PRECIO: '+price_element.text.strip(),bold)
        worksheet.write(9+a, 1,'CANTIDAD: '+cantidad,bold)
        worksheet.write(11+a, 1,'LINK: '+link_element.get('href'),bold)
            
        a=a+13
        i=i+1
        if i > 10 :
           break
    if i > 10 :
       break         
                
               
workbook.close()      
    



