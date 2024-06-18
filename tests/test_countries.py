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
        cls.ASSERT_CODE(200)

        cls.ASSERT_VALUE("code", "UY")
        cls.ASSERT_VALUE("name", "Uruguay")

        cls.ASSERT_VALUE("code", "AR")
        cls.ASSERT_VALUE("name", "Argentina")

        cls.ASSERT_VALUE("code", "ES")
        cls.ASSERT_VALUE("name", "Spain")

        cls.ASSERT_VALUE("code", "US")
        cls.ASSERT_VALUE("name", "United States")

        cls.ASSERT_VALUE("code", "BR")
        cls.ASSERT_VALUE("name", "Brazil")


def run():
    TestCountries.run()


if __name__ == "__main__":
    run()
