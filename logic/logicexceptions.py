
'''
    Defines custom exceptions.
    Most are when data from the persistance layer conflicts with new data.
'''


class CountryNotFoundError(Exception):
    '''
        Called when a country code does not correspond to a country.
    '''

    pass

class EmailDuplicated(Exception):
    '''
        Called when trying to set an email and there's a different user with
        the same email.
    '''

    pass

class IDNotFoundError(Exception):
    '''
        Called when trying to get, delete or update by id and the id does
        not correspond to an existing object.
    '''

    pass
