#!/usr/bin/python3

'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from trackedobject import TrackedObject
from validationlib import *
from logicexceptions import IDNotFoundError


class Review(TrackedObject):
    """
        status = Completed

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        place_id (str): ID of place as hex
        user_id (str): ID of user as hex.
        rating (int): How much points it gives to the place.
        comment (str): A comment of why the rating was chose.
    """

    def __init__(self, place_id, user_id, rating, comment,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.place_id = place_id
        self.user_id = user_id
        self.rating = rating
        self.comment = comment

    @property
    def place_id(self) -> str:
        return self.__place_id

    @place_id.setter
    def place_id(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("place_id must be a str")
        if not idChecksum(value):
            raise ValueError("invalid place_id for review")
        if not idExists(value, Review):
            raise IDNotFoundError("place_id doesn't pair with a place")
        self.__place_id = value

    @property
    def user_id(self) -> str:
        return self.__user_id

    @user_id.setter
    def user_id(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("user_id must be a str")
        if not idChecksum(value):
            raise ValueError("invalid user_id for review")
        if not idExists(value, Review):
            raise IDNotFoundError("user_id doesn't pair with a user")
        self.__user_id = value

    @property
    def rating(self) -> int:
        return self.__rating

    @rating.setter
    def rating(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError("rating must be an int")
        if value <= 0 or value > 5:
            raise ValueError("rating must be > 0 and <= 5")
        self.__rating = value

    @property
    def comment(self) -> str:
        return self.__comment

    @comment.setter
    def comment(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("comment must be a str")
        self.__comment = value
