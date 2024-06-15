#!/usr/bin/python3
"""places endpoint
POST /places: Create a new place.
GET /places: Retrieve a list of all places.
GET /places/{place_id}: Retrieve detailed information about a specific place.
PUT /places/{place_id}: Update an existing place’s information.
DELETE /places/{place_id}: Delete a specific place.
"""
from flask import Flask, jsonify, request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import validation as val


app = Flask(__name__)


@app.route('/places', methods=["POST"])
def create_Place():
    data = request.get_json()

    if not data:
        return jsonify({'error': "no data"}), 400

    if not (val.isLatitudeValid(data['latitude']) and val.isLongitudeValid(data['longitude'])):
        return jsonify({'error': "ubicacion invalida"}), 400

    if not (isinstance(data['number_of_rooms'], int) and (data['number_of_rooms'] > 0) and
            isinstance(data['number_of_bathrooms'], int) and
            (data['number_of_bathrooms'] >= 0) and isinstance(data['max_guests'], int) and
            data['max_guests'] > 0 and
            isinstance(data['price_per_night'], (int, float)) and data['price_per_night'] > 0):
        return jsonify({'error': "datos de rooms invalidos"}), 400

    if not val.idChecksum(data['city_id']):
        return jsonify({'error': "el codigo de la city esta mal"}), 400

    for amenity_id in data['amenity_ids']:
        if not val.idChecksum(amenity_id):
            return jsonify({'error': 'Invalid amenity_id'}), 400

    try:
        LogicFacade.createObjectByJson('place', data)
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404


    return jsonify({'OKa'}), 201


@app.route('/places')
def get_All_Places():
    places = LogicFacade.getByType('place')

    if not places:
        return jsonify({'message': 'None places'}), 200

    return jsonify([{
            'id': place['id'],
            'name': place['name'],
            'description': place['description'],
            'address': place['address'],
            'city_id': place['city_id'],
            'latitude': place['latitude'],
            'longitude': place['longitude'],
            'host_id': place['host_id'],
            'number_of_rooms': place['number_of_rooms'],
            'number_of_bathrooms': place['number_of_bathrooms'],
            'price_per_night': place['price_per_night'],
            'max_guests': place['max_guests'],
            'city': place['city_id'],
            'amenities': place['amenity_id'],
            'created_at': place['created_at'],
            'updated_at': place['updated_at']
            } for place in places]), 200


@app.route('/places/<place_id>')
def get_Place(place_id):
    if not val.idChecksum(place_id):
        return jsonify({'message': "todo mal con el id"}), 400

    try:
        place = LogicFacade.getByID(place_id, 'place')

    except (logicexceptions.IDNotFoundError) as message:
         return jsonify(message), 404

    return jsonify({
                    'id': place['id'],
                    'name': place['name'],
                    'description': place['description'],
                    'address': place['address'],
                    'city_id': place['city_id'],
                    'latitude': place['latitude'],
                    'longitude': place['longitude'],
                    'host_id': place['host_id'],
                    'number_of_rooms': place['number_of_rooms'],
                    'number_of_bathrooms': place['number_of_bathrooms'],
                    'price_per_night': place['price_per_night'],
                    'max_guests': place['max_guests'],
                    'city': place['city_id'],
                    'amenities': place['amenity_id'],
                    'created_at': place['created_at'],
                    'updated_at': place['updated_at']
                    }), 200


@app.route('/places/<place_id>', methods=['PUT'])
def update_Place(place_id):
    if not val.idChecksum(place_id):
        return jsonify({'error': "id type invalido"}), 400

    data = request.get_json()

    if not data:
        return jsonify({'error': "no data"}), 400

    if not (val.isLatitudeValid(data['latitude']) and val.isLongitudeValid(data['longitude'])):
        return jsonify({'error': "ubicacion invalida"}), 400

    if not (isinstance(data['number_of_rooms'], int) and (data['number_of_rooms'] > 0) and
            isinstance(data['number_of_bathrooms'], int) and
            (data['number_of_bathrooms'] >= 0) and isinstance(data['max_guests'], int) and
            data['max_guests'] > 0 and
            isinstance(data['price_per_night'], (int, float)) and data['price_per_night'] > 0):
        return jsonify({'error': "datos de rooms invalidos"}), 400

    if not val.idChecksum(data['city_id']):
        return jsonify({'error': "el codigo de la city esta mal"}), 400

    for amenity_id in data['amenity_ids']:
        if not val.idChecksum(amenity_id):
            return jsonify({'error': 'Invalid amenity_id'}), 400

    try:
        LogicFacade.updateByID(place_id, 'place', data)
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({'OKa'}), 200


@app.route('/places/<place_id>', methods=['DELETE'])
def delete_Place(place_id):
    if not val.idChecksum(place_id):
        return jsonify({'error': "el id es cualquiera"})
    try:
        LogicFacade.deleteByID(place_id, 'place')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({'message': 'Place deleted successfully'}), 204




'''     
    for place in places:

        city = getCity(place['city_id'])
        amenities = [getAmenity(amenity_id) for amenity_id in place['amenity_ids']]
        response.append({
            'id': place['id'],
            'name': place['name'],
            'description': place['description'],
            'address': place['address'],
            'city_id': place['city_id'],
            'latitude': place['latitude'],
            'longitude': place['longitude'],
            'host_id': place['host_id'],
            'number_of_rooms': place['number_of_rooms'],
            'number_of_bathrooms': place['number_of_bathrooms'],
            'price_per_night': place['price_per_night'],
            'max_guests': place['max_guests'],
            'city': city,
            'amenities': amenities,
            'created_at': place['created_at'],
            'updated_at': place['updated_at']
            })
            '''
