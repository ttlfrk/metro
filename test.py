from performers import BrandPerformer
from database import models


model = models.Brand(
    site_id='test',
    name='test',
)
performer = BrandPerformer(
    site_id='test',
    name='test',
)
x = model == performer
print(x)
