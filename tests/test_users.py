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
    def createUser(cls,
                    num: int,
                    dic: dict | None = None,
                    *,
                    expectAtPOST: int = 201,
                    overrideNone: bool = False
                    ) -> dict:
        cls.FROM(f"users/valid_user_{num}.json")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.CHANGE_VALUE(key, dic[key])

        if expectAtPOST != 201:
            cls.POST("/users")
            cls.ASSERT_CODE(expectAtPOST)
            return {}

        cls.POST("/users")
        cls.ASSERT_CODE(201)

        output = cls.json.copy()
        output["id"] = cls.GET_RESPONSE_VALUE("id")
        return output

    @classmethod
    def deleteUser(cls, **kwargs):
        id = kwargs["id"]
        cls.DELETE(f"/users/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/users")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_02_valid_POST_GET(cls):
        for i in range(1, 4):
            user = cls.createUser(i)
            cls.deleteUser(**user)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/users")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_04_valid_name_PUT(cls):
        for i in range(1, 4):
            user = cls.createUser(i)
            cls.CHANGE_VALUE("first_name", user["first_name"] + "UPDATED")
            cls.PUT("/users/" + user["id"])
            cls.ASSERT_CODE(201)
            cls.deleteUser(**user)

    @classmethod
    def test_05_valid_email_PUT(cls):
        user = cls.createUser(1)
        cls.CHANGE_VALUE("email", "elpibito@outlook.com")
        cls.PUT("/users/" + user["id"])
        cls.ASSERT_CODE(201)
        cls.deleteUser(**user)

    @classmethod
    def test_06_existing_email_PUT(cls):
        user1 = cls.createUser(1)
        user2 = cls.createUser(2)
        cls.CHANGE_VALUE("email", user1["email"])
        cls.PUT("/users/" + user2["id"])
        cls.ASSERT_CODE(409)
        cls.deleteUser(**user1)
        cls.deleteUser(**user2)

    @classmethod
    def test_08_empty_id_GET(cls):
        cls.GET("/users/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_09_empty_id_DELETE(cls):
        cls.DELETE("/users/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_10_empty_id_PUT(cls):
        user = cls.createUser(1)
        cls.PUT("/users/")
        cls.ASSERT_CODE(404)
        cls.deleteUser(**user)

    @classmethod
    def test_11_less_attributes_POST(cls):
        cls.createUser(1, {"first_name": None}, expectAtPOST=400)
        cls.createUser(2, {"last_name": None}, expectAtPOST=400)
        cls.createUser(3, {"email": None}, expectAtPOST=400)

    @classmethod
    def test_12_more_attributes_POST(cls):
        cls.createUser(1, {"example": "lechuga"}, expectAtPOST=400)

    @classmethod
    def test_13_different_attributes_POST(cls):
        cls.createUser(2, {"first_name": None, "example": "pechuga"},
                       expectAtPOST=400)


    @classmethod
    def test_14_less_attributes_PUT(cls):
        user = cls.createUser(3)
        cls.REMOVE_VALUE("first_name")
        cls.PUT("/users/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteUser(**user)

    @classmethod
    def test_15_more_attributes_PUT(cls):
        user = cls.createUser(3)
        cls.CHANGE_VALUE("food", "yes")
        cls.PUT("/users/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteUser(**user)

    @classmethod
    def test_16_different_attributes_PUT(cls):
        user = cls.createUser(3)
        cls.REMOVE_VALUE("first_name")
        cls.CHANGE_VALUE("food", "yes")
        cls.PUT("/users/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteUser(**user)

    @classmethod
    def test_17_duplicate_entry_POST(cls):
        user = cls.createUser(3)
        cls.createUser(3, expectAtPOST=409)
        cls.deleteUser(**user)

    @classmethod
    def test_18_id_that_doesnt_exist_GET(cls):
        user = cls.createUser(3)
        id = user["id"]
        cls.deleteUser(**user)
        cls.GET(f"/users/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_19_id_that_doesnt_exist_PUT(cls):
        user = cls.createUser(3)
        id = user["id"]
        cls.deleteUser(**user)
        cls.PUT(f"/users/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_20_id_that_doesnt_exist_DELETE(cls):
        user = cls.createUser(3)
        id = user["id"]
        cls.deleteUser(**user)
        cls.GET(f"/users/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_21_empty_first_name_POST(cls):
        cls.createUser(2, {"first_name": ""}, expectAtPOST=400)
        cls.createUser(2, {"first_name": "    "}, expectAtPOST=400)

    @classmethod
    def test_22_empty_last_name_POST(cls):
        cls.createUser(2, {"last_name": ""}, expectAtPOST=400)
        cls.createUser(2, {"last_name": "    "}, expectAtPOST=400)

    @classmethod
    def test_23_empty_email_POST(cls):
        cls.createUser(2, {"email": ""}, expectAtPOST=400)
        cls.createUser(2, {"email": "    "}, expectAtPOST=400)

    @classmethod
    def test_24_invalid_email_POST(cls):
        def checkEmailPUT(email):
            cls.createUser(1, {"email": email}, expectAtPOST=400)

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
        cls.createUser(1, {"first_name": "ex\nmple"}, expectAtPOST=400)
        cls.createUser(1, {"first_name": "prr😀m"}, expectAtPOST=400)
        cls.createUser(1, {"first_name": "777"}, expectAtPOST=400)

    @classmethod
    def test_26_invalid_last_name_POST(cls):
        cls.createUser(1, {"last_name": "ex\nmple"}, expectAtPOST=400)
        cls.createUser(1, {"last_name": "prr😀m"}, expectAtPOST=400)
        cls.createUser(1, {"last_name": "777"}, expectAtPOST=400)


def run():
    TestUsers.run()


if __name__ == "__main__":
    run()
