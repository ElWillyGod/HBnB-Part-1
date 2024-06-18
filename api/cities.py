
"""cities endpoint
GET /countries/{country_code}/cities: Retrieve all cities belonging to a specific country.
POST /cities: Create a new city.
GET /cities: Retrieve all cities.
GET /cities/{city_id}: Retrieve details of a specific city.
PUT /cities/{city_id}: Update an existing city's information.
DELETE /cities/{city_id}: Delete a specific city.
"""
from api import app
from flask import jsonify, request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.route('/countries/<country_code>/cities')
def get_Cities_For_Contr(country_code):
    """
    Retrieve cities for a specific country
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: country_code
        type: string
        required: true
        description: ISO country code (e.g., 'US' for United States)
    responses:
      200:
        description: A list of cities for the country
      400:
        description: Bad request, invalid country code
      404:
        description: Country not found
    """
    if not val.isCountryValid(country_code):
        return jsonify({'error': "Invalid country code"}), 400

    try:
        cities = LogicFacade.getContryCities(country_code)

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify(cities), 200


@app.route('/cities', methods=["POST"])
def create_Cities():
    """
    Create a new city
    ---
    tags:
      - cities
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - country_code
          properties:
            name:
              type: string
              description: The name of the city
              example: New York
            country_code:
              type: string
              description: The ISO code of the country to which the city belongs
              example: US
    responses:
      201:
        description: City created successfully
      400:
        description: Bad request, invalid data or missing fields
      409:
        description: City name already exists
    """
    data = request.get_json()

    if val.isNoneFields('city', data):
        return jsonify({'error': "Invalid data"}), 400

    name = data['name']
    code = data['country_code']

    if not val.isNameValid(name) or not val.isCountryValid(code):
        return jsonify({'error': "Invalid data"}), 400

    try:
        LogicFacade.createObjectByJson("city", data)

    except (logicexceptions.CountryNotFoundError) as message:
        return jsonify({'error': str(message)}), 400

    except (logicexceptions.CityNameDuplicated) as message:
        return jsonify({'error': str(message)}), 409

    return jsonify({'message': "City created successfully"}), 201



@app.route('/cities')
def get_All_Cities():
    """
    Retrieve all cities
    ---
    tags:
      - cities
    responses:
      200:
        description: A list of all cities
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              country_code:
                type: string
    """
    cities = LogicFacade.getByType("city")

    if cities is not None and len(cities) > 0:
        return jsonify(cities), 200

    return jsonify({'message': "A list of all cities"}), 200


@app.route('/cities/<city_id>')
def get_Cities(city_id):
    """
    Retrieve a city by ID
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of the city to retrieve
    responses:
      200:
        description: City details
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
            country_code:
              type: string
      400:
        description: Bad request, invalid ID format
      404:
        description: City not found
    """

    if not val.idChecksum(city_id):
        return jsonify({'error': "Invalid ID format"}), 400

    try:
        city = LogicFacade.getByID(city_id, "city")
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify(city), 200


@app.route('/cities/<city_id>', methods=["PUT"])
def update_Cities(city_id):
    """
    Update a city by ID
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of the city to update
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
            - country_code
          properties:
            name:
              type: string
              description: The name of the city
              example: Los Angeles
            country_code:
              type: string
              description: The ISO code of the country to which the city belongs
              example: US
    responses:
      200:
        description: City updated successfully
      400:
        description: Bad request, invalid data or ID format
      404:
        description: City not found
      409:
        description: City name already exists
    """
    data = request.get_json()

    if not val.idChecksum(city_id):
        return jsonify({'error': "Invalid ID format"}), 400

    if val.isNoneFields('city', data):
        return jsonify({'error': "Invalid data"}), 400

    name = data['name']
    code = data['country_code']

    if not val.isNameValid(name) or not val.isCountryValid(code):
        return jsonify({'error': "Invalid data"}), 400

    try:
        LogicFacade.updateByID(city_id, "city", data)

    except (logicexceptions.CountryNotFoundError) as message:
        return jsonify({'error': str(message)}), 400

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    except (logicexceptions.CityNameDuplicated) as message2:
        return jsonify({'error': str(message2)}), 409

    return jsonify({"message": "City updated successfully"}), 201


@app.route('/cities/<city_id>', methods=["DELETE"])
def delete_Cities(city_id):
    """
    Delete a city by ID
    ---
    tags:
      - cities
    parameters:
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of the city to delete
    responses:
      204:
        description: City deleted successfully
      400:
        description: Bad request, invalid ID format
      404:
        description: City not found
    """
    if not val.idChecksum(city_id):
        return jsonify({'error': 'Invalid ID'}), 400

    try:
        LogicFacade.deleteByID(city_id, "city")

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify({'message': "City deleted successfully"}), 204
