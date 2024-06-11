#!/usr/bin/python3

'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from trackedobject import TrackedObject
from validationlib import isUserEmailDuplicated, isNameValid, isEmailValid
from logicexceptions import EmailDuplicated


class User(TrackedObject):
    '''
        status = Completed

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        email (str): Email of user, unique.
        first_name (str): First name of user.
        last_name (str): Last name of user.
    '''

    def __init__(self, email, first_name, last_name,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, value):
        if not isinstance(value, str):
            raise TypeError("email must be a string")
        if not isEmailValid(value):
            raise ValueError("invalid email")
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
        if len(value) == 0:
            raise ValueError("first_name must not be empty")
        if isNameValid(value):
            raise ValueError("invalid first_name")
        self.__first_name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        if not isinstance(value, str):
            raise TypeError("last_name must be a string")
        if len(value) == 0:
            raise ValueError("last_name must not be empty")
        if isNameValid(value):
            raise ValueError("invalid last_name")
        self.__last_name = value
