#!/usr/bin/python3

'''
    Defines tests for 'Countries' endpoints.
'''

from testlib import HTTPTestClass


class TestCountries(HTTPTestClass):
    '''
        #1: Test country get.
    '''

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/countries")
        cls.CODE_ASSERT(200)

        cls.VALUE_ASSERT("code", "UY")
        cls.VALUE_ASSERT("name", "Uruguay")

        cls.VALUE_ASSERT("code", "AR")
        cls.VALUE_ASSERT("name", "Argentina")

        cls.VALUE_ASSERT("code", "ES")
        cls.VALUE_ASSERT("name", "Spain")

        cls.VALUE_ASSERT("code", "US")
        cls.VALUE_ASSERT("name", "United States")

        cls.VALUE_ASSERT("code", "BR")
        cls.VALUE_ASSERT("name", "Brazil")


def run():
    TestCountries.run()


if __name__ == "__main__":
    run()
