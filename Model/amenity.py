#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject


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
        if False:
            raise NotImplementedError
        self.__name = value
