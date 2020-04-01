import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)


    '''
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, origins="*")
    #cors = CORS(app, resources={r"*": {"origins": "*"}})


    '''
    @TODO: Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET,PATCH,POST,DELETE,OPTIONS")
        return response

    def format_paginate_questions(in_request, selection):
        page = in_request.args.get("page", default=1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        selection_paginated = selection[start:end]
        selection_formatted_paginated = [question.format() for question in selection_paginated]
        return selection_formatted_paginated

    def simplify_categories(categories_selection):
        categories_simplified_dict = {
            category.id: category.type
            for category in categories_selection
        }
        return categories_simplified_dict

    def questions_count_categories(in_request):
        questions_all = Question.query.order_by(Question.id).all()
        questions_count = Question.query.count()
        questions_formatted_paginated = format_paginate_questions(in_request, questions_all)

        categories_all = Category.query.all()
        categories_simplified_dict = simplify_categories(categories_all)

        return questions_formatted_paginated, questions_count, categories_simplified_dict

    @app.route('/questions', methods=['GET'])
    def questions():
        print(request.data)
        out_questions, questions_count, out_categories = questions_count_categories(request)

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

        if question_to_delete is None:
            abort(404)

        question_to_delete.delete()

        out_questions, questions_count, out_categories = questions_count_categories(request)

        return jsonify({
            'questions': out_questions,
            'total_questions': questions_count,
            'categories': out_categories,
            'current_category': None,
            'success': True,
            'status_code': 200,
            'message': 'DELETE Success',
        })


    '''
    @TODO: 
    Create an endpoint to DELETE question using a question ID. 
  
    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page. 
    '''

    '''
    @TODO: 
    Create an endpoint to POST a new question, 
    which will require the question and answer text, 
    category, and difficulty score.
  
    TEST: When you submit a question on the "Add" tab, 
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.  
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions based on a search term. 
    It should return any questions for whom the search term 
    is a substring of the question. 
  
    TEST: Search by any phrase. The questions list will update to include 
    only question that include that string within their question. 
    Try using the word "title" to start. 
    '''

    '''
    @TODO: 
    Create a GET endpoint to get questions based on category. 
  
    TEST: In the "List" tab / main screen, clicking on one of the 
    categories in the left column will cause only questions of that 
    category to be shown. 
    '''

    '''
    @TODO: 
    Create a POST endpoint to get questions to play the quiz. 
    This endpoint should take category and previous question parameters 
    and return a random questions within the given category, 
    if provided, and that is not one of the previous questions. 
  
    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not. 
    '''

    '''
    @TODO: 
    Create error handlers for all expected errors 
    including 404 and 422. 
    '''

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "status_code": 404,
            "message": "Resource not found",
        }), 404

    return app
