
'''
    Defines the Review class.
    Reviews are linked with a user and a review.
'''

from logic.model.trackedobject import TrackedObject
from logic.model.validationlib import idExists, isOwnerIDTheSame
from logic.logicexceptions import IDNotFoundError, TryingToReviewOwnPlace


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
                 updated_at: str = None):
        super().__init__(id, created_at, updated_at)

        if rating <= 0 or rating > 5:
            raise ValueError("rating must be > 0 and <= 5")
        self.rating = rating

        if not idExists(place_id, Review):
            raise IDNotFoundError("place_id doesn't pair with a place")
        self.place_id = place_id

        if not idExists(user_id, Review):
            raise IDNotFoundError("user_id doesn't pair with a user")
        if isOwnerIDTheSame(place_id, user_id):
            raise TryingToReviewOwnPlace("you cannot review your own place")
        self.user_id = user_id

        self.comment = comment
