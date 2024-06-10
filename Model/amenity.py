#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject
from validationlib import isAmenityNameOk


class Amenity(TrackedObject):
    '''
        quickdoc
    '''

    def __init__(self, name):
        super().__init__()
        self.__name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self.__name = value
