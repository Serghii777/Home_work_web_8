import pika
from faker import Faker
from mongoengine import connect
from tabls import Contact
import certifi

# З'єднання з базою даних MongoDB
connect("web19", host="mongodb+srv://user19:456123@clusterdbgoit.xlgrzju.mongodb.net/", ssl=True, tlsCAFile=certifi.where())


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=5672, credentials=credentials))
channel = connection.channel()


channel.queue_declare(queue='email_queue')


fake = Faker()
for _ in range(10):
    full_name = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    contact = Contact(full_name=full_name, email=email, phone_number=phone_number)
    contact.save()
    
    channel.basic_publish(exchange='', routing_key='email_queue', body=str(contact.id))

print("Fake contacts generated and added to the database.")

connection.close()