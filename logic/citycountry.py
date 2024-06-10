#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject
from validationlib import isNameValid, isCountryCodeValid, countryExists
from logicexceptions import CountryNotFoundError


class City(TrackedObject):
    """
        quickdoc
    """

    def __init__(self, name, country_code,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__()
        self.__name = name
        self.__country_code = country_code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if not isNameValid(value):
            raise ValueError("invalid name")
        self.__name = value

    @property
    def country_code(self):
        return self.__country_code

    @country_code.setter
    def country_code(self, value):
        if False:
            raise NotImplementedError
        self.__country_code = value


class Country(TrackedObject):
    """
        quickdoc
    """

    def __init__(self, code, name,
                 *, id=None, created_at=None, updated_at=None):
        self.__code = code
        self.__name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        if not isinstance(value, str):
            raise TypeError("code must be a string")
        if not isCountryCodeValid(value):
            raise ValueError("invalid country code")
        if not countryExists(value):
            raise CountryNotFoundError("country does not exist")
        self.__code = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if not isNameValid(value):
            raise ValueError("invalid name")
        self.__name = value
