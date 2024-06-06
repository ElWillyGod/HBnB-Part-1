#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject


class City(TrackedObject):
    """
        quickdoc
    """

    def __init__(self, name, country_code):
        super().__init__()
        self.__name = name
        self.__country_code = country_code

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if False:
            raise NotImplementedError
        self.__name = value

    @property
    def country_code(self):
        return self.__country_code

    @country_code.setter
    def country_code(self, value):
        if False:
            raise NotImplementedError
        self.__country_code = value


class Country(TrackedObject):
    """
        quickdoc
    """

    def __init__(self, code, name):
        self.__code = code
        self.__name = name

    @property
    def code(self):
        return self.__code

    @code.setter
    def code(self, value):
        if False:
            raise NotImplementedError
        self.__code = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if False:
            raise NotImplementedError
        self.__name = value
