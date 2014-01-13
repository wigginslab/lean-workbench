from database import db

class Facebook_model:
	id = db.Column(db.Integer, primary_key=True)
	created = db.Column(db.DateTime)
	updated = db.Column(db.DateTime)
	name = db.Column(db.String)
	username = db.Column(db.String)
	profile_url = db.Column(db.String)
	access_token = db.Column(db.String)