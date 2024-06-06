#!/usr/bin/python3
"""users endpoint
POST /users: Create a new user.
GET /users: Retrieve a list of all users.
GET /users/{user_id}: Retrieve details of a specific user.
PUT /users/{user_id}: Update an existing user.
DELETE /users/{user_id}: Delete a user.
"""
from flask import Flask, flask, jsonify, request


app = Flask(__name__)


@app.route("/users", methods=["POST"])
def create_user(email, first_name, last_name):
     userValid = createUser(email, first_name, last_name)

     if userValid:
         return jsonify({'error': "201 Created"}), 201
     
     return jsonify({'error': ""})


@app.route("/users")
def getAllUsers():
    

