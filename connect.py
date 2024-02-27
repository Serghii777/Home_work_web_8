import json
import certifi
from mongoengine import connect
from models import Author, Quote

# З'єднання з базою даних MongoDB Atlas
connect("web19", host="mongodb+srv://user19:456123@clusterdbgoit.xlgrzju.mongodb.net/", ssl=True, tlsCAFile=certifi.where())

def load_authors_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        authors_data = json.load(file)
        for author_data in authors_data:
            Author(**author_data).save()

def load_quotes_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        quotes_data = json.load(file)
        for quote_data in quotes_data:
            author = Author.objects(fullname=quote_data['author']).first()
            if author:
                quote_data['author'] = author
                Quote(**quote_data).save()

if __name__ == "__main__":
    load_authors_from_json('authors.json')
    load_quotes_from_json('quotes.json')