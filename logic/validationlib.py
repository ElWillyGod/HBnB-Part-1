
'''
    Defines validation functions.
    Some make calls to the persistance layer.
'''

from string import ascii_letters, digits, ascii_lowercase
import json

from persistence.persistence_manager import FileDataManager, CountryDataManager

countries = json.loads(CountryDataManager.get())


def idExists(id: str, cls:str) -> bool: 
    '''
        Calls persistance layer to see if an id within cls exists.
    '''

    call = json.loads(FileDataManager.get(id, cls))
    if len(call) == 0:
        return False
    return True

def idChecksum(id: str) -> bool:
    '''
        Checks if an id's lenght is valid.
    '''

    return len(id) == 32


def isUserEmailDuplicated(email: str) -> bool:
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = json.loads(FileDataManager.getByAttr(email, "users"))
    if len(call) == 0:
        return False
    return True


def isCountryValid(country_code: str) -> bool:
    '''
        Checks if a country's code is valid.
    '''

    if len(country_code) != 2:
        return False
    for char in country_code:
        if char not in ascii_lowercase:
            return False
    return True


def getCountry(country_code: str):
    '''
        Gets a country object by code.
    '''

    for country in countries:
        if country.code == country_code:
            return country
    raise Exception("country not found")


def doesCountryExist(country_code: str) -> bool:
    '''
        Checks if a country exists.
    '''

    for country in countries:
            if country.code == country_code:
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


def isCoordinateValid(coord) -> bool:
    '''
        status = WIP(0%)
    '''

    return True


def isDatetimeValid(dtt) -> bool:
    '''
        status = WIP(0%)
    '''

    return True
