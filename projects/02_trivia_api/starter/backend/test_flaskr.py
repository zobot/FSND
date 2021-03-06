import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from db_password import username, db_password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    QUESTIONS_PER_PAGE = 10

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
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
        # helper for noting changes in the number of questions in the table
        res = self.client().get('/questions?page=1')
        num_questions = json.loads(res.data)['total_questions']
        return num_questions

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
        # no page 100
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_questions_neg_page_num_400(self):
        # no negative pages
        res = self.client().get('/questions?page=-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message'], 'Bad request')

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
        # no question with id 1
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

    def test_post_question_bad_missing_data_400(self):
        # not all data is present in this request
        new_question_missing_data = {"question": "New input question?"}
        res = self.client().post('/questions', json=new_question_missing_data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_post_question_bad_category_422(self):
        new_question_bad_category = self.new_question.copy()
        # categories are 1-6
        new_question_bad_category["category"] = -5
        res = self.client().post('/questions', json=new_question_bad_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_post_question_search_success(self):
        # successfully matches at least one question
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
        Here we have defined that a search quUnittests in test_ncc.pyery with no matches still
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

    def test_questions_by_category_success(self):
        category = 6
        res = self.client().get(f'/categories/{category}/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories'].items()))
        self.assertTrue(len(data['questions']))
        for question in data['questions']:
            self.assertEqual(question['category'], category)
        self.assertEqual(data['message'], 'GET Success')

    def test_questions_by_category_less_than_full_num(self):
        res = self.client().get('/categories/1/questions?page=1')
        data = json.loads(res.data)
        category_questions = data['total_questions']
        total_questions = self.get_current_num_questions()

        # num of questions in a category should be strictly less than total question num
        self.assertLess(category_questions, total_questions)

    def test_questions_by_category_high_page_num_404(self):
        # no page 100
        res = self.client().get('/categories/1/questions?page=100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    def test_questions_by_category_neg_page_num_400(self):
        # no negative pages
        res = self.client().get('/categories/1/questions?page=-1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_questions_by_category_bad_category(self):
        # no category 100
        res = self.client().get('/categories/100/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 422)
        self.assertEqual(data['message'], 'Unprocessable')

    def test_questions_no_patch_405(self):
        # there's no endpoint for PATCH requests
        res = self.client().patch('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 405)
        self.assertEqual(data['message'], 'Method not allowed')

    def test_quizzes_no_prev_no_category_success(self):
        id = 0
        no_prev_no_category_json = {'quiz_category': {'id': id}, 'previous_questions': []}
        res = self.client().post('/quizzes', json=no_prev_no_category_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['question'])
        self.assertEqual(data['message'], 'POST Success')

    def test_quizzes_no_prev_category_success(self):
        id = 1
        no_prev_category_json = {'quiz_category': {'id': id}, 'previous_questions': []}
        res = self.client().post('/quizzes', json=no_prev_category_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['category'] == id)
        self.assertEqual(data['message'], 'POST Success')

    def test_quizzes_prev_category_success(self):
        id = 1
        prev_question = 20
        prev_category_json = {'quiz_category': {'id': id}, 'previous_questions': [prev_question]}
        res = self.client().post('/quizzes', json=prev_category_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['question'])
        self.assertTrue(data['question']['category'] == id)
        self.assertTrue(data['question']['id'] != prev_question)
        self.assertEqual(data['message'], 'POST Success')

    def test_quizzes_no_more_questions_sports(self):
        no_more_questions_json = {'quiz_category': {'id': 6}, 'previous_questions': [10, 11]}
        res = self.client().post('/quizzes', json=no_more_questions_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['status_code'], 200)
        self.assertTrue(data['question'] is False)
        self.assertEqual(data['message'], 'POST Success')

    def test_quizzes_unprocessable(self):
        # no category 100
        unprocessable_json = {'quiz_category': {'id': 100}, 'previous_questions': []}
        res = self.client().post('/quizzes', json=unprocessable_json)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['status_code'], 422)
        self.assertEqual(data['message'], 'Unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()