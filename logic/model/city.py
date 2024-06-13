
'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from trackedobject import TrackedObject
from validationlib import doesCountryExist
from logicexceptions import CountryNotFoundError


class City(TrackedObject):
    """
        City Class

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        name (str): Name of city.
        country_code (str): Code that corresponds to a country. Similar to ID.
    """

    def __init__(self, name, country_code,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.name = name
        if not doesCountryExist(country_code):
            raise CountryNotFoundError("country not found")
        self.country_code = country_code
