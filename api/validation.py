#!/usr/bin/python3
"""validaciones de los endpoint"""
from string import ascii_letters, digits, ascii_lowercase


def idChecksum(id: str) -> bool: # TUYO
    '''
        Checks if an id's lenght is valid.
    '''

    return len(id) == 32



def isCountryValid(country_code: str) -> bool: # TUYO
    '''
        Checks if a country's code is valid.
    '''

    if len(country_code) != 2:
        return False
    for char in country_code:
        if char not in ascii_lowercase:
            return False
    return True



def isStrValid(string, ignoreStr: str="", ignoreDigits=True) -> bool: # TUYO
    '''
        Checks if the string does not have any special character aside
        from chars from ignoreStr.
    '''

    if not string.isascii():
        return False
    
    if not string.isprintable():
        return False

    for char in string:
        if char not in ascii_letters and char not in ignoreStr:
            if not ignoreDigits and char in digits:
                return False
    return True


def isLatitudeValid(latitude) -> bool: # TUYO
    '''
        Check if the latitude is valid.
    '''

    return latitude >= -90 and latitude <= 90


def isLongitudeValid(longitude) -> bool: # TUYO
    '''
        Checks if the longitude is valid.
    '''

    return longitude >= -180 and longitude <= 180


def isNameValid(string: str) -> bool: # TUYO
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


def isEmailValid(email: str) -> bool: # TUYO
    
    return isStrValid(email)
