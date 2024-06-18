
'''
    Defines custom exceptions.
    Most are when data from the persistance layer conflicts with new data.
'''


class MoreThanOneReview(Exception):  # 400
    '''
        Called when trying to make more than one review of a place.
    '''

    pass


class TryingToReviewOwnPlace(Exception):  # 400
    '''
        Called when the reviewer id and the host id of the place match.
    '''

    pass


class CountryNotFoundError(Exception):  # 404
    '''
        Called when a country code does not correspond to a country.
    '''

    pass


class IDNotFoundError(Exception):  # 404
    '''
        Called when trying to get, delete or update by id and the id does
        not correspond to an existing object.
    '''

    pass


class EmailDuplicated(Exception):  # 409
    '''
        Called when trying to set an email and there's a different user with
        the same email.
    '''

    pass


class CityNameDuplicated(Exception):  # 409
    '''
        Called when trying to set a city that has the same name as another in
        the same country
    '''

    pass


class AmenityNameDuplicated(Exception):  # 409
    '''
        Called when trying to set an email and there's a different user with
        the same email.
    '''

    pass
