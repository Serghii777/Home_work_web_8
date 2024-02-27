import pika
from mongoengine import connect
from tabls import Contact
import certifi

# З'єднання з базою даних MongoDB
connect("web19", host="mongodb+srv://user19:456123@clusterdbgoit.xlgrzju.mongodb.net/", ssl=True, tlsCAFile=certifi.where())


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='sms_queue')


def send_sms(contact_id):
    
    print(f"SMS sent to contact with ID: {contact_id}")


def callback(ch, method, properties, body):
    contact_id = body.decode()
    contact = Contact.objects.with_id(contact_id)
    if contact:
        if contact.preferred_method == "sms":
            send_sms(contact_id)
            
            contact.update(set__message_sent=True)
            print(f"SMS sent to {contact.phone_number}.")
    else:
        print(f"Contact with ID {contact_id} not found.")


channel.basic_consume(queue='sms_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()