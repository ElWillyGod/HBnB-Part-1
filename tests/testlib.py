
'''
    Provides common functions for testing.
'''

import inspect
from typing import Any
import requests
import json
from pathlib import Path


class HTTPTestClass:
    '''
        Test Base Class for testing the API.
        Test Classes inherit from this class to get all methods.
        Flask Server must be running for tests to work.
    '''

    URL = "http://127.0.0.1:5000/"

    testPassed = 0
    lastResponse = None
    json = {}
    headers = {'Content-type': 'application/json',
               'Accept': 'application/json'}

    @classmethod
    def CODE_ASSERT(cls,
        code_expected: int,
        errormsg: str | None = None
        ) -> None:

        code = cls.lastResponse.status_code

        if errormsg is None:
            errormsg = f"Code was not expected:\
            {code} != {code_expected}"

        assert code == code_expected, errormsg

        cls.testPassed += 1

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
                try:
                    value = dic[key]
                    found_one = True
                    if errormsg is None:
                        errormsg = f"Code was not expected:\
                        {value} != {value_expected}"
                    try:
                        assert value == value_expected, errormsg
                        cls.testPassed += 1
                        return
                    except AssertionError:
                        pass
                except KeyError:
                    pass
            if found_one:
                raise AssertionError(errormsg)
            raise KeyError(f"key not found for test: {key}")

        try:
            value = data[key]
        except KeyError:
            raise KeyError(f"key not found for test: {key}")
        if errormsg is None:
            errormsg = f"Code was not expected:\
            {value} != {value_expected}"
        assert value == value_expected, errormsg

        cls.testPassed += 1

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
        return cls.json[key]

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
        for name in tests:
            print(f"Running {name}...")
            tests[name]()
