#!/usr/bin/python3

'''
    Defines validation functions.
    Some make calls to the persistance layer.
'''

from string import ascii_letters, digits
from logic.classutilitieslib import classes

from persistence.persistence_manager import countryDataManager

countries = countryDataManager.get()


def idExists(id: str, cls) -> bool: 
    '''
        status = WIP (0%)

        Calls persistance layer to see if an id within cls exists.
    '''

    raise NotImplementedError

def idChecksum(id: str) -> bool:
    '''
        Checks if an id's lenght is valid.
    '''

    return len(id) == 32


def isUserEmailDuplicated(email: str) -> bool:
    '''
        status = WIP (0%)

        Calls persistance layer to see if a user has the same email.
    '''

    raise NotImplementedError


def isCountryValid(country_code: str) -> bool:
    '''
        Checks if a country's code is valid.
    '''

    if False:
        pass
    return True


def getCountry(country_code: str):
    '''
        GIL
    '''

    return country


def doesCountryExist(country_code: str) -> bool:
    '''
        GIL
    '''

    for country in countries:
            if country.code == code:
                return False

    return True


def isStrValid(string, ignoreDigits=True, ignoreStr: str="") -> bool:
    '''
        Checks if the string does not have any special character aside
        from chars from ignoreStr.
    '''

    for char in string:
        if char not in ascii_letters and char not in ignoreStr:
            if not ignoreDigits and char in digits:
                return False
    return True


def isNameValid(string: str) -> bool:
    '''
        Checks if a name is valid.

        Returns false if:
            str is not valid having no special character aside from:
                '-', '_', ' '.
            starts with a special character or digit.
    '''

    if not isStrValid(string, "-_ "):
        return False

    if string[0] not in ascii_letters:
        return False

    return True


def isEmailValid(string: str) -> bool:
    '''
        status = WIP (10%)

        Returns false if:
            it haves a special character aside from:
                '-', '_', '.', '@'
            starts with a special character or digit,
            has not exactly one '@',
            empty before the '@',
            has not at least one '.' and is after the '@',
            empty between '@' and '.',
            special characters, or digits after the '@',
            empty after the '.'.

        valid example: "user@gmail.com"
        valid example: "user@ceibal.edu.uy"
    '''

    if not isStrValid(string, "-_.@"):
        return False

    return True


def isCoordinateValid(coord):
    '''
        status = WIP(0%)
    '''

    pass


def isDatetimeValid(dtt):
    '''
        status = WIP(0%)
    '''

    pass
