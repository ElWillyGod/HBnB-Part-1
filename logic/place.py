
'''
    Defines the Place Class.
'''

from trackedobject import TrackedObject
from validationlib import (
    idChecksum, isCoordinateValid, idExists, isNameValid)


class Place(TrackedObject):
    """
        status = Completed

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        host_id (str): ID of the user that has ownership of the place.
        name (str): Name of the place.
        description (str): Description of the place.
        number_of_rooms (int): Number of rooms.
        number_of_bathrooms (int): Number of bathrooms.
        max_guests (int): Maximum amount of guests that the place can have.
        price_per_night (float): Price per night in dollars.
        latitude (float): Latitude of the location of the place.
        longitude (float): Longitude of the location of the place.
        city_id (str): ID of the city where the place resides.
        amenity_ids (list(str)): List of all the ID of amenities.
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
    def host_id(self) -> str:
        return self.__host_id

    @host_id.setter
    def host_id(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("host_id must be a string")
        if not idChecksum(value):
            raise ValueError('invalid host_id')
        if not idExists(value):
            raise idExists("host_id does not exist")
        self.__host_id = value

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        if not isNameValid(value):
            raise ValueError("invalid name")
        self.__name = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("description must be a string")
        self.__description = value

    @property
    def number_of_rooms(self) -> int:
        return self.__number_of_rooms

    @number_of_rooms.setter
    def number_of_rooms(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError("number_of_rooms must be an int")
        if value < 0:
            raise ValueError("number_of_rooms must be >= 0")
        self.__number_of_rooms = value

    @property
    def number_of_bathrooms(self) -> int:
        return self.__number_of_bathrooms

    @number_of_bathrooms.setter
    def number_of_bathrooms(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError("number_of_bathrooms must be an int")
        if value < 0:
            raise ValueError("number_of_bathrooms must be >= 0")
        self.__number_of_bathrooms = value

    @property
    def price_per_night(self) -> float:
        return self.__price_per_night

    @price_per_night.setter
    def price_per_night(self, value) -> None:
        if not isinstance(value, float):
            raise TypeError("price_per_night must be a float")
        if value <= 0:
            raise ValueError("price_per_night must be > 0")
        self.__price_per_night = value

    @property
    def latitude(self) -> float:
        return self.__latitude

    @latitude.setter
    def latitude(self, value) -> None:
        if not isinstance(value, float):
            raise TypeError("latitude must be a float")
        if not isCoordinateValid(value):
            raise ValueError("invalid latitude")
        self.__latitude = value

    @property
    def longitude(self) -> float:
        return self.__longitude

    @longitude.setter
    def longitude(self, value) -> None:
        if not isinstance(value, float):
            raise TypeError("longitude must be a float")
        if not isCoordinateValid(value):
            raise ValueError("invalid longitude")
        self.__longitude = value

    @property
    def city_id(self) -> str:
        return self.__city_id

    @city_id.setter
    def city_id(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("city_id must be a string")
        if not idChecksum(value):
            raise ValueError('invalid city_id')
        if not idExists(value):
            raise idExists("city_id does not exist")
        self.__city_id = value

    @property
    def amenity_ids(self) -> list:
        return self.__amenity_ids

    @amenity_ids.setter
    def amenity_ids(self, value) -> None:
        if not isinstance(value, list):
            raise TypeError("amenity_ids must be a list")
        for id in value:
            if not isinstance(id, str):
                raise TypeError("amenity_ids must be a list of strings")
            if not idChecksum(id):
                raise ValueError(f"'{id}' in amenity_ids is invalid")
            if not idExists(id):
                raise idExists(f"'{id}' in amenity_ids does not exist")
        self.__amenity_ids = value
