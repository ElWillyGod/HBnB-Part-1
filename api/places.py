#!/usr/bin/python3
"""places endpoint
POST /places: Create a new place.
GET /places: Retrieve a list of all places.
GET /places/{place_id}: Retrieve detailed information about a specific place.
PUT /places/{place_id}: Update an existing place’s information.
DELETE /places/{place_id}: Delete a specific place.
"""
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route('/places', methods=["POST"])
def create_Place():
    data = request.get_json()

    if not data:
        return jsonify({'error': "no data"}), 400

    if not validCamp(data):
        return jsonify({'error': "not validCamp"}), 400

    if not (-90 <= data['latitude'] <= 90) or not (-180 <= data['longitude'] <= 180):
        return jsonify({'error': "ubicacion invalida"}), 400

    if not (isinstance(data['number_of_rooms'], int) and (data['number_of_rooms'] > 0) and
            isinstance(data['number_of_bathrooms'], int) and
            (data['number_of_bathrooms'] >= 0) and isinstance(data['max_guests'], int) and
            data['max_guests'] > 0 and
            isinstance(data['price_per_night'], (int, float)) and data['price_per_night'] > 0):
        return jsonify({'error': "datos de rooms invalidos"}), 400

    if not getCityId(data['city_id']):
        return jsonify({'error': "el codigo de la city esta mal"}), 400

    for amenity_id in data['amenity_ids']:
        amenity = getAmenity(amenity_id)
        if not amenity:
            return jsonify({'error': 'Invalid amenity_id'}), 400

    createPlace(data)
    return jsonify({'OKa'}), 201


@app.route('/places')
def get_All_Places():
    places = getAllPlaces()
    response = []

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
    return jsonify(response), 200


@app.route('/places/<place_id>')
def get_Place(place_id):
    place = getPlace(place_id)

    if not place:
        return jsonify({'error': 'error con el id'}), 404

    city = getCity(place['city_id'])
    amenities = [getAmenity(amenity_id) for amenity_id in place['amenity_ids']]
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
        'ax_guests': place['max_guests'],
        'amenity_ids': place['amenity_ids'],
        'city': {
            'id': city['id'],
            'name': city['name'],
            'country': city['country']
        },
        'amenities': [{
            'id': amenity['id'],
            'name': amenity['name'],
            'created_at': amenity['created_at'],
            'updated_at': amenity['updated_at']
        } for amenity in amenities],
        'created_at': place['created_at'],
        'updated_at': place['updated_at']
        }), 200


@app.route('/places/<place_id>', methods=['PUT'])
def update_Place(place_id):

    place = getPlace(place_id)

    if not place:
        return jsonify({'error': "place not found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({'error': "no data"}), 400

    if not validCamp(data):
        return jsonify({'error': "not validCamp"}), 400

    if not (-90 <= data['latitude'] <= 90) or not (-180 <= data['longitude'] <= 180):
        return jsonify({'error': "ubicacion invalida"}), 400

    if not (isinstance(data['number_of_rooms'], int) and (data['number_of_rooms'] > 0) and
            isinstance(data['number_of_bathrooms'], int) and
            (data['number_of_bathrooms'] >= 0) and isinstance(data['max_guests'], int) and
            data['max_guests'] > 0 and
            isinstance(data['price_per_night'], (int, float)) and data['price_per_night'] > 0):
        return jsonify({'error': "datos de rooms invalidos"}), 400

    if not getCityId(data['city_id']):
        return jsonify({'error': "el codigo de la city esta mal"}), 400

    for amenity_id in data['amenity_ids']:
        amenity = getAmenity(amenity_id)
        if not amenity:
            return jsonify({'error': 'Invalid amenity_id'}), 400

    createPlace(place_id, data)
    return jsonify({'OKa'}), 201


@app.route('/places/<place_id>', methods=['DELETE'])
def delete_Place(place_id):
    place = getPlace(place_id)

    if not place:
        return jsonify({'error': 'Place not found'}), 404

    deletePlace(place_id)
    return jsonify({'message': 'Place deleted successfully'}), 204
