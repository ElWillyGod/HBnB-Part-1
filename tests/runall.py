#!/usr/bin/python3

'''
    Run all tests.
'''

import sys

import test_smoke


if test_smoke.result == False:
    sys.exit(1)
