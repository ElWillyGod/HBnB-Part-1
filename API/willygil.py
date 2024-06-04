#!/usr/bin/python3


'''
    Cosas importantes.
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


class User(TrackedObject):
    '''
        quickdoc
    '''

    def __init__(self, email, first_name, last_name):
        super().__init__()
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name

