from database import db
import datetime
import time

class Facebook_model(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	name = db.Column(db.String)
	username = db.Column(db.String)
	profile_url = db.Column(db.String)
	access_token = db.Column(db.String)
	key_name = db.Column(db.String)
	expired = db.Column(db.Boolean)

	def __init__(self, name, username, profile_url, access_token, key_name):
		self.created = datetime.datetime.now()
		self.updated = datetime.datetime.now()
		self.name =	name
		self.username = username
		self.profile_url = profile_url
		self.access_token = access_token
		self.key_name = key_name
		self.expired = False

class Facebook_page_data(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column(db.DateTime)
	likes = db.Column(db.Integer)
	posts = db.Column(db.String)
	username = db.Column(db.String)
	page_name = db.Column(db.String)

	def __init__(self, likes=None, posts=None, username=username, page_name=None):
		self.date = datetime.datetime.now()
		self.likes = likes
		self.posts = posts
		self.username = username
		self.page_name = page_name

	def as_dict(self):
		return {
			"id": self.id,
			"page_name": self.page_name,
			"date": str(self.date),
			"likes": self.likes,
			"posts": self.posts,
			"username": self.username
		}

	def as_count(self):
		return [time.mktime(datetime.datetime.timetuple(self.date))*1000, self.likes]