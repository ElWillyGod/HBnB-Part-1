
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from trackedobject import TrackedObject
from validationlib import isCountryValid, doesCountryExist
from logicexceptions import CountryNotFoundError


class Country(TrackedObject):
    """
        status = Completed

        code (str): 2 char code to identify the country. ISO 3166-1 alpha-2.
        name (str): Name of country.
    """

    def __init__(self, code, name):
        self.code = code
        self.name = name

    @property
    def code(self) -> str:
        return self.__code

    @code.setter
    def code(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("code must be a string")
        if not isCountryValid(value):
            raise ValueError("invalid country code")
        if not doesCountryExist(value):
            raise CountryNotFoundError("country does not exist")
        self.__code = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if len(value):
            raise ValueError("name must not be empty")
        self.__name = value
