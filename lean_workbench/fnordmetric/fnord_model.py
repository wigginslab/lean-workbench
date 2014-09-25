from lean_workbench.core import db

class FnordUserModel(db.Model):
	__tablename__ = "fnord_user"

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(60))

	def __init__(self,username):
		self.username = username
