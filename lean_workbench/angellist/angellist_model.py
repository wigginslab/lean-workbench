from lean_workbench.core import db

class AngellistUserModel(db.Model):
	__tablename__ = "angellist_user"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String)
	
	def __init__(self,username):
		self.username = username