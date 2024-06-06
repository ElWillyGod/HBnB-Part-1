#!/usr/bin/python3

'''
    Defines unit test cases for API.
    Tests for version 0.1

    Smoke tests for critical failiures upon importing the module.
    Sanity tests does something similar but more localized.

    Usage: in programs directory (API);
    python3 -m unittest -v tests/smoke_and_unit_tests.py

    To add more tests add them below the sanity tests.
    Remember that tests start with "test". Also they run in
    alphabetical order so name them "test_x_y_testname" where
    x is the test class, and y the test id within. This matters
    as if the sanity test fails all other tests are skipped.
'''

import unittest
import uuid


MODULE = "willygil"
AFTERSANITYSUCCESS = "\033[32mSanity ok\033[0m"
AFTERSANITYFAILURE = "\033[31mSanity fail\033[0m"
AFTERSMOKESUCCESS = "\033[32mSmoke ok\033[0m"
AFTERSMOKEFAILURE = "\033[31m\033[5m\n   <<EXLPOSION NUCLEAR!!!>>\n\033[0m"


class SmokePass():
    '''
        Global variables didn't work. So doing it with class vars.
    '''

    passedSmoke = False


class API_1_Smoke(unittest.TestCase):
    '''
        Tests if the module doesn't cause a nuclear explosion.
    '''

    def tearDown(self):
        if hasattr(self._outcome, 'errors'):
            # Python 3.4 - 3.10  (These two methods have no side effects)
            result = self.defaultTestResult()
            self._feedErrorsToResult(result, self._outcome.errors)
        else:
            # Python 3.11+
            result = self._outcome.result
        ok = all(test != self for test, text in
                 result.errors + result.failures)
        if ok:
            SmokePass.passedSmoke = True
            print(AFTERSMOKESUCCESS)
        else:
            print(AFTERSMOKEFAILURE)

    def test_1_01_smoke(self):
        __import__(MODULE)


class API_BaseTest(unittest.TestCase):
    '''
        Base class for tests.
    '''

    passedSanity = False
    isSanity = True

    def setUp(self):
        if not SmokePass.passedSmoke:
            self.skipTest("Smoke Test Failed")
        elif self.__class__.isSanity:
            pass
        elif not self.__class__.passedSanity:
            self.skipTest("Sanity Test Failed")
        return super().setUp()

    def tearDown(self) -> None:
        if self.__class__.isSanity:
            self.__class__.isSanity = False
            if not self.__class__.passedSanity:
                print(AFTERSANITYFAILURE)
        return super().tearDown()

    def sanityTest(self):
        self.createInstance()
        self.__class__.passedSanity = True
        print(AFTERSANITYSUCCESS)


class API_2_TrackedObject(API_BaseTest):
    '''
        Tests the TrackedObject class.
        TrackedObject()
    '''

    @classmethod
    def importClass(cls):
        return __import__(MODULE).TrackedObject

    @classmethod
    def createInstance(cls):
        TrackedObject = cls.importClass()
        return TrackedObject()

    def test_2_01_sanity(self):
        self.sanityTest()

    def test_2_02_basicOperations(self):
        to = self.createInstance()
        to.id
        to.created_at
        to.updated_at
        to.update_time()


