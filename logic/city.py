#!/usr/bin/python3

'''
    Defines the city class.
    A city contains places and is inside a country.
    The name must also be unique in the same country.
'''

from trackedobject import TrackedObject
from validationlib import isNameValid, isCountryCodeValid, countryExists
from logicexceptions import CountryNotFoundError


class City(TrackedObject):
    """
        status = Completed

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
        self.country_code = country_code

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        elif not isNameValid(value):
            raise ValueError("invalid name")
        self.__name = value

    @property
    def country_code(self) -> str:
        return self.__country_code

    @country_code.setter
    def country_code(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("country_code must be a string")
        if len(value) != 2:
            raise ValueError("country_code must have 2 characters")
        if isCountryCodeValid(value):
            raise ValueError("invalid country_code")
        self.__country_code = value
