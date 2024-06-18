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
    def getIDAndJson(cls, path):
        cls.FROM(path)
        name = cls.SAVE_VALUE("name")
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)
        try:
            return cls.GET_RESPONSE_WITH("name", name, "id")
        except Exception:
            return cls.GET_RESPONSE_WITH("name", f"{name}updated", "id")

    @classmethod
    def createPostGet(cls, path: str) -> tuple[str, str]:
        cls.FROM(path)
        name: str = cls.SAVE_VALUE("name")
        cls.POST("/amenities")
        cls.ASSERT_CODE(201)

        cls.GET(f"/amenities")
        cls.ASSERT_CODE(200)

        id: str = cls.GET_RESPONSE_WITH("name", name, "id")
        return name, id

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_02_valid_POST_GET(cls):  # linked
        for i in range(1, 6):
            cls.FROM(f"amenities/valid_amenity_{i}.json")
            cls.POST("/amenities")
            cls.ASSERT_CODE(201)
            name = cls.SAVE_VALUE("name")

            cls.GET("/amenities")
            cls.ASSERT_CODE(200)
            id = cls.GET_RESPONSE_WITH("name", name, "id")

            cls.GET(f"/amenities/{id}")
            cls.ASSERT_CODE(200)
            cls.ASSERT_VALUE("name", name)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/amenities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_04_valid_PUT(cls):  # linked
        for i in range(1, 6):
            id = cls.getIDAndJson(f"amenities/valid_amenity_{i}.json")
            name = cls.SAVE_VALUE("name")
            name = f"{name}updated"
            cls.CHANGE_VALUE("name", name)

            cls.PUT(f"/amenities/{id}")
            cls.ASSERT_CODE(201)

            cls.GET(f"/amenities/{id}")
            cls.ASSERT_CODE(200)
            cls.ASSERT_VALUE("name", name)

    @classmethod
    def test_05_valid_DELETE(cls):  # linked
        for i in range(1, 6):
            id = cls.getIDAndJson(f"amenities/valid_amenity_{i}.json")

            cls.DELETE(f"/amenities/{id}")
            cls.ASSERT_CODE(204)

            cls.GET(f"/amenities/{id}")
            cls.ASSERT_CODE(404)

    @classmethod
    def test_06_existing_name_PUT(cls):
        name1, id1 = cls.createPostGet("amenities/valid_amenity_4.json")
        name2, id2 = cls.createPostGet("amenities/valid_amenity_5.json")
        cls.CHANGE_VALUE("name", name1)

        cls.PUT(f"/amenities/{id2}")
        cls.ASSERT_CODE(409)

        cls.DELETE(f"/amenities/{id1}")
        cls.ASSERT_CODE(204)
        cls.DELETE(f"/amenities/{id2}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_07_empty_id_GET(cls):
        cls.GET("/amenities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_08_empty_id_DELETE(cls):
        cls.DELETE("/amenities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_09_empty_id_PUT(cls):
        cls.FROM("amenities/valid_amenity_2.json")
        cls.PUT("/amenities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_10_more_attributes_POST(cls):
        cls.FROM("amenities/valid_amenity_3.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

    @classmethod
    def test_11_different_attributes_POST(cls):
        cls.FROM("amenities/valid_amenity_1.json")
        cls.REMOVE_VALUE("name")
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

    @classmethod
    def test_12_more_attributes_PUT(cls):
        name, id = cls.createPostGet("amenities/valid_amenity_2.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.PUT(f"/amenities/{id}")
        cls.ASSERT_CODE(400)

        cls.DELETE(f"/amenities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_13_different_attributes_PUT(cls):
        name, id = cls.createPostGet("amenities/valid_amenity_2.json")
        cls.REMOVE_VALUE("first_name")
        cls.REMOVE_VALUE("last_name")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT(f"/amenities/{id}")
        cls.ASSERT_CODE(400)

        cls.DELETE(f"/amenities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_14_duplicate_entry_POST(cls):
        name, id = cls.createPostGet("amenities/valid_amenity_1.json")
        cls.POST("/amenities")
        cls.ASSERT_CODE(409)

        cls.DELETE(f"/amenities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_15_id_that_doesnt_exist_GET(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_16_id_that_doesnt_exist_PUT(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.PUT(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_17_id_that_doesnt_exist_DELETE(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/amenities/{id}")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_18_empty_name_POST(cls):
        cls.FROM("amenities/valid_amenity_4.json")
        cls.CHANGE_VALUE("name", "")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

        cls.CHANGE_VALUE("name", "     ")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

    @classmethod
    def test_19_invalid_name_POST(cls):
        cls.FROM("amenities/valid_amenity_1.json")
        cls.CHANGE_VALUE("name", "\n")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

        cls.CHANGE_VALUE("name", "COck😂😂😂")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

        cls.CHANGE_VALUE("name", "🗿")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

        cls.CHANGE_VALUE("name", "777")
        cls.POST("/amenities")
        cls.ASSERT_CODE(400)

def run():
    TestAmenities.run()


if __name__ == "__main__":
    run()
