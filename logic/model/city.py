
'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import doesCountryExist, isCityNameDuplicated
from logic.model.logicexceptions import CountryNotFoundError, CityNameDuplicated


class City(TrackedObject):
    """
        City Class.
    """

    def __init__(self,
                 name: str,
                 country_code: str,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 update: dict | None = None
                 ) -> None:
        super().__init__(id, created_at, updated_at)
        if not doesCountryExist(country_code):
            raise CountryNotFoundError(
                f"country '{country_code}' not found")
        if update is None or "name" in update:
            if isCityNameDuplicated(name, country_code):
                raise CityNameDuplicated(
                    f"{name} already exists in {country_code}")
        self.name = name
        self.country_code = country_code
