from datetime import datetime
from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)
app.secret_key = os.environ.get('secret_key')
app.debug = True


class Google_Analytics_User_Model(db.Model):
	__tablename__ = "google_analytics"
	uid = db.Column(db.Integer, primary_key=True)
	token_expiry = db.Column(db.String)
	access_token = db.Column(db.String)
	client_id = db.Column(db.String)
	client_secret = db.Column(db.String)
	profile_id = db.Column(db.String)
