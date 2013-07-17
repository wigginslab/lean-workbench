from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')
db = SQLAlchemy(app)

class Angellist_User_Model(db.Model):
	__tablename__ = "angellist_oauth_credentials"
	
	uid = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	code = db.Column(db.String)

def __init__(self, username=None, code=None):
	self.username = username
	self.code = code
