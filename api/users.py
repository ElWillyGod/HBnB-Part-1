#!/usr/bin/python3
"""users endpoint
POST /users: Create a new user.
GET /users: Retrieve a list of all users.
GET /users/{user_id}: Retrieve details of a specific user.
PUT /users/{user_id}: Update an existing user.
DELETE /users/{user_id}: Delete a user.
"""
from flask import Flask, jsonify, request


app = Flask(__name__)


@app.route("/users", methods=["POST"])
def create_User():
    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not first_name or not last_name:
        return jsonify({'error': "400 Bad Request"}), 400

    if not '@' in data['email']:
        return jsonify({'error': "400 Format email Error"}), 400

    if not isUserEmailDuplicated(email):
        return jsonify({'error': "409 Conflict"}), 409

    if createUser(data):
        return jsonify({"201 Created"}), 201

    return jsonify({'error': 'error createUser'}), 400


@app.route('/users')
def get_Users_All():
    users = getUsersAll()
    return jsonify([{'id': user['id'], 'email': user['email'], 'first name': user['first_name'], 'last name': user['last_name'], 'created at': user['created_at'], 'updated at': user['updated_at']} for user in users]), 200


@app.route('/users/<user_id>')
def get_User(user_id):
    user = getUser(user_id)

    if not user:
        return jsonify({'error': "404 Not Found"}), 404

    return jsonify({'message': user}), 200


@app.route('/users/<user_id>', methods=["PUT"])
def updata_User(user_id):
    user = getUser(user_id)

    if not user:
        return jsonify({'error': "404 Not Found"}), 404

    data = request.get_json()

    if not data:
        return jsonify({'error': "400 Bad Request"}), 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if not email or not first_name or not last_name:
        return jsonify({'error': "400 Bad Request"}), 400

    if not '@' in data['email']:
        return jsonify({'error': "400 Format email Error"}), 400

    if not isUserEmailDuplicated(email):
        return jsonify({'error': "409 Conflict"}), 409

    if updateDataUser(user_id, data):
        return 'OK', 201

    return jsonify({'error': "error al hacer Update"}), 404


@app.route('/users/<user_id>', methods=["DELETE"])
def delete_user(user_id):
    user = getUser(user_id)

    if not user:
        return jsonify({'error': "404 Not Found"}), 404

    if deleteUser(user_id):
        return 'OK', 201
    
    return jsonify({'error': "error al Delete"}), 404
