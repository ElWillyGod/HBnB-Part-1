
'''
    Defines the Country class.
    A country has cities.
    Instead of an ID they have a code.
    They also lack creation datetime and update datetime.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import doesCountryExist
from logic.model.logicexceptions import CountryNotFoundError


class Country(TrackedObject):
    """
        Country Class

        code (str): 2 char code to identify the country. ISO 3166-1 alpha-2.
        name (str): Name of country.
    """

    def __init__(self,
                 code: str,
                 name: str):
        if not doesCountryExist(code):
            raise CountryNotFoundError("country does not exist")
        self.code = code
        self.name = name
