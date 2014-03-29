from database import db
import datetime

class Hypothesis_model(db.Model):

	__tablename__ = 'hypotheses'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60))
	title = db.Column(db.String)
	google_analytics = db.Column(db.String)
	wufoo = db.Column(db.String)
	twitter_keyword = db.Column(db.String)
	endpoint = db.Column(db.String)
	event = db.Column(db.String)
	creation_date = db.Column(db.DateTime)
	end_date = db.Column(db.DateTime)

	def __init__(self, form_dict):
		print form_dict
		self.username = form_dict.get('username')
		self.title = form_dict.get('title')
		self.google_analytics = form_dict.get('google_analytics')
		self.wufoo = form_dict.get('wufoo')
		self.endpoint = form_dict.get('endpoint')
		self.twitter_keyword = form_dict.get('twitter_keyword') 
		self.event =form_dict.get('event')
		self.end_date = form_dict.get('end_date')
		self.creation_date = datetime.datetime.now()

	def end(self):
		self.end_date = datetime.datetime.now()

	@property
	def serialize(self):
		"""Return object data in easily serializeable format"""
		return {
			'id': self.id,
		}