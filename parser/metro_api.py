import os
import json
import logging
from typing import List

import aiohttp


class MetroApi:

    def __init__(
        self,
        _slfs: str,
        store_id: str,
        metro_api_session: str,
    ):
        '''
        Перечень куки:
        * metroStoreId
        * ! _slfs - обязателен
        * ! metro_api_session - обязателен
        '''
        self.__products_request = dict()
        self.__store_id = store_id
        self.__set_cookie(
            _slfs=_slfs,
            metro_api_session=metro_api_session,
        )

    async def get_products(
        self,
        slug: str,
        user_agent: str,
        skip: int = 0,
        limit: int = 30,
        filters: List[dict] = [{
            "field": "main_article",
            "value": "0"
        }],
        attributes: List = [],
        in_stock: bool = False,
        eshop_order: bool = False,
        allStocks: bool = False,
        sort: str = "default",
    ) -> dict:
        url = 'https://api.metro-cc.ru/products-api/graph'
        # url = 'http://python.org'
        request_data = self.__request_generator(
            size=limit,
            _from=skip,
            filters=filters,
            attributes=attributes,
            in_stock=in_stock,
            eshop_order=eshop_order,
            allStocks=allStocks,
            slug=slug,
            sort=sort,
        )
        get_params = dict(
            url=url,
            cookies=self.__cookies,
            headers={'user-agent': user_agent},
            json=request_data,
            timeout=10.0,
        )
        async with aiohttp.ClientSession() as session:
            logging.info('Get products slug="%s", skip=%s, limit=%s' % (
                slug,
                skip,
                limit,
            ))
            async with session.options(url) as response:
                pass
            async with session.post(**get_params) as response:
                response = await response.json()
                print(response)
        return response

    def __set_cookie(
        self,
        _slfs: str,
        metro_api_session: str,
        is18Confirmed: bool = False,
    ) -> None:
        '''
        Перечень куки:
        * ! _slfs: str - обязателен
        * ! metro_api_session: str - обязателен
        * is18Confirmed: bool
        * metroStoreId: int
        '''
        self.__cookies = dict(
            _slfs=_slfs,
            metro_api_session=metro_api_session,
            is18Confirmed=is18Confirmed,
            metroStoreId=self.__store_id,
        )

    def __request_generator(
        self,
        size: int,
        _from: int,
        filters: List[dict],
        attributes: List,
        in_stock: bool,
        eshop_order: bool,
        allStocks: bool,
        slug: str,
        sort: str,
    ) -> dict:
        '''
        Генерация json данных для запроса:
        * storeId: int - ID магазина
        * sort: str - сортиовка
        * size: int - количество запрашиваемых элементов
        * from: int - пропустить первые n элементов
        * filters: List[dict]
        * attributes: List
        * in_stock: bool - фильтр "в наличии"
        * eshop_order: bool
        * allStocks: bool
        * slug: str - slug категории

        Полный пример в ./request_example.json

        ### Example
        ```
        {
            "storeId": 356,
            "sort": "default",
            "size": 30,
            "from": 0,
            "filters": [
                {
                    "field": "main_article",
                    "value": "0"
                }
            ],
            "attributes": [],
            "in_stock": false,
            "eshop_order": false,
            "allStocks": false,
            "slug": "chay"
        }
        ```
        '''
        if not self.__products_request:
            path = os.path.join(
                os.getcwd(),
                'parser/request_example.json',
            )
            with open(path, 'r', encoding='utf-8') as f:
                self.__products_request: dict = json.load(f)
        self.__products_request['variables'].update({
            "storeId": int(self.__store_id),
            "sort": str(sort),
            "size": int(size),
            "from": int(_from),
            "filters": filters,
            "attributes": attributes,
            "in_stock": bool(in_stock),
            "eshop_order": bool(eshop_order),
            "allStocks": bool(allStocks),
            "slug": str(slug),
        })
        return self.__products_request
