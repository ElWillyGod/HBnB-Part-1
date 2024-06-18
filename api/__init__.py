
'''
    Package where endpoints and type validations are made.
'''

from flask import Flask
from flasgger import Swagger

from api.swagger import template

app = Flask("AirBnB-MWA")

swagger = Swagger(app, template=template)

import api.amenities
import api.cities
import api.countries
import api.places
import api.reviews
import api.users
