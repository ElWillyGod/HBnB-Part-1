#!/usr/bin/python3
"""Countries end point
GET /countries: Retrieve all pre-loaded countries.
GET /countries/{country_code}: Retrieve details of a specific country by its code.
"""
from flask import Flask, jsonify, request


app = Flask(__name__)

@app.route('/countries')
def get_All_Countries():

    countries = getAllCountries()

    if countries:
        return jsonify([{'name': country['name'], 'code': country['code']} for country in countries]), 200

    return jsonify({'error': 'error getAllCountries'}), 404


@app.route('/countries/<country_code>')
def get_Countries(country_code):

    country = getCountries(country_code)

    if not country:
        return jsonify({'error': '404 Not Found'}), 404

    return jsonify({'name': country['name'], 'code': country['code']}), 200
