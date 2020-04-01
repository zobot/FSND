import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import CORS
import json
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, origins="*")

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
        return response

    #  ----------------------------------------------------------------
    #  Helper functions
    #  ----------------------------------------------------------------

    def format_paginate_questions(in_request, selection):
        """Selects a page from selection and formats the output list"""
        page = in_request.args.get("page", default=1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        selection_paginated = selection[start:end]
        selection_formatted_paginated = [question.format() for question in selection_paginated]
        return selection_formatted_paginated

    def simplify_categories(categories_selection):
        """Transforms a list of Category's into an {id:type} dict"""
        categories_simplified_dict = {
            category.id: category.type
            for category in categories_selection
        }
        return categories_simplified_dict

    def questions_count_categories(in_request, questions_selection):
        """Returns a tuple of (questions, count, categories) formatted nicely and paginated"""
        questions_count = len(questions_selection)
        questions_formatted_paginated = format_paginate_questions(in_request, questions_selection)

        categories_all = Category.query.all()
        categories_simplified_dict = simplify_categories(categories_all)

        return questions_formatted_paginated, questions_count, categories_simplified_dict

    #  ----------------------------------------------------------------
    #  API Endpoints
    #  ----------------------------------------------------------------

    @app.route('/questions', methods=['GET'])
    def questions():
        page = request.args.get("page", default=1, type=int)
        if page <= 0:
            # only positive pages
            abort(400)

        questions_all = Question.query.order_by(Question.id).all()
        out_questions, questions_count, out_categories = questions_count_categories(request, questions_all)

        if len(out_questions) == 0:
            abort(404)

        return jsonify({
            'questions': out_questions,
            'total_questions': questions_count,
            'categories': out_categories,
            'current_category': None,
            'success': True,
            'status_code': 200,
            'message': 'GET Success',
        })

    @app.route('/categories', methods=['GET'])
    def categories():
        categories_all = Category.query.all()
        categories_simplified_dict = simplify_categories(categories_all)

        if len(categories_all) == 0:
            abort(404)

        return jsonify({
            'categories': categories_simplified_dict,
            'success': True,
            'status_code': 200,
            'message': 'GET Success',
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question_to_delete = Question.query.get(question_id)

        # no question of that id
        if question_to_delete is None:
            abort(404)

        question_to_delete.delete()

        # repopulate page
        questions_all = Question.query.order_by(Question.id).all()
        out_questions, questions_count, out_categories = questions_count_categories(request, questions_all)

        # conscious decision to not return 404 if out_questions is empty,
        # since we want the response to reflect the DELETE and not the subsequent paginated questions

        return jsonify({
            'questions': out_questions,
            'total_questions': questions_count,
            'categories': out_categories,
            'current_category': None,
            'success': True,
            'status_code': 200,
            'message': 'DELETE Success',
        })

    @app.route('/questions', methods=['POST'])
    def post_question():
        data = request.get_json()
        if 'searchTerm' in data:
            # using the search endpoint
            questions_selection = \
                Question.query.filter(Question.question.ilike(f"%{data['searchTerm']}%")).order_by(Question.id).all()

        else:
            # using the create endpoint

            # validate that the request contains the desired data
            request_contains_question_data = ("question" in data) and ("answer" in data) and \
                                             ("category" in data) and ("difficulty" in data)
            if not request_contains_question_data:
                abort(400)

            try:
                new_question = Question(**data)
                new_question.insert()
                questions_selection = Question.query.order_by(Question.id).all()
            except SQLAlchemyError:
                # bad data
                abort(422)

        # either populate search results page or regular page
        out_questions, questions_count, out_categories = questions_count_categories(request, questions_selection)

        return jsonify({
            'questions': out_questions,
            'total_questions': questions_count,
            'categories': out_categories,
            'current_category': None,
            'success': True,
            'status_code': 200,
            'message': 'POST Success',
        })

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def questions_in_category(category_id):
        page = request.args.get("page", default=1, type=int)
        if page <= 0:
            # only positive pages
            abort(400)

        category = Category.query.get(category_id)
        if category is None:
            # invalid category
            abort(422)

        questions_in_category = Question.query.filter_by(category=category_id).order_by(Question.id).all()
        out_questions, questions_count, out_categories = questions_count_categories(request, questions_in_category)

        if len(out_questions) == 0:
            # no questions in that category
            abort(404)

        return jsonify({
            'questions': out_questions,
            'total_questions': questions_count,
            'categories': out_categories,
            'current_category': category_id,
            'success': True,
            'status_code': 200,
            'message': 'GET Success',
        })

    @app.route('/quizzes', methods=['POST'])
    def quiz():
        data = request.get_json()
        category_id = data['quiz_category']['id']
        if category_id == 0:
            # all categories are valid here, none specified
            questions_selection = Question.query.all()
        elif Category.query.get(category_id) is not None:
            questions_selection = Question.query.filter_by(category=category_id).all()
        else:
            # no category with that id
            abort(422)

        # filter out previously asked questions
        previous_questions_set = {question for question in data['previous_questions']}
        questions_not_asked_yet = [question for question in questions_selection
                                   if question.id not in previous_questions_set]

        if len(questions_not_asked_yet) == 0:
            # no more questions left
            random_question = False
        else:
            random_question = random.choice(questions_not_asked_yet).format()

        return jsonify({
            'question': random_question,
            'success': True,
            'status_code': 200,
            'message': 'POST Success',
        })

    #  ----------------------------------------------------------------
    #  Error handlers
    #  ----------------------------------------------------------------

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "status_code": 400,
            "message": "Bad request",
        }), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "status_code": 404,
            "message": "Resource not found",
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "status_code": 405,
            "message": "Method not allowed",
        }), 405

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "status_code": 422,
            "message": "Unprocessable",
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False,
            "status_code": 500,
            "message": "Server error",
        }), 500

    return app
