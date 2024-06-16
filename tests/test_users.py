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
    def postGet(c, path):
        c.FROM(path)
        c.POST("/users")
        c.CODE_ASSERT(201)
        email = c.SAVE_VALUE("email")

        c.GET("/users")
        c.CODE_ASSERT(200)
        c.VALUE_ASSERT("email", email)

    @classmethod
    def test_postGets(c):
        for i in range (1, 4):
            c.postGet(f"users/valid_user_{i}.json")


def run():
    TestUsers.run()


if __name__ == "__main__":
    run()
