
'''
    quickdoc
'''

from user import User
from citycountry import City, Country
from amenity import Amenity
from place import Place
from review import Review


classes = [
           ["user", "users", User],
           ["city", "cities", City],
           ["country", "countries", Country],
           ["amenity", "amenities", Amenity],
           ["place", "places", Place],
           ["review", "reviews", Review]
          ]

def typeExists(type_of_data) -> bool:
    '''
        quickdoc
    '''

    for cls in classes:
        if cls.__name__ == type_of_data:
            return True
    return False