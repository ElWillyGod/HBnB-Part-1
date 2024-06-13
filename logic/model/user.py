
'''
    Defines the User class.
    This class is identified by either it's id or it's email,
    as both are unique within the database.
'''

from trackedobject import TrackedObject
from validationlib import isUserEmailDuplicated
from logicexceptions import EmailDuplicated


class User(TrackedObject):
    '''
        User Class

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        email (str): Email of user, unique.
        first_name (str): First name of user.
        last_name (str): Last name of user.
    '''

    def __init__(self, email, first_name, last_name,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        self.first_name = first_name
        self.last_name = last_name
        if isUserEmailDuplicated(email):
            raise EmailDuplicated("email already exists")
        self.email = email
