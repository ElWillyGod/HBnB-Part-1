#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject


class Review(TrackedObject):
    """
        quickdoc
    """

    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.__place_id = place_id
        self.__user_id = user_id
        self.__rating = rating
        self.__comment = comment

    @property
    def place_id(self):
        return self.__place_id

    @place_id.setter
    def place_id(self, value):
        if False:
            raise NotImplementedError
        self.__place_id = value

    @property
    def user_id(self):
        return self.__user_id

    @user_id.setter
    def user_id(self, value):
        if False:
            raise NotImplementedError
        self.__user_id = value

    @property
    def rating(self):
        return self.__rating

    @rating.setter
    def rating(self, value):
        if False:
            raise NotImplementedError
        self.__rating = value

    @property
    def comment(self):
        return self.__rating

    @comment.setter
    def comment(self, value):
        if False:
            raise NotImplementedError
        self.__comment = value
