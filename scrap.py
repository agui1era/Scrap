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

LIMITE = 10    

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
      'https://listado.mercadolibre.cl/drones-y-accesorios#D[A:drones%20y%20accesorios]']

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
                  "CANTIDAD":price_element.text.strip(),
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
fromaddr = "notificaciones@igromi.com"
# instance of MIMEMultipart 
msg = MIMEMultipart() 

# storing the senders email address 
msg['From'] = fromaddr 

# storing the receivers email address 


# storing the subject 
msg['Subject'] = "Informe de producto"

# string to store the body of the mail 
body = "Informe de producto"

# attach the body with the msg instance 
msg.attach(MIMEText(body, 'plain')) 

# open the file to be sent 
filename = '/home/oscar/informe_productos-' + str(date.today())+'.xlsx'
attachment = open('/home/oscar/informe_productos-' + str(date.today())+'.xlsx', "rb") 

# instance of MIMEBase and named as p 
p = MIMEBase('application', 'octet-stream') 

# To change the payload into encoded form 
p.set_payload((attachment).read()) 

# encode into base64 
encoders.encode_base64(p) 

p.add_header('Content-Disposition', "attachment; filename= %s" % filename) 

# attach the instance 'p' to instance 'msg' 
msg.attach(p) 

# creates SMTP session 
s = smtplib.SMTP('smtp.zoho.com', 587) 

# start TLS for security 
s.starttls() 

# Authentication 
s.login(fromaddr, "Hkm150716") 

# Converts the Multipart msg into a string 
text = msg.as_string() 

# sending the mail 
msg['To'] = "aguileraelectro@gmail.com",
s.sendmail(fromaddr,"aguileraelectro@gmail.com", text)
escribir_log("email sent to aguileraelectro@gmail.com")

time.sleep(10)

msg['To'] = "victor.ruz@igromi.com"
s.sendmail(fromaddr, "victor.ruz@igromi.com", text) 

time.sleep(10)

msg['To'] = "barbara@ondustri.com "
s.sendmail(fromaddr, "barbara@ondustri.com ", text) 

# terminating the session 
s.quit() 