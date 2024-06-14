#!/usr/bin/python3
"""Countries end point
GET /countries: Retrieve all pre-loaded countries.
GET /countries/{country_code}: Retrieve details of a specific country by its code.
"""
from flask import Flask, jsonify
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import validation as val


app = Flask(__name__)

@app.route('/countries')
def get_All_Countries():

    countries = LogicFacade.getByType("country")

    if countries:
        return jsonify([{'name': country['name'], 'code': country['code']}
                        for country in countries]), 200

    return jsonify({'message': "empy"}), 200


@app.route('/countries/<country_code>')
def get_Countries(country_code):


    if not val.isCountryValid(country_code):
        return jsonify({'error': '404 Not Found'}), 404

    try:
        countrys = LogicFacade.getCountry(country_code)

    except (logicexceptions.IDNotFoundError) as message:
        
        return jsonify(message), 404

    return jsonify({'name': countrys['name'], 'code': countrys['code']}), 200
