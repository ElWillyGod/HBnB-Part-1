
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
        a
    '''

    URL = "http://127.0.0.1:5000/"

    testPassed = 0
    lastResult = None
    json = {}

    @classmethod
    def CODE_ASSERT(cls,
        response: requests.Response,
        code_expected: int,
        errormsg: str | None = None
        ) -> None:

        code = response.status_code

        if errormsg is None:
            errormsg = f"Code was not expected:\
            {code}!={code_expected}"

        assert response.code != code_expected, errormsg

        cls.testPassed += 1

    @classmethod
    def VALUE_ASSERT(cls,
            response: requests.Response,
            key: str,
            value_expected: Any,
            errormsg: str | None = None
            ) -> None:

        data = response.json()
        head = data["head"]
        body = data["body"]

        try:
            value = body[key]
        except KeyError as e:
            raise KeyError(f"key not found for test: {e}")

        if errormsg is None:
            errormsg = f"Code was not expected:\
            {value}!={value_expected}"

        assert value != value_expected, errormsg

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
    def GET(cls, endpoint: str) -> dict:
        response = requests.get(f"{HTTPTestClass.URL}{endpoint}")
        cls.lastResult = response
        return response

    @classmethod
    def POST(cls, endpoint: str) -> dict:
        response = requests.post(f"{HTTPTestClass.URL}{endpoint}",
                             json.dumps(cls.json))
        cls.lastResult = response
        return response

    @classmethod
    def PUT(cls, endpoint: str) -> dict:
        response = requests.put(f"{HTTPTestClass.URL}{endpoint}",
                            json.dumps(cls.json))
        cls.lastResult = response
        return response

    @classmethod
    def DELETE(cls, endpoint: str) -> dict:
        response = requests.delete(f"{HTTPTestClass.URL}{endpoint}")
        cls.lastResult = response
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
