
'''
    Defines TrackedObject class.
    This abstract class defines common elements and passes them down to most
    other classes.
'''

from abc import ABC
from datetime import datetime
import uuid
import json
import inspect


class TrackedObject(ABC):
    '''
        id (str): UUID4 as hex.
        created_at: datetime as string at time of creation.
        updated_at: datetime as string at time of last update.
        update_time() -> None: Updates the updated_at attribute.
        toJson() -> str: Returns a JSON representation of this object.
    '''

    def __init__(self,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None):
        now = str(datetime.now())
        self.created_at = now if created_at is None else created_at
        self.updated_at = now if updated_at is None else updated_at
        self.id = str(uuid.uuid4()) if id is None else id

    def getAllInstanceAttributes(self):
        attributes = inspect.getmembers(self,
                                        lambda a: not inspect.isroutine(a))
        return {key: value for key, value in attributes
                if not (key[0:2] == "__" and key[-2:] == "__")
                and not key == "_abc_impl"}

    def toJson(self) -> str:
        return self.getAllInstanceAttributes()
