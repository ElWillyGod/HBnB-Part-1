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
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if isUserEmailDuplicated(value):
            raise EmailDuplicated("email already exists")
        self.__email = value

    @property
    def first_name(self):
        return self.__first_name

    @first_name.setter
    def first_name(self, value):
        if not isinstance(value, str):
            raise TypeError("first_name must be a string")
        if False:
            raise ValueError("first_name must not be empty")
        if False:
            raise ValueError("first_name must not have spaces")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if False:
            raise NotImplementedError
        self.__last_name = value
