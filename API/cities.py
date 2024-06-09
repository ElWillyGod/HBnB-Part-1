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
        return jsonify([{'id': city['id'], 'name': city['name'],
                         'country_code': city['country_code'],
                         'created_at': city['created_at'],
                         'updated_at': city['updated_at']} for city in cities]), 200

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

    if CodeValidCountry(code):
        return jsonify({'error': "el codigo no es valido"}), 400

    if CodeAndCityValid(code, name):
        return jsonify({'error': "nombre diplicado o invalido"}), 409
    
    city = cereateCities(data)

    if city:
        return jsonify({"id": city['id'], "name": city['name'],
                        "country_code": city['country_code'],
                        "created_at": city['country_code'],
                        "updated_at": city['updated_at']}), 201

    return jsonify({'error': "error al crear la city"}), 400


@app.route('/cities')
def get_All_Cities():
    cities = getAllCities()

    if cities:
        return jsonify([{"id": city['id'], "name": city['name'],
                         "country_code": city['country_code'],
                         "created_at": city['created_at'],
                         "updated_at": city['updated_at']} for city in cities]), 200

    return jsonify({'message': "no tiene cities"}), 200


@app.route('/cities/<city_id>')
def get_Cities(city_id):
    city = getCitiesInId(city_id)

    if not city:
        return jsonify({'error': "404 Not Fund"}), 404

    return jsonify({"id": city['id'], "name": city['name'],
                    "country_code": city['country_code'],
                    "created_at": city['created_at'],
                    "updated_at": city['updated_at']}), 200


@app.route('/cities/<city_id>', methods=["PUT"])
def update_Cities(city_id):
    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    city = getCitiesInId(city_id)

    if not city:
        return jsonify({'error': "404 Not Fund"}), 404

    if not data['name'] or not data['country_code']:
        return jsonify({'error': "faltan campos en la data"}), 400

    if CodeValidCountry(data['country_code']):
        return jsonify({'error': "Error de codigo country"}), 400

    if CodeAndCityValid(data['code'], data['name']) and data['name'] != city['name']:
        return jsonify({'error': "409 Conflisct"}), 409

    city = updateCities(city_id, data)

    if city:
        return jsonify({"id": city['id'], "name": city['name'],
                        "country_code": city['country_code'],
                        "created_at": city['created_at'],
                        "updated_at": city['updated_at']}), 200

    return jsonify({'error': "error al actualizar"}), 400


@app.route('/cities/<city_id>', methods=["DELETE"])
def delete_Cities(city_id):
    city = getCitiesInId(city_id)

    if not city_id:
        return jsonify({'error': 'city not found'}), 404

    if deleteCities(city_id):
        return jsonify({'message': "City delete OK"}), 204

    return jsonify({'error': "error al deletear"}), 400
