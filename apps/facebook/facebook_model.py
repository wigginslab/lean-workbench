from datetime import datetime
from flask import Flask
from werkzeug import generate_password_hash, check_password_hash
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)

class Facebook_model:
	pass