import os
from flask import Flask, request, jsonify, abort
from sqlalchemy.exc import SQLAlchemyError
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .database.initialize_db_mock_data import initialize_db_mock_data
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
#db_drop_and_create_all()
#initialize_db_mock_data()


## ROUTES
@app.route('/drinks')
def drinks():
    try:
        drinks_db = Drink.query.all()
    except SQLAlchemyError as e:  # server error, db uninitialized?
        abort(500)

    return jsonify({
        "success": True,
        "status_code": 200,
        "drinks": [drink.short() for drink in drinks_db]
    }), 200


@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def drinks_detail():
    try:
        drinks_db = Drink.query.all()
    except SQLAlchemyError as e:   # server error, db uninitialized?
        abort(500)

    return jsonify({
        "success": True,
        "status_code": 200,
        "drinks": [drink.long() for drink in drinks_db]
    }), 200


@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def post_drink():
    drink_dict = request.get_json()
    try:
        recipe = drink_dict['recipe']
        title = drink_dict['title']
    except KeyError:  # request contains no recipe or no title
        abort(422)

    try:
        drink = Drink(
            title=title,
            recipe=json.dumps(recipe)
        )
    except SQLAlchemyError as e:  # bad input
        abort(422)

    try:
        drink.insert()
    except SQLAlchemyError as e:   # server error, db uninitialized?
        abort(500)

    return jsonify({
        "success": True,
        "status_code": 200,
        "drinks": [drink.long()],
    }), 200


@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def patch_drink(id):
    try:
        drink_matching = Drink.query.get(id)
    except SQLAlchemyError:  # not found
        abort(404)

    try:
        drink_dict = request.get_json()
        if 'recipe' in drink_dict:
            recipe = drink_dict['recipe']
            drink_matching.recipe = json.dumps(recipe)
        if 'title' in drink_dict:
            title = drink_dict['title']
            drink_matching.title = title
    except SQLAlchemyError:  # bad input
        abort(422)

    try:
        drink_matching.update()
    except SQLAlchemyError:  # server error
        abort(500)

    return jsonify({
        "success": True,
        "status_code": 200,
        "drinks": [drink_matching.long()],
    }), 200


@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(id):
    try:
        drink_matching = Drink.query.get(id)
    except SQLAlchemyError:  # not found
        abort(404)

    try:
        drink_matching.delete()
    except SQLAlchemyError:  # server error
        abort(500)

    return jsonify({
        "success": True,
        "status_code": 200,
        "delete": id,
    }), 200


## Error Handling
@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error,
    }), error.status_code


@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": "method not allowed"
    }), 405


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(500)
def server_db_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "server_db_error"
    }), 500
