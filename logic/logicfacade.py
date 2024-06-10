#!/usr/bin/python3

'''
    Defines LogicFacade and calls integration layer to get countries.
    This static class is called from API to handle HTTP requests logically.
    Imports from integration layer are WIP.
'''

from abc import ABC
import json
from validationlib import (idChecksum,
                           typeExists,
                           idExists,
                           isCountryValid)
from utilitieslib import classes, getPlural
from logicexceptions import *

from persistence.persistence_manager import fileDataManager, countryDataManager

countries = countryDataManager.get()


class LogicFacade(ABC):
    '''
        status = WIP (75%)

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
            getByType()
            getByID()
            createObjectByJson()
            updatedByID()
            deleteByID()
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
    def getByType(cls: str) -> str:
        if not typeExists(cls):
            raise TypeError("invalid type for get")
        clsPlural = getPlural(cls)
        return fileDataManager.getAll(clsPlural)

    @staticmethod
    def getByID(id, cls: str) -> str:
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not idChecksum(id):
            raise ValueError("invalid id")
        clsPlural = getPlural(cls)
        return fileDataManager.get(id, clsPlural)

    @staticmethod
    def deleteByID(id: str, cls: str) -> None:
        if not isinstance(id, str):
            raise TypeError("id must be a string")
        if not idChecksum(id):
            raise ValueError("invalid id")
        clsPlural = getPlural(cls)
        return fileDataManager.delete(id, clsPlural)

    @staticmethod
    def updateByID(id: str, cls: str, data: str) -> None:
        # id check made within the class __init__
        for c in classes:
            # c[0]: singular str, c[1]: plural str, c[2]: class
            if cls == c[0]:
                new = c[2].createFromJson(data, id)
                clsPlural = c[1]
        return fileDataManager.update(id, cls, data)

    @staticmethod
    def createObjectByJson(cls: str, data: str) -> None:
        # id check made within the class __init__
        for c in classes:
            # c[0]: singular str, c[1]: plural str, c[2]: class
            if cls == c[0]:
                new = c[2].createFromJson(json.loads(data))
                clsPlural = c[1]
                fileDataManager.save(clsPlural, new)
        raise TypeError("invalid class")

    @staticmethod
    def getCountry(code) -> str:
        if not isinstance(code, str):
            raise TypeError("country code must be a string")
        if not isCountryValid(code):
            raise ValueError("country code is not valid")
        for country in countries:
            if country.code == code:
                return country
        raise CountryNotFoundError("country does not exist")

    @staticmethod
    def getContryCities(code: str) -> str:
        if not isinstance(code, str):
            raise TypeError("country code must be a string")
        if not isCountryValid(code):
            raise ValueError("country code is not valid")
        for country in countries:
            if country.code == code:
                return fileDataManager.getAllWithProperty(
                        "cities", "country_code", code)
        raise CountryNotFoundError("country does not exist")
