import pika, json
from main import Product, db

#Verbindung zu RabbitMQ-Broker herstellen
params = pika.URLParameters('amqps://dgfojelw:Pc_-A7Ty2vNgFlA8wZpwCz1O0Rw_f5H0@cow.rmq2.cloudamqp.com/dgfojelw')
connection = pika.BlockingConnection(params)
channel = connection.channel() #Channel eröffnen
channel.queue_declare(queue='main') #Warteschlange erstellen oder bereits Vorhandene verwenden

#Funktion wird aufgerufen, wenn eine Nachricht empfangen wird
def callback(ch, method, properties, body):
    print('Received in main')
    data = json.loads(body) #Deserialisierung
    print(data)
#Content-Typ der Properties wird überprüft durch if-Abfragen

    #neues Produkt-Objekt wird, mit in Nachricht enthaltenen Daten, erstellt und in DB hinzugefügt
    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print('Product Created')

    #Produkt, mit in Nachricht enthaltenen ID, wird aus DB abgerufen und mit neuen Daten aktualisiert
    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print('Product Updated')

    #Produkt, mit in Nachricht enthaltenen ID, wird aus DB abgerufen und gelöscht
    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print('Product Deleted')

#Warteschlange wird zum Empfangen von Nachrichten geöffnet
channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)
print('Started Consuming')
channel.start_consuming() #Empfang von Nachrichten wurde gestartet
channel.close()
