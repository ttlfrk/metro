import pytest

from performers import BrandPerformer
from database import models


@pytest.mark.parametrize('site_id, name, in_list, is_same', (
    ('test', 'test', True, True),
    ('other_test', 'test', False, False),
    ('test', 'other_test', True, True),
    ('other_test', 'other_test', False, False),
))
def test_compare(site_id: str, name: str, in_list: bool, is_same: bool):
    model = models.Brand(
        site_id='test',
        name='test',
    )
    performer = BrandPerformer(
        site_id=site_id,
        name=name,
    )

    assert (model == performer) == is_same
    assert (model in [performer]) == in_list
    assert (performer in [model]) == in_list
