from wtforms import Form, BooleanField, TextField, PasswordField, validators

class HypothesisForm(Form):
	title = TextField('Hypothesis Title')
	wufoo = TextField('Wufoo Url')
	google_analytics = TextField('Feature url')
	event  = TextField('Event')




