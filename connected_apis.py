"""
Tables to store what users have connected what APIs
"""

from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
import sys


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

users_apis_association = db.Table('user_apis_association',
			db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
			db.Column('api_id', db.Integer, db.ForeignKey('api.id'))
		)

Connected_API(db.Model):

	__tablename__ = "api"
	id = db.Column(db.Integer, primary_key=True)
	# user 
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) 



