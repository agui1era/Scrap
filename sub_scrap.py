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

workbook = xlsxwriter.Workbook('/home/oscar/informe.xlsx')
worksheet = workbook.add_worksheet()

URL = 'https://articulo.mercadolibre.cl/MLC-534301591-35dbi-inalambrico-3g-4g-lte-antena-de-enrutamiento-dual-ts9-_JM#position=1&type=item&tracking_id=d7d88181-66e8-4771-bae1-b02f8ce9f314'
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

        print(int(cantidad_string))
     
       
        
                
        




