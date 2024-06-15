
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC

from logic.model.classes import getPlural, getClassByName
from logic.model.countrieslib import getCountry, getCountries

from logic import DM as Persistence


class LogicFacade(ABC):
    '''
        Static class that defines static methods meant to be called from API.

        Each method handles a particular HTTP request.
        The get methods return dictionaries.
        Data arguments should also be dictionaries.

        --HTTP--
        GET:
            getByType(cls: str) -> dict
            getByID(id: str, cls: str) -> dict
            getCountry(code: str) -> dict
            getAllCountries() -> dict
            getCountryCities(code: str) -> dict
            getReviewsOfPlace(id: str) -> dict
        POST:
            createObjetByJson(cls: str, data: dict) -> None
        PUT:
            updateByID(id: str, cls: str, data: dict) -> None
        DELETE:
            deleteByID(id: str, cls: str) -> Node
    '''

    @staticmethod
    def getByType(type: str) -> dict:
        typePlural = getPlural(type)
        return Persistence.get_all(typePlural)

    @staticmethod
    def getByID(id: str, type: str) -> dict:
        typePlural = getPlural(type)
        return Persistence.get(id, typePlural)

    @staticmethod
    def deleteByID(id: str, type: str) -> None:
        typePlural = getPlural(type)
        Persistence.delete(id, typePlural)

    @staticmethod
    def updateByID(id: str, type: str, data: str) -> None:
        typePlural: str = getPlural(type)
        old_data: dict = Persistence.get(id, typePlural)
        old = getClassByName(type)(**old_data)
        updated = old.toJson(update=data)
        Persistence.update(id, typePlural, updated)

    @staticmethod
    def createObjectByJson(type: str, data: str) -> None:
        typePlural = getPlural(type)
        new = getClassByName(type)(**data)
        id = new.id
        Persistence.save(id, typePlural, new.toJson())

    @staticmethod
    def getAllCountries(code: str) -> dict:
        return getCountries()

    @staticmethod
    def getCountry(code: str) -> dict:
        return getCountry(code)

    @staticmethod
    def getContryCities(code: str) -> dict:
        return Persistence.get_by_property(
            "cities", "country_code", code
        )

    @staticmethod
    def getReviewsOfPlace(id: str) -> dict:
        return Persistence.get_by_property(
            "places", "id", id
        )
