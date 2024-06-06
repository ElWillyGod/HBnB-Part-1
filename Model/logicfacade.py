#!/usr/bin/python3

'''
    quickdoc
'''

from abc import ABC
import json


class LogicFacade(ABC):
    '''
        quickdoc
    '''

    @staticmethod
    def getByType(type):
        raise NotImplementedError

    @staticmethod
    def getByID(id:str):
        raise NotImplementedError

    @staticmethod
    def deleteByID(id:str) -> None:
        raise NotImplementedError

    @staticmethod
    def updateByID(id:str, json) -> None:
        raise NotImplementedError

    @staticmethod
    def createObjectByJson(cls, json) -> None:
        raise NotImplementedError

    @staticmethod
    def getCountry(code:str):
        raise NotImplementedError

    @staticmethod
    def getContryCities(code:str):
        raise NotImplementedError
