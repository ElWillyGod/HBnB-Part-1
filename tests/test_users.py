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
    def getIDAndJson(cls, path):
        cls.FROM(path)
        email = cls.SAVE_VALUE("email")
        cls.GET("/users")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("email", email, "id")

    @classmethod
    def createPostGet(cls, path: str):
        cls.FROM(path)
        email = cls.SAVE_VALUE("email")
        cls.POST("/users")
        cls.CODE_ASSERT(201)

        cls.GET(f"/users")
        cls.CODE_ASSERT(200)

        id = cls.GET_VALUE_WITH("email", email, "id")
        return email, id

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/users")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_02_valid_POST_GET(cls):
        for i in range (1, 4):
            cls.FROM(f"users/valid_user_{i}.json")
            cls.POST("/users")
            cls.CODE_ASSERT(201)
            email = cls.SAVE_VALUE("email")
            first_name = cls.SAVE_VALUE("first_name")
            last_name = cls.SAVE_VALUE("last_name")

            cls.GET("/users")
            cls.CODE_ASSERT(200)
            id = cls.GET_VALUE_WITH("email", email, "id")

            cls.GET(f"/users/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("email", email)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/users")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_04_valid_PUT(cls):
        for i in range (1, 4):
            id = cls.getIDAndJson(f"users/valid_user_{i}.json")
            email = cls.SAVE_VALUE("email")
            first_name = "Vanessa"
            cls.CHANGE("first_name", first_name)
            last_name = cls.SAVE_VALUE("last_name")

            cls.PUT(f"/users/{id}")
            cls.CODE_ASSERT(201)

            cls.GET(f"/users/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("email", email)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_05_valid_DELETE(cls):
        for i in range (1, 4):
            id = cls.getIDAndJson(f"users/valid_user_{i}.json")

            cls.DELETE(f"/users/{id}")
            cls.CODE_ASSERT(204)

            cls.GET(f"/users/{id}")
            cls.CODE_ASSERT(404)

    @classmethod
    def test_06_valid_PUT_of_email(cls):
        email, id = cls.createPostGet("users/valid_user_2.json")
        email = "alisonalvez@duckduckgo.com"
        cls.CHANGE("email", email)

        cls.PUT(f"/users/{id}")
        cls.CODE_ASSERT(201)

        cls.GET(f"/users/{id}")
        cls.CODE_ASSERT(200)
        cls.VALUE_ASSERT("email", email)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_07_try_PUT_with_existing_email(cls):
        email1, id1 = cls.createPostGet("users/valid_user_2.json")
        email2, id2 = cls.createPostGet("users/valid_user_3.json")
        cls.CHANGE("email", email1)

        cls.PUT(f"/users/{id2}")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/users/{id1}")
        cls.CODE_ASSERT(204)
        cls.DELETE(f"/users/{id2}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_08_empty_id_GET(cls):
        cls.GET("/users/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_09_try_POST_with_duplicate_entry(cls):
        email, id = cls.createPostGet("users/valid_user_1.json")
        cls.POST("/users")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_10_POST_with_less_attributes(cls):
        cls.FROM("users/valid_user_2.json")
        cls.REMOVE_VALUE("last_name")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

def run():
    TestUsers.run()


if __name__ == "__main__":
    run()
