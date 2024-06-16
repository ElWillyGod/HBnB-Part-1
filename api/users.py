#!/usr/bin/python3
"""users endpoint
POST /users: Create a new user.
GET /users: Retrieve a list of all users.
GET /users/{user_id}: Retrieve details of a specific user.
PUT /users/{user_id}: Update an existing user.
DELETE /users/{user_id}: Delete a user.
"""
from api import app
from flask import jsonify, request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.route("/users", methods=["POST"])
def create_User():
    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if (not val.isStrValid(email) or not val.isNameValid(first_name) or
        not val.isNameValid(last_name)):

        return jsonify({'error': "400 Bad Request"}), 400

    if not val.isEmailValid(email):
        return jsonify({'error': "400 Format email Error"}), 400

    try:
        LogicFacade.createObjectByJson("user", data)

    except (logicexceptions.EmailDuplicated) as message:

        return jsonify({'error': str(message)}), 409

    return jsonify({'message':"201 Created"}), 201


@app.route('/users')
def get_Users_All():
    users = LogicFacade.getByType("user")

    if users is not None:
        return jsonify(users), 200

    return jsonify({'message': "empy"}), 200


@app.route('/users/<user_id>')
def get_User(user_id):

    if not val.idChecksum(user_id):
        return jsonify({'error': "format id invalid"}), 400

    try:

        data = LogicFacade.getByID(user_id, 'user')

    except (logicexceptions.IDNotFoundError) as message:
        
        return jsonify({'error': str(message)}), 404

    return jsonify(data), 200


@app.route('/users/<user_id>', methods=["PUT"])
def updata_User(user_id):

    if not val.idChecksum(user_id):
        return jsonify({'error': 'invalid id'}), 400

    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if (not val.isStrValid(email) or not val.isNameValid(first_name) or
        not val.isNameValid(last_name)):

        return jsonify({'error': "400 Bad Request"}), 400

    if not val.isEmailValid(email):
        return jsonify({'error': "400 Format email Error"}), 400

    try:
        LogicFacade.updateByID(user_id, "user", data)

    except (logicexceptions.EmailDuplicated) as message:

        return jsonify({'error': str(message)}), 409

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify({'message': "OKa"}), 201

@app.route('/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    if not val.idChecksum(user_id):
        return jsonify({'error': 'invalid id'}), 400

    try:
        LogicFacade.deleteByID(user_id, "user")

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify({'message': 'todo OKa'}), 204
