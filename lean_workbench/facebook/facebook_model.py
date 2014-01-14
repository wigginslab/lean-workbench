from database import db

class Facebook_model(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	name = db.Column(db.String)
	username = db.Column(db.String)
	profile_url = db.Column(db.String)
	access_token = db.Column(db.String)

	def __init(self, **kwargs):
		self.created = kwargs.get('created')
		self.updated = kwargs.get('updated')
		self.name =	kwargs.get('name')
		self.username = kwargs.get('username')
		self.profile_url = kwargs.get('profile_url')
		self.access_token = kwargs.get('access_token')