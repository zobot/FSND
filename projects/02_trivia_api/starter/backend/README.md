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

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/questions'
GET '/categories'
GET '/categories/[category_id]/questions'
DELETE '/questions/[question_id]'
POST '/questions'
POST '/quizzes'



GET '/questions'
- Fetches a list of paginated questions
- Request Arguments: page: Determines which page of questions to display.  Each page is 10 questions long.
- Returns: If successful, returns a message with the following structure: 

Example:
/questions?page=1

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
/questions?page=-1

Responds:
{'message': 'Bad request', 'status_code': 400, 'success': False} 
with status code 400

404:
If there are no questions on the given page, returns error 404:

Example:
/questions?page=100

Responds:
{'message': 'Resource not found', 'status_code': 404, 'success': False} 
with status code 404



GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 

Example:
/categories

Responds:
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}


GET '/categories/[category_id]/questions'
- Fetches a list of paginated questions that belong to category_id
- Request Arguments: page: Determines which page of questions to display.  Each page is 10 questions long.
- Returns: If successful, returns a message with the following structure: 

Example:
/categories/6/questions?page=1

Responds:
{'categories': {'1': 'Science', '2': 'Art', '3': 'Geography', '4': 'History', '5': 'Entertainment', '6': 'Sports'},
'current_category': 6,
'message': 'GET Success',
'questions': [
  {'answer': 'Brazil', 'category': 6, 'difficulty': 3, 'id': 10, 'question': 'Which is the only team to play in every soccer World Cup tournament?'},
  {'answer': 'Uruguay', 'category': 6, 'difficulty': 4, 'id': 11, 'question': 'Which country won the first ever soccer World Cup in 1930?'}],
'status_code': 200,
'success': True,
'total_questions': 2}
with status code 200


Errors:

400:
If the page is not a positive integer, returns error 400:

Example:
/categories/1/questions?page=-1

Responds:
{'message': 'Bad request', 'status_code': 400, 'success': False} 
with status code 400

404:
If there are no questions on the given page, returns error 404:

Example:
/categories/1/questions?page=100

Responds:
{'message': 'Resource not found', 'status_code': 404, 'success': False} 
with status code 404



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