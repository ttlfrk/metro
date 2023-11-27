import pytest

from performers import ProductPerformer
from performers import BrandPerformer
from database import models


@pytest.mark.parametrize(
    'site_id, store_id, article, slug, name,'
    'price, old_price, in_list, is_same', (
        (1, 1, 'article', 'slug', 'name', 99.0, 98.0, True, True),
        (1, 1, 'other_article', 'slug', 'name', 99.0, 98.0, True, True),
        (1, 1, 'article', 'other_slug', 'name', 99.0, 98.0, True, True),
        (1, 1, 'article', 'slug', 'name', 99.0, 98.0, True, True),
        (1, 1, 'article', 'slug', 'other_name', 99.0, 98.0, True, True),
        (1, 1, 'article', 'slug', 'name', 0, 98.0, True, True),
        (1, 1, 'article', 'slug', 'name', 99.0, 0, True, True),
        (1, 2, 'article', 'slug', 'name', 99.0, 0, False, False),
        (2, 1, 'article', 'slug', 'name', 99.0, 0, False, False),
        (2, 2, 'article', 'slug', 'name', 99.0, 0, False, False),
    ),
)
def test_compare(
    site_id: int,
    store_id: int,
    article: str,
    slug: str,
    name: str,
    price: float,
    old_price: float,
    in_list: bool,
    is_same: bool,
):
    model = models.Product(
        site_id=1,
        store_id=1,
        article='article',
        slug='slug',
        name='name',
        price=99.0,
        old_price=98.0,
    )
    performer = ProductPerformer(
        site_id=site_id,
        store_id=store_id,
        article=article,
        slug=slug,
        name=name,
        price=price,
        old_price=old_price,
        brand=BrandPerformer(
            site_id='test',
            name='test',
        ),
    )

    assert (model == performer) == is_same
    assert (model in [performer]) == in_list
    assert (performer in [model]) == in_list
