from wtforms import Form, BooleanField, TextField, PasswordField, validators

class HypothesisForm(Form):
	title = TextField('Hypothesis Title')
	wufoo = TextField('Wufoo Url')
	wufoo_handshake = TextField('Wufoo Handshake')
	google_analytics = TextField('Feature url')
	event  = TextField('Event')




