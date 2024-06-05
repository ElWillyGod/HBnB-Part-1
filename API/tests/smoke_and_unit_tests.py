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


MODULE = "willygil"


class SmokePass():
    '''
        Global variables didn't work.
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
            print("\033[31m\033[5m>>EXLPOSION NUCLEAR<<\033[0m")


    def test_smoke(self):
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


class API_2_UserTests(API_BaseTest):
    '''
        Tests the User class.
        User(email, first_name, last_name)
    '''

    def test_2_1_sanity(self):
        User = __import__(MODULE).User
        user = User("test@test.com", "tester", "MCGee")
        self.__class__.passedSanity = True

class API_3_ReviewTests(API_BaseTest):
    '''
        Tests the Review class.
        Review(place_id, user_id, rating, comment)
    '''

    def test_3_1_sanity(self):
        Review = __import__(MODULE).Review
        review = Review("", "", 1, "")
        self.__class__.passedSanity = True


class API_4_PlaceTests(API_BaseTest):
    '''
        Tests the Place class.
        Place(host_id, name, description, number_of_rooms,
        number_of_bathrooms, max_guests, price_per_night,
        latitude, longitude, city_id, amenity_ids)
    '''

    def test_4_1_sanity(self):
        Place = __import__(MODULE).Place
        place = Place("", "Motel Exctasis", "Bueno", 4,
                 1, 6, 1000,
                 69.69, 69.69, "", ["", ""])
        self.__class__.passedSanity = True


class API_5_CityTests(API_BaseTest):
    '''
        Tests the City class.
        City(name, country_code)
    '''

    def test_5_1_sanity(self):
        City = __import__(MODULE).City
        city = City("Montevideo", "uy")
        self.__class__.passedSanity = True


class API_6_CountryTests(API_BaseTest):
    '''
        Tests the Country class.
        Country(code, name)
    '''

    def test_6_1_sanity(self):
        Country = __import__(MODULE).Country
        country = Country("uy", "Uruguay")
        self.__class__.passedSanity = True


if __name__ == '__main__':
    unittest.main()
