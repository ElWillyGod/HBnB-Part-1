#!/usr/bin/python3

'''
    quickdoc
'''

from testlib import HTTPTestClass


class TestUsers(HTTPTestClass):
    '''
        Defines test for Users
    '''

    def test_1(self):
        self.FROM("users/valid_user_1.json")
        response = self.POST("/users")
        self.CODE_ASSERT(response, 201)

        response = self.GET("/users")


TestUsers.run()