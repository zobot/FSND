from flask import jsonify
from .models import Drink


def initialize_db_mock_data():
    drinks = [
        Drink(
            title="Coffee",
            recipe='[{"color": "black", "name": "coffee", "parts": 1}]'
        ),
        Drink(
            title="Mocha",
            recipe='[{"color": "black", "name": "coffee", "parts": 1}, ' +
                   '{"color": "brown", "name": "chocolate", "parts": 1}]'
        ),
        Drink(
            title="Cappuccino",
            recipe='[{"color": "black", "name": "coffee", "parts": 1}, ' +
                     '{"color": "white", "name": "milk", "parts": 1}]'
    ),
    ]
    [drink.insert() for drink in drinks]
    print('initialized db')


