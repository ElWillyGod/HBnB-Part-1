
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC
import json

from model import getPlural, getClassByName
from model.validationlib import getCountry

from persistence.persistence_manager import FileDataManager


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
        return FileDataManager.getAll(typePlural)

    @staticmethod
    def getByID(id: str, type: str) -> dict:
        typePlural = getPlural(type)
        return FileDataManager.get(id, typePlural)

    @staticmethod
    def deleteByID(id: str, type: str) -> None:
        typePlural = getPlural(type)
        FileDataManager.delete(id, typePlural)

    @staticmethod
    def updateByID(id: str, type: str, data: dict) -> None:
        typePlural = getPlural(type)
        new = getClassByName(type)(json.loads(data))
        old = FileDataManager.get(id, typePlural)
        updated = new.toJson(update=old)
        FileDataManager.update(id, typePlural, updated)

    @staticmethod
    def createObjectByJson(type: str, data: dict) -> None:
        new = getClassByName(type)(json.loads(data))
        id = new.id
        typePlural = getPlural(type)
        FileDataManager.save(typePlural, new.toJson())

    @staticmethod
    def getCountry(code: str) -> dict:
        return getCountry(code)

    @staticmethod
    def getContryCities(code: str) -> dict:
        return FileDataManager.getAllWithProperty(
            "cities", "country_code", code)
