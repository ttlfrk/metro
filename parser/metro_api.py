import os
import re
import time
import json
import logging
from typing import Union
from typing import List

from requests import Session
from requests import cookies
from fake_http_header import FakeHttpHeader


class MetroApi:

    def __init__(self):
        self.__products_request = None
        self.__metro_api_domain = 'https://api.metro-cc.ru/'

    def init_new_session(self, city_id: Union[int, None] = None) -> None:
        '''
        Создает и возвращает инициализированную сессию

        Параметры
        ---------
        * city_id: int - ID города для сбора данных
        '''
        # Необходимые cookies:
        # * _slfs - это unix time + 3 числа в конце (неизвестно что за числа).
        # * metro_api_session - можно получить, отправив запрос на
        #   https://api.metro-cc.ru/api/v1/{магическая_строка}/{id_магазина}/disclaimer
        #   Вышеуказанный адресс можно получить в js файле, по адресу
        #   https://cdn01.stellarlabs.ai/sections/{токен_stellarlabs}/dynamic.js,
        #   который можно найти на странице online.metro-cc.ru в самом начале.
        # Т.е. действия:
        #   1. На странице online.metro-cc.ru, получить ссылку на
        #      js файл от stellarlabs.ai
        #   2. В этом файле ищем токен для получения metro_api_session
        #   3. Отправляем запрос для получения metro_api_session

        logging.info('Init new session')
        self.__session = Session()
        self.__session.headers = FakeHttpHeader(
            domain_name='ru',
        ).as_header_dict(),
        stellarlabs_url = self.__get_stellarlabs_link()
        metro_token_url = self.__get_metro_token_url(stellarlabs_url)
        # Перед получением токена сессии, необходимо отправить
        # options запрос на тот же адрес
        r = self.__session.options(metro_token_url)
        r.raise_for_status()
        # Получаем куки metro_api_session
        r = self.__session.get(metro_token_url)
        r.raise_for_status()
        # Create _slfs cookie time.time() + 3 random numbers
        now = time.time()
        self.__session.cookies.set_cookie(
            cookies.create_cookie(
                domain='.metro-cc.ru',
                name='_slfs',
                path='/',
                secure=False,
                value='%s%s' % (int(now), int(now % 1 * 1000)),
            ),
        )
        if city_id:
            self.__session.cookies.set_cookie(
                cookies.create_cookie(
                    domain='online.metro-cc.ru',
                    name='metroStoreId',
                    path='/',
                    secure=False,
                    value=int(city_id),
                )
            )
        # Проверка наличия всех cookies
        need_cookies = {
            '_slfs',
            'metro_api_session',
            'exp_auth',
            'is18Confirmed',
            'metroStoreId',
        }
        exists_cookies = {c.name for c in self.__session.cookies}
        assert need_cookies == exists_cookies, \
            'Куки %s не установлены' % need_cookies.difference(exists_cookies)

    def get_products(
        self,
        slug: str,
        start: int = 0,
        step: int = 30,
        filters: List[dict] = [{
            'field': 'main_article',
            'value': '0',
        }],
        attributes: List = [],
        in_stock: bool = False,
        eshop_order: bool = False,
        allStocks: bool = False,
        sort: str = 'default',
    ) -> dict:
        '''
        Поиск товаров в категории

        Параметры:
        * slug: str - наименование категории (в адресной строке)
        * start: int - сколько пропустить
        * step: int - загружать с шагом (рекомендуется 30, как на сайте)
        * filters: List[dict] - список фильтров для поиска товаров
        * in_stock: bool - есть в наличии
        * eshop_order: bool - доступно к заказу
        * allStocks: bool - цена по акции
        * sort: str - сортировка (default)
        '''
        if not self.__session:
            self.init_new_session()
        url = self.__metro_api_domain + 'products-api/graph'
        while True:
            request_data = self.__request_generator(
                size=step,
                _from=start,
                filters=filters,
                attributes=attributes,
                in_stock=in_stock,
                eshop_order=eshop_order,
                allStocks=allStocks,
                slug=slug,
                sort=sort,
            )
            logging.info('Get products slug="%s", start=%s, step=%s' % (
                slug, start, step,
            ))
            r = self.__session.options(url)
            r.raise_for_status()
            r = self.__session.post(
                url=url,
                json=request_data,
            )
            r.raise_for_status()
            category = r.json()['data']['category']
            products = [p for p in category['products']]
            yield products
            if start + step > category['total'] or not products:
                break
            time.sleep(2)
            start += step

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
            'storeId': int(self.__session.cookies['metroStoreId'],),
            'sort': str(sort),
            'size': int(size),
            'from': int(_from),
            'filters': filters,
            'attributes': attributes,
            'in_stock': bool(in_stock),
            'eshop_order': bool(eshop_order),
            'allStocks': bool(allStocks),
            'slug': str(slug),
        })
        return self.__products_request

    def __get_stellarlabs_link(self) -> str:
        '''
        Возвращает ссылку на js от stellarlabs,
        и устанвливает куки:
        * ext_auth
        * is18Confirmed
        * metroStoreId
        '''
        # Получаем страницу online.metro-cc.ru, и ищем
        # ссылку на cdn.stellarlabs.ai/sections...js
        logging.debug('Поиск ссылки на js от stellarlabs.ai')
        r = self.__session.get('https://online.metro-cc.ru/')
        r.raise_for_status()
        stellarlabs_url = re.search(
            pattern=r'src="//(cdn\d{1,2}.stellarlabs.ai/sections/\w+/\w+.js)',
            string=r.text,
        )
        if not stellarlabs_url:
            raise ValueError('Токен для stellarlabs.io не найден')
        return 'https://' + stellarlabs_url.group(1)

    def __get_metro_token_url(self, stellarlabs_url: str) -> str:
        '''
        Возвращает ссылку для получения metro_api_session

        Параметры:
        ---------
        * stellarlabs_url: str - ссылка на js скрипт от stellarlabs
        '''
        # Отправляем запрос на cdn.stellarlabs.ai/sections...js,
        # в ответе получааем js, и ищем в нем ссылку
        # на api.metro для получения токена
        logging.debug('Поиск токена для api.metro')
        r = self.__session.get(stellarlabs_url)
        r.raise_for_status()
        metro_token = re.search(
            pattern=r'api.metro-cc.ru\\/api\\/v1\\/(\w+)',
            string=r.text,
        )
        if not metro_token:
            raise ValueError('Токен для metro-cc не найден')
        return '%s/api/v1/%s/%s/disclaimer' % (
            self.__metro_api_domain,
            metro_token.group(1),
            self.__session.cookies['metroStoreId'],
        )
