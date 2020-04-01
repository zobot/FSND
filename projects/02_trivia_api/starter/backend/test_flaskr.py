import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

from db_password import db_password


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        username = 'zoe'
        self.database_path = "postgres://{}:{}@{}/{}".format(username, db_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

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


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()