# load db url from the env variable. you can use python-dotenv package

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from dotenv import load_dotenv
import os
from datetime import timedelta


load_dotenv()
db_url = os.environ["DATABASE_URL"]

db_url = db_url.replace('postgres', 'postgresql', 1)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3000)
db = SQLAlchemy(app)

from application.views import *






# Run the app in port 5000 and in debug mode
if __name__ == '__main__':
    app.run(port=5000, debug=True)