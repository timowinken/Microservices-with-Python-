import pika, json

#Um Nachrichten an Message-Queue zu senden
params = pika.URLParameters('amqps://dgfojelw:Pc_-A7Ty2vNgFlA8wZpwCz1O0Rw_f5H0@cow.rmq2.cloudamqp.com/dgfojelw')

connection = pika.BlockingConnection(params)

channel = connection.channel()

#Damit Nachricht gesendet wird, wird diese Methode aufgerufen
def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)