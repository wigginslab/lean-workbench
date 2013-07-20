from datetime import datetime
from flask.ext.sqlalchemy import *
import os
from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

class Wufoo_User_Model(db.Model):
	__tablename__ = "fnord_user"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	
	def __init__(self,username):
		self.username = username
