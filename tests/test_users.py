#!/usr/bin/python3

'''
    Defines tests for 'users' endpoints.
'''

from testlib import HTTPTestClass


class TestUsers(HTTPTestClass):
    '''
        #1: Post-Get user_1
    '''

    @classmethod
    def test_1(c):
        c.FROM("users/valid_user_1.json")
        c.POST("/users")
        c.CODE_ASSERT(201)
        email = c.SAVE_VALUE("email")

        c.GET("/users")
        c.CODE_ASSERT(200)
        c.VALUE_ASSERT("email", email)


def run():
    TestUsers.run()


if __name__ == "__main__":
    run()
