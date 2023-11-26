import logging

from parser.metro_api import MetroApi
from database.connect import get_db
from database import crud


def main():

    # Настройка логгирования
    logging.basicConfig(
        filename='metro.log',
        filemode='w',
        level=logging.DEBUG,
    )
    # Парсинг категории Чаи
    products = list()
    metro = MetroApi()
    metro.init_new_session()
    [products.extend(p) for p in metro.get_products('chay', 0, 30)]

    products = {
        product['id']: dict(
            name=product['name'],
            slug=product['slug'],
            article=product['article'],
            price=product['stocks'][0]['prices_per_unit']['price'],
            old_price=product['stocks'][0]['prices_per_unit']['old_price'],
            brand=dict(
                id=product['manufacturer']['id'],
                name=product['manufacturer']['name'],
            )
        )
        for product in products
    }
    logging.info('Запись/обновление %s продуктов' % len(products))
    crud.create_or_update_products(
        db=get_db(),
        products=products,
    )


main()
