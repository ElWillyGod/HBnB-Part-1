
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import idExists, isOwnerIDTheSame
from logic.model.logicexceptions import IDNotFoundError, TryingToReviewOwnPlace


class Review(TrackedObject):
    """
        Review Class.
    """

    def __init__(self,
                 place_id: str,
                 user_id: str,
                 rating: int,
                 comment: str,
                 *,
                 id: str = None,
                 created_at: str = None,
                 updated_at: str = None,
                 update: dict | None = None
                 ) -> None:
        super().__init__(id, created_at, updated_at)
        if not idExists(place_id, "places"):
            raise IDNotFoundError("place_id doesn't pair with a place")
        if not idExists(user_id, "users"):
            raise IDNotFoundError("user_id doesn't pair with a user")
        if isOwnerIDTheSame(place_id, user_id):
            raise TryingToReviewOwnPlace("you cannot review your own place")
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id
        self.comment = comment
