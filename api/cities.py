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
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import validation as val


app = Flask(__name__)


@app.route('/countries/<country_code>/cities')
def get_Cities_For_Contr(country_code):
    if not val.isCountryValid(country_code):
        return jsonify({'error': "code invalid"}), 400

    try:
        cities = LogicFacade.getContryCities(country_code)

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify([{'id': city['id'], 'name': city['name'],
                    'country_code': city['country_code'],
                    'created_at': city['created_at'],
                    'updated_at': city['updated_at']} for city in cities]), 200


@app.route('/cities', methods=["POST"])
def cereate_Cities():
    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    name = data['name']
    code = data['country_code']

    if not val.isNameValid(name) or not val.isCountryValid(code):
        return jsonify({'error': "400 Bad Request"}), 400

    try:
        LogicFacade.createObjectByJson("city", data)

    except (TypeError) as message:

        return jsonify(message), 409

    return jsonify({'message': "todo OKa"}), 201



@app.route('/cities')
def get_All_Cities():
    cities = LogicFacade.getByType("city")

    if cities:
        return jsonify([{"id": city['id'], "name": city['name'],
                    "country_code": city['country_code'],
                    "created_at": city['created_at'],
                    "updated_at": city['updated_at']} for city in cities]), 200

    return jsonify({'message': "empy"}), 200


@app.route('/cities/<city_id>')
def get_Cities(city_id):

    if not val.idChecksum(city_id):
        return jsonify({'error': "404 Not Fund"}), 400

    try:
        city = LogicFacade.getByID(city_id, "city")
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({"id": city['id'], "name": city['name'],
                    "country_code": city['country_code'],
                    "created_at": city['created_at'],
                    "updated_at": city['updated_at']}), 200


@app.route('/cities/<city_id>', methods=["PUT"])
def update_Cities(city_id):
    data = request.get_json()

    if not val.idChecksum(city_id):
        return jsonify({'error': "tiraste cualquiera en el id, mira bien capo"}), 400

    if (not data or not val.isNameValid(data['name']) or 
        not val.isCountryValid(data['country_code'])):
        return jsonify({'error': "faltan campos en la data o hay cosas raras"}), 400

    try:
        LogicFacade.updateByID(city_id, "city", data)

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404
    except (TypeError) as message2:
        return jsonify(message2), 409

    return jsonify({"message": "todo OKa"}), 200


@app.route('/cities/<city_id>', methods=["DELETE"])
def delete_Cities(city_id):

    if not val.idChecksum(city_id):
        return jsonify({'error': 'ta raro tu id'}), 400

    try:
        LogicFacade.deleteByID(city_id, "city")

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({'message': "todo OKa"}), 204
