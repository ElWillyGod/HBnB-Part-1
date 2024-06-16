
"""amenities endpoint
POST /amenities: Create a new amenity.
GET /amenities: Retrieve a list of all amenities.
GET /amenities/{amenity_id}: Retrieve detailed information about a specific amenity.
PUT /amenities/{amenity_id}: Update an existing amenity’s information.
DELETE /amenities/{amenity_id}: Delete a specific amenity."""
from api import app
from flask import request, jsonify
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.route('/amenities', methods=["POST"])
def create_Amenities():
    """
    Create a new amenity
    ---
    tags:
      - amenities
    parameters:
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: The name of the amenity
              example: Pool
    responses:
      201:
        description: Amenity created successfully
      400:
        description: Bad request, invalid data
      409:
        description: Amenity name already exists
    """
    data = request.get_json()

    if not data or not val.isNameValid(data['name']):
        return jsonify({'error': "Invalid data"}), 400

    try:
        LogicFacade.createObjectByJson('amenity', data)

    except (logicexceptions.AmenityNameDuplicated) as message:
        return jsonify({'error': str(message)}), 409

    return jsonify({'message': "Amenity created successfully"}), 201


@app.route('/amenities')
def get_all_amenities():
    """
    Retrieve a list of all amenities
    ---
    tags:
      - amenities
    responses:
      200:
        description: A list of amenities
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              name:
                type: string
              created_at:
                type: string
              updated_at:
                type: string
      200:
        description: No amenities found
    """
    amenities = LogicFacade.getByType('amenity')

    if amenities is not None and len(amenities) >0:
        return jsonify(amenities), 200

    return jsonify({'message': ""}), 200

@app.route('/amenities/<amenity_id>')
def get_amenities(amenity_id):
    """
    Retrieve an amenity by ID
    ---
    tags:
      - amenities
    parameters:
      - in: path
        name: amenity_id
        type: string
        required: true
        description: The ID of the amenity to retrieve
    responses:
      200:
        description: Amenity details
        schema:
          type: object
          properties:
            id:
              type: string
            name:
              type: string
      400:
        description: Bad request, invalid ID format
      404:
        description: Amenity not found
    """
    if not val.idChecksum(amenity_id):
        return jsonify({'error': "Invalid ID"}), 400

    try:
        amenities = LogicFacade.getByID(amenity_id, 'amenity')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify(amenities), 200


@app.route('/amenities/<amenity_id>', methods=["PUT"])
def update_Amenities(amenity_id):
    """
    Update an amenity by ID
    ---
    tags:
      - amenities
    parameters:
      - in: path
        name: amenity_id
        type: string
        required: true
        description: The ID of the amenity to update
      - in: body
        name: body
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
              description: The name of the amenity
              example: Gym
    responses:
      200:
        description: Amenity updated successfully
      400:
        description: Bad request, invalid data or ID format
      404:
        description: Amenity not found
      409:
        description: Amenity name already exists
    """
    data = request.get_json()

    if not data or not val.isNameValid(data['name']):
        return jsonify({'error': "Invalid data"}), 400

    if not val.idChecksum(amenity_id):
        return jsonify({'error': 'Invalid ID format'}), 400

    try:
        LogicFacade.updateByID(amenity_id, 'amenity', data)

    except (logicexceptions.AmenityNameDuplicated) as message:
        return jsonify({'error': str(message)}), 409

    except (logicexceptions.IDNotFoundError) as message2:
        return jsonify({'error': str(message2)}), 404

    return jsonify({'message': "Amenity updated successfully"}), 200
    

@app.route('/amenities/<amenity_id>', methods=["DELETE"])
def delete_Amenities(amenity_id):
    """
    Delete an amenity by ID
    ---
    tags:
      - amenities
    parameters:
      - in: path
        name: amenity_id
        type: string
        required: true
        description: The ID of the amenity to delete
    responses:
      204:
        description: Amenity deleted successfully
      400:
        description: Bad request, invalid ID format
      404:
        description: Amenity not found
    """
    if not val.idChecksum(amenity_id):
        return jsonify({'message': "Invalid ID format"}), 400

    try:
        LogicFacade.deleteByID(amenity_id, 'amenity')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify({'message': "Amenity deleted successfully"}), 204
