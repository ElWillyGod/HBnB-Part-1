#!/usr/bin/python3
"""reviews endpoint
POST /places/{place_id}/reviews: Create a new review for a specified place.
GET /users/{user_id}/reviews: Retrieve all reviews written by a specific user.
GET /places/{place_id}/reviews: Retrieve all reviews for a specific place.
GET /reviews/{review_id}: Retrieve detailed information about a specific review.
PUT /reviews/{review_id}: Update an existing review.
DELETE /reviews/{review_id}: Delete a specific review.
"""
from flask import Flask, jsonify, request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import validation as val

app = Flask(__name__)


@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_Review(place_id):
    data = request.get_json()

    if not data or not val.idChecksum(place_id) or not val.isStrValid('comment'):
        return jsonify({'error': 'data no valid'}), 400

    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'invalid rating'}), 400

    try:
        LogicFacade.createReview(place_id, data)

    except (logicexceptions.IDNotFoundError) as message:

        return jsonify(message), 404

    except (TypeError) as message:

        return jsonify(message), 400

    return jsonify({'OKa'}), 201


@app.route('/users/<user_id>/reviews')
def get_User_Reviews(user_id):
    if not val.idChecksum(user_id):
        return jsonify({'error': "fomat id "}), 400

    try:
        reviews = LogicFacade.getByID(user_id, "reviewUser")
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    if reviews is not None:
        return jsonify([{
            'id': review['id'],
            'place_id': review['place_id'],
            'user_id': review['user_id'],
            'rating': review['rating'],
            'comment': review['comment'],
            'created_at': review['created_at'],
            'updated_at': review['updated_at']
            } for review in reviews]), 200

    return jsonify({'message': "empy reviews for user"}), 200


@app.route('/places/<place_id>/reviews')
def get_Place_Reviews(place_id):
    if not val.idChecksum(place_id):
        return jsonify({'error': "la id no tiene el formato"}), 400

    try:

        reviews = LogicFacade.getByID(place_id, 'reviewPlace')
    
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    if reviews is not None:
        return jsonify([{
            'id': review['id'],
            'place_id': review['place_i d'],
            'user_id': review['user_id'],
            'rating': review['rating'],
            'comment': review['comment'],
            'created_at': review['created_at'],
            'updated_at': review['updated_at']
            } for review in reviews]), 200

    return jsonify({'message': "empy reviews"}), 200


@app.route('/reviews/<review_id>')
def get_review(review_id):
    if not val.idChecksum(review_id):
        return jsonify({'error': "la id no tiene el formato"}), 400

    try:

        review = LogicFacade.getByID(review_id, 'review')
    
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    if review is not None:
        return jsonify({
            'id': review['id'],
            'place_id': review['place_i d'],
            'user_id': review['user_id'],
            'rating': review['rating'],
            'comment': review['comment'],
            'created_at': review['created_at'],
            'updated_at': review['updated_at']
            }), 200

    return jsonify({'message': "empy reviews"}), 200


@app.route('/reviews/<review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.get_json()

    if not data or not val.idChecksum(review_id) or not val.isStrValid('comment'):
        return jsonify({'error': 'data no valid'}), 400

    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'invalid rating'}), 400

    try:
        LogicFacade.updateByID(review_id, 'review', data)

    except (logicexceptions.IDNotFoundError) as message:

        return jsonify(message), 404

    except (TypeError) as message:

        return jsonify(message), 400

    return jsonify({'OKa'}), 200


@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    if not val.idChecksum(review_id):
        return jsonify({'error': "el id es cualquiera"})
    try:
        LogicFacade.deleteByID(review_id, 'review')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify(message), 404

    return jsonify({'message': 'review deleted successfully'}), 204
