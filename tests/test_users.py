#!/usr/bin/python3

'''
    Defines tests for 'users' endpoints.
'''

from testlib import HTTPTestClass


class TestUsers(HTTPTestClass):
    '''
    Tests:
        #1:  General GET
        #2:  valid POSTs then GET   -linked
        #3:  General GET
        #4:  valid name PUTs        -linked
        #5:  valid DELETEs          -linked
        #6:  valid email PUT
        #7:  existing email PUT
        #8:  empty GET
        #9:  empty PUT
        #10: empty DELETE
        #11: less attributes POST
        #12: more attributes POST
        #13: different attributes POST
        #14: less attributes PUT
        #15: more attributes PUT
        #16: different attributes PUT
        #17: duplicate entry POST
    '''

    @classmethod
    def getIDAndJson(cls, path):
        cls.FROM(path)
        email = cls.SAVE_VALUE("email")
        cls.GET("/users")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("email", email, "id")

    @classmethod
    def createPostGet(cls, path: str) -> tuple[str, str]:
        cls.FROM(path)
        email: str = cls.SAVE_VALUE("email")
        cls.POST("/users")
        cls.CODE_ASSERT(201)

        cls.GET(f"/users")
        cls.CODE_ASSERT(200)

        id: str = cls.GET_VALUE_WITH("email", email, "id")
        return email, id

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/users")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_02_valid_POST_GET(cls):  # linked
        for i in range(1, 4):
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
    def test_04_valid_PUT(cls):  # linked
        for i in range(1, 4):
            id = cls.getIDAndJson(f"users/valid_user_{i}.json")
            email = cls.SAVE_VALUE("email")
            first_name = "Vanessa"
            cls.CHANGE_VALUE("first_name", first_name)
            last_name = cls.SAVE_VALUE("last_name")

            cls.PUT(f"/users/{id}")
            cls.CODE_ASSERT(201)

            cls.GET(f"/users/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("email", email)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_05_valid_DELETE(cls):  # linked
        for i in range(1, 4):
            id = cls.getIDAndJson(f"users/valid_user_{i}.json")

            cls.DELETE(f"/users/{id}")
            cls.CODE_ASSERT(204)

            cls.GET(f"/users/{id}")
            cls.CODE_ASSERT(404)

    @classmethod
    def test_06_valid_email_PUT(cls):
        email, id = cls.createPostGet("users/valid_user_2.json")
        email = "alisonalvez@duckduckgo.com"
        cls.CHANGE_VALUE("email", email)

        cls.PUT(f"/users/{id}")
        cls.CODE_ASSERT(201)

        cls.GET(f"/users/{id}")
        cls.CODE_ASSERT(200)
        cls.VALUE_ASSERT("email", email)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_07_existing_email_PUT(cls):
        email1, id1 = cls.createPostGet("users/valid_user_2.json")
        email2, id2 = cls.createPostGet("users/valid_user_3.json")
        cls.CHANGE_VALUE("email", email1)

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
    def test_09_empty_id_DELETE(cls):
        cls.DELETE("/users/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_10_empty_id_PUT(cls):
        cls.FROM("users/valid_user_2.json")
        cls.PUT("/users/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_11_less_attributes_POST(cls):
        cls.FROM("users/valid_user_2.json")
        cls.REMOVE_VALUE("last_name")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_12_more_attributes_POST(cls):
        cls.FROM("users/valid_user_3.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_13_different_attributes_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.REMOVE_VALUE("first_name")
        cls.REMOVE_VALUE("last_name")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_14_less_attributes_PUT(cls):
        email, id = cls.createPostGet("users/valid_user_2.json")
        cls.REMOVE_VALUE("last_name")
        cls.PUT(f"/users/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_15_more_attributes_PUT(cls):
        email, id = cls.createPostGet("users/valid_user_2.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.PUT(f"/users/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_16_different_attributes_PUT(cls):
        email, id = cls.createPostGet("users/valid_user_2.json")
        cls.REMOVE_VALUE("first_name")
        cls.REMOVE_VALUE("last_name")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT(f"/users/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_17_duplicate_entry_POST(cls):
        email, id = cls.createPostGet("users/valid_user_1.json")
        cls.POST("/users")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/users/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_18_id_that_doesnt_exist_GET(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/users/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_19_id_that_doesnt_exist_PUT(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.PUT(f"/users/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_20_id_that_doesnt_exist_DELETE(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/users/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_21_empty_first_name_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("first_name", "")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("first_name", "     ")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_22_empty_last_name_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("last_name", "")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("last_name", "    ")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_23_empty_email_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("email", "")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("email", "     ")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_24_invalid_email_POST(cls):
        cls.FROM("users/valid_user_1.json")
        def checkEmailPUT(email):
            cls.CHANGE_VALUE("email", email)
            cls.POST("/users")
            cls.CODE_ASSERT(400)

        checkEmailPUT(" example@gmail.com")
        checkEmailPUT("example@gmail.com ")
        checkEmailPUT("example.com")
        checkEmailPUT("example@com@com.uy")
        checkEmailPUT("example@com..uy")
        checkEmailPUT("example@.com")
        checkEmailPUT("example@gmail.com.")
        checkEmailPUT("@gmail.com")
        checkEmailPUT("example@")
        checkEmailPUT("example@")
        checkEmailPUT("Hola😀@gmail.com")
        checkEmailPUT("Hola@gm😀ail.com")
        checkEmailPUT("Hola@gmail.co😀m")

    @classmethod
    def test_25_invalid_first_name_POST(cls):
        cls.FROM("users/valid_user_2.json")
        cls.CHANGE_VALUE("first_name", "ex\nmple")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("first_name", "prr😀m")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("first_name", "777")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_26_invalid_first_name_POST(cls):
        cls.FROM("users/valid_user_3.json")
        cls.CHANGE_VALUE("last_name", "ex\nmple")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("last_name", "prr😀m")
        cls.POST("/users")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("last_name", "777")
        cls.POST("/users")
        cls.CODE_ASSERT(400)


def run():
    TestUsers.run()


if __name__ == "__main__":
    run()
