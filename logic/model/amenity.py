
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from trackedobject import TrackedObject
from validationlib import doesAmenityExist
from logicexceptions import AmenityNameDuplicated


class Amenity(TrackedObject):
    '''
        Amenity Class

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        name (str): Name of amenity.
    '''

    def __init__(self, name,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        if not doesAmenityExist(name):
            raise AmenityNameDuplicated("amenity already exists")
        self.name = name
