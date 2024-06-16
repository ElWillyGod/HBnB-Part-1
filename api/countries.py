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
    """
    Retrieve all countries
    ---
    tags:
      - countries
    responses:
      200:
        description: A list of all countries
        schema:
          type: array
          items:
            type: object
            properties:
              country_code:
                type: string
                description: The ISO code of the country
              name:
                type: string
                description: The name of the country
    """
    countries = LogicFacade.getAllCountries()

    return jsonify(countries), 200


@app.route('/countries/<country_code>')
def get_Countries(country_code):
    """
    Retrieve details of a specific country by its code
    ---
    tags:
      - countries
    parameters:
      - in: path
        name: country_code
        type: string
        required: true
        description: ISO code of the country (e.g., 'US' for United States)
    responses:
      200:
        description: Details of the country
        schema:
          type: object
          properties:
            country_code:
              type: string
              description: The ISO code of the country
            name:
              type: string
              description: The name of the country
      404:
        description: Country not found
    """

    if not val.isCountryValid(country_code):
        return jsonify({'error': '404 Not Found'}), 404

    try:
        countrys = LogicFacade.getCountry(country_code)

    except (logicexceptions.IDNotFoundError) as message:
        
        return jsonify({'error': str(message)}), 404

    return jsonify(countrys), 200
