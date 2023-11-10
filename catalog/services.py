from django.conf import settings
from django.core.cache import cache

from catalog.models import Product
from config.settings import CACHE_ENABLED


def get_assortment_cache():
    if settings.CACHE_ENABLED:
        # Проверяем включенность кеша
        key = 'assortment_list'  # Создаем ключ для хранения
        product_list = cache.get(key)  # Пытаемся получить данные
        if product_list is None:
            # Если данные не были получены из кеша, то выбираем из БД и записываем в кеш
            product_list = Product.objects.all()
            cache.set(key, product_list)
    else:
        # Если кеш не был подключен, то просто обращаемся к БД
        product_list = Product.objects.all()
    # Возвращаем результат
    return product_list
