
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC
import json

from logic.model.classes import getPlural, getClassByName
from logic.model.validationlib import getCountry

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
            getCountryCities(code: str) -> dict
        POST:
            createObjetByJson(cls: str, data: dict) -> None
        PUT:
            updateByID(id: str, cls: str, data: dict) -> None
        DELETE:
            deleteByID(id: str, cls: str) -> Node

        --Exceptions--
        from logicexceptions.py:
        CountryNotFoundError:
            updateByID()
            createObjectByJson()
            getCountry()
            getCountryCities()
        EmailDuplicated:
            updateByID()
            createObjectByJson()
        from db.dbexceptions.py:
        IDNotFoundError:
            getByID()
            deleteByID()
            updateByID()
            createObjectByJson()
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
        data = json.loads(data)
        typePlural = getPlural(type)
        new = getClassByName(type)(data)
        old = Persistence.get(id, typePlural)
        updated = old.toJson(update=new)
        Persistence.update(id, typePlural, updated)

    @staticmethod
    def createObjectByJson(type: str, data: str) -> None:
        # data = json.loads(data)
        typePlural = getPlural(type)
        new = getClassByName(type)(**data)
        id = new.id
        Persistence.save(id, typePlural, new.toJson())

    @staticmethod
    def getCountry(code: str) -> dict:
        return getCountry(code)

    @staticmethod
    def getContryCities(code: str) -> dict:
        return Persistence.getAllWithProperty(
            "cities", "country_code", code)
