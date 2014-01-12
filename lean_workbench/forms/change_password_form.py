from wtforms import Form, BooleanField, TextField, PasswordField, validators

class ChangePasswordForm(Form):
	password = PasswordField('New Password', [
	validators.Required(),
	validators.EqualTo('confirm', message='Passwords must match')
	])
	confirm = PasswordField('Repeat Password')