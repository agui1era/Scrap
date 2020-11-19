
from pymongo import MongoClient
import datetime

#cantidad de productos vendidos minimos vendidos por dia a guardar
var_busqueda=1
#dias hacia atras
var_dias=30
#cantidad de ventas diferentes
conteo_ventas=5

client = MongoClient()
client = MongoClient('localhost', 27017)

# connecting or switching to the database
db = client.scrapDB

collectionx = db.MLX

collection = db.ML2
collectionx.drop()

z=0

for i in range(var_dias):
  
    now_date = datetime.datetime.now()
    end_date = now_date  - datetime.timedelta(days=z)
    str_end_date=end_date.strftime("%Y-%m-%d")
   
    now_date = datetime.datetime.now()
    begin_date = now_date  - datetime.timedelta(days=z+1)
    str_begin_date=begin_date.strftime("%Y-%m-%d")
    
    z=z+1

    result=collection.find({"FECHA":str_begin_date})
    
    print("_____________________________________________________________________")
    print("")
    print("ANÁLISIS DE VENTA ML DESDE EL " + str_begin_date +" AL "+str_end_date)
    print("PARA PRODUCTOS CON VARIACIÓN MAYOR A: " +str(var_busqueda) )
    print("_____________________________________________________________________")

    for doc in result:
        
        query = {'$and': [{'PRODUCTO': doc['PRODUCTO']}, {'FECHA': str_end_date}]} 
        result2=collection.find_one(query)

        try:
            
            cantidad_ayer = int(doc['CANTIDAD'])
        except:
            cantidad_ayer = -1

        try:
            cantidad_actual = int(result2['CANTIDAD'])
        except:
            cantidad_actual = -1

        try:
            precio = result2['PRECIO']
        except:
            precio= -1

        variacion = (cantidad_actual - cantidad_ayer) 
        
        if (variacion > var_busqueda) and (cantidad_actual != -1) and (cantidad_ayer != -1) and ( precio != -1):
                print("") 
                print(doc['PRODUCTO'])         
                print('Cantidad primer día: '+str(cantidad_actual))
                print('Cantidad último día: '+str(cantidad_ayer))
                print('Precio: $'+precio)
                print("Variación de stock: "+ str(variacion))
                print("_____________________________________")
                       
                # first document
                documentx = {
                    "PRODUCTO":doc['PRODUCTO'],
                    "PRECIO": precio,
                    "VARIACIÓN":variacion,
                    "FECHA":str_begin_date,
                    }

                # Inserting both document one by one
                collectionx.insert_one(documentx)
    
print()
print('XXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('ANÁLISIS DE VENTA DE ' + str(var_dias)+' DÍAS ATRAS')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXX')
print()

result=collectionx.distinct('PRODUCTO')


for doc in result:
    result2=collectionx.find({'PRODUCTO': doc}).count()
    if (result2 > conteo_ventas):
        print("___________________________________________")
        print("PRODUCTO: "+doc)
        producto=collectionx.find_one({'PRODUCTO': doc})
        print("PRECIO: "+producto['PRECIO'])
        print("CANTIDAD DE VENTAS DISTINTAS: "+str(result2))
        print("___________________________________________")
