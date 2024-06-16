#!/usr/bin/python3
"""reviews endpoint
POST /places/{place_id}/reviews: Create a new review for a specified place.
GET /users/{user_id}/reviews: Retrieve all reviews written by a specific user.
GET /places/{place_id}/reviews: Retrieve all reviews for a specific place.
GET /reviews/{review_id}: Retrieve detailed information about a specific review.
PUT /reviews/{review_id}: Update an existing review.
DELETE /reviews/{review_id}: Delete a specific review.
"""
from api import app
from flask import jsonify, request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.route('/places/<place_id>/reviews', methods=['POST'])
def create_Review(place_id):
    data = request.get_json()

    if not data or not val.idChecksum(place_id) or not val.isStrValid('comment'):
        return jsonify({'error': 'data no valid'}), 400

    if not (1 <= data['rating'] <= 5):
        return jsonify({'error': 'invalid rating'}), 400

    data['place_id'] = place_id

    try:
        LogicFacade.createObjectByJson('review', data)

    except (logicexceptions.IDNotFoundError) as message:

        return jsonify({'error': str(message)}), 404

    except (logicexceptions.TryingToReviewOwnPlace) as message:

        return jsonify({'error': str(message)}), 400

    return jsonify({"message": 'OKa'}), 201


@app.route('/users/<user_id>/reviews')
def get_User_Reviews(user_id):
    if not val.idChecksum(user_id):
        return jsonify({'error': "fomat id "}), 400

    try:
        reviews = LogicFacade.getByID(user_id, "reviewUser")
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    if reviews is not None:
        return jsonify(reviews), 200

    return jsonify({'message': "empy reviews for user"}), 200


@app.route('/places/<place_id>/reviews')
def get_Place_Reviews(place_id):
    if not val.idChecksum(place_id):
        return jsonify({'error': "la id no tiene el formato"}), 400

    try:

        reviews = LogicFacade.getByID(place_id, 'reviewPlace')
    
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    if reviews is not None:
        return jsonify(reviews), 200

    return jsonify({'message': "empy reviews"}), 200


@app.route('/reviews/<review_id>')
def get_review(review_id):
    if not val.idChecksum(review_id):
        return jsonify({'error': "la id no tiene el formato"}), 400

    try:

        review = LogicFacade.getByID(review_id, 'review')
    
    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    if review is not None:
        return jsonify(review), 200

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

        return jsonify({'error': str(message)}), 404

    except (logicexceptions.TryingToReviewOwnPlace) as message:

        return jsonify({'error': str(message)}), 400

    return jsonify({'OKa'}), 200


@app.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review(review_id):
    if not val.idChecksum(review_id):
        return jsonify({'error': "el id es cualquiera"})
    try:
        LogicFacade.deleteByID(review_id, 'review')

    except (logicexceptions.IDNotFoundError) as message:
        return jsonify({'error': str(message)}), 404

    return jsonify({'message': 'review deleted successfully'}), 204
