
'''
    Module that handles the deletion of reviews when deleting it's place
    and a place when deleting it's host.
'''

from logic import DM


def placeDeletedEvent(object: dict) -> None:
    '''
        Deletes all associated reviews of place.
    '''

    reviews = DM.get_by_property("reviews", "place_id", object["id"])

    for review in reviews:
        DM.delete(review["id"], "reviews")
        raiseDeleteEvent("review", review)

def userDeletedEvent(object: dict) -> None:
    '''
        Deletes all associated places of user.
    '''

    places = DM.get_by_property("places", "host_id", object["id"])

    for place in places:
        DM.delete(place["id"], "places")
        raiseDeleteEvent("place", place)

    reviews = DM.get_by_property("reviews", "user_id", object["id"])

    for review in reviews:
        DM.delete(review["id"], "reviews")
        raiseDeleteEvent("review", review)

def raiseDeleteEvent(type: str, object: dict) -> None:
    '''
        Called when an object is deleted.
    '''

    if type == "place" or type == "places":
        placeDeletedEvent(object)
    elif type == "user" or type == "users":
        userDeletedEvent(object)
