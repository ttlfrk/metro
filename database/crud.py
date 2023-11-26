from typing import List

from sqlalchemy import select
from sqlalchemy.orm import Session

from database import models
from performers import BrandPerformer
from performers import ProductPerformer


def create_or_update_products(
    db: Session,
    products: List[ProductPerformer],
) -> None:
    '''
    Обновление или создание новых продуктов (и брендов)
    '''

    products = list(set(products))
    brands = get_or_create_brands(
        db=db,
        brands={product.brand for product in products},
    )
    db.add_all(brands.values())
    exists_products: tuple[models.Product] = db.execute(
        select(
            models.Product,
        ).where(
            models.Product.site_id.in_({
                product.site_id for product in products
            })
        ),
    ).scalars().all()

    # Создание новых продуктов
    new_products = {
        product: models.Product(
            **product.to_dict(),
            brand=brands[product.brand],
        ) for product in products
        if product not in list(exists_products)
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
        new = products[products.index(product)]
        for param in params_for_update:
            if getattr(product, param) != getattr(new, param):
                setattr(product, param, getattr(new, param))
                db.add(product)
        if product.brand != new.brand:
            product.brand = brands[new.brand]
            db.add(product)
    db.commit()


def get_or_create_brands(
    db: Session,
    brands: List[BrandPerformer],
) -> dict:
    '''
    Поиск и/или создание брендов
    '''
    exists = db.execute(
        select(
            models.Brand,
        ).where(
            models.Brand.site_id.in_({
                brand.site_id for brand in brands
            }),
        ),
    ).scalars().all()
    brands = list(set(brands))

    new_brands = {
        brand: models.Brand(**brand.to_dict())
        for brand in brands
        if brand not in list(exists)
    }
    db.add_all(new_brands.values())
    db.commit()
    new_brands.update({
        brands[brands.index(brand_model)]: brand_model
        for brand_model in exists
    })
    return new_brands
