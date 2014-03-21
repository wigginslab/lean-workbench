from flask_security.forms import RegisterForm, Required
from wtforms import TextField
class ExtendedRegisterForm(RegisterForm):
	"""
	Extend flask-security registration form to include company name
	"""
	company = TextField('Company Name', [Required()])
