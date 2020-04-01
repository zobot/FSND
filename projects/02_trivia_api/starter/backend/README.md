# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

```
API Documentation:

Endpoints
GET /questions
GET /categories
GET /categories/<int:category_id>/questions
DELETE /questions/<int:question_id>
POST /questions
POST /quizzes



GET /questions
- Fetches a list of paginated questions
- Request Arguments: page: Determines which page of questions to display.  Each page is 10 questions long.
- Returns: If successful, returns a page message with the following structure: 

Example:
GET /questions?page=1

Responds:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': None,
'message': 'GET Success',
'questions': [
  {'answer': 'Tom Cruise', 'category': 5, 'difficulty': 4, 'id': 4, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'},
  {'answer': 'Edward Scissorhands', 'category': 5, 'difficulty': 3, 'id': 6, 'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'},
  {'answer': 'Muhammad Ali', 'category': 4, 'difficulty': 1, 'id': 9, 'question': "What boxer's original name is Cassius Clay?"},
  {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'},
  {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'},
  {'answer': 'George Washington Carver', 'category': 4, 'difficulty': 2, 'id': 12, 'question': 'Who invented Peanut Butter?'},
  {'answer': 'Lake Victoria', 'category': 3, 'difficulty': 2, 'id': 13, 'question': 'What is the largest lake in Africa?'},
  {'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3, 'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?'},
  {'answer': 'Agra', 'category': 3, 'difficulty': 2, 'id': 15, 'question': 'The Taj Mahal is located in which Indian city?'},
  {'answer': 'Escher', 'category': 2, 'difficulty': 1, 'id': 16, 'question': 'Which Dutch graphic artist–initials M C was a creator of optical illusions?'}
],
'status_code': 200,
'success': True,
'total_questions': 19}
with status code 200


Errors:

400:
If the page is not a positive integer, returns error 400:

Example:
GET /questions?page=-1

Responds:
{'message': 'Bad request', 'status_code': 400, 'success': False} 
with status code 400

404:
If there are no questions on the given page, returns error 404:

Example:
GET /questions?page=100

Responds:
{'message': 'Resource not found', 'status_code': 404, 'success': False} 
with status code 404



GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example:
GET /categories

Responds:
{'categories': 
  {'1': 'Science',
  '2': 'Art',
  '3': 'Geography',
  '4': 'History',
  '5': 'Entertainment',
  '6': 'Sports'},
'message': 'GET Success',
'status_code': 200,
'success': True}
with status code 200


GET /categories/<int:category_id>/questions
- Fetches a list of paginated questions that belong to category_id
- Request Arguments: page: Determines which page of questions to display.  Each page is 10 questions long.
- Returns: If successful, returns a page message with the following structure: 

Example:
GET /categories/6/questions?page=1

Responds:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': 6,
'message': 'GET Success',
'questions': [
  {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'},
  {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'}
],
'status_code': 200,
'success': True,
'total_questions': 2}
with status code 200


Errors:

400:
If the page is not a positive integer, returns error 400:

Example:
GET /categories/1/questions?page=-1

Responds:
{'message': 'Bad request', 'status_code': 400, 'success': False} 
with status code 400

404:
If there are no questions on the given page, returns error 404:

Example:
GET /categories/1/questions?page=100

Responds:
{'message': 'Resource not found', 'status_code': 404, 'success': False} 
with status code 404



DELETE '/questions/<int:question_id>'
- Deletes the question with id=question_id from the database
- Request Arguments: None
- Returns: If successful, returns a refreshed page message with the following structure: 

Example:
DELETE /questions/2

Responds:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': None,
'message': 'DELETE Success',
'questions': [
  {'answer': 'Tom Cruise', 'category': 5, 'difficulty': 4, 'id': 4, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'},
  {'answer': 'Edward Scissorhands', 'category': 5, 'difficulty': 3, 'id': 6, 'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'},
  {'answer': 'Muhammad Ali', 'category': 4, 'difficulty': 1, 'id': 9, 'question': "What boxer's original name is Cassius Clay?"},
  {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'},
  {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'},
  {'answer': 'George Washington Carver', 'category': 4, 'difficulty': 2, 'id': 12, 'question': 'Who invented Peanut Butter?'},
  {'answer': 'Lake Victoria', 'category': 3, 'difficulty': 2, 'id': 13, 'question': 'What is the largest lake in Africa?'},
  {'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3, 'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?'},
  {'answer': 'Agra', 'category': 3, 'difficulty': 2, 'id': 15, 'question': 'The Taj Mahal is located in which Indian city?'},
  {'answer': 'Escher', 'category': 2, 'difficulty': 1, 'id': 16, 'question': 'Which Dutch graphic artist–initials M C was a creator of optical illusions?'}
],
'status_code': 200,
'success': True,
'total_questions': 17}
with status code 200


Errors:

404:
If the supplied question_id doesn't match any questions, return error 404:

Example:
DELETE /questions/1

Responds:
{'message': 'Resource not found', 'status_code': 404, 'success': False} 
with status code 404



POST /questions
- This endpoint has two functionalities depending on the JSON passed into the request.  
It can either search or create a question.

Search:
- Request Arguments: JSON data: {'searchTerm': input}.

- Returns: If successful, returns a page message with the following structure where all questions 
partially match the search term, or an empty question list if no questions match the search term.  
total_questions refers to the total number of matching questions, even if longer than a single page: 

Example:
POST /questions
JSON: {'searchTerm': 'Which'}

Response:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': None,
'message': 'POST Success',
'questions': [
  {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'},
  {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'},
  {'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3, 'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?'},
  {'answer': 'Agra', 'category': 3, 'difficulty': 2, 'id': 15, 'question': 'The Taj Mahal is located in which Indian city?'},
  {'answer': 'Escher', 'category': 2, 'difficulty': 1, 'id': 16, 'question': 'Which Dutch graphic artist–initials M C was a creator of optical illusions?'},
  {'answer': 'Jackson Pollock', 'category': 2, 'difficulty': 2, 'id': 19, 'question': 'Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?'},
  {'answer': 'Scarab', 'category': 4, 'difficulty': 4, 'id': 23, 'question': 'Which dung beetle was worshipped by the ancient Egyptians?'}
],
'status_code': 200,
'success': True,
'total_questions': 7}
with status code 200

If no matches are found:

Example:
POST /questions
JSON: {'searchTerm': 'Nonsensical search term'}

Response:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': None,
'message': 'POST Success',
'questions': [],
'status_code': 200,
'success': True,
'total_questions': 0}
with status code 200


POST /questions
- This endpoint has two functionalities depending on the JSON passed into the request.  
It can either search or create a question.

Create:
- Inserts the new question defined by the input JSON into the database.
- Request Arguments: JSON data: 
{'question': input_question,
'answer': input_answer,
'category': category_id,
'difficulty': difficulty}.

- Returns: If successful, inserts the question into the database and 
returns a refreshed page message with the following structure: 

Example:
POST /questions
JSON: 
{'question': 'new_question',
'answer': 'new_answer',
'category': 100,
'difficulty': 3}.

Response:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': None,
'message': 'POST Success',
'questions': [
  {'answer': 'Tom Cruise', 'category': 5, 'difficulty': 4, 'id': 4, 'question': 'What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?'},
  {'answer': 'Edward Scissorhands', 'category': 5, 'difficulty': 3, 'id': 6, 'question': 'What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?'},
  {'answer': 'Muhammad Ali', 'category': 4, 'difficulty': 1, 'id': 9, 'question': "What boxer's original name is Cassius Clay?"},
  {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'},
  {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'},
  {'answer': 'George Washington Carver', 'category': 4, 'difficulty': 2, 'id': 12, 'question': 'Who invented Peanut Butter?'},
  {'answer': 'Lake Victoria', 'category': 3, 'difficulty': 2, 'id': 13, 'question': 'What is the largest lake in Africa?'},
  {'answer': 'The Palace of Versailles', 'category': 3, 'difficulty': 3, 'id': 14, 'question': 'In which royal palace would you find the Hall of Mirrors?'},
  {'answer': 'Agra', 'category': 3, 'difficulty': 2, 'id': 15, 'question': 'The Taj Mahal is located in which Indian city?'},
  {'answer': 'Escher', 'category': 2, 'difficulty': 1, 'id': 16, 'question': 'Which Dutch graphic artist–initials M C was a creator of optical illusions?'}
],
'status_code': 200,
'success': True,
'total_questions': 19}
with status code 200


Errors:

400:
If not all input data to define a Question is present in the JSON body, error 400

Example:
POST /questions
JSON {'question': 'just question, nothing else'}

Responds:
{'message': 'Bad request', 'status_code': 400, 'success': False} 
with status code 400


422:
If the category argument is not a valid category_id, error 422

Example:
POST /questions
JSON 
{'question': 'new_question',
'answer': 'new_answer',
'category': 100,
'difficulty': 3}.

Responds:
{'message': 'Unprocessable', 'status_code': 422, 'success': False} 
with status code 422



POST /quizzes
- Fetches a list of paginated questions that belong to category_id
- Request Arguments: JSON data
{'quiz_category': {'id': id}, 'previous_questions':[list_of_previous_questions]}
- Returns: If successful, returns a random single question that is not in list_of_previous_questions
 with the following structure.
If id=0, all categories are included in the question pool: 

Example:
POST /quizzes
JSON
{'quiz_category': {'id': 6}, 'previous_questions':[10]}

Responds:
{'message': 'POST Success',
'question': 
{'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'},
'status_code': 200,
'success': True}
with status code 200

If there are no questions that have not been previously asked in the given category, 'question' is set to False

Example:
POST /quizzes
JSON
{'quiz_category': {'id': 6}, 'previous_questions':[10, 11]}

Responds:
{'message': 'POST Success',
'question': False,
'status_code': 200,
'success': True}
with status code 200


Errors:

422
If the quiz_category argument is not a valid category_id, error 422

POST /quizzes
JSON
{'quiz_category': {'id': 100}, 'previous_questions':[10]}

Responds:
{'message': 'Unprocessable', 'status_code': 422, 'success': False} 
with status code 422




Error responses:

400:

Responds:
{'message': 'Bad request', 'status_code': 400, 'success': False} 
with status code 400


404:

Responds:
{'message': 'Resource not found', 'status_code': 404, 'success': False} 
with status code 404

405:

Responds:
{'message': 'Method not allowed', 'status_code': 405, 'success': False} 
with status code 405

422:

Responds:
{'message': 'Unprocessable', 'status_code': 422, 'success': False} 
with status code 422


500:

Responds:
{'message': 'Server error', 'status_code': 500, 'success': False} 
with status code 500


```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

or run 
```
sh run_tests.sh
```
while in the backend directory.