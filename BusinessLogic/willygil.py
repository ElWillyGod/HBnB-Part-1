#!/usr/bin/python3


'''
    Cosas importantes.
'''

from abc import ABC
from datetime import datetime
import uuid


class TrackedObject(ABC):
    '''
        quickdoc
    '''

    def __init__(self):
        now = datetime.now()
        self.__created_at = now
        self.__updated_at = now
        self.__id = uuid.uuid4()

    def update_time(self):
        self.__updated_at = datetime.now()


class User(TrackedObject):
    '''
        quickdoc
    '''

    def __init__(self, email, first_name, last_name):
        super().__init__()
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name


class Place(TrackedObject):
    """ place init"""

    def __init__(self, host_id, name, description, number_of_rooms,
                 number_of_bathrooms, max_guests, price_per_night,
                 latitude, longitude, city_id, amenity_ids):

        super().__init__()
        self.__host_id = host_id
        self.__name = name
        self.__description = description
        self.__number_of_rooms = number_of_rooms
        self.__number_of_bathrooms = number_of_bathrooms
        self.__max_guests = max_guests
        self.__price_per_night = price_per_night
        self.__latitude = latitude
        self.__longitude = longitude
        self.__city_id = city_id
        self.__amenity_ids = amenity_ids


class City(TrackedObject):
    """City init"""

    def __init__(self, name, country_code):
        super().__init__()
        self.__name = name
        self.__country_code = country_code


class Country(TrackedObject):
    """code and name"""

    def __init__(self, code, name):
        self.__code = code
        # arreglar para sacar los codigos, con api o de una
        self.__name = name


class Review(TrackedObject):
    """cositas"""

    def __init__(self, place_id, user_id, rating, comment):
        super().__init__()
        self.__place_id = place_id
        self.__user_id = user_id
        self.__rating = rating
        self.__comment = comment