class API_3_User(API_BaseTest):
    '''
        Tests the User class.
        User(email, first_name, last_name)
    '''

    @classmethod
    def importClass(cls):
        return __import__(MODULE).User

    @classmethod
    def createInstance(
        cls, email="test@test.com",
        first_name="tester",
            last_name="MCGee"):
        User = cls.importClass()
        return User(email, first_name, last_name)

    def test_3_01_sanity(self):
        self.sanityTest()

    def test_3_02_basic_Operations(self):
        user = self.createInstance()
        user.email
        user.first_name
        user.last_name

    def test_3_03_email_Type(self):
        ERRORMESSAGE = "email must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(email=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(email=69)

    def test_3_04_email_Emptiness(self):
        ERRORMESSAGE = "email must not be empty"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(email="")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(email="    ")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(email="@")

    def test_3_05_email_Format(self):
        ERRORMESSAGE = "email must have "
        with self.assertRaises(ValueError, msg=ERRORMESSAGE + "@"):
            self.createInstance(email="my_email")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE + "domain"):
            self.createInstance(email="my_email@")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE + "name"):
            self.createInstance(email="@gmail.com")

    def test_3_06_email_Spaces(self):
        ERRORMESSAGE = "email must not have spaces"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(email="    tester@gmail.com     ")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(email="test @gmail.com")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(email="test@g ma il.com")

    def test_3_07_first_name_Type(self):
        ERRORMESSAGE = "first_name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(first_name=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(first_name=69)

    def test_3_08_first_name_Emptiness(self):
        ERRORMESSAGE = "first_name must not be empty"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(first_name="")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(first_name="  ")

    def test_3_09_first_name_Spaces(self):
        ERRORMESSAGE = "first_name must not have spaces"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(first_name=" Tester ")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(first_name="Te ste r")

    def test_3_10_first_name_SpecialCharacters(self):
        ERRORMESSAGE1 = "first_name must only contain a-zA-z0-9,-_"
        ERRORMESSAGE2 = "first_name must have at least one letter"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE1):
            self.createInstance(first_name="@tester")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE1):
            self.createInstance(first_name="Hello******")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE2):
            self.createInstance(first_name="____")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE2):
            self.createInstance(first_name="-__-")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE2):
            self.createInstance(first_name="01234567")

    def test_3_11_last_name_Type(self):
        ERRORMESSAGE = "last_name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(last_name=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(last_name=69)

    def test_3_12_last_name_Emptiness(self):
        ERRORMESSAGE = "last_name must not be empty"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(last_name="")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(last_name="    ")

    def test_3_13_last_name_Spaces(self):
        ERRORMESSAGE = "last_name cannot have spaces"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(last_name=" MCGee ")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(last_name="MC Gee")

    def test_3_14_last_name_SpecialCharacters(self):
        ERRORMESSAGE1 = "last_name must only contain a-zA-z0-9,-_"
        ERRORMESSAGE2 = "last_name must have at least one letter"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE1):
            self.createInstance(last_name="@MCGee")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE1):
            self.createInstance(last_name="MC$Gee")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE2):
            self.createInstance(last_name="____")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE2):
            self.createInstance(last_name="-__-")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE2):
            self.createInstance(last_name="012345678")


class API_4_Country(API_BaseTest):
    '''
        Tests the Country class.
        Country(code, name)
    '''

    @classmethod
    def importClass(cls):
        return __import__(MODULE).Country

    @classmethod
    def createInstance(cls, code="uy", name="Uruguay"):
        Country = cls.importClass()
        return Country(code, name)

    def test_4_01_sanity(self):
        self.sanityTest()

    def test_4_02_basicOperations(self):
        country = self.createInstance()
        country.code
        country.name

    def test_4_03_code_Type(self):
        ERRORMESSAGE = "Code must be a 2 char string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(code=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(code=69)

    def test_4_04_code_Emptiness(self):
        ERRORMESSAGE = "Code must be a 2 char string"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="  ")

    def test_4_05_code_InvalidLenght(self):
        ERRORMESSAGE = "Code must be a 2 char string"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="a")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="abc")

    def test_4_06_code_InvalidContent(self):
        ERRORMESSAGE = "Code can only be a-z"
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="12")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="a*")
        with self.assertRaises(ValueError, msg=ERRORMESSAGE):
            self.createInstance(code="UY")

    def test_4_07_name_Type(self):
        ERRORMESSAGE = "Name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name=69)

    def test_4_08_name_Emptiness(self):
        ERRORMESSAGE = "Name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="")
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="    ")

    def test_4_09_name_InvalidContent(self):
        ERRORMESSAGE = "Name must be a-zA-Z"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="A55GHAR")
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="$Hola")


class API_5_City(API_BaseTest):
    '''
        Tests the City class.
        country_code isn't tested
        City(country_code, name)
    '''

    @classmethod
    def importClass(cls):
        return __import__(MODULE).City

    @classmethod
    def createInstance(cls, country_code="uy", name="Montevideo"):
        Country = cls.importClass()
        return Country(country_code, name)

    def test_5_01_sanity(self):
        self.sanityTest()

    def test_5_02_basicOperations(self):
        city = self.createInstance()
        city.name
        city.country_code

    def test_5_03_nameType(self):
        ERRORMESSAGE = "Name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name=69)

    def test_5_04_nameEmptiness(self):
        ERRORMESSAGE = "Name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="")
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="    ")

    def test_5_05_nameInvalidContent(self):
        ERRORMESSAGE = "Name must be a-zA-Z"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="A55ghar")
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="$Hola")


