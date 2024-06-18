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
    def createCity(cls,
                    num: int,
                    dic: dict | None = None,
                    *,
                    expectAtPOST: int = 201,
                    overrideNone: bool = False
                    ) -> dict:
        '''
            Creates a city.
        '''
        cls.FROM(f"cities/valid_city_{num}.json")
        name = cls.SAVE_VALUE("name")

        if dic is not None:
            for key in dic:
                if dic[key] is None or overrideNone:
                    cls.REMOVE_VALUE(key)
                else:
                    cls.CHANGE_VALUE(key, dic[key])

        if expectAtPOST != 201:
            cls.POST("/cities")
            cls.ASSERT_CODE(expectAtPOST)
            return {}

        cls.POST("/cities")
        cls.ASSERT_CODE(201)

        output = cls.json.copy()
        output["id"] = cls.GET_RESPONSE_VALUE("id")
        return output

    @classmethod
    def deleteCity(cls, **kwargs):
        id = kwargs["id"]
        cls.DELETE(f"/cities/{id}")
        cls.ASSERT_CODE(204)

    @classmethod
    def test_01_general_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_02_valid_POST_GET_DELETE(cls):
        for i in range(1, 5):
            city = cls.createCity(i)
            cls.deleteCity(**city)

    @classmethod
    def test_03_another_general_GET(cls):
        cls.GET("/cities")
        cls.ASSERT_CODE(200)

    @classmethod
    def test_04_valid_PUT(cls):
        for i in range(1, 5):
            city = cls.createCity(i)
            cls.CHANGE_VALUE("name", city["name"] + "UPDATED")
            cls.PUT("/cities/" + city["id"])
            cls.ASSERT_CODE(201)

    @classmethod
    def test_05_valid_country_code_PUT(cls):
        city = cls.createCity(1)
        cls.CHANGE_VALUE("country_code", "CA")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(201)

    @classmethod
    def test_06_duplicated_entry_POST(cls):
        cls.createCity(2)
        cls.createCity(2, expectAtPOST=409)

    @classmethod
    def test_07_duplicated_entry_PUT(cls):
        city1 = cls.createCity(2)
        city2 = cls.createCity(3)
        cls.CHANGE_VALUE("name", city1["name"])
        cls.CHANGE_VALUE("country_code", city1["country_code"])
        cls.PUT("/cities/" + city2["id"])
        cls.ASSERT_CODE(409)

    @classmethod
    def test_08_empty_id_GET(cls):
        cls.GET("/cities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_09_empty_id_DELETE(cls):
        cls.DELETE("/cities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_10_empty_id_PUT(cls):
        cls.createCity(4)
        cls.PUT("/cities/")
        cls.ASSERT_CODE(404)

    @classmethod
    def test_11_less_attributes_POST(cls):
        cls.createCity(3, {"name": None}, expectAtPOST=400)
        cls.createCity(4, {"country_code": None}, expectAtPOST=400)

    @classmethod
    def test_12_more_attributes_POST(cls):
        cls.createCity(1, {"favorite_fruit": "banana"}, expectAtPOST=400)

    @classmethod
    def test_13_different_attributes_POST(cls):
        cls.createCity(3,{"name": None,
                          "favorite_fruit": "banana"}, expectAtPOST=400)
        cls.createCity(4, {"country_code": None,
                           "favorite_fruit": "banana"}, expectAtPOST=400)
        cls.createCity(1, {"country_code": None, "name": None,
                           "explosive_type": "C4",
                           "favorite_fruit": "banana"}, expectAtPOST=400)

    @classmethod
    def test_14_less_attributes_PUT(cls):
        city = cls.createCity(1)

        cls.REMOVE_VALUE("name")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)
        cls.CHANGE_VALUE("name", city["name"])

        cls.REMOVE_VALUE("country_code")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)

    @classmethod
    def test_15_more_attributes_PUT(cls):
        city = cls.createCity(2)
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)

    @classmethod
    def test_16_different_attributes_PUT(cls):
        city = cls.createCity(3)

        cls.REMOVE_VALUE("name")
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)
        cls.REMOVE_VALUE("favorite_fruit")
        cls.CHANGE_VALUE("name", city["name"])

        cls.REMOVE_VALUE("country_code")
        cls.CHANGE_VALUE("explosive_type", "C4")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)
        cls.REMOVE_VALUE("explosive_type")
        cls.CHANGE_VALUE("country_code", city["country_code"])

        cls.REMOVE_VALUE("name")
        cls.REMOVE_VALUE("country_code")
        cls.CHANGE_VALUE("favorite_fruit", "banana")
        cls.CHANGE_VALUE("explosive_type", "C4")
        cls.PUT("/cities/" + city["id"])
        cls.ASSERT_CODE(400)

    @classmethod
    def test_17_id_that_doesnt_exist_GET(cls):
        city = cls.createCity(4)
        cls.deleteCity(**city)
        cls.GET(f"/cities/" + city["id"])
        cls.ASSERT_CODE(404)

    @classmethod
    def test_18_id_that_doesnt_exist_PUT(cls):
        city = cls.createCity(1)
        cls.deleteCity(**city)
        cls.PUT(f"/cities/" + city["id"])
        cls.ASSERT_CODE(404)

    @classmethod
    def test_19_id_that_doesnt_exist_DELETE(cls):
        city = cls.createCity(2)
        cls.deleteCity(**city)
        cls.DELETE(f"/cities/" + city["id"])
        cls.ASSERT_CODE(404)

    @classmethod
    def test_20_empty_name_POST(cls):
        cls.createCity(3, {"name": ""}, expectAtPOST=400)
        cls.createCity(4, {"name": "    "}, expectAtPOST=400)

    @classmethod
    def test_21_empty_country_code_POST(cls):
        cls.createCity(1, {"country_code": ""}, expectAtPOST=400)
        cls.createCity(2, {"country_code": "    "}, expectAtPOST=400)

    @classmethod
    def test_22_invalid_country_code_POST(cls):
        def testPOST(email):
            cls.createCity(3, {"country_code": email}, expectAtPOST=400)

        testPOST("URU")
        testPOST("U")
        testPOST("uy")
        testPOST("10")
        testPOST("U5")
        testPOST("U😀")
        testPOST("😀😀")
        testPOST("😀")

    @classmethod
    def test_23_invalid_name_POST(cls):
        def testPOST(name):
            cls.createCity(4, {"name": name}, expectAtPOST=400)

        testPOST("prr😀m")
        testPOST("777")
        testPOST("Mi\nColon\n")

    @classmethod
    def test_24_null_args_POST(cls):
        cls.createCity(1, {"country_code": None},
                       expectAtPOST=400, overrideNone=True)
        cls.createCity(2, {"name": None},
                       expectAtPOST=400, overrideNone=True)
        cls.createCity(3, {"country_code": None, "name": None},
                       expectAtPOST=400, overrideNone=True)

    @classmethod
    def test_24_null_args_POST(cls):
        pass


def run():
    TestCities.run()


if __name__ == "__main__":
    run()
