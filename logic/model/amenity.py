
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import isAmenityDuplicated
from logic.logicexceptions import AmenityNameDuplicated


class Amenity(TrackedObject):
    '''
        Amenity Class.
    '''

    def __init__(self,
                 name: str,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None):
        super().__init__(id, created_at, updated_at)

        if isAmenityDuplicated(name):
            raise AmenityNameDuplicated("amenity already exists")
        self.name = name
