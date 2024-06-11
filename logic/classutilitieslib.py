
'''
    Defines utilities to be used later in the code.
    Most notably class type utilites.
'''

from user import User
from city import City
from country import Country
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

def typeExists(type_of_data: str) -> bool:
    '''
        Checks if the parameter corresponds with an existing class.
    '''

    for cls in classes:
        if cls[0] == type_of_data:
            return True
    return False

def getPlural(name: str) -> str:
    '''
        Gets the plural string of a class.
    '''

    for clas in classes:
        if name == clas[0]:
            return clas[1]
    raise ValueError("class not found")

def getClassByName(name):
    '''
        Gets a class by it's singular name (classes[0])
    '''

    for cls in classes:
        if cls[0] == name:
            return cls[2]

    raise ValueError("class not found")
