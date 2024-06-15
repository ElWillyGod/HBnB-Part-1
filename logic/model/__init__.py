
'''
    Defines this folder as a package

    Also makes classes accesable through the package.
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
