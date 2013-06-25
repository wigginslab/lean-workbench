from datetime import datetime
from flask import Flask, abort
from flask.ext.sqlalchemy import *
from werkzeug import generate_password_hash, check_password_hash
import os
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('db_url')

db = SQLAlchemy(app)

# Standard Databases
class User(db.Model):

    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60))
    pwdhash = db.Column(db.String())
    email = db.Column(db.String(60))
    activate = db.Column(db.Boolean)
    created = db.Column(db.DateTime)
		
    def __init__(self, username, password, email):
        self.username = username
        error = self.check_username()
        self.pwdhash = generate_password_hash(password)
        self.email = email
        self.activate = True
        self.created = datetime.utcnow()

    def check_password(self, password):
      	return check_password_hash(self.pwdhash, password)
		
    def check_username(self):
        sameUsername = User.query.filter_by(username=self.username).all()
        print 'sameUsername: '
        print sameUsername
        if sameUsername: 
				 abort(401)
    def __repr__(self):
      """
      Representation of the user object
      """
      return '<User %s>' %self.username
