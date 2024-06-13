
'''
    Defines the amenity class.
    An amenity is something that places have.
'''

from trackedobject import TrackedObject


class Amenity(TrackedObject):
    '''
        status = Complete

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
        self.name = name

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError("name must be a string")
        self.__name = value
