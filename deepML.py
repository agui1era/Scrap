
from pymongo import MongoClient
import datetime

#cantidad de productos vendidos minimos vendidos por dia a guardar
variacion_busqueda=1

#dias hacia atras
rango_dias=30

#cantidad de ventas diferentes
limite_de_conteo_ventas=3

client = MongoClient()
client = MongoClient('localhost', 27017)

# connecting or switching to the database
db = client.scrapDB

collectionx = db.MLX
collection = db.ML2
collectionx.drop()

z=0

for i in range(rango_dias):
  
    now_date = datetime.datetime.now()
    end_date = now_date  - datetime.timedelta(days=z)
    str_end_date=end_date.strftime("%Y-%m-%d")
   
    now_date = datetime.datetime.now()
    begin_date = now_date  - datetime.timedelta(days=z+1)
    str_begin_date=begin_date.strftime("%Y-%m-%d")
    
    z=z+1

    result_todos_ayer=collection.find({"FECHA":str_begin_date})
    
    print("_____________________________________________________________________")
    print("")
    print("ANÁLISIS DE VENTA ML DESDE EL " + str_begin_date +" AL "+str_end_date)
    print("PARA PRODUCTOS CON VARIACIÓN MAYOR A: " +str(variacion_busqueda) )
    print("_____________________________________________________________________")

    for doc_ayer in result_todos_ayer:
        
        query = {'$and': [{'PRODUCTO': doc_ayer['PRODUCTO']}, {'FECHA': str_end_date}]} 
        result_actual=collection.find_one(query)


        #consutlo si ya existe el ingreso de variacion para una fecha
        
        query = {'$and': [{'PRODUCTO': doc_ayer['PRODUCTO']}, {'FECHA': str_begin_date}]} 
        result=collectionx.find_one(query)

        try:
            
            cantidad_ayer = int(doc_ayer['CANTIDAD'])
        except:
            cantidad_ayer = -1

        try:
            cantidad_actual = int(result_actual['CANTIDAD'])
        except:
            cantidad_actual = -1

        try:
            precio = result_actual['PRECIO']
        except:
            precio= -1

        variacion = (cantidad_actual - cantidad_ayer) 
        
        if  (variacion > variacion_busqueda) and (cantidad_actual != -1) and (cantidad_ayer != -1) and ( precio != -1):
                print("") 
                print(doc_ayer['PRODUCTO'])         
                print('Cantidad primer día: '+str(cantidad_actual))
                print('Cantidad último día: '+str(cantidad_ayer))
                print('Precio: $'+precio)
                print("Variación de stock: "+ str(variacion))
                print("_____________________________________")
                       
                # first document
                documentx = {
                    "PRODUCTO":doc_ayer['PRODUCTO'],
                    "PRECIO": precio,
                    "VARIACIÓN":variacion,
                    "FECHA":str_begin_date,
                    }

                # Inserting both document one by one
                
                collectionx.insert_one(documentx)
    
print()
print('XXXXXXXXXXXXXXXXXXXXXXXXXXX')
print('ANÁLISIS DE VENTA DE ' + str(rango_dias)+' DÍAS ATRAS')
print('XXXXXXXXXXXXXXXXXXXXXXXXXXX')
print()

result=collectionx.distinct('PRODUCTO')

for doc in result:
    cantidad_de_ventas=collectionx.find({'PRODUCTO': doc}).count()
    if ( cantidad_de_ventas > limite_de_conteo_ventas):
        print("___________________________________________")
        print("PRODUCTO: "+doc)
        producto=collectionx.find_one({'PRODUCTO': doc})
        print("PRECIO: "+producto['PRECIO'])
        print("CANTIDAD DE VENTAS DISTINTAS: "+str(cantidad_de_ventas))
        print("___________________________________________")
