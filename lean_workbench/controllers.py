import json
import os
from flask import request, Response, render_template, make_response, session, escape,redirect, url_for, jsonify, redirect
import datetime
import random
import re
from datetime import datetime
from lean_workbench import app, api
from flask.ext.security import login_required, auth_token_required, current_user, UserMixin, logout_user
from flask.ext import restful
from apps.hypotheses.hypotheses_resource import Hypothesis_resource
from apps.facebook.facebook_resource import Facebook_resource
from apps.twitter.twitter_resource import Twitter_resource
from apps.wufoo.wufoo_resource import Wufoo_resource
from apps.google_analytics.google_analytics_resource import Google_analytics_resource

@app.route('/')
def index():
	print current_user
	if current_user.is_authenticated():
		print current_user
		logged_in = True
		return redirect(url_for('dashboard'))
	else:
		logged_in=False
		return render_template('public.html', logged_in=logged_in)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
    
@auth_token_required
@app.route('/onboarding/stick', methods=['POST', 'GET'])
@app.route('/onboarding/virality', methods=['POST','GET'])
@app.route('/onboarding/pay', methods=['POST','GET'])
@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
	"""
	"""
	return render_template('public.html', logged_in=True)

@app.route('/api/v1/logout', methods=['POST','GET'])
def logout():
	print session
	logout_user()
	user_db.session.remove()
	return jsonify(status=200, message='User has been successfully logged out.')
	#return redirect(url_for('index'))

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


@app.route('/connect/quickbooks/callback')
def quickbooks_callback():
	print 'inside quickbooks callback'
	print request.args



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


api.add_resource(Hypothesis_resource, '/api/v1/hypotheses')
api.add_resource(Facebook_resource, '/api/v1/facebook')
api.add_resource(Twitter_resource, '/api/v1/twitter')
api.add_resource(Wufoo_resource, '/api/v1/wufoo')
api.add_resource(Google_analytics_resource, '/api/v1/googleanalytics')