import pika, json, os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")
django.setup()

#Nachrichten werden aus Message Broker-Warteschlange konsumiert, ggf. wird darauf reagiert

from products.models import Product

#Stellt Verbindung zum Message Broker her
params = pika.URLParameters('amqps://dgfojelw:Pc_-A7Ty2vNgFlA8wZpwCz1O0Rw_f5H0@cow.rmq2.cloudamqp.com/dgfojelw')

connection = pika.BlockingConnection(params)

channel = connection.channel() #Erstellt channel

channel.queue_declare(queue='admin') #Erstellt Warteschlange

#Wird aufgerufen, wenn Nachricht in der Warteschlange empfangen wird
def callback(ch, method, properties, body):
    print('Received in admin')
    id = json.loads(body) #Deserialisierung
    print(id)
    product = Product.objects.get(id=id) #Abruf des entsprechendes Produkts aus Datenbank
    product.likes = product.likes + 1 #Erhöhung der Anzahl an Likes
    product.save() #Speicherung des Produkts in Datenbank
    print('Product likes increased!')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming() #Weitere Nachrichten empfangen

channel.close()
