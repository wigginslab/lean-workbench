from database import db
import datetime

class Facebook_model(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	name = db.Column(db.String)
	username = db.Column(db.String)
	profile_url = db.Column(db.String)
	access_token = db.Column(db.String)
	key_name = db.Column(db.String)

	def __init(self, name, username, profile_url, access_token, key_name):
		self.created = datetime.datetime.now()
		self.updated = datetime.datetime.now()
		self.name =	kwargs.get('name')
		self.username = kwargs.get('username')
		self.profile_url = profile_url
		self.access_token = access_token
		self.key_name = key_name