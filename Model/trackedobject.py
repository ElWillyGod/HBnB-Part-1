#!/usr/bin/python3

'''
    quickdoc
'''

from abc import ABC
from datetime import datetime
import uuid
import json

from validationlib import idChecksum, isDatetimeValid
from logicexceptions import IDChecksumError


class TrackedObject(ABC):
    '''
        quickdoc
    '''

    def __init__(self, id=None, created_at=None, updated_at=None):
        now = datetime.now()
        self.created_at = now if created_at is None else created_at
        self.updated_at = now if updated_at is None else updated_at
        self.id = str(uuid.uuid4()) if id is None else id

    def update_time(self):
        self.__updated_at = str(datetime.now())

    def toJson(self) -> str:
        try:
            instance_vars = self.__dict__
            converted_data = json.loads(instance_vars)
            output = self(converted_data)
        except Exception:
            raise ValueError("object conversion to json failed")
        return output

    def createFromJson(self, data):
        try:
            converted_data = json.loads(data)
            output = self(converted_data)
        except TypeError:
            raise TypeError("json conversion to object failed")
        except Exception:
            raise ValueError("keys do not match the object's attributes")
        return output

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not idChecksum(value):
            raise IDChecksumError('invalid id')
        self.__id == value

    def createFromJson(self):
        pass

    @property
    def created_at(self):
        return self.__created_at

    @created_at.setter
    def created_at(self, value):
        if not isDatetimeValid(value):
            raise ValueError('invalid creation time')
        self.__created_at == value

    @property
    def updated_at(self):
        return self.__updated_at

    @updated_at.setter
    def updated_at(self, value):
        if not isDatetimeValid(value):
            raise ValueError('invalid update time')
        self.__updated_at == value
