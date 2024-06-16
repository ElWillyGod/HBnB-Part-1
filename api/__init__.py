'''
    Defines this folder as a package
'''
from flask import Flask
from flasgger import Swagger

app = Flask(__name__)
template = {
    "swagger": "2.0",
    "info": {
        "title": "HBNB API",
        "description": "API for Holberton AirBNB project",
        "contact": {
            "responsibleDeveloper": "Wilson Antognazza, Matias Davezac, Alison Alvez",
            "email": "alisonalvez05@gmailcom, w@w.com, m@a.com",
        },
        "version": "0.0.1"
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
}

swagger = Swagger(app, template=template)

import api.main
