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
        '''
            Creates city to create place.
        '''

        cls.FROM(f"cities/valid_city_{num}.json")
        name = cls.SAVE_VALUE("name")
        cls.POST("/cities")
        cls.CODE_ASSERT(201)
        cls.GET("/cities")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("name", name, "id")

    @classmethod
    def createAmenity(cls, num: int) -> str:
        '''
            Creates amenity to create place.
        '''

        cls.FROM(f"amenities/valid_amenity_{num}.json")
        name = cls.SAVE_VALUE("name")
        cls.POST("/amenities")
        cls.CODE_ASSERT(201)
        cls.GET("/amenities")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("name", name, "id")

    @classmethod
    def createUser(cls, num: int) -> str:
        '''
            Creates user to host place.
        '''

        cls.FROM(f"users/valid_user_{num}.json")
        email = cls.SAVE_VALUE("email")
        cls.POST("/users")
        cls.CODE_ASSERT(201)
        cls.GET("/users")
        cls.CODE_ASSERT(200)
        return cls.GET_VALUE_WITH("email", email, "id")

    @classmethod
    def createPlace(cls,
                    num: int,
                    dic: dict | None = None,
                    *,
                    expectAtPOST: int = 201,
                    overrideNone: bool = False
                    ) -> dict:
        '''
            Creates a place:
                -> Creates all the necessary objects to create a place.
                -> Creates place using POST.
                -> GETs all places.
                -> Takes created place via name.
                -> Asserts that attributes were assigned successfully.
                -> Returns place w/o created_at or updated_at
        '''

        # Create external objects
        host_id = cls.createUser(num)
        city_id = cls.createCity(num)
        amenity_id = cls.createAmenity(num)
        amenity_ids = [amenity_id]

        # Take dict from json number num
        cls.FROM(f"places/valid_place_{num}.json")

        # Assign ids to place json
        cls.CHANGE_VALUE("host_id", host_id)
        cls.CHANGE_VALUE("city_id", city_id)
        cls.CHANGE_VALUE("amenity_ids", [amenity_id])

        # If dic is passed then override attributes.
        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.CHANGE_VALUE(key, dic[key])

        # If expected to fail at POST don't continue
        if expectAtPOST != 201:
            cls.POST("/places")
            cls.CODE_ASSERT(expectAtPOST)
            cls.deleteAll(host_id=host_id,
                          city_id=city_id,
                          amenity_ids=amenity_ids)
            return {}

        # POST Place
        cls.POST("/places")
        cls.CODE_ASSERT(201)  # 201

        # GET all places
        cls.GET(f"/places")
        cls.CODE_ASSERT(200)

        # Search in result for a place with this name and get the id
        id = cls.GET_VALUE_WITH("name", cls.json["name"], "id")

        # Assert that all values are correct
        for key in cls.json:
            cls.VALUE_ASSERT(key, cls.json[key])

        # Return dictionary of place + id
        output = cls.json.copy()
        output["amenity_ids"] = amenity_ids.copy()  # Deep copy
        output["id"] = id
        return output

    @classmethod
    def deleteAll(cls, **kwargs):
        '''
            Deletes a place given it's dict.
        '''
        host_id = kwargs["host_id"]
        amenity_ids = kwargs["amenity_ids"]
        city_id = kwargs["city_id"]
        cls.DELETE(f"/users/{host_id}")
        cls.CODE_ASSERT(204)
        for amenity_id in amenity_ids:
            cls.DELETE(f"/amenities/{amenity_id}")
            cls.CODE_ASSERT(204)
        cls.DELETE(f"/cities/{city_id}")
        cls.CODE_ASSERT(204)

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/places")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 4):
            place = cls.createPlace(i)
            cls.deleteAll(**place)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/places")
        cls.CODE_ASSERT(200)

    @classmethod
    def test_04_description_PUT(cls):
        place = cls.createPlace(1)
        id = place["id"]
        description = "UPDATED"
        cls.CHANGE_VALUE("description", description)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(201)

        cls.GET(f"/places/{id}")
        cls.CODE_ASSERT(200)
        cls.VALUE_ASSERT("description", description)

    @classmethod
    def test_05_empty_id_GET(cls):
        cls.GET("/places/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_06_empty_id_DELETE(cls):
        cls.DELETE("/places/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_07_empty_id_PUT(cls):
        place = cls.createPlace(2)
        cls.PUT("/places/")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_08_less_attributes_POST(cls):
        cls.createPlace(1, {"name": None}, expectAtPOST=400)
        cls.createPlace(2, {"description": None}, expectAtPOST=400)
        cls.createPlace(3, {"latitude": None, "longitude": None}, expectAtPOST=400)
        cls.createPlace(1, {"host_id": None, "city_id": None}, expectAtPOST=400)
        cls.createPlace(2, {"amenity_ids": None}, expectAtPOST=400)

    @classmethod
    def test_09_more_attributes_POST(cls):
        cls.createPlace(1, {"rating": 100}, expectAtPOST=400)

    @classmethod
    def test_10_different_attributes_POST(cls):
        cls.createPlace(1, {"description": None, "rating": 100}, expectAtPOST=400)
        cls.createPlace(2, {"name": None, "favorite_fruit": "banana"}, expectAtPOST=400)
        cls.createPlace(3, {"host_id": None, "explosive_type": "C4"}, expectAtPOST=400)
        cls.createPlace(1, {"city_id": None, "car": "Toyota"}, expectAtPOST=400)
        cls.createPlace(2, {"host_id": None, "explosive_type": "C4",
                            "city_id": None, "car": "Toyota"}, expectAtPOST=400)

    @classmethod
    def test_11_less_attributes_PUT(cls):
        place = cls.createPlace(1)
        id = place["id"]
        cls.REMOVE_VALUE("name")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("name", place["name"])

        cls.REMOVE_VALUE("host_id")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("host_id", place["host_id"])

        cls.REMOVE_VALUE("city_id")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("city_id", place["city_id"])

        cls.REMOVE_VALUE("host_id")
        cls.REMOVE_VALUE("city_id")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("host_id", place["host_id"])
        cls.CHANGE_VALUE("city_id", place["city_id"])

    @classmethod
    def test_12_more_attributes_PUT(cls):
        place = cls.createPlace(2)
        id = place["id"]
        cls.CHANGE_VALUE("rating", 100)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)

    @classmethod
    def test_13_different_attributes_PUT(cls):
        place = cls.createPlace(3)
        id = place["id"]
        cls.REMOVE_VALUE("description")
        cls.CHANGE_VALUE("rating", 100)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("description", place["description"])
        cls.REMOVE_VALUE("rating")

        cls.REMOVE_VALUE("name")
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("name", place["name"])
        cls.REMOVE_VALUE("favorite_fruit")

        cls.REMOVE_VALUE("host_id")
        cls.CHANGE_VALUE("explosive_type", "C4")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("host_id", place["host_id"])
        cls.REMOVE_VALUE("explosive_type")

        cls.REMOVE_VALUE("city_id")
        cls.CHANGE_VALUE("car", "Toyota")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("city_id", place["city_id"])
        cls.REMOVE_VALUE("car")

        cls.REMOVE_VALUE("host_id")
        cls.REMOVE_VALUE("city_id")
        cls.CHANGE_VALUE("explosive_type", "C4")
        cls.CHANGE_VALUE("car", "Toyota")
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(400)
        cls.CHANGE_VALUE("host_id", place["host_id"])
        cls.CHANGE_VALUE("city_id", place["city_id"])
        cls.REMOVE_VALUE("explosive_type")
        cls.REMOVE_VALUE("car")

    @classmethod
    def test_14_id_that_doesnt_exist_GET(cls):
        place = cls.createPlace(1)
        id = place["id"]
        cls.deleteAll(**place)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_15_id_that_doesnt_exist_PUT(cls):
        place = cls.createPlace(2)
        id = place["id"]
        cls.deleteAll(**place)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_16_id_that_doesnt_exist_DELETE(cls):
        place = cls.createPlace(3)
        id = place["id"]
        cls.deleteAll(**place)
        cls.PUT(f"/places/{id}")
        cls.CODE_ASSERT(404)

    @classmethod
    def test_17_empty_strings_POST(cls):
        def checkIfEmpty(key):
            cls.createPlace(2, {key: ""}, expectAtPOST=400)
            cls.createPlace(3, {key: "    "}, expectAtPOST=400)

        checkIfEmpty("host_id")
        checkIfEmpty("city_id")
        checkIfEmpty("name")

        cls.createPlace(2, {"amenity_ids": [""]}, expectAtPOST=400)
        cls.createPlace(3, {"amenity_ids": ["    "]}, expectAtPOST=400)

    @classmethod
    def test_18_invalid_ints_POST(cls):
        cls.createPlace(1, {"number_of_rooms": -1}, expectAtPOST=400)
        cls.createPlace(2, {"number_of_bathrooms": -1}, expectAtPOST=400)
        cls.createPlace(3, {"max_guests": -1}, expectAtPOST=400)

    @classmethod
    def test_19_invalid_floats_POST(cls):
        cls.createPlace(1, {"price_per_night": -1}, expectAtPOST=400)
        cls.createPlace(2, {"price_per_night": 0}, expectAtPOST=400)
        cls.createPlace(2, {"latitude": 120.0}, expectAtPOST=400)
        cls.createPlace(3, {"latitude": -120.0}, expectAtPOST=400)
        cls.createPlace(2, {"longitude": 200.0}, expectAtPOST=400)
        cls.createPlace(3, {"longitude": -200.0}, expectAtPOST=400)

    @classmethod
    def test_20_invalid_strings_POST(cls):
        def testStr(key):
            cls.createPlace(1, {key: "\n"}, expectAtPOST=400)
            cls.createPlace(2, {key: "Ex\nmple"}, expectAtPOST=400)
            cls.createPlace(3, {key: "🤔"}, expectAtPOST=400)
            cls.createPlace(1, {key: "Ex🤔mple"}, expectAtPOST=400)

        testStr("host_id")
        testStr("name")
        testStr("city_id")

        cls.createPlace(2, {"host_id": "Fish"}, expectAtPOST=400)
        cls.createPlace(3, {"city_id": "Fish"}, expectAtPOST=400)
        cls.createPlace(1, {"amenity_ids": ["Fish"]}, expectAtPOST=400)
        cls.createPlace(2, {"amenity_ids": ["\n"]}, expectAtPOST=400)
        cls.createPlace(3, {"amenity_ids": ["Ex\nmple"]}, expectAtPOST=400)
        cls.createPlace(1, {"amenity_ids": ["🤔"]}, expectAtPOST=400)
        cls.createPlace(2, {"amenity_ids": ["Ex🤔mple"]}, expectAtPOST=400)

    @classmethod
    def test_21_amenity_ids_can_be_empty_POST(cls):
        place = cls.createPlace(1, {"amenity_ids": []})


def run():
    TestPlaces.run()


if __name__ == "__main__":
    run()
