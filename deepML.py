
from pymongo import MongoClient
import datetime


client = MongoClient()
client = MongoClient('localhost', 27017)

# connecting or switching to the database
db = client.scrapDB

# creating or switching to demoCollection
collection = db.ML2

end_date = datetime.datetime.now()
str_end_date=end_date.strftime("%Y-%m-%d")

begin_date = end_date  - datetime.timedelta(days=1)
str_begin_date=begin_date.strftime("%Y-%m-%d")

result=collection.find({"FECHA":str_begin_date})

for doc in result:
    print (doc['PRODUCTO'])
    print (doc['CANTIDAD'])
    
    
    query = {'$and': [{'PRODUCTO': doc['PRODUCTO']}, {'FECHA': str_end_date}]}

  
    result2=collection.find_one(query)

    try:
       print(result2['CANTIDAD'])
    except:
       print("Producto no encontrado")
    print('XXXXXXXXXXXXXXXXXXXXXX')

    #cantidad_actual = int(result2['CANTIDAD'])
    #cantidad_ayer = int(doc['CANTIDAD'])
    
    #variacion = (cantidad_actual - cantidad_ayer) / cantidad_ayer
    
    #print('VARIACIÓN % =' )
