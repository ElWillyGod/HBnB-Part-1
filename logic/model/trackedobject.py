
'''
    Defines TrackedObject class.
    This abstract class defines common elements and passes them down to most
    other classes.
'''

from abc import ABC
from datetime import datetime
import uuid
import json


class TrackedObject(ABC):
    '''
        status = WIP (75%) needs some implementation and testing

        id (str): UUID4 as hex.
        created_at: datetime as string at time of creation.
        updated_at: datetime as string at time of last update.
        update_time() -> None: Updates the updated_at attribute.
        toJson() -> str: Returns a JSON representation of this object.
    '''

    def __init__(self, id=None, created_at=None, updated_at=None):
        now = str(datetime.now())
        self.created_at = now if created_at is None else created_at
        self.updated_at = now if updated_at is None else updated_at
        self.id = str(uuid.uuid4()) if id is None else id

    def update_time(self) -> None:
        self.__updated_at = str(datetime.now())

    def getAllInstanceAttributes(self):
        return {key: value for key, value in vars(self)
                if not (key[0:2] == "__" and key[-2:0] == "__")}

    def toJson(self, *, update=None) -> str:
        if update is None:
            try:
                instance_vars = self.getAllInstanceAttributes()
                converted_data = json.dumps(instance_vars)
                output = self(converted_data)
            except Exception:
                raise ValueError("object conversion to json failed")
        else:
            try:
                instance_vars = self.getAllInstanceAttributes()
                instance_vars.pop()
                output.update({})
                converted_data = json.dumps(instance_vars)
                output = update
            except Exception:
                raise ValueError("object conversion to json failed")
        return output
