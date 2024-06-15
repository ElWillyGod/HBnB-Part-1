
'''
    Defines validation functions.
    Makes calls to the persistance layer.
'''

from logic.logicexceptions import CountryNotFoundError
from persistence.persistence_manager import FileDataManager, CountryDataManager

countries = CountryDataManager.get()


def idExists(id: str, cls:str) -> bool: 
    '''
        Calls persistance layer to see if an id of type cls exists.
    '''

    call = FileDataManager.get(id, cls)

    if len(call) == 0:
        return False

    return True


def isUserEmailDuplicated(email: str) -> bool:
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = FileDataManager.getByAttr(email, "users")

    if len(call) == 0:
        return False

    return True


def getCountry(country_code: str):
    '''
        Gets a country object by code.
    '''

    for country in countries:
        if country.code == country_code:
            return country

    raise CountryNotFoundError("country not found")


def doesCountryExist(country_code: str) -> bool:
    '''
        Checks if a country exists.
    '''

    for country in countries:
            if country.code == country_code:
                return False

    return True
