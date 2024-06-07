#!/usr/bin/python3
"""cities endpoint
GET /countries/{country_code}/cities: Retrieve all cities belonging to a specific country.
POST /cities: Create a new city.
GET /cities: Retrieve all cities.
GET /cities/{city_id}: Retrieve details of a specific city.
PUT /cities/{city_id}: Update an existing city’s information.
DELETE /cities/{city_id}: Delete a specific city.
"""
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/countries/<country_code>/cities')
def get_All_Cities(country_code):
    cities = getCitiesFromContries(country_code)

    if cities:
        return jsonify([{'id': city['id'], 'name': city['name'], 'country_code': city['country_code'], 'created_at': city['created_at'], 'updated_at': city['updated_at']} for city in cities]), 200

    return jsonify({'error': 'no hay elementos'}), 200
