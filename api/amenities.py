#!/usr/bin/python3
"""amenities endpoint
POST /amenities: Create a new amenity.
GET /amenities: Retrieve a list of all amenities.
GET /amenities/{amenity_id}: Retrieve detailed information about a specific amenity.
PUT /amenities/{amenity_id}: Update an existing amenity’s information.
DELETE /amenities/{amenity_id}: Delete a specific amenity."""

from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/amenities', methods=["POST"])
def create_Amenities():
    data = request.get_json()

    if not data or not data['name']:
        return jsonify({'error': "No date"}), 400

    if not ValidNameAmenities(data):
        return jsonify({'error': "amenities duplicated"}), 409

    amenities = createAmenities(data)

    if amenities:
        return jsonify({"id": amenities['id'], "name": amenities['name'],
                        "created_at": amenities['created_at'],
                        "updated_at": amenities['updated_at']}), 201

    return jsonify({'error': "error al crear"}), 400

@app.route('/amenities')
def ger_all_amenities():
    amenities = getAllAmenities()

    return jsonify([{"id": ameni['id'], "name": ameni['name'],
                     "created_at": ameni['created_at'],
                     "updated_at": ameni['updated_at']} for ameni in amenities]), 200

@app.route('/amenities/<amenity_id>')
def get_amenities(amenity_id):
    amenities = getAmenities(amenity_id)

    if not amenities:
        return jsonify({'error': "amenitie not fund"}), 404

    return jsonify({"id": amenities['id'], "name": amenities["name"],
                    "created_at": amenities['created_at'],
                    "updated_at": amenities['updated_at']}), 200


@app.route('/amenities/<amenity_id>', methods=["PUT"])
def update_Amenities(amenity_id):
    data = request.get_json()

    if not data or data['name']:
        return jsonify({'error': "data Null"}), 400

    amenity = getAmenities(amenity_id)

    if not amenity:
        return jsonify({'error': "no se encontro la amenity"}), 404

    if getAmenitiesName(amenity['name']) and data['name'] != amenity['name']:
        return jsonify({'error': "amenity not exists"}), 409

    amenity = updateAmenities(amenity_id, data)

    if amenity:
        return jsonify({"id": amenity['id'], "name": amenity["name"],
                        "created_at": amenity['created_at'],
                        "updated_at": amenity['updated_at']}), 200
    
    return jsonify({'error': "no se pudo updatear"}), 400


@app.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_Amenities(amenity_id):
    amenity = getAmenities(amenity_id)

    if not amenity:
        return jsonify({'error': "error al eliminar"}), 404

    deleteAmenities(amenity_id)
    
    return jsonify({'message': "se borro la amenity"}), 204
