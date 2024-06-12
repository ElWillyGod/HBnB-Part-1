
'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC
import json
from validationlib import (
    idChecksum, isCountryValid, doesCountryExist, getCountry)
from classutilitieslib import getPlural, typeExists, getClassByName
from logicexceptions import CountryNotFoundError

from persistence.persistence_manager import FileDataManager


class LogicFacade(ABC):
    '''
        status = WIP

        Static class that defines static methods meant to be called from API.

        Each method handles a particular HTTP request.
        The get methods return a json string.
        Data arguments should also be json strings.

        --HTTP--
        GET:
            getByType(cls: str) -> str
            getByID(id: str, cls: str) -> str
            getCountry(code: str) -> str
            getCountryCities(code: str) -> str
        POST:
            createObjetByJson(cls: str, data: str)
        PUT:
            updateByID(id: str, cls: str, data: str)
        DELETE:
            deleteByID(id: str, cls: str)

        --Exceptions--
        from logicexceptions.py:
        TypeError, ValueError:
            --all--
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
    def __checkID(id) -> None:
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not idChecksum(id):
            raise ValueError("invalid id")

    @staticmethod
    def __checkType(type) -> None:
        if not isinstance(type, str):
            raise TypeError("class must be a string")
        if not typeExists(type):
            raise ValueError("invalid class")

    @staticmethod
    def __checkCode(code) -> None:
        if not isinstance(code, str):
            raise TypeError("country code must be a string")
        if not isCountryValid(code):
            raise ValueError("country code is not valid")

    @staticmethod
    def __checkCountryExistance(code):
        if not doesCountryExist(code):
            raise CountryNotFoundError("country does not exist")

    @staticmethod
    def getByType(type) -> str:
        LogicFacade.__checkType(type)
        typePlural = getPlural(type)
        return FileDataManager.getAll(typePlural)

    @staticmethod
    def getByID(id, type) -> str:
        LogicFacade.__checkID(id)
        LogicFacade.__checkType(type)
        typePlural = getPlural(type)
        return FileDataManager.get(id, typePlural)

    @staticmethod
    def deleteByID(id, type) -> None:
        LogicFacade.__checkID(id)
        LogicFacade.__checkType(type)
        typePlural = getPlural(type)
        FileDataManager.delete(id, typePlural)

    @staticmethod
    def updateByID(id, type, data: str) -> None:
        LogicFacade.__checkID(id)
        LogicFacade.__checkType(type)
        typePlural = getPlural(type)
        new = getClassByName(type)(json.loads(data))
        old = FileDataManager.get(id, typePlural)
        updated = new.toJson(update=old)
        FileDataManager.update(id, typePlural, updated)

    @staticmethod
    def createObjectByJson(type: str, data: str) -> None:
        LogicFacade.__checkType(type)
        new = getClassByName(type)(json.loads(data))
        id = new.id
        typePlural = getPlural(type)
        FileDataManager.save(typePlural, new.toJson())

    @staticmethod
    def getCountry(code) -> str:
        LogicFacade.__checkCode(code)
        LogicFacade.__checkCode(code)
        return getCountry(code)

    @staticmethod
    def getContryCities(code: str) -> str:
        LogicFacade.__checkCode(code)
        LogicFacade.__checkCountryExistance(code)
        return FileDataManager.getAllWithProperty(
            "cities", "country_code", code)
