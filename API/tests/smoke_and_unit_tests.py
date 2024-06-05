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


class SmokePass():
    '''
        Global variables didn't work. So doing it with class vars.
    '''

    passedSmoke = False


class API_1_SmokeTest(unittest.TestCase):
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
        ok = all(test != self for test, text in result.errors + result.failures)
        if ok:
            SmokePass.passedSmoke = True
        else:
            print("\033[31m\033[5m\n   <<EXLPOSION NUCLEAR!!!>>\n\033[0m")


    def test_1_01_smoke(self):
        __import__(MODULE)


class API_BaseTest(unittest.TestCase):
    '''
        Base class for tests.
    '''

    passedSanity = False
    checkedSanity = False

    def setUp(self):
        if not SmokePass.passedSmoke:
            self.skipTest("Smoke Test Failed")
        elif not self.__class__.checkedSanity:
            self.__class__.checkedSanity = True
        elif not self.__class__.passedSanity:
            self.skipTest("Sanity Test Failed")


class API_2_TrackedObjectTests(API_BaseTest):
    '''
        Tests the TrackedObject class.
        TrackedObject()
    '''

    @classmethod
    def importClass(self):
        return __import__(MODULE).TrackedObject

    def test_2_01_sanity(self):
        TrackedObject = self.importClass()
        to = TrackedObject()
        self.__class__.passedSanity = True

    def test_2_02_basicOperations(self):
        TrackedObject = self.importClass()
        to = TrackedObject()
        to.id
        to.created_at
        to.updated_at
        to.update_time()


class API_3_UserTests(API_BaseTest):
    '''
        Tests the User class.
        User(email, first_name, last_name)
    '''

    @classmethod
    def importClass(self):
        return __import__(MODULE).User

    def test_3_01_sanity(self):
        User = self.importClass()
        user = User("test@test.com", "tester", "MCGee")
        self.__class__.passedSanity = True


    def test_3_02_basicOperations(self):
        User = self.importClass()
        user = User("test@test.com", "tester", "MCGee")
        user.email
        user.first_name
        user.last_name

    def test_3_03_testEmailType(self):
        User = self.importClass()
        with self.assertRaises(TypeError, msg="Email type not checked"):
            user = User(None, "tester", "MCGee")
        with self.assertRaises(TypeError, msg="Email type not checked"):
            user = User(69, "tester", "MCGee")

    def test_3_04_testEmailEmptiness(self):
        User = self.importClass()
        with self.assertRaises(ValueError, msg="Email emptiness not checked"):
            user = User("", "tester", "MCGee")
        with self.assertRaises(ValueError, msg="Email emptiness not checked"):
            user = User("    ", "tester", "MCGee")
        with self.assertRaises(ValueError, msg="Email emptiness not checked"):
            user = User("@", "tester", "MCGee")

    def test_3_05_testEmailFormat(self):
        User = self.importClass()
        with self.assertRaises(ValueError, msg="Email has to have @"):
            user = User("my_email", "tester", "MCGee")
        with self.assertRaises(ValueError, msg="Email has to have domain"):
            user = User("my_email@", "tester", "MCGee")
        with self.assertRaises(ValueError, msg="Email has to have name"):
            user = User("@gmail.com", "tester", "MCGee")

    def test_3_06_testEmailSpaces(self):
        User = self.importClass()
        with self.assertRaises(ValueError, msg="Email can't have empty spaces"):
            user = User("    tester@gmail.com     ", "tester", "MCGee")
        with self.assertRaises(ValueError, msg="Email can't have empty spaces"):
            user = User("test @gmail.com", "tester", "MCGee")
        with self.assertRaises(ValueError, msg="Email can't have empty spaces"):
            user = User("test@g ma il.com", "tester", "MCGee")

    def test_3_07_testFirstNameType(self):
        User = self.importClass()
        with self.assertRaises(TypeError, msg="Name type not checked"):
            user = User("test@test.com", None, "MCGee")
        with self.assertRaises(TypeError, msg="Name type not checked"):
            user = User("test@test.com", 69, "MCGee")

    def test_3_08_testFirstNameEmptiness(self):
        User = self.importClass()
        with self.assertRaises(ValueError, msg="Name emptiness not checked"):
            user = User("test@test.com", "", "MCGee")
        with self.assertRaises(ValueError, msg="Name emptiness not checked"):
            user = User("test@test.com", "  ", "MCGee")

    def test_3_09_testFirstNameSpaces(self):
        User = self.importClass()
        with self.assertRaises(ValueError, msg="Name can't have empty spaces"):
            user = User("test@test.com", " Tester ", "MCGee")
        with self.assertRaises(ValueError, msg="Name type not checked"):
            user = User("test@test.com", "Te ste r", "MCGee")

    def test_3_10_testFirstNameSpecialCharacters(self):
        User = self.importClass()
        with self.assertRaises(ValueError,
            msg="Name can only have a-z, A-z, 0-9, '-', '_'"):
            user = User("test@test.com", "@tester", "MCGee")
        with self.assertRaises(ValueError,
            "Name can only have a-z, A-z, 0-9, '-', '_'"):
            msg=user = User("test@test.com", "Hello******", "MCGee")
        with self.assertRaises(ValueError,
            "Name cannot be only underscores"):
            msg=user = User("test@test.com", "____", "MCGee")
        with self.assertRaises(ValueError,
            "Name cannot be only hyphens"):
            msg=user = User("test@test.com", "----", "MCGee")
        with self.assertRaises(ValueError,
            "Name cannot be only numers"):
            msg=user = User("test@test.com", "01234567", "MCGee")

    def test_3_11_testLastNameType(self):
        User = self.importClass()
        with self.assertRaises(TypeError, msg="Name type not checked"):
            user = User("test@test.com", "Tester", None)
        with self.assertRaises(TypeError, msg="Name type not checked"):
            user = User("test@test.com", "Tester", 69)

    def test_3_12_testLastNameEmptiness(self):
        User = self.importClass()
        with self.assertRaises(ValueError, msg="Name emptiness not checked"):
            user = User("test@test.com", "Test", "")
        with self.assertRaises(ValueError, msg="Name emptiness not checked"):
            user = User("test@test.com", "  ", "    ")

    def test_3_13_testLastNameSpaces(self):
        User = self.importClass()
        with self.assertRaises(ValueError, "Name can't have empty spaces"):
            user = User("test@test.com", "Tester", " MCGee ")
        with self.assertRaises(ValueError, "Name type not checked"):
            user = User("test@test.com", "Tester", "MC Gee")

    def test_3_14_testLastNameSpecialCharacters(self):
        User = self.importClass()
        with self.assertRaises(ValueError,
            "Name can only have a-z, A-z, 0-9, '-', '_'"):
            user = User("test@test.com", "tester", "@MCGee")
        with self.assertRaises(ValueError,
            "Name can only have a-z, A-z, 0-9, '-', '_'"):
            user = User("test@test.com", "Hello", "MC$Gee")
        with self.assertRaises(ValueError,
            "Name cannot be only underscores"):
            user = User("test@test.com", "Test", "____")
        with self.assertRaises(ValueError,
            "Name cannot be only hyphens"):
            user = User("test@test.com", "Test", "----")
        with self.assertRaises(ValueError,
            "Name cannot be only numers"):
            user = User("test@test.com", "Test", "012345678")


