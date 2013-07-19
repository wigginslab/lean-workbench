import json
from werkzeug import SharedDataMiddleware
import os
from flask import Flask, request, Response, render_template, make_response, session, escape,redirect, url_for, jsonify, redirect
import datetime
import random
import re
from models.user import User
from datetime import datetime
from app import db, app, mail, Message
# google analytics imports
from oauth2client.client import flow_from_clientsecrets
import httplib2
from apiclient.discovery import build
from apps.googleanalytics.google_analytics_client import Google_Analytics_API
#form validation imports
from forms.registration_form import RegistrationForm
from forms.change_password_form import ChangePasswordForm
from apps.angellist.angellist import AngelList
from apps.hypotheses.hypotheses_model import Hypothesis_Model
from forms.hypothesis_form import HypothesisForm

port = int(os.getenv('port'))

def authenticate_page(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		if not getattr(func, 'authenticated', True):
			return func(*args, **kwargs)
		acct = check_authentication(kwargs.get('username'))  # custom account lookup function
		if acct:
 			return func(*args, **kwargs)
		return redirect(url_for('index'))
	return wrapper


@app.route('/')
def index():
	print 'in index'
	if 'username' in session:
		username = escape(session['username'])
		hypotheses = Hypothesis_Model.query.filter_by(username=username)
		return redirect(url_for('hypotheses'))
	else:
		reg_form = RegistrationForm(request.form)
		return render_template('public.html', form=reg_form)

@app.route('/hypothesis/<int:hyp_id>')
def get_hypothesis(hyp_id):
	#TODO
	hypothesis = Hypothesis_Model.query.filter_by(id=hyp_id).first()
	title = hypothesis.goal
	if not title:
		title=""
	return render_template('goals.html', hypothesis = title)

@app.route('/hypotheses', methods=['POST', 'GET'])
def hypotheses():
	if 'username' in session:
		username = escape(session['username'])
		if request.method == "POST":
			hypothesis = Hypothesis_Model(request.form, username)
			print hypothesis
			db.session.add(hypothesis)
			db.session.commit()
			db.session.close()
			return  redirect(url_for('hypotheses'))
		hypotheses = Hypothesis_Model.query.filter_by(username=username)
		form = HypothesisForm()
		return render_template('hypotheses.html', username=username, hypotheses=hypotheses, form=form)
	else:
		return redirect(url_for('index'))


@app.errorhandler(401)
def user_already_exists(error):
	return render_template("error.html", error = "This user already exists.")

@app.route('/register', methods=['POST','GET'])
def register():
	"""
	user registration endpoint
	"""
	print 'in register'
	username = request.form['username']
	print username
	password = request.form['password']
	email = request.form['email']
	user = User(username, password, email)
	if user == "Error":
		return render_template("error.html", error="Error: user already exists")
	print user
	print db
	db.session.add(user)
	db.session.commit()
	db.session.close()
	print 'registration success!'
	session['username'] = request.form['username']
	return render_template('index.html', username=username)
	
@app.route('/login', methods=['POST','GET'])
def login():
	username = request.form['username']
	password = request.form['password']
	user = User.query.filter_by(username=username).first()
	# if no users by that username
	if not user: 		
		return render_template("error.html", error="This user does not exist yet")
	# if user and password correct
	if user.check_password(password):
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	# password incorrect
	else:
		print 'password is incorrect'
		return render_template("error.html", error="Invalid Password")

@app.route('/user/<user>')
def profile(user):
	# check if user logged in
	if 'username' not in session:
		return redirect(url_for('index'))
	#check is user exists
	user = User.query.filter_by(username=user).first()
	profileUser = user.username
	if user:
		return render_template('profile.html',username=profileUser)
	else:
		return render_template('error.html', error="User does not exist")

@app.route('/logout', methods=["GET","POST"])
def logout():
	session.pop('username', None)
	return redirect(url_for('index'))

@app.route('/password/change/', methods=["POST"])
def change_password():
	form = ChangePasswordForm(request.form)
	if form.validate():
		print request.data
		print request.form['password']
		password = request.form['password']
		reset_code = request.form['reset_code']
		print "reset_code = " + reset_code
		change_password_form = ChangePasswordForm()
		reset_password = Password_Reset().query.filter_by(reset_code=reset_code).first()
		registration_form = RegistrationForm()
		if not reset_password:
			flash("This is not a valid password reset page.")
			return render_template("change_password.html", form=change_password_form)
		else:
			username = reset_password.username 
			user = User.query.filter_by(username=username).first()
			user.change_password(username,password)
			flash("Your password has been reset")
			return render_template("index.html", form=registration_form)
	else:
		print 'form did not validate'

@app.route('/password/reset/', methods=['POST', 'GET'])
def reset_password_request():
	"""
	Request a password change, which results in an email sent to the user whose endpoint allows the user to change their password.
	"""
	print 'hi'
	print request.data
	if request.args.get('reset_code'):
		reset_code = request.args['reset_code']
		reset_password = Password_Reset.query.filter_by(reset_code=reset_code).first()
		if not reset_password:
			flash("This password reset link is invalid. Try again here.")
			return render_template("reset_password.html")
		else:
			form = ChangePasswordForm()
			return render_template("change_password.html", form=form, reset_code=reset_code)
	if request.method == "POST":
		username = request.form['username']
		print username
		user = User.query.filter_by(username=username).first()
		if not user:
			flash("User does not exist")
			return render_template('reset_password.html')
		reset_password = Password_Reset(user.username)
		user_email = user.email
		reset_code = reset_password.reset_code
		reset_msg = Message("Resetting Your Chatover Password",
                  sender="jen@example.com",
                  recipients=[user.email])
		reset_msg.html = "Go to "+ host + "/password/reset/?reset_code="+reset_code+"/ to reset your Chatover password.<p> Thanks, <p> Jen@Chatover"
		mail.send(reset_msg)
			
		db.session.add(reset_password)
		db.session.commit()
		db.session.close()
		flash('An email has been sent to you with a link to reset your password.')
		return render_template('reset_password.html')
	else:
		return render_template('reset_password.html')

# google analytics routes

@app.route('/connect/google-analytics/')
def google_analytics_oauth():
	username = escape(session.get('username'))
	if not username:
		print 'not logged in'
		return redirect(url_for('index'))
	GA_API = Google_Analytics_API(username)
	if GA_API.credentials:
		expires_on = GA_API.credentials.as_dict()['token_expiry']
		current_time = datetime.now().isoformat()
		# if credentials have not expired
		if expires_on > current_time:
			print GA_API.credentials.as_dict()
			# you shouldn't have hit this link
			print "you have credentials for GA"
			return redirect(url_for('index'))
		else:
			print "credentials expired, start oauth process"
			# start OAuth process
			redirect_url = GA_API.step_one()
			return redirect(redirect_url)
	else:
		print "start oauth process"
		# start OAuth process
		redirect_url = GA_API.step_one()
		return redirect(redirect_url)

@app.route('/connect/google-analytics/callback/')
def google_analytics_callback():
	if 'username' in session:
		username = escape(session['username'])
		GA_API = Google_Analytics_API('username')
		ga_api_code= request.args.get("code")
		print 'ga callback args'
		print request.args
		print GA_API
		client = GA_API.step_two(username, ga_api_code)
	else:
		print 'no user logged in'
	return redirect(url_for('index'))

@app.route('/google-analytics/profile/<int:profile_id>')
def get_profile_data(profile_id):
	pass

@app.route('/connect/angellist/')
def connect_angellist():
	"""
	Step 1 of connection to angellist api
	"""
	redirect_url = AngelList().getAuthorizeURL()
	return redirect(redirect_url)

@app.route('/connect/angellist/callback')
def angellist_callback():
	if 'username' in session:
		username = escape(session['username'])
	else:
		username = None
	code = request.args.get("code")
	al = AngelList()
	code = al.getAccessToken(code=code)
	al.save(code=code, username=username)
	return redirect(url_for('index'))

@app.route('/goals')
def goals():
	if 'username' in session:
		print 'logged in'
		username = escape(session['username'])
	else:
		return redirect(url_for('index'))
	return render_template('goals.html', username=username)
		
@app.route('/wufoo', methods=['GET', 'POST'])
def wufoo():
	print request.args

# store static files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
	app.run(debug=True, port=port)
