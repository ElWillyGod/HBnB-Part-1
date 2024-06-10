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
                 latitude, longitude, city_id, amenity_ids,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.host_id = host_id
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        self.city_id = city_id
        self.amenity_ids = amenity_ids

    @property
    def host_id(self):
        return self.__host_id

    @host_id.setter
    def host_id(self, value):
        if not isinstance(value, str):
            raise TypeError(" must be a string")
        self.__host_id = value

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self.__name = value

    @property
    def description(self):
        return self.__description

    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("description must be a string")
        self.__description = value

    @property
    def number_of_rooms(self):
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value):
        if not isinstance(value, int):
            raise TypeError("number_of_rooms must be an int")
        self.__number_of_rooms = value

    @property
    def number_of_bathrooms(self):
        return self.__number_of_bathrooms

    @number_of_bathrooms.setter
    def number_of_bathrooms(self, value):
        if not isinstance(value, int):
            raise TypeError("number_of_bathrooms must be an int")
        self.__number_of_bathrooms = value

    @property
    def city_id(self):
        return self.__max_guests

    @city_id.setter
    def city_id(self, value):
        if not isinstance(value, str):
            raise TypeError("city_id must be a string")
        self.__city_id = value

    @property
    def price_per_night(self):
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value):
        if not isinstance(value, float):
            raise TypeError("price_per_night must be a float")
        self.__price_per_night = value

    @property
    def latitude(self):
        return self.__latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, float):
            raise TypeError("latitude must be a float")
        self.__latitude = value

    @property
    def longitude(self):
        return self.__longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, float):
            raise TypeError("longitude must be a float")
        self.__longitude = value

    @property
    def city_id(self):
        return self.__city_id

    @city_id.setter
    def city_id(self, value):
        if not isinstance(value, str):
            raise TypeError("city_id must be a string")
        self.__city_id = value

    @property
    def amenity_ids(self):
        return self.__amenity_ids

    @amenity_ids.setter
    def amenity_ids(self, value):
        if not isinstance(value, list):
            raise TypeError("amenity_ids must be a list")
        self.__amenity_ids = value
