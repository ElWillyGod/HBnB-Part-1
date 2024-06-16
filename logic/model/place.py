
'''
    Defines the Place Class.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import idExists
from logic.logicexceptions import IDNotFoundError


class Place(TrackedObject):
    """
        Place Class.
    """

    def __init__(self,
                 host_id: str,
                 name: str,
                 description: str,
                 number_of_rooms: int,
                 number_of_bathrooms: int,
                 max_guests: int,
                 price_per_night: float,
                 latitude: float,
                 longitude: float,
                 city_id: str,
                 amenity_ids: list[str],
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 update: bool = False
                 ) -> None:
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
                raise IDNotFoundError(f"'{id}' in amenity_ids does not exist")
        self.amenity_ids = amenity_ids
