
"""reviews endpoint
POST /places/{place_id}/reviews: Create a new review for a specified place.
GET /users/{user_id}/reviews: Retrieve all reviews written by a specific user.
GET /places/{place_id}/reviews: Retrieve all reviews for a specific place.
GET /reviews/{review_id}: Retrieve detailed information about a specific review.
PUT /reviews/{review_id}: Update an existing review.
DELETE /reviews/{review_id}: Delete a specific review.
"""
from api import app
from flask import request
from logic import logicexceptions
from logic.logicfacade import LogicFacade
import api.validation as val


@app.post('/places/<place_id>/reviews')
def create_Review(place_id):
    """
    Create a new review for a specified place.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place to review
      - in: body
        name: review
        required: true
        schema:
          type: object
          properties:
            rating:
              type: integer
              description: Rating for the place (1 to 5)
              example: 5
            comment:
              type: string
              description: Optional comment about the place
              example: muy bueno
    responses:
      201:
        description: Review created successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: Place ID not found or trying to review own place
    """
    data = request.get_json()

    if val.isNoneFields('review', data) or not val.idChecksum(place_id) or not val.isStrValid('comment'):
        return {'error': 'Invalid data'}, 400

    if not (1 <= data['rating'] <= 5):
        return {'error': 'Invalid rating'}, 400

    data['place_id'] = place_id

    try:
        review = LogicFacade.createObjectByJson('review', data)

    except (logicexceptions.IDNotFoundError) as message:

        return {'error': str(message)}, 404

    except (logicexceptions.TryingToReviewOwnPlace) as message:

        return {'error': str(message)}, 400

    return review, 201


@app.get('/users/<user_id>/reviews')
def get_User_Reviews(user_id):
    """
    Retrieve all reviews written by a specific user.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: user_id
        type: string
        required: true
        description: ID of the user whose reviews are to be retrieved
    responses:
      200:
        description: List of reviews written by the user
      400:
        description: Invalid user ID format
      404:
        description: User ID not found or no reviews found for the user
    """
    if not val.idChecksum(user_id):
        return {'error': "Invalid user ID"}, 400

    try:
        reviews = LogicFacade.getByID(user_id, "reviewUser")
    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    if reviews is not None:
        return reviews, 200

    return reviews, 200


@app.get('/places/<place_id>/reviews')
def get_Place_Reviews(place_id):
    """
    Retrieve all reviews for a specific place.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: place_id
        type: string
        required: true
        description: ID of the place whose reviews are to be retrieved
    responses:
      200:
        description: List of reviews for the place
      400:
        description: Invalid place ID format
      404:
        description: Place ID not found or no reviews found for the place
    """
    if not val.idChecksum(place_id):
        return {'error': "Invalid place ID format"}, 400

    try:

        reviews = LogicFacade.getByID(place_id, 'reviewPlace')
    
    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    if reviews is not None:
        return reviews, 200

    return reviews, 200


@app.get('/reviews/<review_id>')
def get_review(review_id):
    """
    Retrieve detailed information about a specific review.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: review_id
        type: string
        required: true
        description: ID of the review to retrieve
    responses:
      200:
        description: Detailed information about the review
      400:
        description: Invalid review ID format
      404:
        description: Review ID not found
    """
    if not val.idChecksum(review_id):
        return {'error': "Invalid review ID"}, 400

    try:

        review = LogicFacade.getByID(review_id, 'review')
    
    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    if review is not None:
        return review, 200

    return review, 200


@app.put('/reviews/<review_id>')
def update_review(review_id):
    """
    Update an existing review.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: review_id
        type: string
        required: true
        description: ID of the review to update
      - in: body
        name: review
        required: true
        schema:
          type: object
          properties:
            rating:
              type: integer
              description: Updated rating for the review (1 to 5)
            comment:
              type: string
              description: Updated comment for the review
    responses:
      200:
        description: Review updated successfully
      400:
        description: Invalid request data or missing fields
      404:
        description: Review ID not found or trying to update own review
    """
    data = request.get_json()

    if (val.isNoneFields('review', data) or not val.idChecksum(review_id) or
        not val.isStrValid('comment')):
        return {'error': 'Invalid data'}, 400

    if not (1 <= data['rating'] <= 5):
        return {'error': 'Invalid rating'}, 400

    try:
        review = LogicFacade.updateByID(review_id, 'review', data)

    except (logicexceptions.IDNotFoundError) as message:

        return {'error': str(message)}, 404

    except (logicexceptions.TryingToReviewOwnPlace) as message:

        return {'error': str(message)}, 400

    return review, 200


@app.delete('/reviews/<review_id>')
def delete_review(review_id):
    """
    Delete a specific review.
    ---
    tags:
      - reviews
    parameters:
      - in: path
        name: review_id
        type: string
        required: true
        description: ID of the review to delete
    responses:
      204:
        description: Review deleted successfully
      400:
        description: Invalid review ID format
      404:
        description: Review ID not found
    """
    if not val.idChecksum(review_id):
        return {'error': "Invalid review ID format"}, 400
    try:
        LogicFacade.deleteByID(review_id, 'review')

    except (logicexceptions.IDNotFoundError) as message:
        return {'error': str(message)}, 404

    return "", 204
