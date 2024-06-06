#!/usr/bin/python3

'''
    quickdoc
'''

from trackedobject import TrackedObject


class Place(TrackedObject):
    """
        quickdoc
    """

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

    @property
    def host_id(self):
        return self.__host_id

    @host_id.setter
    def host_id(self, value):
        if False:
            raise NotImplementedError
        self.__host_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if False:
            raise NotImplementedError
        self.__name = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if False:
            raise NotImplementedError
        self.__description = value

    @property
    def number_of_rooms(self):
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        if False:
            raise NotImplementedError
        self.__number_of_rooms = value

    @property
    def number_of_bathrooms(self):
        return self.__number_of_bathrooms

    @number_of_bathrooms.setter
    def number_of_bathrooms(self, value):
        if False:
            raise NotImplementedError
        self.__number_of_bathrooms = value

    @property
    def city_id(self):
        return self.__max_guests

    @city_id.setter
    def city_id(self, value):
        if False:
            raise NotImplementedError
        self.__city_id = value

    @property
    def price_per_night(self):
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        if False:
            raise NotImplementedError
        self.__price_per_night = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if False:
            raise NotImplementedError
        self.__latitude = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if False:
            raise NotImplementedError
        self.__longitude = value

    @property
    def city_id(self):
        return self.__city_id

    @city_id.setter
    def city_id(self, value):
        if False:
            raise NotImplementedError
        self.__city_id = value

    @property
    def amenity_ids(self):
        return self.__amenity_ids

    @amenity_ids.setter
    def amenity_ids(self, value):
        if False:
            raise NotImplementedError
        self.__amenity_ids = value
