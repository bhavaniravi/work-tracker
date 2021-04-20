# load db url from the env variable. you can use python-dotenv package

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


load_dotenv()
db_url = os.environ["DATABASE_URL"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

db.create_all()
db.init_app(app)

from application.views import *

# Run the app in port 5000 and in debug mode
if __name__ == '__main__':
    app.run(port=5000, debug=True)