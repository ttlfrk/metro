import time
import urllib.parse
from typing import List

import requests


def get_auchan_products(
    category: str,
    page: int = 1,
    step: int = 40,
) -> List[dict]:
    url = 'merchantId=1&page=1&perPage=40'
    while True:
        url = '%s%s' % (
            'https://www.auchan.ru/v1/catalog/products?',
            urllib.parse.urlencode(dict(
                merchantId=1,
                page=page,
                perPage=step,
            ))
        )
        r = requests.post(
            url=url,
            json={
                'filter': {
                    'category': category,
                    'promo_only': False,
                    'active_only': False,
                    'cashback_only': False,
                },
            },
        )
        products = r.json()['items']
        yield products
        if page * step > r.json()['activeRange'] or not len(products):
            break
        time.sleep(2)
        page += 1
