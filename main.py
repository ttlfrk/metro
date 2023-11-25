import asyncio

from parser.metro_api import MetroApi


async def main():

    metro = MetroApi(
        _slfs='1700931145735',
        store_id='356',
        metro_api_session='N0utlQGDi1FNIViVVZLYsahZpgGpJAiZiXQGJI7H',
    )
    r = await metro.get_products(
        slug='chay',
        user_agent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0',
    )


asyncio.run(main())
