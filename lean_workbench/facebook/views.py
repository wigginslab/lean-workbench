from flask import Blueprint, render_template, jsonify, request, session, redirect, url_for
from flask.ext.security import current_user
import os
from facebook_model import Facebook_model, db
import urllib

app = Blueprint('facebook', __name__, template_folder='templates')

@app.route('/connect/facebook', methods=['GET', 'POST'])
def facebook_oauth_step_one():
	app_key = os.getenv('facebook_app_key')
	print app_key
	app_secret = os.getenv('facebook_app_secret')
	callback_url=os.getenv('facebook_callback_url')
	args = dict(client_id=app_key,
                    redirect_uri=callback_url)
	return jsonify({"redirect_url": "https://graph.facebook.com/oauth/authorize?" +
                urllib.urlencode(args), 'status':100})

@app.route('/connect/facebook/callback/',methods=['GET', 'POST'])
def facebook_oauth_callback():
	args = {}
	args["client_secret"] = os.getenv('facebook_app_secret')
	args["code"] = request.args.get("code")
	response = urllib.urlopen(
		"https://graph.facebook.com/oauth/access_token?" +
		urllib.urlencode(args)).read()
	access_token = response["access_token"][-1]

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