class API_4_CountryTests(API_BaseTest):
    '''
        Tests the Country class.
        Country(code, name)
    '''

    @classmethod
    def importClass(self):
        return __import__(MODULE).Country

    def test_4_01_sanity(self):
        Country = self.importClass()
        country = Country("uy", "Uruguay")
        self.__class__.passedSanity = True

    def test_4_02_basicOperations(self):
        Country = self.importClass()
        country = Country("uy", "Uruguay")
        country.code
        country.name


class API_5_CityTests(API_BaseTest):
    '''
        Tests the City class.
        City(name, country_code)
    '''

    @classmethod
    def importClass(self):
        return __import__(MODULE).City

    def test_5_01_sanity(self):
        City = self.importClass()
        city = City("Montevideo", "uy")
        self.__class__.passedSanity = True

    def test_5_02_basicOperations(self):
        City = self.importClass()
        city = City("Montevideo", "uy")
        city.name
        city.country_code


class API_6_PlaceTests(API_BaseTest):
    '''
        Tests the Place class.
        Place(host_id, name, description, number_of_rooms,
        number_of_bathrooms, max_guests, price_per_night,
        latitude, longitude, city_id, amenity_ids)
    '''

    @classmethod
    def importClass(self):
        return __import__(MODULE).Place

    @classmethod
    def createInstance(self, name, description, n_of_rooms, n_of_bathrooms,
        max_guests, price_per_night, latitude, longitude, amenity_ids):
        Place = self.importClass()
        Country = API_4_CountryTests.importClass()
        City = API_5_CityTests.importClass()
        User = API_3_UserTests.importClass()

        user = User("juanpedrolo@gmail.com", "juan", "pedrolo")
        country = Country("uy", "Uruguay")
        city = City("Montevideo", "uy")

        return [Place(user.id, name, description,
            number_of_rooms, number_of_bathrooms, max_guests,
            price_per_night, latitude, longitude, city.id, amenity_ids),
            user, city, country]

    def test_6_01_sanity(self):
        Place = self.importClass()
        place = Place(uuid.uuid4().hex, "Testing Place", "Test", 4,
                1, 6, 1000,
                69.69, 69.69, uuid.uuid4().hex,
                [uuid.uuid4().hex, uuid.uuid4().hex])
        self.__class__.passedSanity = True

    def test_6_02_basicOperations(self):
        name = "Choza de madera"
        desc = "Para dormir tenes que poner un acolchado"
        number_of_rooms = 1
        number_of_bathrooms = 0
        max_guests = 2
        price_per_night = 200
        latitude = -34.878084970819934
        longitude = -56.11451859541931
        amenity_ids = [uuid.uuid4().hex, uuid.uuid4().hex, uuid.uuid4().hex]
        n = self.createInstance(self, name, description, number_of_rooms,
            number_of_bathrooms, max_guests, price_per_night, latitude,
            longitude, amenity_ids)
        n.name
        n.description
        n.number_of_rooms
        n.number_of_bathrooms
        n.max_guests
        n.price_per_night
        n.latitude
        n.longitude
        n.amenity_ids

        n.name = "Choza de madera de calidad"
        n.description = "Ahora con cama y todo!"
        amenity_ids.pop(), amenity_ids.append()
        n.ammenities = amenity_ids
        n.price_per_night = 500
        n.max_guests = 4


class API_7_ReviewTests(API_BaseTest):
    '''
        Tests the Review class.
        Review(place_id, user_id, rating, comment)
    '''

    @classmethod
    def importClass(self):
        return __import__(MODULE).Review

    def test_7_01_sanity(self):
        Review = self.importClass()
        review = Review(uuid.uuid4().hex, uuid.uuid4().hex, 1, "Test")
        self.__class__.passedSanity = True

    def test_7_02_basicOperations(self):
        Review = self.importClass()
        review = Review(uuid.uuid4().hex, uuid.uuid4().hex, 1, "Test")
        review.place_id
        review.user_id
        review.rating
        review.comment


if __name__ == '__main__':
    unittest.main()
