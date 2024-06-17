#!/usr/bin/python3

'''
    Defines tests for 'cities' endpoints.
'''

from testlib import HTTPTestClass


class TestCities(HTTPTestClass):
    '''
        #1: Post-Get city
    '''

    @classmethod
    def getIDAndJson(cls, path):
        cls.FROM(path)
        name = cls.SAVE_VALUE("name")
        cls.GET("/cities")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("name", name, "id")

    @classmethod
    def createPostGet(cls, path: str) -> tuple[str, str]:
        cls.FROM(path)
        name: str = cls.SAVE_VALUE("name")
        cls.POST("/cities")
        cls.CODE_ASSERT(201)

        cls.GET(f"/cities")
        cls.CODE_ASSERT(200)

        id: str = cls.GET_VALUE_WITH("name", name, "id")
        try:
            return cls.GET_VALUE_WITH("name", name, "id")
        except Exception:
            return cls.GET_VALUE_WITH("name", f"{name}updated", "id")

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/cities")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_02_valid_POST_GET(cls):  # linked
        for i in range(1, 5):
            cls.FROM(f"cities/valid_city_{i}.json")
            cls.POST("/cities")
            cls.CODE_ASSERT(201)
            name = cls.SAVE_VALUE("name")
            first_name = cls.SAVE_VALUE("first_name")
            last_name = cls.SAVE_VALUE("last_name")

            cls.GET("/cities")
            cls.CODE_ASSERT(200)
            id = cls.GET_VALUE_WITH("name", name, "id")

            cls.GET(f"/cities/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("name", name)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/cities")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_04_valid_PUT(cls):  # linked
        for i in range(1, 5):
            id = cls.getIDAndJson(f"cities/valid_city_{i}.json")
            name = cls.SAVE_VALUE("name")
            first_name = "Vanessa"
            cls.CHANGE_VALUE("first_name", first_name)
            last_name = cls.SAVE_VALUE("last_name")

            cls.PUT(f"/cities/{id}")
            cls.CODE_ASSERT(201)

            cls.GET(f"/cities/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("name", name)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_05_valid_DELETE(cls):  # linked
        for i in range(1, 5):
            id = cls.getIDAndJson(f"cities/valid_city_{i}.json")

            cls.DELETE(f"/cities/{id}")
            cls.CODE_ASSERT(204)

            cls.GET(f"/cities/{id}")
            cls.CODE_ASSERT(404)

    @classmethod
    def test_06_valid_country_code_PUT(cls):
        name, id = cls.createPostGet("cities/valid_city_4.json")
        country_code = "VN"
        cls.CHANGE_VALUE("country_code", country_code)

        cls.PUT(f"/cities/{id}")
        cls.CODE_ASSERT(201)

        cls.GET(f"/cities/{id}")
        cls.CODE_ASSERT(200)
        cls.VALUE_ASSERT("country_code", country_code)

        cls.DELETE(f"/cities/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_07_existing_name_PUT(cls):
        name1, id1 = cls.createPostGet("cities/valid_city_2.json")
        name2, id2 = cls.createPostGet("cities/valid_city_3.json")
        cls.CHANGE_VALUE("name", name1)

        cls.PUT(f"/cities/{id2}")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/cities/{id1}")
        cls.CODE_ASSERT(204)
        cls.DELETE(f"/cities/{id2}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_08_empty_id_GET(cls):
        cls.GET("/cities/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_09_empty_id_DELETE(cls):
        cls.DELETE("/cities/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_10_empty_id_PUT(cls):
        cls.FROM("cities/valid_city_2.json")
        cls.PUT("/cities/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_11_less_attributes_POST(cls):
        cls.FROM("cities/valid_city_2.json")
        cls.REMOVE_VALUE("name")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.FROM("cities/valid_city_2.json")
        cls.REMOVE_VALUE("country_code")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_12_more_attributes_POST(cls):
        cls.FROM("cities/valid_city_3.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_13_different_attributes_POST(cls):
        cls.FROM("cities/valid_city_1.json")
        cls.REMOVE_VALUE("name")
        cls.REMOVE_VALUE("country_code")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_14_less_attributes_PUT(cls):
        name, id = cls.createPostGet("cities/valid_city_2.json")
        cls.REMOVE_VALUE("name")
        cls.PUT(f"/cities/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/cities/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_15_more_attributes_PUT(cls):
        name, id = cls.createPostGet("cities/valid_city_3.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.PUT(f"/cities/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/cities/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_16_different_attributes_PUT(cls):
        name, id = cls.createPostGet("cities/valid_city_2.json")
        cls.REMOVE_VALUE("name")
        cls.REMOVE_VALUE("country_code")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT(f"/cities/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/cities/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_17_duplicate_entry_POST(cls):
        name, id = cls.createPostGet("cities/valid_city_4.json")
        cls.POST("/cities")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/cities/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_18_id_that_doesnt_exist_GET(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/cities/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_19_id_that_doesnt_exist_PUT(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.PUT(f"/cities/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_20_id_that_doesnt_exist_DELETE(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/cities/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_21_empty_name_POST(cls):
        cls.FROM("cities/valid_city_1.json")
        cls.CHANGE_VALUE("name", "")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "     ")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_22_empty_last_name_POST(cls):
        cls.FROM("cities/valid_city_2.json")
        cls.CHANGE_VALUE("country_code", "")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("country_code", "  ")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_23_invalid_country_code_POST(cls):
        cls.FROM("cities/valid_city_1.json")
        cls.CHANGE_VALUE("country_code", "uy")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("country_code", "10")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("country_code", "U5")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("country_code", "U😀")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("country_code", "😀😀")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("country_code", "😀")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_25_invalid_name_POST(cls):
        cls.FROM("cities/valid_city_2.json")
        cls.CHANGE_VALUE("name", "prr😀m")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "777")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "Mi\nColon\n")
        cls.POST("/cities")
        cls.CODE_ASSERT(400)


def run():
    TestCities.run()


if __name__ == "__main__":
    run()
