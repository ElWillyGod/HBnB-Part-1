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


def typeExists(type_of_data) -> bool:
    '''
        quickdoc
    '''

    all_types = [TrackedObject, User, City, Country, Amenity, Place, Review]
    for cls in all_types:
        if cls.__name__ == type_of_data:
            return True
    return False

def idExists(id:str, cls) -> bool:
    '''
        quickdoc
    '''

    raise NotImplementedError

def idChecksum(id:str) -> bool:
    '''
        quickdoc
    '''

    return len(id) == 32

def isUserEmailDuplicated(email:str) -> bool:
    '''
        quickdoc
    '''

    raise NotImplementedError

def countryExistsAndIsValid(country_code:str) -> bool:
    '''
        quickdoc
    '''

    raise NotImplementedError
