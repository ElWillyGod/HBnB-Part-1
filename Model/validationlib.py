#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject
from user import User
from citycountry import City, Country
from amenity import Amenity
from place import Place
from review import Review

from string import ascii_lowercase


classes = [
           ["user", "users", User],
           ["city", "cities", City],
           ["country", "countries", Country],
           ["amenity", "amenities", Amenity],
           ["place", "places", Place],
           ["review", "reviews", Review]
          ]


def typeExists(type_of_data) -> bool:
    '''
        quickdoc
    '''

    for cls in all_types:
        if cls.__name__ == type_of_data:
            return True
    return False


def idExists(id: str, cls) -> bool: 
    '''
        quickdoc
    '''

    raise NotImplementedError

def idChecksum(id: str) -> bool:
    '''
        quickdoc
    '''

    return len(id) == 32


def isUserEmailDuplicated(email: str) -> bool:
    '''
        quickdoc
    '''

    raise NotImplementedError


def isCountryValid(country_code: str) -> bool:
    '''
        quickdoc
    '''

    raise NotImplementedError


def isStrValid(string, ignoreStr="": str) -> bool:
    '''
        Returns False if:
            is not a string,
            is empty,
            has any spaces,
            has any special character aside from chars from ignoreStr
    '''

    for char in string:
        if char not in ascii_lowercase and char not in ignoreStr:
            return False
    return True


def isNameValid(string: str) -> bool:
    '''
        Returns false if:
            str is not valid,
            has any special character aside from '-', '_'
    '''

    if not isStrValid(string, "-_"):
        return False

    return True


def isEmailValid(string: str) -> bool:
    '''
        Returns false if:
            str is not valid,
            has any special character aside from '-', '_', '.', '@',
            has exactly one '@',
            not empty after '@',
            has at least one '.' and no '-', '_' after the '@'
    '''

    if not isStrValid(string, "-_.@"):
        return False

    return True
