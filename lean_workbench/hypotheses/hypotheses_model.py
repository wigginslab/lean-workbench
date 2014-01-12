from database import db

# Standard Databases
class Hypothesis_model(db.Model):

	__tablename__ = 'hypotheses'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60))
	goal = db.Column(db.String)
	google_analytics = db.Column(db.String)
	wufoo = db.Column(db.String)
	endpoint = db.Column(db.String)
	event = db.Column(db.String)

	def __init__(self, form_dict, username):
		self.username = username
		self.goal = form_dict.get('title')
		self.google_analytics = form_dict.get('google_analytics')
		self.wufoo = form_dict.get('wufoo')
		self.endpoint = form_dict.get('endpoint')
		self.event = db.Column(db.String)