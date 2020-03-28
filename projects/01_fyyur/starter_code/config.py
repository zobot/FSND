import os
# Import secret password for postgres account from a non-version control file.
from db_password import db_password

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Turn off the warning for tracking modifications.
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Connect to the database.
SQLALCHEMY_DATABASE_URI = 'postgresql://zoe:' + db_password + '@localhost:5432/fyyur'
