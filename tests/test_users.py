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
    def valid_postGet(c, path: str):
        c.FROM(path)
        c.POST("/users")
        c.CODE_ASSERT(201)
        email = c.SAVE_VALUE("email")
        first_name = c.SAVE_VALUE("first_name")
        last_name = c.SAVE_VALUE("last_name")

        c.GET("/users")
        c.CODE_ASSERT(200)
        id = c.GET_VALUE_WITH("email", email, "id")

        c.GET(f"/users/{id}")
        c.CODE_ASSERT(200)
        c.VALUE_ASSERT("email", email)
        c.VALUE_ASSERT("first_name", first_name)
        c.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def valid_DELETE(c, path: str):
        c.FROM(path)
        email = c.SAVE_VALUE("email")
        c.GET("/users")
        c.CODE_ASSERT(200)
        id = c.GET_VALUE_WITH("email", email, "id")

        c.DELETE(f"/users/{id}")
        c.CODE_ASSERT(204)

        c.GET(f"/users/{id}")
        c.CODE_ASSERT(404)

    @classmethod
    def test_1_general_GET(c):
        c.GET("/users")
        c.CODE_ASSERT(200)

    @classmethod
    def test_2_valid_POST_GET(c):
        for i in range (1, 4):
            c.valid_postGet(f"users/valid_user_{i}.json")

    @classmethod
    def test_3_another_general_GET(c):
        c.GET("/users")
        c.CODE_ASSERT(200)

    @classmethod
    def test_4_valid_PUT(c):
        pass

    @classmethod
    def test_5_valid_DELETE(c):
        for i in range (1, 4):
            c.valid_DELETE(f"users/valid_user_{i}.json")

    @classmethod
    def test_6_empty_id_GET(c):
        c.GET("/users/")
        c.CODE_ASSERT(404)
        c.PRINT_RESPONSE()

def run():
    TestUsers.run()


if __name__ == "__main__":
    run()
