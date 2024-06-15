
'''
    Defines validation functions.
    Makes calls to the persistance layer.
'''

from persistence.persistence_manager import FileDataManager, CountryDataManager

countries = CountryDataManager.get()


def idExists(id: str, cls: str) -> bool:
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


def isAmenityDuplicated(name: str) -> bool:
    '''
        Calls persistance layer to see if a user has the same email.
    '''

    call = FileDataManager.getByAttr(name, "amenities")

    if len(call) == 0:
        return False

    return True


def isCityNameDuplicated(name: str, code: str) -> bool:
    '''
        Calls persistance layer to see if a city has the same name.
    '''

    call = FileDataManager.getAllWithProperty("cities", "country_code", code)

    for city in call:
        if city["name"] == name:
            return True

    return False


def isOwnerIDTheSame(place_id: str, user_id: str) -> bool:
    '''
        Calls persistance layer to compare the owner id of a place with the
        given id.
    '''

    call = FileDataManager.get(place_id)

    return call["host_id"] == user_id


def getCountry(country_code: str):
    '''
        Gets a country object by code.
    '''

    for country in countries:
        if country["code"] == country_code:
            return country

    raise Exception("country not found")


def doesCountryExist(country_code: str) -> bool:
    '''
        Checks if a country exists.
    '''

    for country in countries:
        if country["code"] == country_code:
            return False

    return True
