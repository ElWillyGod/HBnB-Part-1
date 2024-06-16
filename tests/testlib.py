
'''
    Provides common functions for testing.
'''

import inspect
from typing import Any
import requests
import json
from pathlib import Path

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"


class HTTPTestClass:
    '''
        Test Base Class for testing the API.
        Test Classes inherit from this class to get all methods.
        Flask Server must be running for tests to work.
        If debug == True it shows the result of all passed assertions.
    '''

    URL: str = "http://127.0.0.1:5000/"

    assertionsPassed: int = 0
    assertionsFailed: int = 0
    testsPassed: int = 0
    testsFailed: int = 0
    lastResponse: requests.Response | None = None
    json: dict = {}
    headers: dict = {'Content-type': 'application/json',
                     'Accept': 'application/json'}
    prefix: str = f">>> "
    suffix: str = f"{RESET}"
    debug: bool = False

    @classmethod
    def _ASSERTION_SUCCESS(cls,
                           msg: str | None = None
                           ) -> None:

        if msg is None:
            msg = "Assertion Passed"
        if cls.debug:
            print(f"{cls.prefix}{GREEN}{msg}{cls.suffix}")
        cls.assertionsPassed += 1

    @classmethod
    def _ASSERTION_FAILURE(cls,
                           msg: str | None = None
                           ) -> None:

        if msg is None:
            msg = "Assertion Failed"
        print(f"{cls.prefix}{RED}{msg}{cls.suffix}")
        cls.assertionsFailed += 1

    @classmethod
    def _ASSERT(cls,
                value: Any,
                expected_value: Any,
                errormsg: str | None = None
                ) -> None:
        if value == expected_value:
            errormsg = f"{value} == {expected_value}" if errormsg is None\
                else errormsg
            cls._ASSERTION_SUCCESS(errormsg)
        else:
            errormsg = f"{value} != {expected_value}" if errormsg is None\
                else errormsg
            cls._ASSERTION_FAILURE(errormsg)

    @classmethod
    def CODE_ASSERT(cls,
                    code_expected: int,
                    errormsg: str | None = None
                    ) -> None:

        code = cls.lastResponse.status_code
        cls._ASSERT(code, code_expected, errormsg)

    @classmethod
    def VALUE_ASSERT(cls,
            key: str,
            value_expected: Any,
            errormsg: str | None = None
            ) -> None:

        data = cls.lastResponse.json()
        if isinstance(data, list):
            found_one = False
            for dic in data:
                if key in dic:
                    value = dic[key]
                    found_one = True
                    if value == value_expected:
                        cls._ASSERT(value, value_expected, errormsg)
                        return
            if found_one:
                if errormsg is None:
                    errormsg = (f"No key with expected value found " +
                    f"{key}: {value_expected}")
                raise AssertionError(errormsg)
            else:
                raise KeyError(f"key not found for test: {key}")

        if key not in data:
            raise KeyError(f"key not found for test: {key}")
        value = data[key]
        cls._ASSERT(value, value_expected, errormsg)

    @classmethod
    def FROM(cls, filename: str) -> None:
        current_dir = Path(__file__).parent.resolve()
        content: dict
        with open(f"{current_dir}/{filename}", "r") as file:
            content = json.load(file)
        cls.json = content

    @classmethod
    def CLEAR(cls) -> None:
        cls.json = {}

    @classmethod
    def CHANGE(cls, key: str, value: Any):
        cls.json[key] = value

    @classmethod
    def SAVE_VALUE(cls, key: str):
        '''
            Gets value from key of sent json.
        '''
        return cls.json[key]

    @classmethod
    def GET_VALUE(cls, key: str):
        '''
            Gets value from key of last response.
        '''
        if isinstance(cls.lastResponse, dict):
            return cls.lastResponse[key]
        else:
            for dic in cls.lastResponse:
                if key in dic:
                    return dic[key]
            raise KeyError(f"key not found for test: {key}")

    @classmethod
    def GET(cls, endpoint: str) -> dict:
        response = requests.get(f"{HTTPTestClass.URL}{endpoint}")
        cls.lastResponse = response
        return response

    @classmethod
    def POST(cls, endpoint: str) -> dict:
        response = requests.post(f"{HTTPTestClass.URL}{endpoint}",
                                 json=cls.json,
                                 headers=cls.headers)
        cls.lastResponse = response
        return response

    @classmethod
    def PUT(cls, endpoint: str) -> dict:
        response = requests.put(f"{HTTPTestClass.URL}{endpoint}",
                                 json=cls.json,
                                 headers=cls.headers)
        cls.lastResponse = response
        return response

    @classmethod
    def DELETE(cls, endpoint: str) -> dict:
        response = requests.delete(f"{HTTPTestClass.URL}{endpoint}")
        cls.lastResponse = response
        return response

    @classmethod
    def run(cls) -> None:
        '''
            Gets all methods, and then filters them to get only methods that
            have the word "test" in them and are not from Object.
        '''
        methods = inspect.getmembers(cls, lambda a: inspect.isroutine(a))
        tests = {
                 attr: func for attr, func in methods if
                 not (attr[0:2] == "__" and attr[-2:] == "__") and
                 attr.find("test") != -1
                }

        print(f"{cls.prefix}{BLUE}Running {cls.__name__}...{cls.suffix}")
        for name in tests:
            print(f"{cls.prefix}{YELLOW}Running {name}...{cls.suffix}")
            try:
                tests[name]()
                cls.testsPassed += 1
            except AssertionError as e:
                print(f"{cls.prefix}{RED}Check failed on {name}:{RESET}\n" +
                      f"\t{e}{cls.suffix}")
                cls.testsFailed += 1
            except KeyError as e:
                print(f"{cls.prefix}{RED}{name} did not find key to check:" +
                      f"{RESET}\n\t{e}{cls.suffix}")
                cls.testsFailed += 1

        if cls.assertionsFailed == 0:
            print(f"{cls.prefix}{GREEN}All tests from " +
                  f"{cls.__name__} passed: ", end="")
        elif cls.assertionsPassed == 0:
            print(f"{cls.prefix}{RED}All tests from " +
                  f"{cls.__name__} failed: ", end="")
        else:
            print(f"{cls.prefix}{YELLOW}Some tests from " +
                  f"{cls.__name__} failed: ", end="")
        tests_total = cls.testsPassed + cls.testsFailed
        assertions_total = cls.assertionsFailed + cls.assertionsPassed
        print(f"{RESET}{cls.testsPassed}/{tests_total} - " +
              f"{cls.assertionsPassed}/{assertions_total}" +
              f"{cls.suffix}\n")
