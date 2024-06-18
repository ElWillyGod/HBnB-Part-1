
"""
    Endpoint validation library.
"""



def idChecksum(id: str) -> bool:
    '''
        Checks if an id's lenght is valid.
    '''

    return len(id) == 36



def isCountryValid(country_code: str) -> bool:
    '''
        Checks if a country's code is valid.
    '''

    if len(country_code) != 2:
        return False

    for char in country_code:
        if not char.isupper():
            return False

    return True



def isStrValid(string: str, ignoreStr: str="", ignoreDigits=True) -> bool:
    '''
        Checks if the string does not have any special character aside
        from chars from ignoreStr.
    '''
    if len(string) == 0:
        return False

    if not string.isascii():
        return False
    
    if not string.isprintable():
        return False

    for char in string:
        if not char.isalpha() and char not in ignoreStr:
            if not ignoreDigits and char.isdigit():
                return False
    return True


def isLatitudeValid(latitude: float) -> bool:
    '''
        Check if the latitude is valid.
    '''

    return latitude >= -90 and latitude <= 90


def isLongitudeValid(longitude: float) -> bool:
    '''
        Checks if the longitude is valid.
    '''

    return longitude >= -180 and longitude <= 180


def isNameValid(string: str) -> bool:
    '''
        Checks if a name is valid.

        Returns false if:
            str is not valid having no special character aside from:
                '-', '_', ' '.
            starts with a special character or digit.
    '''

    if not isStrValid(string, "-_ "):
        return False

    if not string[0].isalpha():
        return False

    return True


def isEmailValid(email: str) -> bool:
    '''
        Checks if an email is valid

        Returns false if:
            it has a restrained special character,
            it has spaces,
            has not exactly one '@',
            empty before the '@',
            has not at least one '.' that is after the '@',
            empty between '@' and '.',
            has special characters, or digits after the '@',
            empty after any '.'.

        valid example: "user@gmail.com"
        valid example: "user@ceibal.edu.uy"
    '''
    
    if " " in email:
        return False

    if not isStrValid(email, "@.!#$%&/*+-_?'^`~{}"):
        return False

    if email.count("@") != 1:
        return False

    if email.count(".") == 0:
        return False

    last_index = 0

    # checks name
    empty_flag = True
    for i, char in enumerate(email):
        if char == "@":
            if empty_flag:
                return False
            else:
                last_index = i
                break
        else:
            empty_flag = False

    # checks domain
    empty_flag = True
    encountered_dot = False
    for i, char in enumerate(email[last_index + 1:]):
        if char == ".":
            encountered_dot = True
            if empty_flag:
                return False
            else:
                empty_flag = True
        elif not char.isalnum():
            return False
        else:
            empty_flag = False
    if empty_flag or not encountered_dot:
        return False

    return True


def isNoneFields(enty: str, data: dict) -> bool:

    required_fields = []

    if enty == 'user':
        required_fields = ['email', 'first_name', 'last_name']

    if enty == 'city':
        required_fields = ['name', 'country_code']

    if enty == 'amenity':
        required_fields = ['name']

    if enty == 'place':
        required_fields = ['name', 'description', 'city_id',  # 'address',
                           'latitude', 'longitude', 'host_id', 'number_of_rooms',
                           'number_of_bathrooms', 'price_per_night', 'max_guests',
                           'amenity_ids']
    if enty == 'review':
        required_fields = ['user_id', 'rating', 'comment']

    if len(data) != len(required_fields):
        return True

    for field in required_fields:

        if field not in data:
            return True

    return False
