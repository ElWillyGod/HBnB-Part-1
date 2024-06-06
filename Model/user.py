#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject


class User(TrackedObject):
    '''
        quickdoc
    '''

    def __init__(self, email, first_name, last_name):
        super().__init__()
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if False:
            raise NotImplementedError
        self.__email = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if False:
            raise NotImplementedError
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if False:
            raise NotImplementedError
        self.__last_name = value
