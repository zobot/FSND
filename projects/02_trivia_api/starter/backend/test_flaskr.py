import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from db_password import db_password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    QUESTIONS_PER_PAGE = 10

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        username = 'zoe'
        self.database_path = "postgres://{}:{}@{}/{}".format(username, db_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            "question": "New input question?",
            "answer": "New input answer!",
            "category": 1,
            "difficulty": 3,
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def get_current_num_questions(self):
        res = self.client().get('/questions?page=1')
        num_questions = json.loads(res.data)['total_questions']
        return num_questions



    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_questions_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories'].items()))
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['message'], 'GET Success')

    def test_questions_paginate_different_pages(self):
        res1 = self.client().get('/questions?page=1')
        data1 = json.loads(res1.data)
        res2 = self.client().get('/questions?page=2')
        data2 = json.loads(res2.data)

        self.assertEqual(data1['success'], True)
        self.assertEqual(data1['status_code'], 200)
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(data1['message'], 'GET Success')

        self.assertEqual(data2['success'], True)
        self.assertEqual(data2['status_code'], 200)
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(data2['message'], 'GET Success')
        for i in range(min(len(data1['questions']), len(data2['questions']))):
            self.assertNotEqual(data1['questions'][i], data2['questions'][i])

    def test_questions_high_page_num_404(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(len(data['categories'].items()))
        self.assertEqual(data['message'], 'GET Success')

    def test_delete_question_success(self):
        res = self.client().delete('/questions/2')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories'].items()))
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['message'], 'DELETE Success')

    def test_delete_question_decreased_num(self):
        pre_num_questions = self.get_current_num_questions()
        res = self.client().delete('/questions/5')
        post_num_questions = self.get_current_num_questions()

        self.assertEqual(pre_num_questions - 1, post_num_questions)

    def test_delete_question_404(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_post_question_success(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertEqual(data['message'], 'POST Success')

    def test_post_question_increased_num(self):
        pre_num_questions = self.get_current_num_questions()
        res = self.client().post('/questions', json=self.new_question)
        post_num_questions = self.get_current_num_questions()

        self.assertEqual(pre_num_questions + 1, post_num_questions)

    def test_post_question_bad_category_422(self):
        new_question_bad_category = self.new_question.copy()
        new_question_bad_category["category"] = -5
        res = self.client().post('/questions', json=new_question_bad_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_post_question_search_success(self):
        search_json = {'searchTerm': 'Which'}
        res = self.client().post('/questions', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories'].items()))
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['message'], 'POST Success')

    def test_post_question_search_empty(self):
        """
        Here we have defined that a search query with no matches still
        returns a successful response with 0 questions.
        """
        search_json = {'searchTerm': 'Nonsensical search term'}
        res = self.client().post('/questions', json=search_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(len(data['questions']) == 0)
        self.assertEqual(data['message'], 'POST Success')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()