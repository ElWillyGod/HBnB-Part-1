
'''
    Defines custom exceptions.
    Most are when data from the persistance layer conflicts with new data.
'''


class CountryNotFoundError(Exception): #404
    '''
        Called when a country code does not correspond to a country.
    '''

    pass

class EmailDuplicated(Exception): #409
    '''
        Called when trying to set an email and there's a different user with
        the same email.
    '''

    pass

class AmenityNameDuplicated(Exception): #409
    '''
        Called when trying to set an email and there's a different user with
        the same email.
    '''

    pass

class IDNotFoundError(Exception): #404
    '''
        Called when trying to get, delete or update by id and the id does
        not correspond to an existing object.
    '''

    pass
