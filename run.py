import json
from werkzeug import SharedDataMiddleware
import os
from flask import Flask, request, Response, render_template, make_response, session, escape,redirect, url_for, jsonify, redirect
import datetime
import random
import re
from models.user import User
from datetime import datetime
from app import db, app
# google analytics imports
from oauth2client.client import flow_from_clientsecrets
import httplib2
from apiclient.discovery import build
from apps.googleanalytics.google_analytics_client import Google_Analytics_API
#form validation imports
from flask.ext.security import Security, SQLAlchemyUserDatastore, login_required, current_user, UserMixin
from models.user import User, Role
from forms.registration_form import ExtendedRegisterForm
from flask.ext.mail import Mail, Message

port = int(os.getenv('port'))
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)
mail = Mail(app)
app.config["DEBUG"] = True

@app.route('/api/login',methods=["GET","POST"])
def login():
	return User.get_auth_token()

@app.route('/')
def index():
	if  current_user.is_authenticated():
		return redirect(url_for('dashboard'))
	else:
		return render_template('public.html')

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
			return redirect(url_for('view_ga'))
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

@app.route('/api/connect/google-analytics')
def ga_partial():
	return render_template('partials/google-analytics.html')

@app.route('/api/connect/fnord')
def fnord_partial():
	return render_template('partials/fnord.html')

@app.route('/api/connect/wufoo')
def wufoo_partial():
	return render_template('partials/view_wufoo.html')


@app.route('/view/google-analytics')
def view_ga():
	return render_template('view_google_analytics.html')

@app.route('/view/wufoo')
def view_wufoo():
	return render_template('partials/view_wufoo.html')

@app.route('/search/crunchbase/',methods=['GET','POST'])
def search_crunchbase():
	print 'inside search crunchbase'
	crunchbase = Crunchbase(os.getenv('crunchbase_key'))
	print crunchbase
	print request.args
	query = request.args["company"]
	print query
	search = crunchbase.search(query)
	print search
	return json.dumps(search["results"])


@app.route('/connect/angellist/', methods=['GET'])
def connect_angellist():
	"""
	Step 1 of connection to angellist api
	"""
	#if request.method =='GET':
	#	return render_template('partials/angellist.html')
	redirect_url = AngelList().getAuthorizeURL()
	print redirect_url
	return redirect(redirect_url)

@app.route('/connect/angellist/callback',methods=['GET'])
def angellist_callback():
	print 'in callback'
	if 'username' in session:
		username = escape(session['username'])
	else:
		username = None
	code = request.args.get("code")
	al = AngelList()
	code = al.getAccessToken(code=code)
	al.save(code=code, username=username)
	return redirect(url_for('index'))

@app.route('/hypotheses')
def hypotheses():
	if 'username' in session:
		print 'logged in'
		username = escape(session['username'])
	else:
		return redirect(url_for('index'))
	return render_template('hypotheses.html', username=username)

@app.route('/wufoo', methods=['GET', 'POST'])
def wufoo():
	data = request.args
	field_titles = {}
	field_values = {} 
	field_structure = data['FieldStructure']
	fields = field_structure['Fields']

	# get field titles
	for field in fields:
		field_title = field['Title']
		field_id = field['Id']
		field_titles[field_id] = field_title
		field_values[field_id]= data[field_title]

	# get field values
	for field in field_titles:
		field_model = Wufoo_Field_Model()
	form_structure = data['FormStructure']
	url = form_structure['Url']
	survey = Wufoo_Survey_Model.query.filter_by(url=url)
	if not survey:
		survey = Wufoo_Survey_Model()

# store static files on server for now
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
	'/': os.path.join(os.path.dirname(__file__), 'static')
})

if __name__ == '__main__':
	app.run(debug=True, port=port)
