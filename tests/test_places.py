#!/usr/bin/python3

'''
    Defines tests for 'places' endpoints.
'''

from testlib import HTTPTestClass


class TestPlaces(HTTPTestClass):
    '''
        #1: Post-Get place
    '''

    @classmethod
    def createCity(cls, num: int) -> str:
        cls.FROM(f"cities/valid_city_{num}.json")
        name = cls.SAVE_VALUE("name")
        cls.POST("/cities")
        cls.CODE_ASSERT(201)
        cls.GET("/cities")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("name", name, "id")

    @classmethod
    def createAmenity(cls, num: int) -> str:
        cls.FROM(f"amenities/valid_amenity_{num}.json")
        name = cls.SAVE_VALUE("name")
        cls.POST("/amenities")
        cls.CODE_ASSERT(201)
        cls.GET("/amenities")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("name", name, "id")

    @classmethod
    def createUser(cls, num: int) -> str:
        cls.FROM(f"users/valid_user_{num}.json")
        name = cls.SAVE_VALUE("name")
        cls.POST("/users")
        cls.CODE_ASSERT(201)
        cls.GET("/users")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("name", name, "id")

    @classmethod
    def createPostGet(cls, num: int) -> tuple[str, str]:
        host_id = cls.create_User(num)
        city_id = cls.create_City(num)
        amenity_id = cls.createAmenity(num)

        cls.FROM(f"places/valid_place_{num}.json")
        name: str = cls.SAVE_VALUE("name")
        cls.CHANGE_VALUE("host_id", host_id)
        cls.CHANGE_VALUE("city_id", city_id)
        cls.CHANGE_VALUE("amenity_ids", [amenity_id])
        cls.POST("/places")
        cls.CODE_ASSERT(201)

        cls.GET(f"/places")
        cls.CODE_ASSERT(200)

        id: str = cls.GET_VALUE_WITH("name", name, "id")
        return {
            "host_id": host_id,
            "city_id": city_id,
            "amenity_ids": [amenity_id],
            "id": id,
            "name": name
            }

    @classmethod
    def deleteAll(cls, host_id, city_id, amenity_ids, id, name):
        cls.DELETE(f"/users/{host_id}")
        cls.CODE_ASSERT(204)
        for amenity_id in amenity_ids:
            cls.DELETE(f"/amenity/{amenity_id}")
            cls.CODE_ASSERT(204)
        cls.DELETE(f"/city/{city_id}")
        cls.CODE_ASSERT(204)
        cls.GET(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/places")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_02_valid_POST_GET(cls):  # linked
        for i in range(1, 4):
            cls.FROM(f"users/valid_user_{i}.json")
            cls.POST("/places")
            cls.CODE_ASSERT(201)
            name = cls.SAVE_VALUE("name")
            first_name = cls.SAVE_VALUE("first_name")
            last_name = cls.SAVE_VALUE("last_name")

            cls.GET("/places")
            cls.CODE_ASSERT(200)
            id = cls.GET_VALUE_WITH("name", name, "id")

            cls.GET(f"/places/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("name", name)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/places")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_04_valid_PUT(cls):  # linked
        for i in range(1, 4):
            id = cls.getIDAndJson(f"users/valid_user_{i}.json")
            name = cls.SAVE_VALUE("name")
            first_name = "Vanessa"
            cls.CHANGE_VALUE("first_name", first_name)
            last_name = cls.SAVE_VALUE("last_name")

            cls.PUT(f"/places/{id}")
            cls.CODE_ASSERT(201)

            cls.GET(f"/places/{id}")
            cls.CODE_ASSERT(200)
            cls.VALUE_ASSERT("name", name)
            cls.VALUE_ASSERT("first_name", first_name)
            cls.VALUE_ASSERT("last_name", last_name)

    @classmethod
    def test_05_valid_DELETE(cls):  # linked
        for i in range(1, 4):
            id = cls.getIDAndJson(f"users/valid_user_{i}.json")

            cls.DELETE(f"/places/{id}")
            cls.CODE_ASSERT(204)

            cls.GET(f"/places/{id}")
            cls.CODE_ASSERT(404)

    @classmethod
    def test_06_valid_name_PUT(cls):
        name, id = cls.createPostGet("users/valid_user_2.json")
        name = "alisonalvez@duckduckgo.com"
        cls.CHANGE_VALUE("name", name)

        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(201)

        cls.GET(f"/places/{id}")
        cls.CODE_ASSERT(200)
        cls.VALUE_ASSERT("name", name)

        cls.DELETE(f"/places/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_07_existing_name_PUT(cls):
        name1, id1 = cls.createPostGet("users/valid_user_2.json")
        name2, id2 = cls.createPostGet("users/valid_user_3.json")
        cls.CHANGE_VALUE("name", name1)

        cls.PUT(f"/places/{id2}")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/places/{id1}")
        cls.CODE_ASSERT(204)
        cls.DELETE(f"/places/{id2}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_08_empty_id_GET(cls):
        cls.GET("/places/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_09_empty_id_DELETE(cls):
        cls.DELETE("/places/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_10_empty_id_PUT(cls):
        cls.FROM("users/valid_user_2.json")
        cls.PUT("/places/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_11_less_attributes_POST(cls):
        cls.FROM("users/valid_user_2.json")
        cls.REMOVE_VALUE("last_name")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_12_more_attributes_POST(cls):
        cls.FROM("users/valid_user_3.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_13_different_attributes_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.REMOVE_VALUE("first_name")
        cls.REMOVE_VALUE("last_name")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_14_less_attributes_PUT(cls):
        name, id = cls.createPostGet("users/valid_user_2.json")
        cls.REMOVE_VALUE("last_name")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/places/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_15_more_attributes_PUT(cls):
        name, id = cls.createPostGet("users/valid_user_2.json")
        cls.CHANGE_VALUE("rating", 100)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/places/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_16_different_attributes_PUT(cls):
        name, id = cls.createPostGet("users/valid_user_2.json")
        cls.REMOVE_VALUE("first_name")
        cls.REMOVE_VALUE("last_name")
        cls.CHANGE_VALUE("rating", 1)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)

        cls.DELETE(f"/places/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_17_duplicate_entry_POST(cls):
        name, id = cls.createPostGet("users/valid_user_1.json")
        cls.POST("/places")
        cls.CODE_ASSERT(409)

        cls.DELETE(f"/places/{id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_18_id_that_doesnt_exist_GET(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_19_id_that_doesnt_exist_PUT(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_20_id_that_doesnt_exist_DELETE(cls):
        id = 'fdfc6cba-c620-4beb-a6d3-9d4fac31ccff'
        cls.GET(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_21_empty_first_name_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("first_name", "")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("first_name", "     ")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_22_empty_last_name_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("last_name", "")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("last_name", "    ")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_23_empty_name_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("name", "")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "     ")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_24_invalid_name_POST(cls):
        cls.FROM("users/valid_user_1.json")
        cls.CHANGE_VALUE("name", "example")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", " example@gmail.com")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@gmail.com ")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example.com")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@com@com.uy")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@com..uy")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@.com")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@gmail.com.")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "@gmail.com")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "example@")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "Hola😀@gmail.com")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "Hola@gm😀ail.com")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("name", "Hola@gmail.co😀m")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_25_invalid_first_name_POST(cls):
        cls.FROM("users/valid_user_2.json")
        cls.CHANGE_VALUE("first_name", "ex*mple")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("first_name", "prr😀m")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("first_name", "777")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_26_invalid_first_name_POST(cls):
        cls.FROM("users/valid_user_3.json")
        cls.CHANGE_VALUE("last_name", "ex*mple")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("last_name", "prr😀m")
        cls.POST("/places")
        cls.CODE_ASSERT(400)

        cls.CHANGE_VALUE("last_name", "777")
        cls.POST("/places")
        cls.CODE_ASSERT(400)


def run():
    TestPlaces.run()


if __name__ == "__main__":
    run()