class API_6_Place(API_BaseTest):
    '''
        Tests the Place class.
        host id and city id are not tested
        Place(host_id, name, description, number_of_rooms,
        number_of_bathrooms, max_guests, price_per_night,
        latitude, longitude, city_id, amenity_ids)
    '''

    @classmethod
    def importClass(cls):
        return __import__(MODULE).Place

    @classmethod
    def createInstance(
        cls, name="Choza de madera",
        description="Para dormir tenes que poner un acolchado",
        number_of_rooms=1, number_of_bathrooms=0,
        max_guests=2, price_per_night=200,
        latitude=-34.878084970819934,
        longitude=-56.11451859541931,
            amenity_ids=[uuid.uuid4(), uuid.uuid4()]):
        Place = cls.importClass()
        Country = API_4_Country.importClass()
        City = API_5_City.importClass()
        User = API_3_User.importClass()

        user = User("juanpedrolo@gmail.com", "juan", "pedrolo")
        country = Country("uy", "Uruguay")
        city = City("Montevideo", "uy")

        return [Place(user.id, name, description,
                      number_of_rooms, number_of_bathrooms, max_guests,
                      price_per_night, latitude, longitude, city.id,
                      amenity_ids), user, city, country]

    def test_6_01_sanity(self):
        self.sanityTest()

    def test_6_02_basicOperations(self):
        ins = self.createInstance()
        n = ins[0]
        n.name
        n.description
        n.number_of_rooms
        n.number_of_bathrooms
        n.max_guests
        n.price_per_night
        n.latitude
        n.longitude
        amenities = n.amenity_ids.copy()

        n.name = "Choza de madera de calidad"
        n.description = "Ahora con cama y todo!"
        amenities.pop(), amenities.append(uuid.uuid4())
        n.ammenities = amenities
        n.price_per_night = 500
        n.max_guests = 4

    def test_6_03_name_Type(self):
        ERRORMESSAGE = "name must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name=69)

    def test_6_04_name_Emptiness(self):
        ERRORMESSAGE = "name must not be empty"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="")
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(name="    ")

    def test_6_05_decription_Type(self):
        ERRORMESSAGE = "description must be a string"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(description=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(description=69)

    def test_6_06_number_of_rooms_Type(self):
        ERRORMESSAGE = "number_of_rooms must be an int"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(number_of_rooms=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(number_of_rooms=69.69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(number_of_rooms=[69])

    def test_6_07_number_of_bathrooms_Type(self):
        ERRORMESSAGE = "number_of_bathrooms must be an int"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(number_of_bathrooms=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(number_of_bathrooms=69.69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(number_of_rooms=[69])

    def test_6_08_max_guests_Type(self):
        ERRORMESSAGE = "max_guests must be an int"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(max_guests=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(max_guests=69.69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(max_guests=[69])

    def test_6_09_price_per_night_Type(self):
        ERRORMESSAGE = "max_guests must be a float"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(price_per_night=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(price_per_night=69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(price_per_night=[69.69])

    def test_6_10_price_per_night_Value(self):
        ERRORMESSAGE = "max_guests must be > 0"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(price_per_night=0)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(price_per_night=-1)

    def test_6_11_latitude_Type(self):
        ERRORMESSAGE = "latitude must be a float"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(latitude=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(latitude=69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(latitude=[69.69])

    def test_6_12_longitude_Type(self):
        ERRORMESSAGE = "longitude must be a float"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(longitude=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(longitude=69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(longitude=[69.69])

    def test_6_13_amenity_ids_Type(self):
        ERRORMESSAGE = "amenity_ids must be a list"
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(amenity_ids=None)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(amenity_ids=69)
        with self.assertRaises(TypeError, msg=ERRORMESSAGE):
            self.createInstance(amenity_ids=uuid.uuid4())


class API_7_Review(API_BaseTest):
    '''
        Tests the Review class.
        Review(place_id, user_id, rating, comment)
    '''

    @classmethod
    def importClass(cls):
        return __import__(MODULE).Review

    @classmethod
    def createInstance(
        cls, place_id=uuid.uuid4(),
        user_id=uuid.uuid4(), rating=1,
            comment="Peor que un basurero"):
        Review = cls.importClass()
        return Review(place_id, user_id, rating, comment)

    def test_7_01_sanity(self):
        self.sanityTest()

    def test_7_02_basicOperations(self):
        review = self.createInstance()
        review.place_id
        review.user_id
        review.rating
        review.comment


if __name__ == '__main__':
    unittest.main()
