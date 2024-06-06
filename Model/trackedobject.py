#!/usr/bin/python3

'''
    quickdoc
'''

from abc import ABC
from datetime import datetime
import uuid


class TrackedObject(ABC):
    '''
        quickdoc
    '''

    def __init__(self):
        now = datetime.now()
        self.__created_at = now
        self.__updated_at = now
        self.__id = uuid.uuid4()

    def update_time(self):
        self.__updated_at = datetime.now()

    @property
    def id(self):
        return self.__id

    @property
    def created_at(self):
        return self.__created_at

    @property
    def update_time(self):
        return self.__updated_at
