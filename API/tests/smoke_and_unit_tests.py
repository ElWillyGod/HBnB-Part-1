#!/usr/bin/python3

'''
    Defines unit test cases for API.
    Tests for version 0.1
    Usage: in programs directory (API);
    python3 -m unittest tests/smoke_and_unit_tests.py
'''

import unittest


MODULE = "willygil"


class API_1_SmokeTest(unittest.TestCase):
    '''
        Tests if the module doesn't cause a nuclear explosion.
    '''

    def tearDown(self):
        print("\033[31m\033[5m>>EXLPOSION NUCLEAR<<\033[0m")


    def test_smoke(self):
        __import__(MODULE)


class API_BaseTest(unittest.TestCase):
    '''
        Base class for tests
    '''

    def run(self, result=None):
        """ Stop after smoke test error """
        if not result.errors:
            super(API_1_SmokeTest, self).run(result)


class API_2_UserTests(API_BaseTest):
    '''
        Tests the User class.
    '''

    def test_sanity(self):
        user = __import__(MODULE).User("test@test.com", "tester", "MCGee")


class API_3_ReviewTests(API_BaseTest):
    '''
        Tests the Review class.
    '''

    def test_sanity(self):
        review = __import__(MODULE).Review()


class API_4_PlaceTests(API_BaseTest):
    '''
        Tests the Place class.
    '''

    def test_sanity(self):
        place = __import__(MODULE).Place()


class API_5_CityTests(API_BaseTest):
    '''
        Tests the City class.
    '''

    def test_sanity(self):
        city = __import__(MODULE).City()


class API_6_CountryTests(API_BaseTest):
    '''
        Tests the Country class.
    '''

    def test_sanity(self):
        country = __import__(MODULE).Country()


if __name__ == '__main__':
    unittest.main()
