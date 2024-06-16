
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC

from logic.model.classes import getPlural, getClassByName
from logic.model.countrieslib import getCountry, getCountries
from logic.logicexceptions import IDNotFoundError
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
        call = Persistence.get(id, typePlural)
        if call is None or len(call) == 0:
            raise IDNotFoundError("ID was not found")
        return call

    @staticmethod
    def deleteByID(id: str, type: str) -> None:
        typePlural = getPlural(type)
        Persistence.delete(id, typePlural)

    @staticmethod
    def updateByID(id: str, type: str, data: str) -> None:
        typePlural: str = getPlural(type)
        old_data = Persistence.get(id, typePlural)
        data["id"] = id
        data["created_at"] = old_data["created_at"]
        updated = getClassByName(type)(**data)
        Persistence.update(id, typePlural, updated.toJson())

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
