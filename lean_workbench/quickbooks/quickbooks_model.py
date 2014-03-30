from database import db
import datetime

class Quickbooks_model(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	username = db.Column(db.String)
	access_token = db.Column(db.String)

	def __init__(self, username, access_token):
		self.created = datetime.datetime.now()
		self.updated = datetime.datetime.now()
		self.username = username
		self.access_token = access_token

class Quickbooks_balance(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	username = db.Column(db.String)
	balance = db.Column(db.Integer)

	def __init__(self,username, balance):
		self.created = datetime.datetime.now()
		self.balance = balance
		self.name =	name
		self.username = username
