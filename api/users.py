
"""users endpoint
POST /users: Create a new user.
GET /users: Retrieve a list of all users.
GET /users/{user_id}: Retrieve details of a specific user.
PUT /users/{user_id}: Update an existing user.
DELETE /users/{user_id}: Delete a user.
"""
from api import app
from flask import request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.post("/users")
def create_User():
    """
    Create a new user.
    ---
    tags:
      - users
    parameters:
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Email address of the user
            first_name:
              type: string
              description: First name of the user
            last_name:
              type: string
              description: Last name of the user
    responses:
      201:
        description: User created successfully
      400:
        description: Invalid request data or missing fields
      409:
        description: Email address already exists
    """
    data = request.get_json()

    if val.isNoneFields('user', data):
        return {'error': "Invalid data or missing fields"}, 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if (not val.isStrValid(email) or not val.isNameValid(first_name) or
        not val.isNameValid(last_name)):

        return {'error': "Invalid data or missing fields"}, 400

    if not val.isEmailValid(email):
        return {'error': "Invalid data"}, 400

    try:
        user = LogicFacade.createObjectByJson("user", data)

    except (logicexceptions.EmailDuplicated) as message:

        return {'error': str(message)}, 409

    return user, 201


@app.get('/users')
def get_Users_All():
    """
    Retrieve details of a specific user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to retrieve
    responses:
      200:
        description: Details of the specified user
    """
    users = LogicFacade.getByType("user")

    if users is not None and len(users) > 0:
        return users, 200

    return {'message': "Details of the specified user"}, 200


@app.get('/users/<user_id>')
def get_User(user_id):
    """
    Update an existing user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to update
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Updated email address of the user
            first_name:
              type: string
              description: Updated first name of the user
            last_name:
              type: string
              description: Updated last name of the user
    responses:
      201:
        description: User updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: User ID not found
    """

    if not val.idChecksum(user_id):
        return {'error': "Invalid data"}, 400

    try:

        users = LogicFacade.getByID(user_id, 'user')

    except (logicexceptions.IDNotFoundError) as message:
        
        return {'error': str(message)}, 404

    return users, 200


@app.put('/users/<user_id>')
def update_User(user_id):
    """
    Update an existing user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to update
      - in: body
        name: user
        required: true
        schema:
          type: object
          properties:
            email:
              type: string
              description: Updated email address of the user
              example: juanpepe@gmail.com
            first_name:
              type: string
              description: Updated first name of the user
              example: juan
            last_name:
              type: string
              description: Updated last name of the 
              example: pepe
    responses:
      201:
        description: User updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: User ID not found
      409:
        description: Email address already exists
    """

    if not val.idChecksum(user_id):
        return {'error': 'Invalid id'}, 400

    data = request.get_json()

    if val.isNoneFields('user', data):
        return {'error': "Invalid data"}, 400

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')

    if (not val.isStrValid(email) or not val.isNameValid(first_name) or
        not val.isNameValid(last_name)):

        return {'error': "Invalid data or missing fields"}, 400

    if not val.isEmailValid(email):
        return {'error': "Invalid email"}, 400

    try:
        user = LogicFacade.updateByID(user_id, "user", data)

    except (logicexceptions.EmailDuplicated) as message:

        return {'error': str(message)}, 409

    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return user, 201

@app.delete('/users/<user_id>')
def delete_user(user_id):
    """
    Delete a user.
    ---
    tags:
      - users
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user to delete
    responses:
      204:
        description: User deleted successfully
      400:
        description: Invalid user ID format
      404:
        description: User ID not found
    """
    if not val.idChecksum(user_id):
        return {'error': 'Invalid user ID'}, 400

    try:
        LogicFacade.deleteByID(user_id, "user")

    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return "", 204
