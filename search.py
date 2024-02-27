import re
import redis
from mongoengine import connect
from models import Author, Quote
import certifi
from redis_lru import RedisLRU
from datetime import timedelta

# Підключення до бази даних MongoDB Atlas
connect("web19", host="mongodb+srv://user19:456123@clusterdbgoit.xlgrzju.mongodb.net/", ssl=True, tlsCAFile=certifi.where())

# Підключення до Redis
client = redis.StrictRedis(host="localhost", port=6379, password=None)
# Створення об'єкту RedisLRU з максимальним розміром кешу 1000 та таймаутом 3600 секунд (1 година)
cache = RedisLRU(client, max_size=1000, default_ttl=timedelta(seconds=3600))

def search_quotes(query):
    # Перевірка, чи є результат у кеші
    cached_result = cache.get(query)
    if cached_result:
        return cached_result

    # Обробка скороченого запису за допомогою регулярних виразів
    name_match = re.match(r'name:(\w{2,})', query)
    tag_match = re.match(r'tag:(\w{2,})', query)
    
    if name_match:
        author_name = name_match.group(1)
        author = Author.objects(fullname__icontains=author_name).first()
        if author:
            quotes = Quote.objects(author=author).values_list('quote', flat=True)
            # Кешування результату
            cache.set(query, "\n".join(quotes))
            return quotes
        else:
            return []