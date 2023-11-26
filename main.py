import logging

from parser.metro_api import MetroApi
from parser.auchan_api import get_auchan_products
from database.connect import get_db
from database import crud
from performers import BrandPerformer
from performers import ProductPerformer


def main():

    # Настройка логгирования
    logging.basicConfig(
        filename='metro.log',
        filemode='w',
        level=logging.DEBUG,
    )
    # Парсинг категории Чаи
    products = dict()
    metro = MetroApi()
    # 51 - Москва
    # 16 - Санкт-Петербург
    for store_id in {51, 16}:
        metro.init_new_session(store_id)
        products.update({
            store_id: [
                product for product_list in
                metro.get_products('chay', in_stock=True)
                for product in product_list
            ],
        })

    products = {
        ProductPerformer(
            name=product['name'],
            slug=product['slug'],
            article=product['article'],
            price=product['stocks'][0]['prices_per_unit']['price'],
            old_price=product['stocks'][0]['prices_per_unit']['old_price'],
            brand=BrandPerformer(
                site_id=product['manufacturer']['id'],
                name=product['manufacturer']['name'],
            ),
            store_id=store_id,
            site_id=product['id'],
        )
        for store_id in products.keys()
        for product in products[store_id]
    }
    logging.info('Метро запись/обновление %s продуктов' % len(products))
    crud.create_or_update_products(
        db=get_db(),
        products=products,
    )

    # 1 - Москва
    # 2 - Санкт-Петербург
    products = dict()
    for store_id in {1, 2}:
        products.update({
            store_id: [
                product for product_list in
                get_auchan_products('posuda-dlya-prigotovleniya')
                for product in product_list
            ],
        })
    products = {
        ProductPerformer(
            name=product['title'],
            slug=product['code'],
            article=product['vendorCode'],
            price=product['price']['value'],
            old_price=product['oldPrice']['value']
            if product['oldPrice'] else None,
            brand=BrandPerformer(
                site_id=product['brand']['code'],
                name=product['brand']['name'],
            ),
            store_id=store_id,
            site_id=product['id'],
        )
        for store_id in products.keys()
        for product in products[store_id]
    }
    logging.info('Ашан запись/обновление %s продуктов' % len(products))
    crud.create_or_update_products(
        db=get_db(),
        products=products,
    )


main()
