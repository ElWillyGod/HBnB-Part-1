#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject
from validationlib import *


class Review(TrackedObject):
    """
        quickdoc
    """

    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        if not isinstance(value, str):
            raise TypeError("place_id must be a str")
        if not idChecksum(value):
            raise InvalidIDError("invalid place_id for review")
        if not idExists(value, Review):
            raise IDDoesNotExistError("place_id doesn't pair with a place")
        self.__place_id = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if not isinstance(value, str):
            raise TypeError("user_id must be a str")
        if not idChecksum(value):
            raise InvalidIDError("invalid user_id for review")
        if not idExists(value, Review):
            raise IDDoesNotExistError("user_id doesn't pair with a user")
        self.__user_id = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int):
            raise TypeError("rating must be an int")
        if value < 0 or value > 10:
            raise ValueError("rating must be >= 0 and <= 10")
        self.__rating = value

    @property
    def comment(self):
        return self.__comment

    @comment.setter
    def comment(self, value):
        if not isinstance(value, str):
            raise TypeError("comment must be a str")
        self.__comment = value
