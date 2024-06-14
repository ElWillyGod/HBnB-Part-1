#!/usr/bin/python3
"""amenities endpoint
POST /amenities: Create a new amenity.
GET /amenities: Retrieve a list of all amenities.
GET /amenities/{amenity_id}: Retrieve detailed information about a specific amenity.
PUT /amenities/{amenity_id}: Update an existing amenity’s information.
DELETE /amenities/{amenity_id}: Delete a specific amenity."""

from flask import Flask, jsonify, request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import validation as val

app = Flask(__name__)


@app.route('/amenities', methods=["POST"])
def create_Amenities():
    data = request.get_json()

    if not data or not val.isNameValid(data['name']):
        return jsonify({'error': "No date"}), 400

    try:
        LogicFacade.createObjectByJson('amenity', data)

    except (logicexceptions.AmenityNameDuplicated) as message:
        return jsonify(message), 409

    return jsonify({'message': "tod OKa"}), 201


@app.route('/amenities')
def ger_all_amenities():
    amenities = LogicFacade.getByType('amenity')

    if amenities:
        return jsonify([{"id": ameni['id'], "name": ameni['name'],
                         "created_at": ameni['created_at'],
                         "updated_at": ameni['updated_at']} for ameni in amenities]), 200

    return jsonify({'message': "no hay amenities"}), 200

@app.route('/amenities/<amenity_id>')
def get_amenities(amenity_id):
    if not val.idChecksum(amenity_id):
        return jsonify({'error': "el id esta cagado"}), 400

    try:
        amenities = LogicFacade.getByID(amenity_id, 'amenity')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({"id": amenities['id'], "name": amenities["name"],
                    "created_at": amenities['created_at'],
                    "updated_at": amenities['updated_at']}), 200


@app.route('/amenities/<amenity_id>', methods=["PUT"])
def update_Amenities(amenity_id):
    data = request.get_json()

    if not data or not val.isNameValid(data['name']):
        return jsonify({'error': "data Null"}), 400

    if not val.idChecksum(amenity_id):
        return jsonify({'error': 'la id esta mal'}), 400

    try:
        LogicFacade.updateByID(amenity_id, 'amenity', data)

    except (logicexceptions.AmenityNameDuplicated) as message:
        return jsonify(message), 409

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({'message': "todo OKa"}), 200
    

@app.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_Amenities(amenity_id):
    if not val.idChecksum(amenity_id):
        return jsonify({'message': "id type error"}), 400

    try:
        LogicFacade.deleteByID(amenity_id, 'amenity')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({'message': 'Todo OKa'}), 204
