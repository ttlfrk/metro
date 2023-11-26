from typing import Union

from database import models
from performers import BrandPerformer


class ProductPerformer:

    def __init__(
        self,
        site_id: int,
        store_id: int,
        article: int,
        slug: str,
        name: str,
        price: Union[int, float],
        old_price: Union[int, float, None],
        brand: BrandPerformer,
    ):
        self.__site_id = site_id
        self.__store_id = store_id
        self.__article = article
        self.__slug = slug
        self.__name = name
        self.__price = self.__check_price(price)
        self.__old_price = self.__check_price(old_price)
        self.__brand = brand

    def __hash__(self) -> int:
        return hash((
            self.__site_id,
            self.__store_id,
        ))

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, ProductPerformer):
            return (
                self.__site_id == __value.site_id
                and self.__store_id == __value.store_id
            )
        elif isinstance(__value, models.Product):
            return (
                self.__site_id == __value.site_id
                and self.__store_id == __value.store_id
            )
        else:
            return NotImplemented

    @property
    def site_id(self) -> int:
        return self.__site_id

    @property
    def store_id(self) -> int:
        return self.__store_id

    @property
    def article(self) -> int:
        return self.__article

    @property
    def slug(self) -> int:
        return self.__slug

    @property
    def name(self) -> int:
        return self.__name

    @property
    def price(self) -> int:
        return self.__price

    @property
    def old_price(self) -> int:
        return self.__old_price

    @property
    def brand(self) -> int:
        return self.__brand

    def __check_price(self, price: Union[int, float, None]) -> int:
        if not price:
            return None
        # Удаляем копейки
        price = price * 100
        if isinstance(price, float):
            return int(price)
        return price

    def to_dict(self) -> dict:
        '''
        Преобразовывает класс в словарь, без brand
        '''
        return dict(
            site_id=self.__site_id,
            store_id=self.__store_id,
            article=self.__article,
            slug=self.__slug,
            name=self.__name,
            price=self.__price,
            old_price=self.__old_price,
        )
