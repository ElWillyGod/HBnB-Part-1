
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from trackedobject import TrackedObject
from validationlib import idExists
from logicexceptions import IDNotFoundError


class Review(TrackedObject):
    """
        Review Class

        from TrackedObject:
            id (str): UUID4 as hex.
            created_at: datetime as string at time of creation.
            updated_at: datetime as string at time of last update.
            update_time() -> None: Updates the updated_at attribute.
            toJson() -> str: Returns a JSON representation of this object.

        place_id (str): ID of place as hex
        user_id (str): ID of user as hex.
        rating (int): How much points it gives to the place.
        comment (str): A comment of why the rating was chose.
    """

    def __init__(self, place_id, user_id, rating, comment,
                 *, id=None, created_at=None, updated_at=None):
        super().__init__(id, created_at, updated_at)
        if rating <= 0 or rating > 5:
            raise ValueError("rating must be > 0 and <= 5")
        self.rating = rating
        if not idExists(place_id, Review):
            raise IDNotFoundError("place_id doesn't pair with a place")
        self.place_id = place_id
        if not idExists(user_id, Review):
            raise IDNotFoundError("user_id doesn't pair with a user")
        self.user_id = user_id
        self.comment = comment
