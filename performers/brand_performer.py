from database import models


class BrandPerformer:

    def __init__(self, site_id: int, name: str):
        self.__site_id = site_id
        self.__name = name

    def __hash__(self) -> int:
        return hash(self.__site_id)

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, BrandPerformer):
            return self.__site_id == __value.site_id
        elif isinstance(__value, models.Brand):
            return self.__site_id == __value.site_id
        else:
            return NotImplemented

    @property
    def site_id(self) -> int:
        return self.__site_id

    @property
    def name(self) -> str:
        return self.__name

    def to_dict(self) -> dict:
        return dict(
            name=self.__name,
            site_id=self.__site_id,
        )
