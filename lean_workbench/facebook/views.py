from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for, current_app
from flask.ext.security import current_user
import os
from facebook_model import Facebook_model, db
import urllib
import requests
import json
import cgi

app = Blueprint('facebook', __name__, template_folder='templates')

@app.route('/connect/facebook', methods=['GET', 'POST'])
def facebook_oauth_step_one():
	app_key = current_app.config['FACEBOOK_APP_KEY']  
	app_secret = current_app.config['FACEBOOK_APP_SECRET']
	callback_url= current_app.config['FACEBOOK_CALLBACK_URL']
	args = dict(client_id=app_key,
                    redirect_uri=callback_url)
	session['redirect_uri'] = callback_url
	return jsonify({"redirect_url": "https://graph.facebook.com/oauth/authorize?" +
                urllib.urlencode(args), 'status':100})

@app.route('/connect/facebook/callback/', methods=['GET', 'POST'])
def facebook_oauth_callback():
	args = {}
	args["client_id"] = current_app.config["FACEBOOK_APP_KEY"]
	args["client_secret"] = current_app.config['FACEBOOK_APP_SECRET'] 
	args["code"] = request.args.get("code")
	args["redirect_uri"] = session.pop('redirect_uri', None)
	#return json.dumps(request.args.get['path_url']
	#response = "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)
	response = cgi.parse_qs(urllib.urlopen("https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args)).read())
	access_token = response["access_token"]
	#return json.dumps()

	# Download the user profile and cache a local instance of the
	# basic profile info
	profile = json.load(urllib.urlopen(
		"https://graph.facebook.com/me?" +
		urllib.urlencode(dict(access_token=access_token))))

	fb_user = Facebook_model(key_name=str(profile["id"]),
		name=profile["name"], access_token=access_token,
		profile_url=profile["link"], username=current_user.email)

	db.session.add(fb_user)
	db.session.commit()
	db.session.close()
