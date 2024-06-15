'''
    Defines this folder as a package
'''
from flask import Flask


app = Flask(__name__)

import api.main
