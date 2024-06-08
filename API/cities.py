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
def get_Cities_For_Contr(country_code):
    cities = getCitiesFromContries(country_code)

    if cities:
        return jsonify([{'id': city['id'], 'name': city['name'], 'country_code': city['country_code'], 'created_at': city['created_at'], 'updated_at': city['updated_at']} for city in cities]), 200

    return jsonify({'message': 'no hay elementos'}), 200


@app.route('/cities', methods=["POST"])
def cereate_Cities():
    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    name = data['name']
    code = data['country_code']

    if not name or not code:
        return jsonify({'error': "400 Bad Request"}), 400

    if CodeValid(code):
        return jsonify({'error': "el codigo no es valido"}), 400

    if CodeAndCityValid(code, name):
        return jsonify({'error': "nombre diplicado o invalido"}), 409

    if cereateCities(data):
        return jsonify({"id": data['id'], "name": data['name'], "country_code": data['country_code'], "created_at": data['country_code'], "updated_at": data['updated_at']}), 201

    return jsonify({'error': "error al crear la city"}), 400


@app.route('/cities')
def get_All_Cities():
    cities = getAllCities()

    if cities:
        return jsonify([{"id": city['id'], "name": city['name'], "country_code": city['country_code'], "created_at": city['created_at'], "updated_at": city['updated_at']} for city in cities]), 200

    return jsonify({'message': "no tiene cities"}), 200
