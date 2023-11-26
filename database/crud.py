from sqlalchemy import select
from sqlalchemy.orm import Session

from database import models


def create_or_update_products(
    db: Session,
    products: dict,
) -> None:
    '''
    Обновление или создание новых продуктов (и брендов)

    products должен быть:
    ```
    {
        site_id: {
            'article': 124,
            'slug': 'chay_vkusniy',
            'name': 'Чай вкусный',
            'price': 124,
            'old_price': 152,
            'brand': {
                'name': 'Чайная компания',
                'id': 124,
            }
        }
    }
    ```
    '''

    brands = get_or_create_brands(
        db=db,
        brands={product['brand']['id']: product['brand']
                for product in products.values()},
    )
    db.add_all(brands.values())
    exists_products: tuple[models.Product] = db.execute(
        select(
            models.Product,
        ).where(
            models.Product.site_id.in_(products.keys())
        ),
    ).scalars().all()

    # Создание новых продуктов
    new_products = {
        product_id: models.Product(
            site_id=product_id,
            article=products[product_id]['article'],
            slug=products[product_id]['slug'],
            name=products[product_id]['name'],
            price=products[product_id]['price'],
            old_price=products[product_id]['old_price'],
            brand=brands[products[product_id]['brand']['id']],
        ) for product_id in products.keys()
        if product_id not in {p.site_id for p in exists_products}
    }
    db.add_all(new_products.values())

    # Обновление существующих продуктов
    params_for_update = {
        'article',
        'slug',
        'name',
        'price',
        'old_price',
    }
    for product in exists_products:
        new = products[product.site_id]
        for param in params_for_update:
            if getattr(product, param) != new[param]:
                setattr(product, param, new[param])
                db.add(product)
        if product.brand_id != new['brand']['id']:
            product.brand_id = new['brand']['id']
    db.commit()


def get_or_create_brands(
    db: Session,
    brands: dict,
) -> dict:
    '''
    Поиск или создание брендов

    brands должен быть:
    ```
    {
        site_id: {'id': 1, 'name': 'test'},
        ...
    }
    ```
    '''
    exists = db.execute(
        select(
            models.Brand,
        ).where(
            models.Brand.site_id.in_(brands.keys()),
        ),
    ).scalars().all()

    new_brands = {
        brand_id: models.Brand(
            site_id=brand_id,
            name=brands[brand_id]['name']
        ) for brand_id in brands.keys()
        if brand_id not in {brand.site_id for brand in exists}
    }
    db.add_all(new_brands.values())
    db.commit()
    new_brands.update({
        brand.site_id: brand for brand in exists
    })
    return new_brands
