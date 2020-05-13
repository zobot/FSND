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
db_drop_and_create_all()
initialize_db_mock_data()


## ROUTES
@app.route('/drinks')
def drinks():
    try:
        drinks_db = Drink.query.all()
        return jsonify({
            "success": True,
            "status_code": 200,
            "drinks": [drink.short() for drink in drinks_db]
        }), 200
    except SQLAlchemyError as e:
        abort(500)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail')
@requires_auth(permission='get:drinks-detail')
def drinks_detail():
    try:
        drinks_db = Drink.query.all()
        return jsonify({
            "success": True,
            "status_code": 200,
            "drinks": [drink.long() for drink in drinks_db]
        }), 200
    except SQLAlchemyError as e:
        abort(500)


'''
@TODO implement endpoint
    POST /drink    drink_dict = request.get_json()
    print(drink_dict)
    recipe = drink_dict['recipe']
    print('recipe: ', recipe)
    drink = Drink(
        title=drink_dict['title'],
        recipe=json.dumps(recipe)
    )
    drink.insert()s
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth(permission='post:drinks')
def post_drink():
    # TODO: error checking
    drink_dict = request.get_json()
    print(drink_dict)
    recipe = drink_dict['recipe']
    print('recipe: ', recipe)
    drink = Drink(
        title=drink_dict['title'],
        recipe=json.dumps(recipe)
    )
    drink.insert()

    return jsonify({
        "success": True,
        "status_code": 200,
        "drinks": [drink.long()],
    }), 200

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth(permission='patch:drinks')
def patch_drink(id):
    try:
        drink_matching = Drink.query.get(id)
    except SQLAlchemyError:
        abort(404)
    try:
        drink_dict = request.get_json()
        if 'recipe' in drink_dict:
            recipe = drink_dict['recipe']
            drink_matching.recipe = json.dumps(recipe)
        if 'title' in drink_dict:
            title = drink_dict['title']
            drink_matching.title = title
        drink_matching.update()
    except SQLAlchemyError:
        abort(422)
    return jsonify({
        "success": True,
        "status_code": 200,
        "drinks": [drink_matching.long()],
    }), 200


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth(permission='delete:drinks')
def delete_drink(id):
    try:
        drink_matching = Drink.query.get(id)
    except SQLAlchemyError:
        abort(404)
    try:
        drink_matching.delete()
    except SQLAlchemyError:
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
