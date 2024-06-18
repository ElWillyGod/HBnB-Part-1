#!/usr/bin/python3

'''
    Defines tests for 'amenities' endpoints.
'''

from testlib import HTTPTestClass


class TestAmenities(HTTPTestClass):
    '''
        #1: Post-Get amenity
    '''

    @classmethod
    def createAmenity(cls,
                    num: int,
                    dic: dict | None = None,
                    *,
                    expectAtPOST: int = 201,
                    overrideNone: bool = False
                    ) -> dict:
        cls.FROM(f"amenities/valid_amenity_{num}.json")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.CHANGE_VALUE(key, dic[key])

        if expectAtPOST != 201:
            cls.POST("/amenities")
            cls.ASSERT_CODE(expectAtPOST)
            return {}

        cls.POST("/amenities")
        cls.ASSERT_CODE(201)

        output = cls.json.copy()
        output["id"] = cls.GET_RESPONSE_VALUE("id")
        return output

    @classmethod
    def deleteAmenity(cls, **kwargs):
        id = kwargs["id"]
        cls.DELETE(f"/amenities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_02_valid_POST_GET(cls):
        for i in range(1, 4):
            user = cls.createAmenity(i)
            cls.deleteAmenity(**user)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_04_valid_name_PUT(cls):
        for i in range(1, 4):
            user = cls.createAmenity(i)
            cls.CHANGE_VALUE("name", user["name"] + "UPDATED")
            cls.PUT("/amenities/" + user["id"])
            cls.ASSERT_CODE(201)
            cls.deleteAmenity(**user)

    @classmethod
    def test_05_empty_id_GET(cls):
        cls.GET("/amenities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_06_empty_id_DELETE(cls):
        cls.DELETE("/amenities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_07_empty_id_PUT(cls):
        user = cls.createAmenity(1)
        cls.PUT("/amenities/")
        cls.ASSERT_CODE(404)
        cls.deleteAmenity(**user)

    @classmethod
    def test_08_less_attributes_POST(cls):
        cls.createAmenity(1, {"name": None}, expectAtPOST=400)

    @classmethod
    def test_09_more_attributes_POST(cls):
        cls.createAmenity(1, {"example": "lechuga"}, expectAtPOST=400)

    @classmethod
    def test_10_different_attributes_POST(cls):
        cls.createAmenity(2, {"name": None, "example": "pechuga"},
                       expectAtPOST=400)

    @classmethod
    def test_11_less_attributes_PUT(cls):
        user = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.PUT("/amenities/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    @classmethod
    def test_12_more_attributes_PUT(cls):
        user = cls.createAmenity(3)
        cls.CHANGE_VALUE("food", "yes")
        cls.PUT("/amenities/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    @classmethod
    def test_13_different_attributes_PUT(cls):
        user = cls.createAmenity(3)
        cls.REMOVE_VALUE("name")
        cls.CHANGE_VALUE("food", "yes")
        cls.PUT("/amenities/" + user["id"])
        cls.ASSERT_CODE(400)
        cls.deleteAmenity(**user)

    @classmethod
    def test_14_duplicate_entry_POST(cls):
        user = cls.createAmenity(3)
        cls.createAmenity(3, expectAtPOST=409)
        cls.deleteAmenity(**user)

    @classmethod
    def test_15_id_that_doesnt_exist_GET(cls):
        user = cls.createAmenity(3)
        id = user["id"]
        cls.deleteAmenity(**user)
        cls.GET(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_16_id_that_doesnt_exist_PUT(cls):
        user = cls.createAmenity(3)
        id = user["id"]
        cls.deleteAmenity(**user)
        cls.PUT(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_17_id_that_doesnt_exist_DELETE(cls):
        user = cls.createAmenity(3)
        id = user["id"]
        cls.deleteAmenity(**user)
        cls.GET(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_18_empty_name_POST(cls):
        cls.createAmenity(2, {"name": ""}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "    "}, expectAtPOST=400)

    @classmethod
    def test_19_invalid_name_POST(cls):
        cls.createAmenity(2, {"name": "\n"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "Lechuga😂😂😂"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "🗿"}, expectAtPOST=400)
        cls.createAmenity(2, {"name": "777"}, expectAtPOST=400)

def run():
    TestAmenities.run()


if __name__ == "__main__":
    run()
