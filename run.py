import json
from werkzeug import SharedDataMiddleware
import os
from app import app
import os
from flask import Flask, request, Response, render_template, make_response, session, escape,redirect, url_for, jsonify, redirect
import datetime
import random
import re
from models.user import User
from datetime import datetime
from app import db, app
#from client import flow_from_clientsecrets
from oauth2client.client import flow_from_clientsecrets
import httplib2
from apiclient.discovery import build
from apps.googleanalytics.save_credentials import save_google_analytics_credentials

@app.route('/')
def index():
	print 'in index'
	if 'username' in session:
		username = escape(session['username'])
		return render_template('index.html', username=username)
	else:
		return render_template('public.html')

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

@app.route('/connect/google-analytics/callback/')
def google_analytics_callback():
	if 'username' in session:
		username = escape(session['username'])
		print username
		google_analytics_callback_url = os.getenv("google_analytics_callback_url")
		ga_api_code = request.args.get("code")
		client_secrets = 'ga_client_secrets.json'
		flow = flow_from_clientsecrets(client_secrets,
						scope='https://www.googleapis.com/auth/analytics.readonly',
								message='%s is missing' % client_secrets, redirect_uri=google_analytics_callback_url)
		print flow.redirect_uri
		credentials = flow.step2_exchange(code=str(ga_api_code))
		print credentials
		credentials_json = json.loads(credentials.to_json())
		credentials_json['username'] = username
		http = httplib2.Http()

		http = credentials.authorize(http)  # authorize the http object
		save_google_analytics_credentials(credentials_json)
		# 3. Build the Analytics Service Object with the authorized http object
		print  build('analytics', 'v3', http=http)
	return url_for('index')

@app.route('/connect/google-analytics/')
def google_analytics_oauth():
	google_analytics_callback_url = os.getenv("google_analytics_callback_url")
	print google_analytics_callback_url
	google_analytics_client_id = os.getenv("google_analytics_client_id") 
	redirect_url = "https://accounts.google.com/o/oauth2/auth?response_type=code&scope=https://www.googleapis.com/auth/analytics.readonly&access_type=offline&redirect_uri="+google_analytics_callback_url+"&client_id="+google_analytics_client_id+"&hl=en&from_login=1&as=819ec18979456db&pli=1&authuser=0"
	return	redirect(redirect_url)

# store static files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
	app.run(debug=True, port=8080)
