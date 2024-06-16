#!/usr/bin/python3
"""Countries end point
GET /countries: Retrieve all pre-loaded countries.
GET /countries/{country_code}: Retrieve details of a specific country by its code.
"""
from api import app
from flask import jsonify
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.route('/countries')
def get_All_Countries():

    countries = LogicFacade.getByType("country")

    if countries is not None:
        return jsonify(countries), 200

    return jsonify({'message': "empy"}), 200


@app.route('/countries/<country_code>')
def get_Countries(country_code):

    if not val.isCountryValid(country_code):
        return jsonify({'error': '404 Not Found'}), 404

    try:
        countrys = LogicFacade.getCountry(country_code)

    except (logicexceptions.IDNotFoundError) as message:
        
        return jsonify({'error': str(message)}), 404

    return jsonify(countrys), 200
