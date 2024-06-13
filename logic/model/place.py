
'''
    Defines the Place Class.
'''

from trackedobject import TrackedObject
from validationlib import idExists


class Place(TrackedObject):
    """
        Place Class

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
        if not idExists(host_id):
            raise idExists("host_id does not exist")
        self.host_id = host_id
        self.name = name
        self.description = description
        self.number_of_rooms = number_of_rooms
        self.number_of_bathrooms = number_of_bathrooms
        self.max_guests = max_guests
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        if not idExists(city_id):
            raise idExists("city_id does not exist")
        self.city_id = city_id
        for id in amenity_ids:
            if not idExists(id):
                raise idExists(f"'{id}' in amenity_ids does not exist")
        self.amenity_ids = amenity_ids
